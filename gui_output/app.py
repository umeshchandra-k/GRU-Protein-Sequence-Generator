import os
import random
import numpy as np
import requests
from flask import Flask, render_template, request, jsonify
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

# ── Load model & data once at startup ──────────────────────────────────────
MODEL_PATH   = os.path.join("model", "model.keras")
DATASET_PATH = os.path.join("data", "dataset.fasta")   # or dataset.txt

model = None
processed_sequences = []
char_to_int = {}
int_to_char = {}
vocab_size   = 0

def load_resources():
    global model, processed_sequences, char_to_int, int_to_char, vocab_size

    # 1. Load sequences
    try:
        from Bio import SeqIO
        for record in SeqIO.parse(DATASET_PATH, "fasta"):
            seq = str(record.seq).upper()
            if all(c in "ACDEFGHIKLMNPQRSTVWY" for c in seq):
                processed_sequences.append(seq)
    except Exception:
        valid = set("ACDEFGHIKLMNPQRSTVWY")
        with open(DATASET_PATH) as f:
            for line in f:
                seq = line.strip().upper()
                if seq and all(c in valid for c in seq):
                    processed_sequences.append(seq)

    # 2. Build mappings
    amino_acids  = sorted(set("".join(processed_sequences)))
    char_to_int  = {c: i for i, c in enumerate(amino_acids)}
    int_to_char  = {i: c for c, i in char_to_int.items()}
    vocab_size   = len(char_to_int)

    # 3. Load Keras model
    import tensorflow as tf
    model = tf.keras.models.load_model(MODEL_PATH)

    # Mask padding token entries if model output > vocab
    model_vocab = model.output_shape[-1]
    if model_vocab > vocab_size:
        for i in range(vocab_size, model_vocab):
            int_to_char[i] = None

    print(f"Loaded {len(processed_sequences)} sequences | vocab={vocab_size} | model output={model.output_shape[-1]}")


# ── Generation helpers ──────────────────────────────────────────────────────
def mutate_seed(seed, mutation_rate=0.1):
    seed = list(seed)
    for i in range(len(seed)):
        if random.random() < mutation_rate:
            seed[i] = random.choice(list(char_to_int.keys()))
    return "".join(seed)


def generate_sequence(seed, length=100, temperature=1.2):
    seq      = list(seed)
    seq_len  = model.input_shape[1]
    mv       = model.output_shape[-1]

    for _ in range(length):
        x     = [char_to_int.get(c, 0) for c in seq[-seq_len:]]
        x     = np.array(x).reshape(1, -1)
        preds = model.predict(x, verbose=0)[0].astype("float64")
        preds = np.log(preds + 1e-8) / temperature
        preds = np.exp(preds) / preds.sum()
        preds[mv - 1] = 0.0          # mask padding token
        preds /= preds.sum()
        idx   = np.random.choice(len(preds), p=preds)
        ch    = int_to_char.get(idx)
        if ch:
            seq.append(ch)

    return "".join(seq)


def score_protein(seq):
    score  = 0
    length = len(seq)
    if 95 <= length <= 105:
        score += 5
    elif 80 <= length <= 120:
        score += 2
    else:
        score -= 2
    for aa in set(seq):
        if seq.count(aa) / length > 0.3:
            score -= 3
    diversity    = len(set(seq)) / length
    score       += diversity * 10
    hydro_ratio  = sum(seq.count(c) for c in "AILMFWV") / length
    score       += (1 - abs(hydro_ratio - 0.45)) * 5
    charge_ratio = sum(seq.count(c) for c in "KRDE") / length
    score       += 2 if 0.1 <= charge_ratio <= 0.3 else -1
    for pat in ["LLLLLL", "AAAAAA", "VVVVVV"]:
        if pat in seq:
            score -= 3
    return round(score, 3)


def is_valid(seq):
    return "*" not in seq and len(seq) >= 30 and "LLLLLLLL" not in seq


def similarity(s1, s2):
    matches = sum(a == b for a, b in zip(s1, s2))
    return matches / max(len(s1), 1)


def check_novelty(gen_seq, dataset):
    return max(
        (similarity(gen_seq[:len(s)], s[:len(gen_seq)]) for s in dataset[:100]),
        default=0
    )


def fold_sequence(seq):
    # Clean sequence — remove anything not a standard AA
    valid = set("ACDEFGHIKLMNPQRSTVWY")
    seq = "".join(c for c in seq.upper() if c in valid)
    
    if len(seq) < 20:
        print("Sequence too short")
        return None

    print(f"Sending sequence ({len(seq)} AA): {seq[:30]}...")

    try:
        resp = requests.post(
            "https://api.esmatlas.com/foldSequence/v1/pdb/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0"
            },
            data=seq.encode("utf-8"),   # explicit encode — fixes Windows issue
            timeout=60,
            verify=False                # skip SSL verify — fixes Windows SSL errors
        )
        print(f"Status: {resp.status_code}")
        print(f"Response preview: {resp.text[:100]}")

        if resp.status_code == 200 and resp.text.strip().startswith("ATOM"):
            return resp.text
        else:
            print(f"Bad response: {resp.status_code} — {resp.text[:200]}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None

# ── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data     = request.json
    n_gen    = min(int(data.get("n_proteins", 10)), 50)
    top_n    = min(int(data.get("top_n", 3)),       10)
    temp     = float(data.get("temperature", 1.2))

    generated = []
    for _ in range(n_gen):
        base = random.choice(processed_sequences)[:30]
        seed = mutate_seed(base)
        seq  = generate_sequence(seed, length=100, temperature=temp)
        if is_valid(seq):
            generated.append(seq)

    scored = sorted(
        [(s, score_protein(s)) for s in generated],
        key=lambda x: x[1], reverse=True
    )[:top_n]

    results = []
    for i, (seq, score) in enumerate(scored):
        sim = round(check_novelty(seq, processed_sequences), 3)
        results.append({"rank": i + 1, "sequence": seq, "score": score, "similarity": sim})

    return jsonify({"results": results})


@app.route("/fold", methods=["POST"])
def fold():
    seq = request.json.get("sequence", "")

    # Clean sequence — strip non-standard AA characters (same as fold_sequence helper)
    valid = set("ACDEFGHIKLMNPQRSTVWY")
    seq = "".join(c for c in seq.upper() if c in valid)

    if len(seq) < 20:
        return jsonify({"error": "Sequence too short (minimum 20 amino acids)"}), 400

    print(f"Folding sequence ({len(seq)} AA): {seq[:30]}...")

    try:
        resp = requests.post(
            "https://api.esmatlas.com/foldSequence/v1/pdb/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0"
            },
            data=seq.encode("utf-8"),
            timeout=60,         # increased from 30s — ESMFold can be slow
            verify=False        # bypass SSL verify (same as fold_sequence helper)
        )
        print(f"ESMFold status: {resp.status_code}")
        print(f"ESMFold response: {resp.text[:200]}")

        # ESMFold PDB files start with "HEADER", not "ATOM" — fixed check
        text = resp.text.strip()
        if resp.status_code == 200 and (text.startswith("HEADER") or text.startswith("ATOM")):
            return jsonify({"pdb": resp.text})
        else:
            return jsonify({"error": f"API returned {resp.status_code}: {resp.text[:100]}"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "ESMFold API timed out (>60s)"}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reach ESMFold API — check internet"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    load_resources()
    app.run(debug=True, port=5000)
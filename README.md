# ProteinGen — AI Protein Designer

> A deep learning–powered web app that generates novel protein sequences using a GRU-based language model trained on the Human Proteome, scores them for biological plausibility, and predicts their 3D structure via the ESMFold API.

---

## 🎬 Demo
https://github.com/umeshchandra-k/GRU-Protein-Sequence-Generator/issues/1#issue-4429343947
---
## abstract 

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Sequence Generation | GRU language model generates novel protein sequences from a mutated seed |
| 🧪 Biological Scoring | Custom scoring for length, diversity, hydrophobicity, and charge balance |
| 🔄 Novelty Check | Compares generated sequences against the real dataset to ensure originality |
| 🌐 3D Structure Prediction | Integrates with ESMFold API to predict 3D protein structure |
| 🖥️ Interactive Web UI | Dark-themed Flask app with live 3D viewer powered by 3Dmol.js |

---

## 📁 Project Structure

```
protein-sequence-generator/
│
├── colab traning fie.ipynb          # Google Colab notebook — model training
│
└── gui_output/
    ├── app.py                       # Flask backend (main entry point)
    ├── requirements.txt             # Python dependencies
    ├── how to run.txt               # Quick-start instructions
    ├── demo.mp4                     # Demo video of the running app
    ├── data/
    │   └── dataset.fasta            # Human proteome dataset (UniProtKB)
    ├── model/
    │   └── model.keras              # Trained GRU model weights
    └── templates/
        └── index.html               # Frontend UI (dark theme + 3Dmol.js)
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **ML Model** | TensorFlow / Keras (GRU), NumPy, BioPython |
| **Web Backend** | Flask, Python 3.x |
| **3D Folding** | ESMFold API (`api.esmatlas.com`) |
| **3D Viewer** | 3Dmol.js |
| **Dataset** | UniProtKB Human Proteome `UP000005640` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- Internet connection *(required for ESMFold 3D folding)*

### Installation & Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/protein-sequence-generator.git
cd protein-sequence-generator

# 2. Go into the app folder
cd gui_output

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser at:

```
http://localhost:5000
```

---

## ⚙️ How It Works

```
Human Proteome (FASTA)
        ↓
  Sequence Preprocessing
  (filter standard amino acids, trim to 100 AA)
        ↓
  GRU Language Model Training   ← colab traning fie.ipynb
  (Embedding → GRU(128) → Dense(vocab_size))
        ↓
  Sequence Generation
  (seed from dataset + temperature sampling + mutation)
        ↓
  Biological Scoring
  (length, diversity, hydrophobicity, charge)
        ↓
  Top-N Sequences Selected
        ↓
  3D Structure Prediction via ESMFold API
        ↓
  Interactive 3D Visualization (3Dmol.js)
```

### Scoring Criteria

The `score_protein()` function evaluates each sequence on:

- ✅ **Length** — ideal range is 95–105 amino acids
- ✅ **Diversity** — penalizes sequences dominated by one amino acid (>30%)
- ✅ **Hydrophobicity** — target ~45% hydrophobic residues (`AILMFWV`)
- ✅ **Charge Balance** — charged residues (`KRDE`) should be 10–30%
- ❌ **Repeat Penalty** — long repeats like `LLLLLL` are penalized

---

## 🧠 Model Architecture

```
Input: 30-character amino acid window
    ↓
Embedding Layer  (vocab_size → 64 dims)
    ↓
GRU Layer        (128 hidden units)
    ↓
Dense Layer      (vocab_size units, softmax)
    ↓
Output: Probability distribution over next amino acid
```

**Training setup:**
- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Callbacks: `EarlyStopping` (patience=5), `ModelCheckpoint` (saves best weights)

---

## 🌐 API Reference

### `POST /generate`
Generates and scores novel protein sequences.

**Request:**
```json
{
  "n_proteins": 10,
  "top_n": 3,
  "temperature": 1.2
}
```

**Response:**
```json
{
  "results": [
    {
      "rank": 1,
      "sequence": "MKTAYIAKQRQISFVKSHFSRQ...",
      "score": 8.5,
      "similarity": 0.23
    }
  ]
}
```

### `POST /fold`
Predicts the 3D structure of a given sequence using ESMFold.

**Request:**
```json
{ "sequence": "MKTAYIAKQRQISFVKSHFSRQ..." }
```

**Response:**
```json
{ "pdb": "HEADER ...\nATOM  ..." }
```

---

## 📊 Dataset

| Property | Value |
|---|---|
| Source | UniProtKB / Swiss-Prot |
| Proteome ID | `UP000005640` (Human) |
| Format | FASTA |
| Filter | No stop codons (`*`), standard amino acids only |

> ⚠️ The `.fasta` file is ~40MB and excluded from version tracking via `.gitignore`. Download it from [UniProt Human Proteome](https://www.uniprot.org/proteomes/UP000005640).

---

## 📄 License

This project is for academic/educational purposes.
Dataset sourced from [UniProtKB](https://www.uniprot.org/) under their public data license.

---

*Built as a Major Project*

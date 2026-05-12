# AI-Guided Synthetic Protein Sequence Generation for Functional Protein Design Using GRU

A lightweight deep learning framework for generating biologically plausible synthetic protein sequences using Gated Recurrent Units (GRUs), physicochemical scoring, novelty assessment, and ESMFold-based 3D structure prediction.

---

# Abstract

Designing novel proteins computationally is a major challenge due to the enormous combinatorial complexity of protein sequence space. This project presents an AI-guided end-to-end protein generation pipeline using a GRU-based autoregressive sequence model trained on UniProtKB protein datasets.

The framework integrates:
- protein sequence preprocessing,
- GRU-based sequence modeling,
- temperature-controlled autoregressive generation,
- sequence scoring and filtering,
- novelty analysis,
- and ESMFold-based tertiary structure prediction.

Generated sequences are evaluated using multiple biological plausibility criteria including amino acid diversity, hydrophobic balance, charged residue composition, repetition penalties, and predicted structural confidence.

The proposed model demonstrates that lightweight recurrent architectures can generate biologically plausible protein-like sequences while remaining computationally efficient and accessible for modest GPU environments.

---

# Features

- GRU-based protein sequence generation
- UniProtKB FASTA dataset preprocessing
- Temperature-based sequence sampling
- Seed mutation strategy
- Multi-criteria protein scoring
- Sequence novelty analysis
- ESMFold 3D structure prediction
- Protein structure visualization
- Lightweight and GPU-efficient architecture

---

# Project Architecture

```text
UniProtKB Dataset
        ↓
Data Preprocessing
        ↓
Character Tokenization
        ↓
Sliding Window Generation
        ↓
GRU Model Training
        ↓
Temperature-Based Sampling
        ↓
Protein Sequence Generation
        ↓
Sequence Scoring & Filtering
        ↓
Novelty Assessment
        ↓
ESMFold 3D Structure Prediction# GRU-Protein-Sequence-Generator

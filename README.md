# AI-Guided Synthetic Protein Sequence Generation for Functional Protein Design Using GRU

A lightweight deep learning framework for generating biologically plausible synthetic protein sequences using Gated Recurrent Units (GRUs), physicochemical scoring, novelty assessment, and ESMFold-based 3D structure prediction.

---

# Abstract

Designing biologically plausible protein sequences from first principles remains a major challenge due to the immense combinatorial complexity of protein sequence space. This project presents a lightweight end-to-end artificial intelligence framework for synthetic protein sequence generation using a character-level Gated Recurrent Unit (GRU) model trained on UniProtKB protein datasets.

The proposed pipeline integrates autoregressive sequence generation, temperature-controlled sampling, sequence mutation, physicochemical scoring, novelty assessment, and ESMFold-based three-dimensional structure prediction within a unified framework. The GRU architecture consists of a 64-dimensional embedding layer, 128 hidden units, and a Softmax output layer trained using sparse categorical cross-entropy and the Adam optimizer.

Experimental results demonstrate that the framework generates diverse and biologically plausible protein-like sequences with quality scores ranging from 6.1 to 6.4 and novelty similarity values between 0.13 and 0.18, indicating low similarity to the training corpus. Predicted tertiary structures exhibit compact alpha-helical and mixed secondary-structure patterns with pLDDT confidence scores above 70, suggesting structurally feasible folding behavior.

Despite requiring only approximately 78K trainable parameters and modest GPU resources, the framework achieves competitive sequence-generation performance while remaining computationally accessible for resource-constrained academic environments. This work highlights the potential of lightweight recurrent architectures for accelerating computational protein design, synthetic biology research, and AI-assisted biomolecular engineering.

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

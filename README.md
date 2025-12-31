# 🧠 Improving Named Entity Recognition for Roman Urdu  
### Through Normalization and Transliteration

📌 **Natural Language Processing | Named Entity Recognition | Low-Resource Languages**

---

## 📖 Overview

Roman Urdu, widely used on social media and informal digital platforms, suffers from severe spelling inconsistencies and lack of standardization. This poses major challenges for Named Entity Recognition (NER) systems, especially those trained on standard Urdu script.

This project proposes a **four-phase preprocessing and modeling pipeline** that significantly improves Roman Urdu NER performance by combining:

- Rule-based normalization  
- Phonetic mapping  
- Roman-to-Urdu transliteration  
- Parameter-efficient fine-tuning (LoRA) of **XLM-RoBERTa**

📈 **Result:**  
F1-score improved from **45.50% → 71.88%** (≈ **58% relative improvement**) without changing model architecture — purely via better preprocessing.

---

## 🚀 Key Contributions
 
- 🧹 Designed a **two-layer normalization pipeline** for noisy Roman Urdu  
- 🔄 Implemented fast **dictionary-based transliteration with caching**  
- 🤖 Fine-tuned **XLM-RoBERTa using LoRA** for efficient NER training  
- 🧪 Demonstrated large performance gains solely from preprocessing  

---

---

### 🔹 Mapping Dictionary Sources

| Dataset | Description | Size |
|------|------------|------|
| English-Urdu-Roman.txt | Trilingual word pairs | 489 |
| urdu_roman.tsv | Urdu–Roman mappings | 4,107 |
| UrduHighFreqList.xlsx | High-frequency Urdu words | 4,999 |
| pos.txt | Positive sentiment words | 1,853 |
| neg.txt | Negative sentiment words | 4,167 |

➡️ **Final dictionary size:** **15,615 unique word pairs**

---

### 🔹 NER Dataset

- **MK-PUCIT Urdu NER Dataset**
- IOB tagging scheme:
  - `B-PER`, `I-PER`
  - `B-LOC`, `I-LOC`
  - `B-ORG`, `I-ORG`
  - `O`

---

## 🧹 Normalization Strategy

### Layer 1: Rule-Based Normalization

Handles common abbreviations:

| Roman Urdu | Normalized |
|---------|------------|
| `lhr` | lahore |
| `khi` | karachi |
| `isb` | islamabad |
| `imrn` | imran |

---

### Layer 2: Phonetic Mapping (OOV Handling)

- Detects unseen words  
- Applies phonetic pattern expansion  
- Iteratively updates dictionary  

---

## 🔄 Transliteration

- Local dictionary lookup (no API latency)  
- Caching for frequent tokens  
- Fallback character-level rules  

Generated outputs:

- **Baseline_Urdu** (no normalization)  
- **Optimized_Urdu** (after normalization)  

Saved in: mkpucit_final_ner_input.csv


---

## 🤖 Model & Training

### Model
- **XLM-RoBERTa (XLM-R)**  
- Multilingual transformer (100+ languages)

### Fine-Tuning Method
- **LoRA (Low-Rank Adaptation)**  
- Frozen base model  
- Trains only lightweight adapter layers  

### Experiments

| Run | Input | F1-Score |
|----|------|---------|
| Baseline | Noisy Roman Urdu → Urdu | 45.50% |
| Optimized | Normalized Roman Urdu → Urdu | **71.88%** |

---

## 📊 Results Summary

- **Absolute improvement:** +26.38%  
- **Relative improvement:** ≈ 58%  
- Major gains in **Location** and **Person** entities  
- Errors mostly due to:
  - Organization name ambiguity  
  - Remaining OOV cases  

---

## 🛠️ Tech Stack

- **Python**
- `pandas`
- `transformers` (Hugging Face)
- `torch`
- `scikit-learn`
- `matplotlib`, `seaborn`

---

## 🔮 Future Work

- Expand normalization dictionary via social media mining  
- Context-aware normalization  
- Joint normalization + NER training  
- Apply pipeline to Roman Hindi & Arabic chat alphabet  
- Real-time social media processing  

---

## 📜 Citation

If you use this work, please cite:

> *Improving Named Entity Recognition for Roman Urdu Through Normalization and Transliteration Pipeline*, 2025.










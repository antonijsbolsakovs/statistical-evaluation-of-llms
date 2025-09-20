# Preserving Linguistic Diversity in the AI Era  
**Analyzing English Intrusion in Danish LLM Outputs**

## 📌 Overview
This project investigates how English words intrude into Danish-language outputs of large language models (LLMs), focusing on Google Gemini 1.5 Flash and 2.0 Flash.  
We conducted a statistical evaluation of model responses across multiple categories (STEM, FAQ, Riddles, Creative, etc.), using methods such as correlation, ANOVA, Association Rule Mining, and Mann-Whitney U tests.  

Key finding:  
- **Gemini 2.0 Flash** shows a significantly stronger correlation between response length and English word usage than Gemini 1.5 Flash.  
- This highlights potential risks for **linguistic diversity** in smaller languages when using advanced LLMs.  

---

## 👥 Authors
- Antonijs Bolsakovs (DTU, General Engineering – Cyber Systems)  
- Mattis Kragh (DTU, AI & Data)  
- Ro Nanak Prasad Lacoul (DTU, AI & Data)  
- Christopher Alexander Holm Kjær (DTU, AI & Data)  

---

## 📂 Repository Structure
```text
.
├── src/                # Source code (Python scripts & notebooks)
│   ├── AMining.py
│   ├── text_analysis.py
│   ├── reading_prompts.py
│   ├── new_text_cleaner.py
│   ├── text-cleaner.py
│   └── generate_danish_words.py
│
├── data/               # Datasets and prompts
│   ├── prompts/        # Danish prompts used for LLM evaluation
│   └── prompts.txt
│
├── docs/               # Reports and documentation
│   ├── Synopsis.pdf
│   └── Project_Report.pdf
│
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
---

## 📊 Methods Used
- **Association Rule Mining (FP-Growth)**  
- **Pearson Correlation** (response length vs. English intrusion)  
- **Two-Way ANOVA** (effects of model & category)  
- **Mann-Whitney U Test** (non-parametric comparison)  
- **Shapiro-Wilk Test** (normality check)  

---

## 📈 Results
- Gemini 2.0 Flash introduces **more English words** in Danish responses compared to 1.5.  
- Stronger correlation between **response length** and English usage in STEM and FAQ categories.  
- English intrusion includes both **general vocabulary** and **technical terms**, raising concerns about bias toward English.  

---

## 📑 Documentation
- 📄 [Final Report (PDF)](docs/Project_Report.pdf)  
- 📄 [Synopsis (PDF)](docs/Synopsis.pdf)  

---

## ⚙️ How to Run
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
2.	Run analysis scripts (examples):
python src/text_analysis.py
python src/AMining.py
## 📌 Disclosure

This project was completed as part of DTU course: Project in Statistical Evaluation for Artificial Intelligence and Data (02445).
AI tools were used in debugging parts of the code.
---

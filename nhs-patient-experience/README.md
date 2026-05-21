# Patient Experience Analytics Using NHS Survey Data

Secondary analysis of NHS patient experience surveys using sentiment analysis, topic modelling, and visualisation to identify satisfaction drivers and service improvement opportunities.

## Project structure

```
nhs-patient-experience/
├── data/
│   ├── raw/           # Downloaded NHS files (do not commit large files without .gitignore)
│   └── processed/     # Cleaned CSV/Parquet for analysis
├── docs/
│   ├── ACRONYM_GLOSSARY.md   # Deep reference: every acronym in the project
│   ├── DATA_SOURCES.md       # Where to download data + NLP suitability
│   ├── PROJECT_SCOPE.md      # Complexity, risks, timeline
│   └── ETHICS_AND_GOVERNANCE.md
├── literature/        # Papers, briefing notes, exports
├── notebooks/         # Exploratory analysis (Jupyter)
├── src/               # Reusable Python modules
├── outputs/
│   ├── figures/
│   └── reports/
└── requirements.txt
```

## Quick start

1. Read `docs/ACRONYM_GLOSSARY.md` — NHS and NLP terminology.
2. Read `docs/DATA_SOURCES.md` — choose primary dataset (weeks 1–2).
3. Install dependencies: `pip install -r requirements.txt`
4. Place downloads in `data/raw/` (see `data/raw/README.md`).

## Research questions

1. What themes emerge from patient feedback across NHS services?
2. How can sentiment analysis help evaluate patient satisfaction?
3. What improvements can be recommended based on the findings?

## Team roles (4 members)

| Role | Focus |
|------|--------|
| Data Preprocessing Lead | Cleaning, sampling, schema documentation |
| NLP Specialist | VADER, TextBlob, LDA, keywords |
| Visualisation Lead | Charts, Streamlit/dashboard |
| Documentation Lead | Literature review, evaluation, report |

## 14-week timeline

| Weeks | Activity |
|-------|----------|
| 1–2 | Literature review, dataset selection, ethics sign-off |
| 3–4 | Data cleaning and exploratory analysis |
| 5–7 | NLP (sentiment, topics, keywords) |
| 8–9 | Visualisation and dashboard |
| 10–11 | Interpretation and recommendations |
| 12–13 | Report writing |
| 14 | Final submission |

## Key references

- [NHS Surveys data library](https://nhssurveys.org/data-library/)
- [GP Patient Survey](https://gp-patient.co.uk/)
- [NHS England FFT data](https://www.england.nhs.uk/statistics/statistical-work-areas/friends-and-family-test-statistics/)
- [ONS Experiences of NHS healthcare (England)](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthcaresystem/datasets/experiencesofnhshealthcareservicesinengland)

## Licence note

NHS and UK government publications are typically under the [Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/). Always cite the source survey and wave/year in your report.

# NHS Patient Experience — Data Sources

Where to obtain data, what each file contains, and suitability for **sentiment analysis / LDA**.

---

## Summary matrix

| Source | Geography | Typical format | Free text? | Best for |
|--------|-----------|----------------|------------|----------|
| **NPSP / Adult Inpatient** | England | .ods, .xlsx aggregates | No (public) | Trust comparisons, Likert drivers |
| **GP Patient Survey (GPPS)** | England | National + practice tables | Rarely public | Access, continuity, satisfaction trends |
| **Friends & Family Test (FFT)** | England | Monthly Excel | No (national); comments local | Headline scores, setting comparisons |
| **ONS Health Insight** | England | Excel/CSV waves | **Sometimes** (open-ended items) | **NLP-primary candidate** |
| **Health & Care Experience (HCE)** | Scotland | gov.scot publications | Limited in open tables | Scottish context / PREM comparison |
| **NHS Surveys qualitative insight** | England | Reports + excerpts | Thematic examples | Literature / validation quotes (cite source) |

---

## 1. NHS Patient Survey Programme (NPSP)

**Portal:** [https://nhssurveys.org/data-library/](https://nhssurveys.org/data-library/)

**Contact for older waves:** patient.survey@cqc.org.uk

### Available surveys (England)

| Survey | Folder on data library | Years (typical) |
|--------|------------------------|-----------------|
| Adult Inpatient | `02-adults-inpatients` | 2015–2022+ |
| Urgent & Emergency Care | `03-urgent-emergency-care` | Type 1 / Type 3 files |
| Maternity | `04-maternity` | 2015–2024 |
| Community Mental Health | `05-community-mental-health` | 2015–2023 |
| Children & Young People | `01-children-patient-experience` | 2016–2020 |

### File types

- **National tables** — England-wide % per question.
- **Benchmark / Trust-level** — Compare organisations.
- **Site-level** — Hospital site (where applicable).

### NLP note

These files are **pre-aggregated statistics**. Your NLP pipeline needs **one row per comment** (or per synthetic document). Plan:

- **Quantitative path:** model satisfaction drivers from Likert (% positive).
- **Mixed path:** request qualitative reports or use ONS open text (below).

---

## 2. GP Patient Survey (GPPS)

**Portal:** [https://gp-patient.co.uk/](https://gp-patient.co.uk/)  
**Statistics:** [NHS England — GP Patient Survey](https://www.england.nhs.uk/statistics/statistical-work-areas/patient-surveys/gp-patient-survey/)

### Scale (2025 example)

- ~2.7M invitations, ~700k responses (~26% response rate).

### Domains (psychometric structure)

1. Doctor/nurse care  
2. Access to care  
3. Overall primary care aspects  

### Time series warning

**2024 onward = new time series.** Document break when plotting multi-year trends.

### NLP note

Public releases are **tabular**. Open-ended patient comments are **not** routinely published at practice level for privacy.

---

## 3. Friends and Family Test (FFT)

**Portal:** [NHS England FFT statistics](https://www.england.nhs.uk/statistics/statistical-work-areas/friends-and-family-test-statistics/)  
**Patient info:** [NHS.uk FFT](https://www.nhs.uk/using-the-nhs/about-the-nhs/friends-and-family-test-fft/)

### Settings in monthly files

A&E, ambulance, community health, dental, GP, inpatient, maternity, mental health, outpatient, etc.

### Core question

> “Overall, how was your experience of our service?”

Responses: very good, good, neither, poor, very poor, don't know.

### Scoring (national publication)

Headline metric commonly:

**% very good − (% poor + % very poor)**

See: [FFT Publication Guidance PDF](https://assets.publishing.service.gov.uk/media/5a7b83b3e5274a7202e17a95/Friends-and-Family-Test-Publication-Guidance-v2-FOR-PUBLIC_E2_80_A6.pdf)

### NLP note

Ideal for **dashboard KPIs** and correlating with other datasets at trust level. **Not** ideal as sole source for LDA unless you obtain comment-level extracts under governance approval.

---

## 4. ONS — Experiences of NHS healthcare services in England

**Portal:** [ONS dataset page](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthcaresystem/datasets/experiencesofnhshealthcareservicesinengland)

Commissioned by NHS England (Health Insight). Covers GP, waiting lists, community services, dentistry, pharmacy, etc.

### Why prioritise for NLP

Microdata files may include **open-ended responses** suitable for tokenisation and sentiment (always read the **technical report** for the wave you use).

### Action (week 1)

1. Download latest **wave** metadata + dataset.  
2. Identify open-text fields and missingness.  
3. Document sample size and weights in `data/processed/DATA_DICTIONARY.md`.

---

## 5. Scotland — PREM-related sources

| Resource | URL / note |
|----------|------------|
| **Health & Care Experience Survey** | [gov.scot news / publications](https://www.gov.scot/news/health-and-care-experience-survey-202324-results-published/) |
| **SCPES** | [PHS Shiny app — SCPES 2024](https://scotland.shinyapps.io/phs-scpes-2024/) |
| **National PREM refresh (Wales example)** | [CEDAR NHS Wales PREM report](https://cedar.nhs.wales/files/national-prem-refresh-interim-report/) |

Use if your brief requires **UK-wide** comparison; otherwise England-only reduces scope.

---

## 6. Suggested dataset strategy for this project

### Path A — Text-first (recommended if ONS text confirmed)

1. **Primary:** ONS Health Insight open-ended fields (one wave).  
2. **Secondary:** FFT trust-level scores merged by region/trust code (if code harmonisation possible).  
3. **Validation:** Manual thematic coding on 50–100 random comments.

### Path B — Tables-first (fallback)

1. **Primary:** GPPS + Adult Inpatient national tables.  
2. **Secondary:** FFT trends by setting.  
3. **NLP-lite:** Treat each **survey question label + national summary sentence** as documents only for pilot — **not** sufficient for full dissertation NLP; use quantitative driver analysis instead.

---

## 7. Download checklist (`data/raw/`)

```
[ ] Dataset chosen and wave/year recorded
[ ] OGL / licence noted in README
[ ] File hash / download date in DATA_DICTIONARY.md
[ ] No PII in raw folder (or encrypted volume if microdata)
[ ] Pilot load: pandas read successful
[ ] Text column identified OR pivot to Path B documented
```

---

## 8. Harmonisation challenges

| Issue | Mitigation |
|-------|------------|
| Different geographies (England vs Scotland) | Analyse separately or harmonise at UK-narrative level only |
| Trust codes change (mergers) | Use publication year trust list |
| GPPS 2024 time series break | Split charts at 2024 |
| FFT monthly vs annual surveys | Aggregate FFT to quarters for comparison |
| British spelling | Custom VADER lexicon optional (`nhs`, `A&E`, `GP`) |

---

*See also: `ACRONYM_GLOSSARY.md`, `PROJECT_SCOPE.md`, `ETHICS_AND_GOVERNANCE.md`*

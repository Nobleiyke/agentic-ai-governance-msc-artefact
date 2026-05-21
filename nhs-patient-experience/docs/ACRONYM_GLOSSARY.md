# Acronym & Terminology Glossary

Deep reference for the **Patient Experience Analytics** project. Acronyms are grouped by domain. Where an acronym has multiple meanings in health data, both are noted.

---

## 1. NHS organisations & governance

| Acronym | Full form | What it means (in this project) |
|---------|-----------|-----------------------------------|
| **NHS** | National Health Service | Publicly funded healthcare system in the UK. Your project uses **England** surveys primarily; Scotland/Wales have separate programmes. |
| **NHSE** / **NHS England** | NHS England | Arms-length body responsible for commissioning and health statistics in England (e.g. FFT publications, GPPS statistics pages). |
| **DHSC** | Department of Health and Social Care | UK government department overseeing health policy; historically launched the Patient Survey Programme (2002). |
| **CQC** | Care Quality Commission | Independent regulator for health and social care in **England**. **Leads the NHS Patient Survey Programme (NPSP)** and publishes inpatient and related survey results with Picker. |
| **ONS** | Office for National Statistics | UK’s national statistics institute. Runs **Health Insight** / “Experiences of NHS healthcare services in England” with NHS England — useful for open-ended text in some waves. |
| **PHS** | Public Health Scotland | National public health agency in Scotland; partners on surveys such as SCPES. |
| **ICB** | Integrated Care Board | Replaced Clinical Commissioning Groups (CCGs) in 2022; local NHS organisations that plan and commission services. FFT/GPPS data may be broken down by ICB or STP legacy areas. |
| **NHS Trust** | NHS Trust | Organisation providing hospital/community services in England. Inpatient survey data often reported at **trust** and **site** level. |
| **GP Practice** | General Practice | Primary care provider; unit of analysis for **GP Patient Survey (GPPS)**. |

---

## 2. Patient experience surveys (your core datasets)

| Acronym | Full form | What it means |
|---------|-----------|---------------|
| **NPSP** | NHS Patient Survey Programme | Umbrella programme (since 2002) coordinated for CQC. Includes **Adult Inpatient**, **Urgent & Emergency Care**, **Maternity**, **Children & Young People**, and **Community Mental Health** surveys. |
| **AIS** | Adult Inpatient Survey | Annual survey of adults (16+) who stayed **at least one night** as inpatients. Measures communication, cleanliness, discharge, dignity, etc. Public data: national/trust/site **tables** (.ods/.xlsx) — typically **not** individual free-text comments. |
| **GPPS** | GP Patient Survey | Large annual survey (~millions invited) on access, appointments, GP/nurse care, pharmacy, dentistry. Managed with NHS England; results at [gp-patient.co.uk](https://gp-patient.co.uk/). **2024+** started a new time series — compare years carefully. |
| **FFT** | Friends and Family Test | Short feedback tool (from April 2013): “Overall, how was your experience of our service?” (very good → very poor). Used across hospitals, GP, A&E, maternity, mental health, etc. National **monthly** aggregate Excel files. Optional **written comments** exist locally but are **rarely** in national open downloads. |
| **UEC** | Urgent and Emergency Care Survey | NPSP survey for adults using **Type 1** (major A&E) and **Type 3** (urgent treatment centres) — “Type 1/3” in data filenames. |
| **CYPPE** | Children and Young People's Patient Experience Survey | Inpatient/day-case experiences for under-16s (since 2014). |
| **CMHS** | Community Mental Health Survey | Experiences of community mental health care (NPSP). |
| **HCE** | Health and Care Experience Survey | **Scotland** — biennial postal survey (GP, out-of-hours, social care) since 2009; over 100k respondents in recent waves. |
| **SCPES** | Scottish Cancer Patient Experience Survey | Scotland-specific cancer pathway experience survey (Scottish Government / Macmillan / PHS). |
| **SIPES** | Scottish Inpatient Patient Experience Survey | Scottish equivalent of inpatient experience measurement (context for **PREM** work in Scotland). |

### FFT scoring (important for analysis)

| Term | Meaning |
|------|---------|
| **FFT headline score** | Often published as: **% “very good”** minus **% (“poor” + “very poor”)** — aligned with **Net Promoter-style** logic (see NHS FFT Publication Guidance). |
| **“Recommend” question (legacy)** | Earlier FFT also asked whether people would recommend the service to friends/family; wording has evolved — check the wave you use. |

---

## 3. Experience vs outcome measures (often confused)

| Acronym | Full form | What it measures | Use in your project |
|---------|-----------|------------------|---------------------|
| **PREM** | Patient-Reported Experience Measure | Whether patients **experienced** aspects of care (communication, involvement, timeliness of information). Focus on **process and service**. | **Core concept** for your dissertation — surveys are PREM instruments. |
| **PROM** | Patient-Reported Outcome Measure | Patient’s **health status/symptoms** (pain, mobility, quality of life) — e.g. after surgery. | **Different** from experience. Weak correlation with PREMs. Mention only if you use PROM data (e.g. national hip/knee programme) — not required for GPPS/FFT. |
| **PRO** | Patient-Reported Outcome | Generic term for outcomes reported by patients (not staff). | Umbrella term; can mean PROM or broader PRO instruments. |
| **PREMs** / **PROMs** | Plural of above | Programme-level collections (e.g. NHS England PROMs for four procedures). | Scotland/Wales run **PREM** refresh programmes; England GPPS/FFT are experience-focused. |
| **EQ-5D** | EuroQol 5-Dimension | Common **PROM** generic health-related quality of life measure (5 dimensions + optional VAS). | Example only — not central unless you link outcomes to experience. |
| **PROMs programme** | NHS national PROMs | Pre/post operative outcomes for selected procedures. | Do not confuse with **patient experience** surveys. |

---

## 4. Frameworks & quality domains

| Acronym | Full form | What it means |
|---------|-----------|---------------|
| **STEEEP** | Safety, Timeliness, Effectiveness, Efficiency, Equity, Person-centredness | Quality framework; PREMs often mapped to these domains. |
| **PEF** | Patient Experience Framework | NHS framework (coordination, communication, physical comfort, emotional support, etc.) — use to **structure recommendations** in your report. |
| **NPS** | Net Promoter Score | Commercial metric: % promoters − % detractors. **FFT national reporting** uses a **similar subtractive method** on experience ratings (very good vs poor/very poor) — cite NHS methodology, don’t assume identical to commercial NPS without checking the guidance PDF. |
| **Likert scale** | (named after Rensis Likert) | Ordered response scale (e.g. “strongly agree” to “strongly disagree”). Most NHS survey questions are **categorical/Likert**, not free text. |

---

## 5. Survey operations & data types

| Term | Meaning |
|------|---------|
| **Picker** | Picker Institute Europe — **CQC-approved contractor** running several NPSP surveys (coordination centre). |
| **SCC** | Survey Coordination Centre | Based at Picker; coordinates fieldwork and national reporting for NPSP. |
| **Mixed-mode** | Survey offered **online and on paper** (common since ~2020 for inpatient survey) — affects response bias; document in limitations. |
| **National tables** | Aggregated % positive / negative / neutral by question for England. |
| **Trust-level / Site-level** | Results for each NHS trust or hospital site — good for **comparative charts**, not for NLP unless you have text. |
| **Benchmark data** | Comparative statistics (e.g. trust vs national distribution). |
| **Response rate** | % of invited patients who completed the survey — GPPS often ~25–30%; low rates affect generalisability. |
| **Weighting** | Statistical adjustment so samples match population demographics — check technical notes before comparing subgroups. |
| **Wave** | Survey round (e.g. ONS Health Insight Wave 22) — always cite **year + wave**. |
| **Time series** | Comparable results over years — **GPPS 2024** reset series; do not merge pre-2024 and post-2024 without adjustment notes. |

---

## 6. Legal, ethics & data protection

| Acronym | Full form | What it means |
|---------|-----------|---------------|
| **GDPR** | General Data Protection Regulation | EU/UK law on personal data. Free-text comments may contain **identifiable information** — handle securely; prefer **aggregated open data** for coursework. |
| **UK GDPR** | UK retained GDPR | Post-Brexit UK version — same practical rules for student projects. |
| **DPA 2018** | Data Protection Act 2018 | UK legislation underpinning GDPR. |
| **PII** / **PID** | Personally Identifiable Information / Data | Names, NHS numbers, rare combinations in small areas — **redact** in any text you process. |
| **IG** | Information Governance | NHS rules for lawful data use — required if accessing **non-public** trust-level comment extracts. |
| **OGL** | Open Government Licence | Permits reuse of many NHS/ONS publications with attribution. |
| **Secondary data** | Data collected by others | Your project type — no new patient recruitment; still needs ethics statement on reuse. |

---

## 7. NLP & methodology (your analysis stack)

| Acronym | Full form | What it means |
|---------|-----------|---------------|
| **NLP** | Natural Language Processing | Computational analysis of text — sentiment, topics, keywords. |
| **VADER** | Valence Aware Dictionary and sEntiment Reasoner | Rule-based sentiment tool tuned for **social media**; handles emphasis (!!!) and emoticons. Fast; works on short text; weaker on clinical jargon and British spelling unless you validate. |
| **TextBlob** | (library name) | Python library wrapping pattern-based sentiment + simple NLP; polarity ∈ [-1, 1]. |
| **LDA** | Latent Dirichlet Allocation | **Unsupervised** topic model — discovers word groups (“topics”) across documents. Requires tuning (# topics, stopwords). |
| **TF-IDF** | Term Frequency–Inverse Document Frequency | Weighting rare important words — used for keywords and sometimes topic models. |
| **BoW** | Bag of Words | Document representation as word counts — ignores word order. |
| **Lemmatization** | (process) | Reduces words to dictionary form (“running” → “run”) using lexicons (NLTK/spaCy). Better than **stemming** for report readability. |
| **Tokenization** | (process) | Splitting text into words/tokens. |
| **Stop words** | Common words filtered out | e.g. “the”, “and” — customise for NHS (“patient”, “nhs”) or topics become trivial. |
| **Sentiment polarity** | Positive vs negative score | Continuous or trinary label from VADER/TextBlob. |
| **Thematic analysis** | Qualitative method | Human-coded themes — complement LDA with **manual coding** of a sample (e.g. 100 comments) for validity. |
| **Topic coherence** | (metric) | How interpretable LDA topics are — optional quality check (e.g. Cv coherence). |

---

## 8. Statistics & visualisation (supporting analysis)

| Acronym | Full form | What it means |
|---------|-----------|---------------|
| **EDA** | Exploratory Data Analysis | Initial charts and summaries before modelling. |
| **OLS** | Ordinary Least Squares | Linear regression — e.g. sentiment vs trust FFT score (if merged). |
| **GLM** | Generalised Linear Model | Regression for non-normal outcomes (counts, binary satisfaction). |
| **Chi-square** | χ² test | Tests association between categorical variables (e.g. setting × rating). |
| **CI** | Confidence Interval | Range for an estimate — report with proportions. |
| **CSV** / **ODS** / **XLSX** | File formats | NHS downloads often **ODS** (OpenDocument) or Excel — load with `pandas` + `odfpy` or export to CSV in LibreOffice/Excel. |

---

## 9. Acronyms that are NOT your main datasets (avoid confusion)

| Acronym | Common meaning | Why it matters |
|---------|----------------|----------------|
| **APMS** | Adult Psychiatric Morbidity Survey | **National mental health prevalence** survey — **not** inpatient experience. |
| **HCAI** | Healthcare-associated infection | Safety metric — different domain. |
| **RTT** | Referral to Treatment | Waiting-time performance — related to satisfaction but different dataset. |
| **NEWS** | National Early Warning Score | Clinical observation score — not patient feedback. |
| **CCG** | Clinical Commissioning Group | **Replaced by ICBs** — old labels in historic FFT files. |

---

## 10. Recommended citations in your report

When you first use each survey, write out the full name then acronym:

> “The Friends and Family Test (FFT) aggregates monthly experience scores across NHS trusts…”

> “Patient-Reported Experience Measures (PREMs) differ from Patient-Reported Outcome Measures (PROMs) in that PREMs capture perceptions of care processes rather than symptom change (BMJ Open Quality, 2020).”

---

## Sources

- [NHS Surveys — About us (NPSP, CQC, Picker)](https://nhssurveys.org/about-us/)
- [NHS Friends and Family Test](https://www.nhs.uk/using-the-nhs/about-the-nhs/friends-and-family-test-fft/)
- [FFT Publication Guidance (GOV.UK)](https://assets.publishing.service.gov.uk/media/5a7b83b3e5274a7202e17a95/Friends-and-Family-Test-Publication-Guidance-v2-FOR-PUBLIC_E2_80_A6.pdf)
- [GP Patient Survey — NHS England statistics](https://www.england.nhs.uk/statistics/statistical-work-areas/patient-surveys/gp-patient-survey/)
- [Patient-reported outcomes and experiences (GOV.UK)](https://www.gov.uk/guidance/patient-reported-outcomes-and-experiences-study)
- [CQC Adult Inpatient Survey](https://www.cqc.org.uk/publications/surveys/adult-inpatient-survey)
- [Picker — Adult Inpatient Survey](https://picker.org/how-we-can-help/national-survey-programmes/adult-inpatient-survey/)

*Last updated: May 2026 — verify survey names and URLs before final submission.*

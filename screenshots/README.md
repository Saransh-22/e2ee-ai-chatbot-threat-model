# Project Demonstration Screenshots & Verification Index

This directory contains the actual visual demonstration captures of the **E2EE AI Chatbot Threat Modeler and Risk Analyzer** micro-project (`22AI73`).

All screenshots were automatically captured from the live application and runtime test environment using Microsoft Edge via Playwright automation.

---

## Verified Screenshot Index

| Filename | Source Interface / Page | Captured Content & Key Elements | Dimensions | Status |
|:---|:---|:---|:---:|:---:|
| **`image1.png`** | `🛡️ STRIDE Threat Model` | Full STRIDE catalog table, category badges (S, T, R, I, D, E), filter selectors (Category, Component, Risk Level), and search bar. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image2.png`** | `📈 Risk Analysis` | Interactive Risk Simulator ($L \times I$ sliders, dynamic tier badge, calculation breakdown), and risk matrix summary. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image3.png`** | `🔐 Mitigation Controls` | Security Control Posture KPI cards (62.5% Mitigated), mitigation domain filter, and Traceability Matrix (Threat ID $\rightarrow$ STRIDE $\rightarrow$ Control $\rightarrow$ Mitigation). | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image4.png`** | `🏛️ System Architecture` | 9-component interactive architecture graph, trust boundary indicators (TB-01 to TB-04), and Draw.io XML export button. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image5.png`** | `🔀 Data Flow Analysis` | Data flows $F_1$ through $F_6$ table, source/destination components, payload protection mechanism (AEAD/Double Ratchet), and trust boundary crossings. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image6.png`** | `📈 Risk Analysis` | Actual 5&times;5 Likelihood vs. Impact Risk Heatmap with color gradients and threat count clusters in cells. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image7.png`** | `📊 Dashboard` | Actual Executive Dashboard showing top KPI cards (24 Total, 4 Critical, 6 High, 11 Med, 3 Low), and STRIDE category / Risk Distribution charts. | 2000 &times; 1313 | **CAPTURED & VERIFIED** |
| **`image8.png`** | Terminal Execution | Exact live `pytest -v` console run showing all **43 passed in 0.14s**. | 1500 &times; 1340 | **CAPTURED & VERIFIED** |

---

## Technical Audit Details
- **Capture Tooling:** Playwright 1.63 + Chromium / Microsoft Edge
- **Render Mode:** Live Streamlit application (`http://localhost:8501`)
- **Image Format:** PNG (Lossless, High Resolution, No Fabrication)
- **Zero Mock Policy:** All metrics, table rows, risk scores, and test assertions match the underlying repository code and datasets.

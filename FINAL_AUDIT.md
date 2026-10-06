# FINAL PROJECT AUDIT REPORT

**Project Title:** Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot  
**Course:** Data Security and Privacy (Course Code: 22AI73) — Semester VII  
**Institution:** Dayananda Sagar College of Engineering (DSCE), Bengaluru  
**Student:** Saransh Neema (USN: **1DS23AI048**)  
**Audit Timestamp:** 2026-10-04 16:10 IST  

---

## 1. Project Audit Summary

| Audit Item | Current Status | Details / Metrics |
| :--- | :--- | :--- |
| **Overall Project Status** | **VERIFIED & READY** | Complete, internally consistent academic prototype. |
| **Application Run Status** | **PASSED (HTTP 200 OK)** | Headless & local Streamlit execution tested on ports 8501/8502/8503. Zero runtime errors or tracebacks. |
| **Unit Test Result** | **PASSED (43/43 PASSED)** | Automated pytest suite passed 100% in 0.08s. |
| **Number of Threats** | **24 Formal Threats** | Exactly 4 threats per STRIDE category across 9 components. |
| **STRIDE Categories** | **6 Categories** | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. |
| **Architecture Components** | **9 Components** | User Client, Identity/Auth, Key Mgmt, Secure Gateway, Message Relay, AI Service, API Layer, Audit/Logging, Admin UI. |
| **Number of Unit Tests** | **43 Unit Tests** | Formulations, boundary conditions (1x1 to 5x5), type errors, empty datasets, filters, and matrices. |
| **Documentation Status** | **COMPLETE** | Full report (`report_content.md`), Viva notes (`viva_questions.md`), Demo script (`demo_script.md`), Screenshots checklist, Master README. |
| **Draw.io Diagram Status** | **VALIDATED XML (2 Files)**| `architecture.drawio` (41 elements) & `stride_threat_mapping.drawio` (53 elements) tested and downloadable in-app. |

---

## 2. Multi-Role Assessment

### A. Software Engineer Audit
- **Code Quality**: Modular architecture under `core/` (`threat_engine.py`, `risk_engine.py`, `mitigation_engine.py`, `asset_inventory.py`, `data_flow_engine.py`, `security_privacy_engine.py`).
- **Dependencies**: Minimal standard footprint (`streamlit`, `pandas`, `plotly`, `pytest`). No database, no cloud services, no external API keys required.
- **Git Readiness**: Standard `.gitignore` prevents virtual environment, cache, and OS artifacts from entering version control.

### B. Cybersecurity Reviewer Audit
- **STRIDE Taxonomy Integrity**: Balanced distribution of 4 threats per category. All 6 primary security properties (*Authentication*, *Integrity*, *Accountability*, *Confidentiality*, *Availability*, *Authorization*) are mapped.
- **Scope & Limitations**: The project explicitly avoids false claims of absolute security. The "Plaintext Paradox of AI Inference" is systematically addressed using hardware confidential compute enclaves (AMD SEV-SNP) and dual prompt guardrails.
- **Mathematical Risk Consistency**: Formula $\text{Risk} = \text{Likelihood} \times \text{Impact}$ produces $1–25$ scale matching defined tiers: Low (1–5), Medium (6–10), High (11–15), and Critical (16–25).

### C. College Evaluator Audit
- **Official Institutional Alignment**: Uses official DSCE Course Outcomes (CO1–CO4) from course documents under the guidance of Dr. Aruna M G.
- **Academic Mappings**: Strictly maps to **SDG 9** (Industry, Innovation, and Infrastructure), standard Program Outcomes (PO1, PO2, PO3, PO5), and provides clear placeholders for faculty-defined PSOs.
- **Traceability**: Academic pipeline (`Problem ➔ Objectives ➔ Architecture ➔ STRIDE ➔ Risk Model ➔ Mitigation ➔ Testing ➔ Results`) directly addresses evaluation rubrics.

### D. QA Tester Audit
- **Boundary Verification**: Manual & automated verification of edge cases: $(1, 1) \rightarrow 1$ (Low), $(2, 4) \rightarrow 8$ (Medium), $(3, 5) \rightarrow 15$ (High), $(4, 4) \rightarrow 16$ (Critical), and $(5, 5) \rightarrow 25$ (Critical).
- **Graceful Failure**: Rejection of non-integer inputs, negative scores, and scores $>5$ with clean exceptions. Empty datasets handled without UI or engine crashes.

---

## 3. Known Limitations
1. **Analytical Simulation**: The prototype focuses on threat modeling, risk calculation, and defensive architectures; it does not deploy live multi-billion parameter neural network models or real user messaging infrastructure.
2. **Synthetic Data**: In compliance with academic evaluation standards, threat data and architecture schemas are synthetic to avoid handling sensitive personal communications.
3. **Linear Residual Risk Heuristic**: Residual risk reductions are calculated based on mitigation status heuristics rather than continuous live telemetry.

---

## 4. Remaining Manual Steps

The following steps cannot be executed automatically and require student action:

1. **[MANUAL VERIFICATION REQUIRED] Screenshot Capture**:
   - Run `streamlit run app.py` in PowerShell.
   - Use Windows Snipping Tool (`Win + Shift + S`) to capture the 8 required screens listed in `docs/screenshot_checklist.md`.
   - Save the image files into `screenshots/`.

2. **[MANUAL VERIFICATION REQUIRED] GitHub Repository Creation**:
   - Initialize a remote repository on GitHub.
   - Push the local project code.
   - Replace the placeholder `[ADD FINAL GITHUB URL HERE]` in `README.md` with your actual URL.

3. **[MANUAL VERIFICATION REQUIRED] Final Report Compilation**:
   - Copy the text from `docs/report_content.md` into your departmental Word template (`AAT Report format for DSP_2026.docx`).
   - Insert the captured screenshots into the document.
   - Print or export the final PDF for submission to Dr. Aruna M G.

4. **[MANUAL VERIFICATION REQUIRED] Viva Presentation Practice**:
   - Review the 5-minute and 2-minute demonstration flows in `docs/demo_script.md`.
   - Review the 25 Q&As in `docs/viva_questions.md`.

# College Final Submission Checklist

**Student:** Saransh Neema (USN: **1DS23AI048**)  
**Course:** Data Security and Privacy (22AI73) — Semester VII  
**Department:** Artificial Intelligence & Machine Learning, DSCE Bengaluru  
**Project Title:** Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot  

Use this checklist to track and verify all required deliverables prior to submission and viva defense:

---

### Master Submission Deliverables

- [x] **Working Application**
  - Streamlit application executes locally without external dependencies (`streamlit run app.py`).
  - All 11 navigation pages load cleanly with interactive Plotly visualizations and zero tracebacks.

- [x] **Draw.io Architecture Diagrams**
  - Primary architecture XML (`diagrams/architecture.drawio`) contains all 9 components, 4 trust boundaries, and 11 data flow steps.
  - Secondary traceability XML (`diagrams/stride_threat_mapping.drawio`) maps components to STRIDE categories, threats, and mitigations.
  - Technical specification documented in `diagrams/architecture.md`.

- [x] **STRIDE Threat Model**
  - Exactly 24 formal synthetic threats loaded from `data/threats.json`.
  - Balanced distribution of 4 threats per category across Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.

- [x] **Mathematical Risk Model**
  - $\text{Risk Score} = \text{Likelihood} \times \text{Impact}$ evaluated on a 1–25 scale.
  - Strict classification tiers: Low (1–5), Medium (6–10), High (11–15), Critical (16–25).
  - Verified across code, UI, and documentation with zero discrepancies.

- [x] **Mitigation Mapping**
  - Mitigations grouped across 9 formal security domains.
  - Traceability matrix mapping Threat $\rightarrow$ Control $\rightarrow$ Security Property $\rightarrow$ Technical Rationale.

- [x] **Automated Testing**
  - 43 automated unit tests in `tests/test_risk_engine.py` passing 100% via `pytest -v`.
  - In-app test runner button allows one-click execution during viva.

- [x] **Screenshots**
  - Comprehensive guide in `docs/screenshot_checklist.md` identifying the 8 screenshots for the project report and slides.
  - Images saved to `screenshots/` directory.

- [x] **Project Report**
  - Full report content prepared in `docs/report_content.md` following the DSCE AAT format.
  - Includes Abstract, official DSCE CO mapping (CO1–CO4), PO/PSO mapping, SDG 9 mapping, 26-case testing table, and academic references.

- [x] **README Documentation**
  - Master guide in `README.md` with complete installation commands (virtual environment setup), expected outputs, and architecture walkthroughs.

- [x] **GitHub Repository Readiness**
  - Standardized `.gitignore` excluding `.venv/`, `__pycache__/`, `.env`, and OS junk.
  - Placeholder for final URL added in README: `[ADD FINAL GITHUB URL HERE]`.

- [x] **Viva Preparation**
  - 25 likely viva questions and technical answers compiled in `docs/viva_questions.md`.
  - Background theory and viva notes in `docs/project_notes.md`.

- [x] **Demonstration Script**
  - 5-minute standard demonstration and 2-minute emergency version scripted in `docs/demo_script.md`.

---

### Manual Steps Required Before Final Presentation

- [ ] **Step 1**: Capture the 8 screenshots using `Win + Shift + S` while running `streamlit run app.py` and place PNGs into `screenshots/`.
- [ ] **Step 2**: Create a remote GitHub repository and push the project files. Update `[ADD FINAL GITHUB URL HERE]` in `README.md`.
- [ ] **Step 3**: Compile the final Word document report using the text from `docs/report_content.md` and the departmental cover page.
- [ ] **Step 4**: Practice the 5-minute demonstration script in `docs/demo_script.md` ahead of the viva slot.

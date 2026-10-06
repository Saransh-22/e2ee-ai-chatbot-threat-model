# Project Report & Viva Screenshot Checklist

This checklist specifies the exact visual evidence to capture from the **E2EE AI Chatbot Threat Modeling & Risk Analyzer** Streamlit application (`http://localhost:8501`) for inclusion in the final micro-project report, presentation slides, and lab record.

---

### Screenshot 1: 📊 Executive Security Dashboard (`dashboard_overview.png`)
* **Page in Application**: `📊 Dashboard`
* **What Must Be Visible**:
  - The top KPI metric cards showing: **Total Threats (24)**, **Critical (4)**, **High (6)**, **Medium (11)**, **Low (3)**, **STRIDE Classes (6)**, and **Components (9)**.
  - The blue informational **Security Posture Summary Callout** explaining that Critical risks ($\text{Score} \ge 16$) demand immediate architectural mitigation.
  - The **Threats by STRIDE Category** bar chart showing a balanced distribution of 4 threats per category.
  - The **Threats by Risk Level** donut chart with color-coded Low (Green), Medium (Yellow), High (Orange), and Critical (Red) slices.
  - The **Threats by Architecture Component** horizontal bar chart showing threat distribution across modules.

---

### Screenshot 2: 🏛️ System Architecture Blueprint (`system_architecture.png`)
* **Page in Application**: `🏛️ System Architecture`
* **What Must Be Visible**:
  - The core pipeline flow sequence: `User` ➔ `Chat Client` ➔ `Authentication` ➔ `Encryption / Key Management` ➔ `Secure Gateway` ➔ `Message Relay` ➔ `AI Processing Service` ➔ `Response Encryption` ➔ `User`.
  - The interactive **Mermaid.js architecture diagram** showing all 4 Trust Boundaries:
    - `TB-01: User Client Zone`
    - `TB-02: Perimeter & Relay DMZ`
    - `TB-03: Secure AI Enclave`
    - `TB-04: Management Zone`
  - The **Potential Attack Surface** summary table mapping each component to its trust boundary and specific attack surfaces.
  - The **Download architecture.drawio** button.

---

### Screenshot 3: 🛡️ STRIDE Threat Catalog Table (`stride_threat_table.png`)
* **Page in Application**: `🛡️ STRIDE Threat Model`
* **What Must Be Visible**:
  - The multi-parameter filter controls: Text Search, STRIDE Category dropdown, Component dropdown, Security Property dropdown, and Risk Level dropdown.
  - The interactive threat catalog table displaying all required columns:
    - `ID`
    - `Component`
    - `STRIDE`
    - `Threat`
    - `Description`
    - `Likelihood`
    - `Impact`
    - `Risk Score`
    - `Risk Level`
    - `Mitigation`
  - Showing active rows for multiple STRIDE categories.

---

### Screenshot 4: 🔍 Deep-Dive Threat Inspector (`threat_details_inspector.png`)
* **Page in Application**: `🛡️ STRIDE Threat Model` (Lower Section)
* **What Must Be Visible**:
  - The Threat Inspector expander with an active threat selected (e.g., `THR-007 - Indirect Prompt Injection & Context Manipulation` or `THR-014 - Cross-Session Attention KV Cache Leakage`).
  - Left panel displaying: **Target Component**, **Affected Asset**, **Data Flow**, **Trust Boundary**, **Threat Description**, **Realistic Attack Scenario**, **Security Impact**, and **Recommended Mitigation**.
  - Right panel displaying: **STRIDE Category**, **Security Property**, **Likelihood (4/5)**, **Impact (4/5)**, **Risk Score (16)**, and **Risk Level (Critical badge)**.

---

### Screenshot 5: 📈 5×5 Risk Matrix Heatmap (`risk_matrix_heatmap.png`)
* **Page in Application**: `📈 Risk Analysis`
* **What Must Be Visible**:
  - The mathematical formula callout: $\text{Risk Score} = \text{Likelihood} \times \text{Impact}$ and classification thresholds (1–5 Low, 6–10 Med, 11–15 High, 16–25 Critical).
  - The full **$5 \times 5$ Plotly Heatmap** with:
    - **Y-Axis**: Impact (1 Negligible to 5 Catastrophic).
    - **X-Axis**: Likelihood (1 Rare to 5 Frequent).
    - Each cell displaying the numeric score, threat count, and bracketed threat IDs (e.g., `[T7, T14, T17, T18]`).
  - The **Top Risks Table** below the heatmap showing threats ranked by highest calculated score.

---

### Screenshot 6: 🔐 Mitigation Controls & Traceability Matrix (`mitigation_controls.png`)
* **Page in Application**: `🔐 Mitigation Controls`
* **What Must Be Visible**:
  - The **Grouped Mitigation Domains** tab displaying one of the 9 categories (e.g., *Authentication*, *Confidentiality*, or *Integrity*) with objective and standard mechanisms.
  - An expanded threat mitigation card showing: **Threat Name**, **Component**, **Security Control**, **Reason for Control**, and **Expected Security Property**.
  - Alternatively, the **Formal Mitigation Traceability Matrix** tab showing the table columns: `ID`, `Threat Name`, `STRIDE Category`, `Security Control`, `Security Property`, and `Technical Rationale`.

---

### Screenshot 7: 🧪 Automated Testing & Verification Page (`testing_verification.png`)
* **Page in Application**: `🧪 Testing & Verification`
* **What Must Be Visible**:
  - The primary **▶️ Execute Pytest Test Suite** button.
  - The green success notification: **"🎉 All 43 Unit Tests Passed Successfully! (100% test pass rate)"**.
  - The terminal execution code block showing `pytest` running across test cases (`TestRiskEngine`, `TestThreatEngine`, `TestMitigationEngine`, `TestAssetAndDataFlowEngines`).
  - The checklist of verified areas (Risk formulas, boundaries, empty datasets, STRIDE balance).

---

### Screenshot 8: 📋 Final Automated Summary & Academic Traceability (`final_summary_traceability.png`)
* **Page in Application**: `🎓 Academic Mapping` or Lower `📊 Dashboard`
* **What Must Be Visible**:
  - The 8-stage academic engineering pipeline cards:
    `Problem Identification ➔ Objectives ➔ Architecture ➔ STRIDE ➔ Risk Model ➔ Mitigation ➔ Testing ➔ Results`.
  - The summary tables showing **Most Frequently Affected Assets** and **Most Frequently Recommended Security Controls**.

---

### Capture Instructions for Windows
1. Run the Streamlit application: `streamlit run app.py`.
2. Maximize the browser window at $100\%$ display zoom.
3. Use Windows Snipping Tool: `Win + Shift + S`.
4. Capture each region cleanly without browser toolbars.
5. Save captured PNG images into the `screenshots/` directory.

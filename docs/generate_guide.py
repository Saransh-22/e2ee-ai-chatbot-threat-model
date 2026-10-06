import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)

with open(os.path.join(root_dir, 'data', 'threats.json'), 'r', encoding='utf-8') as f:
    threats = json.load(f)

with open(os.path.join(base_dir, 'all_threats_formatted.txt'), 'r', encoding='utf-8') as f:
    threats_txt = f.read()

header = """# COMPLETE STUDENT MANUAL: THREAT MODELLING OF AN E2EE AI CHATBOT

**Student:** Saransh Neema  
**USN:** 1DS23AI048  
**Course:** Data Security and Privacy (22AI73)  
**Semester:** VII  
**Department:** Artificial Intelligence & Machine Learning  
**Institution:** Dayananda Sagar College of Engineering (DSCE), Bengaluru  
**Faculty Guide:** Dr. Aruna M G  

---

## TABLE OF CONTENTS
1. [Section A — What is This Project?](#section-a--what-is-this-project)
2. [Section B — Project Architecture](#section-b--project-architecture)
3. [Section C — Data Flows (F1 to F6)](#section-c--data-flows-f1-to-f6)
4. [Section D — STRIDE From Zero](#section-d--stride-from-zero)
5. [Section E — All 24 Threats Catalog](#section-e--all-24-threats-catalog)
6. [Section F — Mathematical Risk Model](#section-f--mathematical-risk-model)
7. [Section G — 5x5 Risk Heatmap Guide](#section-g--5x5-risk-heatmap-guide)
8. [Section H — Risk Distribution Analysis](#section-h--risk-distribution-analysis)
9. [Section I — Mitigation Controls & Residual Risk](#section-i--mitigation-controls--residual-risk)
10. [Section J — Asset Inventory](#section-j--asset-inventory)
11. [Section K — Security vs. Privacy Analysis (Implemented vs. Conceptual)](#section-k--security-vs-privacy-analysis)
12. [Section L — Source Code Architecture & Execution Flow](#section-l--source-code-architecture)
13. [Section M — Complete Application Walkthrough](#section-m--complete-application-walkthrough)
14. [Section N — Manual Testing Testcases](#section-n--manual-testing-testcases)
15. [Section O — Automated Testing (All 43 Pytest Test Cases)](#section-o--automated-testing)
16. [Section P — How to Run Pytest](#section-p--how-to-run-pytest)
17. [Section Q — Teacher Live Demonstration (5-Minute Script)](#section-q--teacher-live-demonstration)
18. [Section R — 2-Minute Emergency Demo](#section-r--2-minute-emergency-demo)
19. [Section S — Viva Preparation (Questions & Answers)](#section-s--viva-preparation)
20. [Section T — "If Teacher Points at This" Quick Reference](#section-t--if-teacher-points-at-this)
21. [Section U — Troubleshooting Guide](#section-u--troubleshooting-guide)

---

## SECTION A — WHAT IS THIS PROJECT?

### 1. What is E2EE (End-to-End Encryption)?
End-to-End Encryption means that data is encrypted on the sender's device and can only be decrypted on the recipient's device. No intermediary—such as a Wi-Fi router, an Internet Service Provider (ISP), or a cloud relay server—can read the content.

### 2. What is an AI Chatbot?
An AI chatbot is an interactive software application powered by Large Language Models (LLMs) or neural networks that accepts natural language text ("prompts") and generates intelligent contextual responses.

### 3. What is Threat Modelling?
Threat modelling is a structured engineering process for identifying, quantifying, and mitigating potential security threats before attackers can exploit them. Instead of waiting for a security breach to happen, engineers model what can go wrong and design defenses proactively.

### 4. What is STRIDE?
STRIDE is Microsoft's industry-standard threat classification model. It categorizes threats into six specific types:
- **S**poofing (Impersonating someone or something else)
- **T**ampering (Modifying data maliciously)
- **R**epudiation (Denying having done an action)
- **I**nformation Disclosure (Exposing private data)
- **D**enial of Service (Making the system crash or unavailable)
- **E**levation of Privilege (Gaining unauthorized admin rights)

### 5. Why is an E2EE AI Chatbot Worth Threat Modelling?
In normal human-to-human E2EE (like WhatsApp or Signal), only human endpoints have keys. But in an AI chatbot, the recipient is a server-side AI model!
To generate an answer, the AI model must decrypt the prompt into plaintext token vectors in server RAM. This creates the **"Plaintext Paradox of AI Inference"**:
Even if communication is encrypted over the network, data is vulnerable at the server processing boundary!

### 6. What Problem Does This Project Solve?
It systematically analyzes the communication boundaries, key exchanges, inference memories, and audit logs of an E2EE AI chatbot, categorizing 24 threats using STRIDE, computing quantitative risk scores (1 to 25), and providing actionable mitigations.

### 7. What is the Final Output?
An interactive security dashboard with risk heatmaps, traceability matrices, data flow analyzers, automated tests, and Draw.io architectural diagrams.

---

## SECTION B — PROJECT ARCHITECTURE

The synthetic chatbot system is decomposed into **9 Core Architectural Components** across **4 Trust Boundaries (TB-01 to TB-04)**:

1. **User / Chat Client (Edge Device)**
   - *Role:* Mobile or web interface running on the user's phone or computer.
   - *Data Handled:* User input plaintext, local session tokens, ephemeral private keys.
   - *Failure Modes:* Device malware scraping keys from RAM, stolen biometric session tokens.
   - *STRIDE Threats:* Spoofing (THR-001), Tampering, Information Disclosure (THR-015).

2. **Identity & Authentication Service**
   - *Role:* Verifies user credentials, handles MFA, and issues cryptographically signed JWT tokens.
   - *Data Handled:* Passwords, biometric challenges, signed JWT identity claims.
   - *Failure Modes:* Brute force password attacks, token forging.
   - *STRIDE Threats:* Denial of Service (THR-020), Spoofing (THR-004).

3. **Encryption & Key Management Service**
   - *Role:* Facilitates initial cryptographic handshakes, pre-key bundle distribution (Double Ratchet protocol), and public key validation.
   - *Data Handled:* Ephemeral Diffie-Hellman public keys, signed pre-keys.
   - *Failure Modes:* In-transit key tampering, compromised root certificates.
   - *STRIDE Threats:* Tampering (THR-006), Information Disclosure.

4. **Secure Gateway (Ingress Reverse Proxy)**
   - *Role:* Edge termination of transport layer security (TLS), rate-limiting, and packet routing.
   - *Data Handled:* Encrypted HTTPS/WSS packets, client IP addresses.
   - *Failure Modes:* TLS exhaustion attacks, DNS spoofing.
   - *STRIDE Threats:* Denial of Service (THR-017), Spoofing (THR-003).

5. **Message Relay Server**
   - *Role:* Asynchronous message queue that buffers and routes encrypted message blobs between clients and the AI compute cluster.
   - *Data Handled:* Ciphertext envelopes, opaque routing headers.
   - *Failure Modes:* Memory buffer flooding, rogue routing manipulation.
   - *STRIDE Threats:* Denial of Service (THR-019), Tampering (THR-005), Information Disclosure (THR-013).

6. **AI Processing Service (Compute Cluster / LLM Enclave)**
   - *Role:* Secure compute boundary where ciphertext is decrypted, tokens are vectorized, neural network inferences are run, and responses are re-encrypted.
   - *Data Handled:* Decrypted plaintext prompt, internal LLM KV attention cache, generated response tokens.
   - *Failure Modes:* Cross-tenant memory bleed, prompt injection, rogue inference worker registration.
   - *STRIDE Threats:* Spoofing (THR-002), Tampering (THR-007), Information Disclosure (THR-014), Denial of Service (THR-018), Elevation of Privilege (THR-023).

7. **API Layer**
   - *Role:* Internal microservices router enforcing RBAC/ABAC authorization checks between internal services.
   - *Data Handled:* Microservice RPC calls, internal bearer tokens.
   - *Failure Modes:* Insecure Direct Object References (IDOR), JWT algorithm confusion.
   - *STRIDE Threats:* Elevation of Privilege (THR-021, THR-022).

8. **Logging & Audit Service**
   - *Role:* Centralized immutable logging of security events, administrative logins, and routing events.
   - *Data Handled:* Timestamped audit records, system diagnostic traces.
   - *Failure Modes:* Malicious audit log erasure, leaking conversational data in error stack traces.
   - *STRIDE Threats:* Repudiation (THR-010, THR-012), Information Disclosure (THR-016).

9. **Administration Interface**
   - *Role:* Operations console for service health monitoring, configuration management, and key rotation.
   - *Data Handled:* Admin credentials, security configurations, policy files.
   - *Failure Modes:* Unsigned policy overrides, unauthorized admin privilege escalation.
   - *STRIDE Threats:* Repudiation (THR-011), Tampering (THR-008), Elevation of Privilege (THR-024).

### Trust Boundaries:
- **TB-01 (Untrusted Client Environment):** Separates the user edge device from the public network.
- **TB-02 (Perimeter Demilitarized Zone - DMZ):** Separates the public internet from internal ingress gateways.
- **TB-03 (Internal Private Subnet):** Separates the message queue from the isolated confidential AI compute cluster.
- **TB-04 (Privileged Management Plane):** Separates general service operations from administrative control consoles.

---

## SECTION C — DATA FLOWS (F1 TO F6)

| Flow ID | Source Component | Destination Component | Data Transferred | Purpose | Protection Mechanism | Trust Boundary Crossed |
|:---:|:---|:---|:---|:---|:---|:---:|
| **F1** | User / Chat Client | Identity & Authentication | Auth credentials, MFA challenge | User login & token acquisition | TLS 1.3 + Certificate Pinning | TB-01 |
| **F2** | User / Chat Client | Key Management Service | Ephemeral DH Public Keys | Double Ratchet handshake setup | Mutual TLS (mTLS) + Signed Pre-keys | TB-01 |
| **F3** | User / Chat Client | Secure Gateway | Encrypted Prompt Ciphertext Blob | Ingress routing of encrypted message | E2EE (AES-256-GCM) + Outer TLS 1.3 | TB-01 -> TB-02 |
| **F4** | Secure Gateway | Message Relay Server | Opaque Encrypted Envelope | Asynchronous queueing & dispatch | Ephemeral Queue Partitioning | TB-02 |
| **F5** | Message Relay Server | AI Processing Service | Ciphertext payload | Decrypt, run LLM inference, re-encrypt | Hardware Enclave (AMD SEV-SNP) + SPIFFE | TB-02 -> TB-03 |
| **F6** | AI Processing Service | Logging & Audit Service | Anonymized audit event telemetry | Audit trail & performance telemetry | Asynchronous TLS + Merkle Root Hashing | TB-03 -> TB-04 |

---

## SECTION D — STRIDE FROM ZERO

### 1. Spoofing (Violates Authenticity)
- *Simple Definition:* Pretending to be someone or something else.
- *Real Life Example:* Someone putting on a fake postal worker uniform to enter your building.
- *In This Project:* An attacker steals a session token to pose as a valid chat user (`THR-001`), or a rogue container joins the cluster pretending to be an AI inference worker (`THR-002`).
- *Mitigation:* Mutual TLS (mTLS), Hardware Keystores (Secure Enclave), and SPIFFE/SPIRE workload attestation.

### 2. Tampering (Violates Integrity)
- *Simple Definition:* Modifying data or instructions without authorization.
- *Real Life Example:* Changing the amount written on a paper check before cashing it.
- *In This Project:* An attacker injects hidden malicious instructions into prompt text to hijack the LLM (`THR-007`), or tampers with public keys in transit (`THR-006`).
- *Mitigation:* Authenticated Encryption with Associated Data (AEAD AES-256-GCM) and prompt injection guardrails.

### 3. Repudiation (Violates Accountability / Non-Repudiation)
- *Simple Definition:* Performing an action and later claiming you never did it because there is no proof.
- *Real Life Example:* Breaking a window when nobody is watching and denying you did it.
- *In This Project:* A rogue administrator deletes audit log files to erase evidence of illegal access (`THR-010`), or a user denies sending a prompt (`THR-009`).
- *Mitigation:* Cryptographically signed action receipts and Write-Once-Read-Many (WORM) Merkle tree audit logs.

### 4. Information Disclosure (Violates Confidentiality)
- *Simple Definition:* Exposing private or confidential data to unauthorized individuals.
- *Real Life Example:* Whispering a secret in a crowded room where eavesdroppers can overhear.
- *In This Project:* Plaintext prompts leaking from LLM attention KV cache memory across different user sessions (`THR-014`), or client malware scraping session keys from RAM (`THR-015`).
- *Mitigation:* Double Ratchet End-to-End Encryption, memory zeroization (`mlock`), and hardware confidential computing enclaves.

### 5. Denial of Service (Violates Availability)
- *Simple Definition:* Overwhelming a service so that legitimate users cannot access it.
- *Real Life Example:* A crowd blocking the entrance of a shop so paying customers cannot enter.
- *In This Project:* Sending millions of complex, recursive prompts to exhaust AI GPU inference compute (`THR-018`), or flooding the gateway with fake TLS handshakes (`THR-017`).
- *Mitigation:* Stateless SYN cookies, edge rate limiting (eBPF XDP), and strict token generation execution quotas.

### 6. Elevation of Privilege (Violates Authorization)
- *Simple Definition:* A standard user gaining administrative or superuser privileges.
- *Real Life Example:* A hotel guest using a master key that opens every bedroom in the building.
- *In This Project:* Modifying a JWT token algorithm header from RS256 to 'none' to gain admin rights (`THR-022`), or breaking out of a worker container into the host OS (`THR-023`).
- *Mitigation:* JWT algorithm pinning, Attribute-Based Access Control (ABAC), and microVM sandboxing (gVisor).

---

## SECTION E — ALL 24 THREATS CATALOG
"""

footer = """
---

## SECTION F — MATHEMATICAL RISK MODEL

### The Risk Formula:
$$\\text{Risk Score} = \\text{Likelihood} \\times \\text{Impact}$$

Where:
- **Likelihood ($L$):** An integer scale from $1$ (Rare) to $5$ (Almost Certain).
- **Impact ($I$):** An integer scale from $1$ (Insignificant) to $5$ (Catastrophic).

### Risk Score Bounds:
- **Minimum Possible Risk Score:** $1 \\times 1 = 1$
- **Maximum Possible Risk Score:** $5 \\times 5 = 25$

### Risk Tier Thresholds Used by Code (`core/risk_engine.py`):
1. **Low Risk:** Score $1$ to $5$ (Green)
   - *Example:* $L=1, I=1 \\rightarrow 1$; $L=2, I=2 \\rightarrow 4$; $L=1, I=5 \\rightarrow 5$.
   - *Action:* Accept risk or mitigate during routine maintenance.
2. **Medium Risk:** Score $6$ to $10$ (Yellow)
   - *Example:* $L=2, I=3 \\rightarrow 6$; $L=2, I=4 \\rightarrow 8$; $L=2, I=5 \\rightarrow 10$.
   - *Action:* Schedule mitigations for next sprint cycle.
3. **High Risk:** Score $11$ to $15$ (Orange)
   - *Example:* $L=3, I=4 \\rightarrow 12$; $L=3, I=5 \\rightarrow 15$.
   - *Action:* High priority remediation required before production release.
4. **Critical Risk:** Score $16$ to $25$ (Red)
   - *Example:* $L=4, I=4 \\rightarrow 16$; $L=4, I=5 \\rightarrow 20$; $L=5, I=5 \\rightarrow 25$.
   - *Action:* Immediate blocking vulnerability; system deployment must halt until mitigated.

---

## SECTION G — 5x5 RISK HEATMAP GUIDE

The $5 \\times 5$ Risk Heatmap organizes all 25 possible risk intersections:
- **X-Axis (Horizontal):** Impact ($1$ to $5$)
- **Y-Axis (Vertical):** Likelihood ($1$ to $5$)

### Viva Cheat-Sheet for Heatmap:
- If your teacher points at **Likelihood = 4 and Impact = 4**:
  $$\\text{Risk Score} = 4 \\times 4 = 16 \\implies \\textbf{Critical Risk}$$
  Threats here include **THR-007** (Prompt Injection), **THR-014** (KV Cache Leakage), **THR-017** (TLS Exhaustion), and **THR-018** (Recursive Prompt DoS).
- If your teacher points at **Likelihood = 2 and Impact = 5**:
  $$\\text{Risk Score} = 2 \\times 5 = 10 \\implies \\textbf{Medium Risk}$$
  Threats here include **THR-002** (Rogue Node Registration) and **THR-006** (Key Tampering). Because Likelihood is low ($2$), the overall risk stays Medium despite high Impact.
- If your teacher points at **Likelihood = 3 and Impact = 4**:
  $$\\text{Risk Score} = 3 \\times 4 = 12 \\implies \\textbf{High Risk}$$
  Threats here include **THR-001** (User Impersonation) and **THR-013** (Plaintext Exposure in Queue).

---

## SECTION H — RISK DISTRIBUTION ANALYSIS

### Actual Threat Distribution in Prototype:
- **Total Threats:** 24
- **Critical Threats (>= 16):** 4 (16.7%)
- **High Threats (11 - 15):** 6 (25.0%)
- **Medium Threats (6 - 10):** 11 (45.8%)
- **Low Threats (1 - 5):** 3 (12.5%)
- **Average Initial Risk Score:** **10.38 / 25**

### Explanation for Teachers:
"The distribution is realistic because most software vulnerabilities fall into Medium and High categories. Only the most severe issues—such as memory attention leaks and prompt injection—rank as Critical. Exactly 4 threats represent each of the six STRIDE categories to maintain rigorous academic balance."

---

## SECTION I — MITIGATION CONTROLS & RESIDUAL RISK

### 9 Mitigation Domains:
1. **Authentication:** Hardware-backed Keystores, mTLS, SPIFFE node identity.
2. **Authorization:** ABAC, RBAC, MicroVM sandboxing (gVisor).
3. **Confidentiality:** E2EE Double Ratchet, Hardware Enclaves (AMD SEV-SNP), Memory Zeroization.
4. **Integrity:** AEAD AES-256-GCM, Prompt Guardrail sanitizers.
5. **Availability:** Stateless SYN cookies, eBPF XDP rate limiting, Inference quotas.
6. **Accountability:** Cryptographic signed receipts, WORM Merkle logs.
7. **Key Management:** Automated key rotation, Ephemeral Diffie-Hellman handshakes.
8. **Logging:** Sanitized error logs, audit trail isolation.
9. **Data Minimization:** Zero retention of conversational data post-inference.

### Residual Risk Math (`core/mitigation_engine.py`):
When a control is marked **Mitigated**:
- Likelihood decreases by $2$ (minimum $1$).
- Impact decreases by $1$ (minimum $1$).
- **Overall Result:** Initial average risk drops from **10.38** to **5.92**, proving a **43.0% quantitative risk reduction**.

---

## SECTION J — ASSET INVENTORY

The chatbot protects **9 Core Assets** evaluated against CIA properties (Confidentiality, Integrity, Availability):

1. **User Identity:** (High C, High I, Med A) - Identity tokens and session credentials.
2. **User Prompts:** (Critical C, High I, Med A) - Plaintext conversational prompts.
3. **AI Responses:** (Critical C, High I, Med A) - Plaintext generated answers.
4. **Encryption Keys:** (Critical C, Critical I, High A) - Ephemeral session keys and identity private keys.
5. **Session Information:** (High C, High I, High A) - Ephemeral session mapping tables.
6. **System Logs:** (Med C, Critical I, High A) - Historical audit and security trace records.
7. **AI Model Weights:** (Critical C, Critical I, High A) - Neural network model parameters.
8. **Inference Compute Capacity:** (Low C, Med I, Critical A) - GPU hardware resources.
9. **Admin Configurations:** (High C, Critical I, High A) - Access control policies and routing rules.

---

## SECTION K — SECURITY VS. PRIVACY ANALYSIS

### Crucial Viva Distinction: What is Implemented vs. What is Conceptual

| Mechanism | Description | Implemented in Python Code? | Viva Explanation |
|:---|:---|:---:|:---|
| **STRIDE Threat Engine** | Data ingestion, filtering, and cataloguing | **YES (Implemented)** | "Fully implemented in `core/threat_engine.py`." |
| **Mathematical Risk Engine** | $R = L \\times I$, bounds checking, tier logic | **YES (Implemented)** | "Fully implemented in `core/risk_engine.py` with 100% test coverage." |
| **Mitigation & Residual Risk** | Traceability mapping & posture computation | **YES (Implemented)** | "Fully implemented in `core/mitigation_engine.py`." |
| **Asset & Data Flow Models** | Structured inventory of assets and flows | **YES (Implemented)** | "Fully implemented in `core/asset_inventory.py` & `data_flow_engine.py`." |
| **Streamlit Interactive UI** | Web visualization, charts, and simulator | **YES (Implemented)** | "Fully implemented in `app.py` using Plotly and Streamlit." |
| **Double Ratchet / Signal E2EE** | Cryptographic key agreement and ratcheting | **NO (Conceptual)** | "Modeled as an architectural mitigation requirement; not a live production crypto service." |
| **Hardware Enclaves (AMD SEV-SNP)** | CPU-enforced memory encryption | **NO (Conceptual)** | "Architectural defense proposed for server-side inference isolation." |
| **RAM Zeroization (`mlock`)** | Operating system RAM flushing after turn | **NO (Conceptual)** | "Proposed endpoint hardening control against memory scraping." |
| **WORM Merkle Audit Logging** | Tamper-proof append-only cryptographic log | **NO (Conceptual)** | "Proposed non-repudiation control." |
| **Packet Traffic Padding** | Masking message lengths to 4KB blocks | **NO (Conceptual)** | "Proposed network defense against side-channel traffic analysis." |

---

## SECTION L — SOURCE CODE ARCHITECTURE

### File Breakdown:
1. `app.py`:
   - *Role:* Streamlit entry point.
   - *Key Functions:* Configures layout, renders navigation radio menu, builds Plotly charts for dashboard, displays interactive risk simulator slider, and outputs Draw.io XML download buttons.
2. `core/risk_engine.py`:
   - *Role:* Pure mathematical calculation engine.
   - *Key Functions:* `calculate_risk(l, i)`, `classify_risk_level(score)`, `enrich_threats_with_risk(threats)`, `get_risk_summary(threats)`.
3. `core/threat_engine.py`:
   - *Role:* Threat data loader and filter.
   - *Key Functions:* `load_threats()`, `filter_by_stride()`, `filter_by_component()`, `search_threats()`, `get_threat_model_summary()`.
4. `core/mitigation_engine.py`:
   - *Role:* Security controls and traceability mapping.
   - *Key Functions:* `calculate_mitigation_posture()`, `compute_residual_risk()`, `get_mitigation_matrix()`.
5. `core/asset_inventory.py`:
   - *Role:* CIA-classified inventory of system assets.
   - *Key Functions:* `get_all_assets()`, `get_asset_by_name()`.
6. `core/data_flow_engine.py`:
   - *Role:* Network flow and trust boundary tracking.
   - *Key Functions:* `get_all_flows()`, `get_flow_by_id()`.
7. `core/security_privacy_engine.py`:
   - *Role:* Analytical engine contrasting privacy vs. security boundaries.
   - *Key Functions:* `get_all_topics()`, `get_topics_by_category()`.

---

## SECTION M — COMPLETE APPLICATION WALKTHROUGH

### Execution Commands (PowerShell):
```powershell
# 1. Navigate to directory
cd e2ee-ai-chatbot-threat-model

# 2. Activate virtual environment
.\\.venv\\Scripts\\Activate.ps1

# 3. Verify packages
python -m pip install -r requirements.txt

# 4. Run automated tests
pytest -v

# 5. Launch Streamlit app
streamlit run app.py
```

### Navigating the UI Pages:
1. **📊 Dashboard:** View top KPIs (24 threats, 4 critical), STRIDE bar chart, and component breakdown.
2. **🏛️ System Architecture:** Inspect the 9-component interactive architecture graph and download the Draw.io file.
3. **🔀 Data Flow Analysis:** Review flows $F_1$ to $F_6$ and trust boundary transitions.
4. **🗄️ Security Asset Inventory:** Inspect the 9 protected assets and CIA requirements.
5. **🛡️ STRIDE Threat Model:** Filter by category (e.g., Spoofing), component, or search keywords.
6. **📈 Risk Analysis:** Adjust Likelihood and Impact sliders in the Risk Simulator; view the $5 \\times 5$ heatmap.
7. **🔐 Mitigation Controls:** Examine the Traceability Matrix and residual risk reduction.
8. **⚖️ Security vs. Privacy:** Review E2EE strengths and the Plaintext Inference Paradox.
9. **🎓 Academic Mapping:** View DSCE Course Outcomes (CO1-CO4) and SDG 9 alignment.
10. **🧪 Testing & Verification:** Run unit tests directly inside the web browser!
11. **ℹ️ About Project:** Review project metadata, USN `1DS23AI048`, and student details.

---

## SECTION N — MANUAL TESTING TESTCASES

| Test ID | UI Component / Action | Input | Expected Output | Verification Purpose |
|:---:|:---|:---|:---|:---|
| **MT-01** | Dashboard KPI Cards | Page Load | Total: 24, Critical: 4, High: 6, Med: 11, Low: 3 | Confirms dataset loaded accurately |
| **MT-02** | STRIDE Filter | Select "Tampering" | Displays exactly 4 threats (THR-005 to THR-008) | Proves category filter logic works |
| **MT-03** | Threat Search Bar | Type "Prompt Injection" | Returns THR-007 exclusively | Validates substring keyword search |
| **MT-04** | Risk Simulator Slider | Set $L=4, I=5$ | Risk Score: 20, Level: "Critical" | Proves dynamic $R = L \\times I$ calculation in UI |
| **MT-05** | Risk Simulator Boundary | Set $L=1, I=1$ | Risk Score: 1, Level: "Low" | Proves minimum boundary score in UI |
| **MT-06** | Heatmap Rendering | View Matrix | $5 \\times 5$ grid rendered with color-coded cells | Confirms Plotly heatmap generation |
| **MT-07** | Traceability Matrix | View Table | Columns: Threat ID, STRIDE, Control, Mitigation | Verifies security traceability |
| **MT-08** | Draw.io Download | Click Download button | XML file downloads (`architecture.drawio`) | Validates binary/file download streaming |
| **MT-09** | Testing Page Run Button| Click "Run Tests" | Output displays "43 passed" | Verifies in-app subprocess test runner |

---

## SECTION O — AUTOMATED TESTING (ALL 43 PYTEST TEST CASES)

The test suite in `tests/test_risk_engine.py` contains **43 automated test cases** across **4 Test Classes**:

### Class 1: `TestRiskEngine` (27 Tests)
1. `test_risk_formula_basic`: Verifies $3 \\times 4 = 12$ (High).
2. `test_boundary_values_min_max`: Verifies $1 \\times 1 = 1$ (Low) and $5 \\times 5 = 25$ (Critical).
3. `test_risk_classification_tiers[1-Low]`: Verifies score 1 is Low.
4. `test_risk_classification_tiers[2-Low]`: Verifies score 2 is Low.
5. `test_risk_classification_tiers[5-Low]`: Verifies score 5 is Low (upper boundary of Low).
6. `test_risk_classification_tiers[6-Medium]`: Verifies score 6 is Medium (lower boundary of Medium).
7. `test_risk_classification_tiers[7-Medium]`: Verifies score 7 is Medium.
8. `test_risk_classification_tiers[10-Medium]`: Verifies score 10 is Medium (upper boundary of Medium).
9. `test_risk_classification_tiers[11-High]`: Verifies score 11 is High (lower boundary of High).
10. `test_risk_classification_tiers[12-High]`: Verifies score 12 is High.
11. `test_risk_classification_tiers[15-High]`: Verifies score 15 is High (upper boundary of High).
12. `test_risk_classification_tiers[16-Critical]`: Verifies score 16 is Critical (lower boundary of Critical).
13. `test_risk_classification_tiers[20-Critical]`: Verifies score 20 is Critical.
14. `test_risk_classification_tiers[25-Critical]`: Verifies score 25 is Critical (maximum possible score).
15. `test_invalid_likelihood_handling[0]`: Ensures $L=0$ raises `ValueError`.
16. `test_invalid_likelihood_handling[-1]`: Ensures $L=-1$ raises `ValueError`.
17. `test_invalid_likelihood_handling[6]`: Ensures $L=6$ raises `ValueError`.
18. `test_invalid_likelihood_handling[10]`: Ensures $L=10$ raises `ValueError`.
19. `test_invalid_likelihood_handling[-99]`: Ensures negative input raises `ValueError`.
20. `test_invalid_impact_handling[0]`: Ensures $I=0$ raises `ValueError`.
21. `test_invalid_impact_handling[-1]`: Ensures $I=-1$ raises `ValueError`.
22. `test_invalid_impact_handling[6]`: Ensures $I=6$ raises `ValueError`.
23. `test_invalid_impact_handling[10]`: Ensures $I=10$ raises `ValueError`.
24. `test_invalid_impact_handling[-99]`: Ensures negative impact raises `ValueError`.
25. `test_invalid_non_numeric_types`: Ensures passing strings or `None` raises `TypeError` or `ValueError`.
26. `test_classify_out_of_range`: Ensures score $>25$ or $<1$ raises `ValueError`.
27. `test_empty_threat_dataset_handling`: Ensures risk summary handles empty list without crashing.

### Class 2: `TestThreatEngine` (9 Tests)
28. `test_threat_loading_and_attributes`: Confirms dataset contains exactly 24 threats with all fields.
29. `test_stride_category_distribution_balance`: Confirms each STRIDE category has exactly 4 threats.
30. `test_security_properties_present`: Confirms all 6 security properties are mapped.
31. `test_stride_category_filtering`: Validates filtering by specific STRIDE category.
32. `test_component_filtering`: Validates filtering by specific architectural component.
33. `test_risk_level_filtering`: Validates filtering by risk tier (Low, Medium, High, Critical).
34. `test_search_by_threat_name_and_query`: Tests free-text search matching.
35. `test_threat_model_summary`: Confirms statistics calculation matches dataset totals.
36. `test_empty_file_handling`: Ensures graceful handling if JSON file is missing.

### Class 3: `TestMitigationEngine` (4 Tests)
37. `test_mitigation_categories_completeness`: Confirms all 9 mitigation categories exist.
38. `test_threat_grouping_by_mitigation_category`: Confirms threats group accurately into controls.
39. `test_mitigation_matrix_generation`: Verifies columns in Traceability Matrix.
40. `test_residual_risk_calculation`: Verifies residual risk drop logic after mitigation.

### Class 4: `TestAssetAndDataFlowEngines` (3 Tests)
41. `test_asset_inventory_has_all_assets`: Confirms all 9 assets exist with CIA ratings.
42. `test_data_flows_f1_to_f6`: Confirms data flows $F_1$ through $F_6$ exist and cross trust boundaries.
43. `test_security_vs_privacy_engine`: Confirms all 9 security/privacy comparative topics are loaded.

---

## SECTION P — HOW TO RUN PYTEST

### Command:
```powershell
pytest -v
```
- `pytest`: The Python testing framework.
- `-v` (verbose): Prints every single test function name and its individual status.

### What Output Means:
- `PASSED`: The code executed, the assertions were true, and the security logic is verified.
- `FAILED`: An assertion was false (e.g., risk math produced an incorrect result).
- **Current Result:** `43 passed in 0.14s` (100% success rate, 0 errors, 0 failures).

---

## SECTION Q — TEACHER LIVE DEMONSTRATION (5-MINUTE SCRIPT)

### Minute 1: Introduction & Objective
- **What You Click:** Sidebar -> **📊 Dashboard**
- **What You Say:** "Good morning, Ma'am/Sir. My name is Saransh Neema, USN 1DS23AI048. My micro-project for Data Security and Privacy (22AI73) is 'Threat Modelling of an End-to-End Encrypted AI Chatbot'. Our objective is to identify security vulnerabilities across the communication pipeline and confidential compute boundaries of an AI chatbot using the STRIDE methodology."
- **What Teacher Sees:** Metric cards showing 24 Total Threats, 4 Critical, and the STRIDE distribution chart.

### Minute 2: System Architecture & Trust Boundaries
- **What You Click:** Sidebar -> **🏛️ System Architecture**
- **What You Say:** "Here is our 9-component architecture. Notice that the chat client communicates over E2EE with the messaging relay, but the message must be decrypted at the AI Processing Service so that the neural network can run inference. This introduces 4 Trust Boundaries, separating untrusted clients, edge gateways, internal message queues, and privileged compute enclaves."
- **What Teacher Sees:** The interactive architecture flow and trust boundary indicators.

### Minute 3: STRIDE Catalog & Critical Threat Deep-Dive
- **What You Click:** Sidebar -> **🛡️ STRIDE Threat Model** -> Filter by **Critical**
- **What You Say:** "We systematically analyzed 24 threats—exactly 4 for each STRIDE category. For example, under Tampering, we have `THR-007: Indirect Prompt Injection`. Even with E2EE, an adversary can embed jailbreak delimiters inside the encrypted payload to hijack model reasoning once decrypted in the enclave. Likelihood is 4 and Impact is 4, yielding a Critical risk score of 16."
- **What Teacher Sees:** Filtered table showing THR-007, THR-014, THR-017, and THR-018 in red Critical badges.

### Minute 4: Risk Heatmap & Traceability Matrix
- **What You Click:** Sidebar -> **📈 Risk Analysis** -> Scroll to **5x5 Risk Heatmap**
- **What You Say:** "We compute Risk as Likelihood times Impact, mapped onto this 5x5 heatmap. Cells with score 16 or higher are Critical. Next, looking at **🔐 Mitigation Controls**, we map every threat to a specific control in our Traceability Matrix. Applying these controls reduces our average risk score from 10.38 down to 5.92—a 43% reduction."
- **What Teacher Sees:** Interactive Plotly heatmap and the mitigation traceability table.

### Minute 5: Testing Verification & Conclusion
- **What You Click:** Sidebar -> **🧪 Testing & Verification** -> Click **Run All Automated Tests**
- **What You Say:** "To guarantee correctness, we wrote a test suite in pytest covering all mathematical formulas, boundary values, and STRIDE distributions. As shown here, all 43 tests pass cleanly. In conclusion, while E2EE protects data in transit, AI chatbots require confidential enclaves and prompt guardrails to remain secure. Thank you!"
- **What Teacher Sees:** Console showing `====== 43 passed in 0.14s ======` in green.

---

## SECTION R — 2-MINUTE EMERGENCY DEMO

*Use this when your evaluator says: "Show me quickly in 2 minutes."*

1. **Step 1 (Dashboard - 30 seconds):**
   - Click **📊 Dashboard**.
   - Say: "I modeled an E2EE AI chatbot using STRIDE. We have 24 threats across 9 components, with 4 balanced threats in each STRIDE category."
2. **Step 2 (Risk Simulator - 45 seconds):**
   - Click **📈 Risk Analysis**.
   - Move Likelihood to 4 and Impact to 4.
   - Say: "Risk equals Likelihood times Impact. $4 \\times 4 = 16$, which places it in the Critical tier, as shown on our 5x5 heatmap."
3. **Step 3 (Mitigation & Testing - 45 seconds):**
   - Click **🧪 Testing & Verification** and hit **Run All Automated Tests**.
   - Say: "Every threat maps to a defense in our traceability matrix, reducing average risk by 43%. Our implementation is mathematically verified with 43 automated unit tests, all passing."

---

## SECTION S — VIVA PREPARATION (QUESTIONS & ANSWERS)

### Q1: What is the difference between E2EE in WhatsApp vs. in an AI Chatbot?
- **Best Simple Answer:** In WhatsApp, both endpoints are humans who hold the decryption keys. In an AI chatbot, the receiving endpoint is an AI server that must decrypt the message to process the prompt.
- **Detailed Answer:** Standard E2EE terminates at the human recipient's screen. For an AI chatbot, token embeddings and attention calculations require plaintext access. Therefore, encryption must terminate inside the server's confidential compute enclave, shifting vulnerabilities to server RAM and multi-tenant attention caches.
- **Keywords:** Plaintext Paradox, Endpoint Termination, Confidential Enclave, Attention Cache.

### Q2: Why did you use synthetic data instead of real user data?
- **Best Simple Answer:** Because Data Security and Privacy regulations strictly forbid collecting or testing with real user credentials, and synthetic data ensures safe, reproducible threat modeling.
- **Detailed Answer:** In compliance with ethical research principles and academic lab guidelines, using synthetic architecture and threat data avoids privacy violations under GDPR and DPDP Act while fully allowing systematic security validation.
- **Keywords:** Privacy Regulations, DPDP Act, Reproducibility, Ethical Modeling.

### Q3: What is the highest possible risk score and why?
- **Best Simple Answer:** 25, because Likelihood is at most 5 and Impact is at most 5 ($5 \\times 5 = 25$).
- **Detailed Answer:** The risk model uses standard NIST 5-point discrete ordinal scales for both likelihood and impact. The mathematical product has a closed range $[1, 25]$, where 1 is minimal risk and 25 represents catastrophic, certain exploitation.
- **Keywords:** NIST Scale, Ordinal Scale, Closed Range, Upper Bound.

### Q4: Why is a score of 16 classified as Critical?
- **Best Simple Answer:** Because any event with high likelihood (4) and high impact (4) causes immediate, severe damage ($4 \\times 4 = 16$).
- **Detailed Answer:** In standard four-tier risk classification, the upper quadrant ($L \\ge 4, I \\ge 4$) represents unacceptable organizational risk requiring immediate deployment halt. Hence, scores $16$ to $25$ form the Critical tier.
- **Keywords:** Four-Tier Classification, Upper Quadrant, Immediate Remediation.

### Q5: What did you actually implement versus what is conceptual?
- **Best Simple Answer:** I implemented the full threat model dataset, mathematical risk calculation engine, filtering logic, automated testing suite, and interactive Streamlit UI. The low-level hardware enclaves (AMD SEV-SNP) and Double Ratchet cryptography are conceptual architectural defenses.
- **Detailed Answer:** The prototype is an academic security threat-modeling and risk-analyzer software suite written in Python. It evaluates synthetic systems against STRIDE. The actual cryptographic hardware (Secure Enclave, AMD SEV-SNP) and network protocols are modeled as architectural requirements, not built as live production services.
- **Keywords:** Implemented Software Prototype vs. Architectural Defense Requirements.

---

## SECTION T — "IF TEACHER POINTS AT THIS" QUICK REFERENCE

- **Teacher points at STRIDE:**
  $$\\rightarrow$$ Say: "STRIDE stands for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. It maps directly to foundational security properties: Authenticity, Integrity, Non-Repudiation, Confidentiality, Availability, and Authorization."
- **Teacher points at Risk Score:**
  $$\\rightarrow$$ Say: "Risk Score is computed as Likelihood times Impact ($R = L \\times I$). The score ranges from 1 to 25, categorized into Low (1-5), Medium (6-10), High (11-15), and Critical (16-25)."
- **Teacher points at Heatmap:**
  $$\\rightarrow$$ Say: "This is a 5x5 matrix mapping Likelihood on the Y-axis against Impact on the X-axis. It visually clusters the 24 threats into risk tiers to prioritize which defenses must be implemented first."
- **Teacher asks about Pytest:**
  $$\\rightarrow$$ Say: "We have 43 automated unit tests in `tests/test_risk_engine.py` that validate our risk formulas, boundary conditions, input error handling, and STRIDE distribution. All 43 tests pass cleanly in 0.14 seconds."
- **Teacher asks 'Is this production ready?':**
  $$\\rightarrow$$ Say: "No, Ma'am/Sir. This is an academic threat-modeling prototype designed to systematically identify and analyze security risks before building production systems."

---

## SECTION U — TROUBLESHOOTING GUIDE

| Issue | Likely Cause | Exact Solution |
|:---|:---|:---|
| `python: command not found` | Python not in system PATH | Run `py` or specify full path `C:\\Users\\saran\\AppData\\Local\\Programs\\Python\\Python311\\python.exe`. |
| `Activate.ps1 cannot be loaded` | PowerShell execution policy restriction | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again. |
| `ModuleNotFoundError` | Dependencies not installed in active environment | Run `.\\.venv\\Scripts\\pip install -r requirements.txt`. |
| `Port 8501 already in use` | Previous Streamlit instance still running | Streamlit will auto-switch to 8502, or run `taskkill /F /IM streamlit.exe`. |
| `pytest: command not found` | pytest not invoked via venv | Run `.\\.venv\\Scripts\\python -m pytest -v`. |
| Browser does not open | Headless setting or default browser issue | Manually open your browser and navigate to `http://localhost:8501`. |

---
**End of Complete Project Guide**
"""

full_content = header + "\n" + threats_txt + "\n" + footer
output_path = os.path.join(base_dir, 'COMPLETE_PROJECT_GUIDE.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_content)

print(f"File {output_path} generated successfully! Size: {len(full_content)} bytes")

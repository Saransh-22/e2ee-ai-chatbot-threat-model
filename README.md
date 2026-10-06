# Threat Modelling of an E2EE AI Chatbot

> **Course**: Data Security and Privacy  
> **Course Code**: 22AI73  
> **Semester**: VII (7th Sem B.E., Artificial Intelligence & Data Science)  
> **Student**: Saransh Neema  
> **USN**: 1DS23AI048  
> **College Micro-Project Submission**

---

## 1. Project Title
**Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot**

---

## 2. Student & Course Information
- **Student Name**: Saransh Neema
- **USN**: 1DS23AI048
- **Course Title**: Data Security and Privacy
- **Course Code**: 22AI73
- **Degree / Branch**: Bachelor of Engineering (B.E.) in Artificial Intelligence & Data Science
- **Semester**: VII

---

## 3. Problem Statement
Modern secure messaging protocols (such as Signal and WhatsApp) achieve end-to-end confidentiality by ensuring that encryption keys reside strictly on human user endpoints. Intermediary servers, cloud relays, and network providers handle only opaque ciphertext.

However, when an **Artificial Intelligence model (LLM agent)** acts as an autonomous conversational respondent, the AI processing system becomes an active communication endpoint. This introduces the fundamental **"Plaintext Paradox of AI Inference"**:
- The language model requires unencrypted prompt representations (tokenized embeddings) to compute attention matrix multiplications and synthesize responses.
- Decrypting prompt content in a conventional cloud environment exposes private user communications to host OS compromises, hypervisor access, rogue worker nodes, memory scraping, and multi-tenant attention cache leaks.
- Furthermore, AI models introduce unique vulnerability surfaces that transport-layer encryption cannot address: **Prompt Injections, Jailbreak Suffixes, Model Alignment Subversion, Attention KV Cache Cross-Bleed, and Algorithmic Token DoS Attacks**.

---

## 4. Objectives
1. **Analyze Security & Trust Boundaries**: Delineate Client (`TB-01`), Perimeter/DMZ (`TB-02`), Secure AI Enclave (`TB-03`), and Management (`TB-04`) trust zones.
2. **Apply STRIDE Threat Taxonomy**: Systematically catalog 24 synthetic threats evenly distributed across all six STRIDE categories (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
3. **Formal Mathematical Risk Modeling**: Evaluate Likelihood ($1–5$) and Impact ($1–5$) using a quantitative formula ($\text{Risk} = L \times I$) on a 1–25 scale, classifying threats into Low, Medium, High, and Critical tiers.
4. **Formulate Defense-in-Depth Mitigations**: Establish controls spanning 9 cybersecurity domains (Authentication, Authorization, Confidentiality, Integrity, Availability, Accountability, Key Management, Logging, Data Minimization).
5. **Security vs. Privacy Conceptual Demarcation**: Clarify why E2EE improves transit confidentiality but does not solve endpoint, semantic, or memory vulnerabilities.
6. **Academic Traceability & Verification**: Provide an end-to-end demonstrable prototype in Streamlit supported by 43 automated unit tests in `pytest`.

---

## 5. Concepts Used
- **STRIDE Threat Modeling Methodology** (Microsoft Security Development Lifecycle).
- **End-to-End Encryption (E2EE)**: Ephemeral Elliptic Curve Diffie-Hellman (ECDH), Double Ratchet Protocol, and Authenticated Encryption with Associated Data (AEAD - AES-256-GCM).
- **Hardware-Enforced Confidential Computing**: Trusted Execution Environments (TEE) using AMD SEV-SNP / Intel TDX.
- **Dual-LLM Guardrail Architecture**: Dedicated input sanitization and output Data Loss Prevention (DLP) guardrail models.
- **Quantitative Risk Assessment**: $5 \times 5$ Risk Matrix with strict boundary cutoffs.
- **Tamper-Evident Auditing**: Write-Once-Read-Many (WORM) storage with cryptographically chained Merkle tree hash proofs.

---

## 6. Architecture & Data Flow

The architecture models an 11-step secure data flow pipeline:

```
[User]
   │ (1. Types Prompt)
   ▼
[Chat Client]
   │ (2. Key Agreement)
   ▼
[Identity & Authentication (JWT/OAuth2)]
   │ (3. Token Grant)
   ▼
[Encryption / Key Management]
   │ (4. AEAD Ciphertext Envelope)
   ▼
[Secure Gateway (TLS 1.3 / Ingress WAF)]
   │ (5. Blind Transit)
   ▼
[Message Relay Server (Zero-Knowledge Broker)]
   │ (6. Queue Dispatch)
   ▼
[AI Processing Service (Confidential LLM Enclave + Guardrails)]
   │ (7. In-Enclave Decryption & Inference)
   ▼
[Response Encryption Engine (Ratchet Re-encryption)]
   │ (8. Re-encrypted Ciphertext)
   ▼
[Message Relay Server ➔ Secure Gateway]
   │ (9. Ciphertext Push)
   ▼
[Chat Client ➔ User (Decryption & Render)]
```

### Trust Boundaries (TB)
- **`TB-01` (User Client Trust Boundary)**: Untrusted host operating system; exposed to device theft, side-loaded malware, and RAM dump scraping.
- **`TB-02` (Perimeter & Relay DMZ)**: Semi-trusted public internet transit; exposed to TLS handshake flooding, DNS spoofing, and packet size traffic profiling.
- **`TB-03` (Secure AI Processing Enclave)**: High-trust confidential computing enclave; exposed to prompt injection, KV cache attention cross-bleed, and container breakout.
- **`TB-04` (Management & Governance Zone)**: Privileged control plane; exposed to IDOR on administrative APIs and audit trail erasure.

### Architectural Data Flows ($F_1$ to $F_6$)
- **$F_1$ (User $\rightarrow$ Chat Client)**: Cleartext prompt entry protected by client OS memory controls and biometric auth.
- **$F_2$ (Chat Client $\rightarrow$ Secure Gateway)**: E2EE payload protected by Double Ratchet AES-256-GCM and transport TLS 1.3 certificate pinning.
- **$F_3$ (Gateway $\rightarrow$ Message Relay)**: Outer routing envelope transit protected by internal mTLS and uniform 4KB packet padding.
- **$F_4$ (Message Relay $\rightarrow$ AI Service)**: Ciphertext queue dispatch protected by SPIFFE/mTLS service mesh into AMD SEV-SNP encrypted RAM.
- **$F_5$ (AI Service $\rightarrow$ Response Handler)**: Generated response tokens screened by DLP guardrails with zero-copy memory transfers.
- **$F_6$ (Response Handler $\rightarrow$ User)**: Re-encrypted response ciphertext pushed back through relay to client UI for local rendering.

---

## 7. STRIDE Explanation & Threat Categories

The model categorizes 24 formal threats across all six STRIDE dimensions (4 threats each):

| STRIDE Category | Target Security Property | Threat Manifestations in AI Chatbot |
| :--- | :--- | :--- |
| **Spoofing (S)** | Authentication | User identity impersonation, Rogue AI inference worker node registration, Gateway DNS spoofing, Session/Bearer token replay. |
| **Tampering (T)** | Integrity | Ciphertext envelope routing header manipulation, Ephemeral DH key tampering, Indirect prompt injection, Security policy config modification. |
| **Repudiation (R)** | Accountability | User denial of malicious prompt dispatch, Audit trail erasure by privileged admin, Unsigned policy override, Gateway log drop under heavy load. |
| **Information Disclosure (I)**| Confidentiality | Plaintext exposure in relay queue, Transformer attention KV cache tenant cross-bleed, Client RAM scraping, Sensitive data leakage in error logs. |
| **Denial of Service (D)** | Availability | Asymmetric TLS handshake exhaustion, AI inference token expansion via recursive prompts, Relay queue buffer saturation, Auth endpoint brute-forcing. |
| **Elevation of Privilege (E)**| Authorization | Insecure Direct Object References (IDOR) on Admin API, JWT algorithm confusion (HS256/RS256), AI inference container breakout, Excessive relay worker IAM permissions. |

---

## 8. Mathematical Risk Model

The quantitative risk score is defined as:

$$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$

Where:
- $\text{Likelihood} \in \{1, 2, 3, 4, 5\}$ (1: Rare, 2: Unlikely, 3: Possible, 4: Likely, 5: Frequent)
- $\text{Impact} \in \{1, 2, 3, 4, 5\}$ (1: Negligible, 2: Minor, 3: Moderate, 4: Major, 5: Catastrophic)
- $\text{Risk Score} \in [1, 25]$

### Risk Classification Thresholds
- **1 – 5**: **Low** (Acceptable baseline; standard operational logging)
- **6 – 10**: **Medium** (Moderate risk; baseline defense-in-depth required)
- **11 – 15**: **High** (Substantial risk; prioritized cryptographic/memory controls)
- **16 – 25**: **Critical** (Severe architectural threat; immediate mandatory remediation)

---

## 9. Mitigation Strategy

Mitigations are systematically structured across **9 formal security control domains**:

1. **Authentication**: Hardware Keystore binding, mutual TLS (mTLS), SPIFFE/SPIRE worker node attestation, certificate pinning.
2. **Authorization**: Attribute-Based Access Control (ABAC), gVisor MicroVM sandboxing, strict JWT algorithm whitelisting.
3. **Confidentiality**: AMD SEV-SNP confidential enclaves, per-turn KV attention cache flushing, Zero-Knowledge relay routing.
4. **Integrity**: Authenticated Encryption with Associated Data (AEAD), Dual-LLM prompt guardrails, cryptographically signed policy manifests.
5. **Availability**: Edge stateless SYN-cookies, eBPF XDP rate limiting, token generation quotas, inference timeouts.
6. **Accountability**: Client-side digital signatures, monotonic sequence counters, FIDO2-signed dual-custody administrative manifests.
7. **Key Management**: Double Ratchet session rotation, signed prekeys (X3DH), immediate memory zeroization (`mlock`).
8. **Logging**: WORM object storage, cryptographically chained Merkle tree hash proofs, zero-plaintext logging.
9. **Data Minimization**: Uniform PKCS#7 packet padding to 4KB blocks, chaff (dummy) traffic injection.

---

## 10. Security vs. Privacy Discussion & Academic Disclaimer

> **CRITICAL SECURITY NOTICE**:  
> **This project does NOT claim that End-to-End Encryption (E2EE) makes an AI chatbot completely secure.**  
> While E2EE provides strong cryptographic confidentiality for data in transit, holistic security and privacy fundamentally depend on:
> 1. **Endpoint Security**: Resisting physical theft, OS debugger hooks, and client-side RAM key scraping.
> 2. **Authentication**: Rigorously verifying device fingerprints and user credentials via hardware keystores.
> 3. **Key Management**: Enforcing ephemeral ratcheting, forward secrecy, and immediate memory zeroization (`mlock`).
> 4. **Server Trust & Enclave Isolation**: Restricting in-memory prompt decryption strictly to hardware-isolated confidential computing enclaves (AMD SEV-SNP).
> 5. **Authorization**: Enforcing Attribute-Based Access Control (ABAC) and rootless microVM process isolation.
> 6. **Logging & Accountability**: Operating tamper-evident WORM Merkle audit records without logging decrypted prompt plaintext.
> 7. **Data Minimization**: Standardizing uniform packet padding and purging transient session queues.
> 8. **AI Semantic Processing**: Deploying dual-LLM input/output guardrails to detect adversarial prompt injections and KV attention cache leaks.
>
> *This system is an **academic threat-modeling prototype** designed for security evaluation and viva demonstration. It utilizes synthetic architecture schemas and simulated threat datasets. It is not intended to operate as a live production messaging system.*

---

## 11. Folder Structure

```
e2ee-ai-chatbot-threat-model/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies (Streamlit, Pandas, Plotly, Pytest)
├── README.md                   # Comprehensive academic documentation
├── .gitignore                  # Git ignore specifications
│
├── data/
│   └── threats.json            # 24 synthetic STRIDE threats across 9 components
│
├── core/
│   ├── __init__.py             # Module initialization and exports
│   ├── threat_engine.py        # Threat loader, query, and summary engine
│   ├── risk_engine.py          # Mathematical risk calculation & classification
│   ├── mitigation_engine.py    # 9 security control domains & residual risk logic
│   ├── asset_inventory.py      # 9 protected assets with CIA triad ratings
│   ├── data_flow_engine.py     # 6 architectural data flows (F1 to F6)
│   └── security_privacy_engine.py # Conceptual analysis of E2EE scope & limits
│
├── diagrams/
│   ├── architecture.drawio     # Complete editable Draw.io XML architecture
│   └── architecture.md         # Detailed plain-English architecture guide
│
├── tests/
│   └── test_risk_engine.py     # 43 automated unit tests
│
├── screenshots/
│   └── README.md               # Screenshot capture guide for viva demonstration
│
└── docs/
    └── project_notes.md        # Comprehensive viva Q&A and theoretical analysis
```

---

## 12. Installation & Execution

### Prerequisites
- Python 3.10+ (tested on Python 3.11.9)
- Pip package manager

### 1. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository (or navigate to directory)
cd e2ee-ai-chatbot-threat-model

# Create a clean virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\activate

# Linux / macOS (bash/zsh):
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Unit Tests
```bash
pytest -v
```
*(All 43 unit tests execute in ~0.10s verifying mathematical formulas, boundary guards, invalid types, and empty dataset handlers).*

### 4. Launch the Streamlit Application
```bash
streamlit run app.py
```

### Expected Output
Upon launching, Streamlit outputs:
```text
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.xxx:8501
```
The browser will automatically render the 11-page interactive cybersecurity dashboard with reactive Plotly visualizations, downloadable Draw.io XML diagrams, and live pytest execution.

---

## 13. GitHub Repository
**GitHub Repository:**  
`[ADD FINAL GITHUB URL HERE]`

---

## 14. Testing & Verification

The prototype includes an automated test suite ([`tests/test_risk_engine.py`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/tests/test_risk_engine.py)) with **43 unit tests** covering:
- **Mathematical Accuracy**: Likelihood $\times$ Impact calculations across all valid score domains.
- **Boundary Analysis**: Verified minimum score ($1 \times 1 = 1$, Low) and maximum score ($5 \times 5 = 25$, Critical).
- **Classification Thresholds**: Exact cutoffs at 5 (Low), 10 (Med), 15 (High), and 16+ (Critical).
- **Exception Handling**: Rejection of zero, negative, out-of-bounds ($>5$), and non-integer inputs.
- **Dataset Integrity**: Loading of all 24 synthetic threats, 4 in each STRIDE category.
- **Summary Generation**: Correct computation of top risks, affected assets, and recommended controls.
- **Traceability Engines**: Validated asset inventories, data flows, and security vs. privacy modules.

---

## 14. Screenshots Section
Guidelines and capture targets for the project report and presentation are detailed in [`screenshots/README.md`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/screenshots/README.md):
1. `dashboard_overview.png`: Top KPIs, STRIDE frequency, and risk severity charts.
2. `system_architecture.png`: Interactive Mermaid diagram and component roles.
3. `data_flow_analysis.png`: Step-by-step breakdown of flows $F_1$ through $F_6$.
4. `asset_inventory.png`: CIA Triad ratings for all 9 protected assets.
5. `stride_threat_model.png`: Multi-parameter filtered threat catalog.
6. `risk_matrix_heatmap.png`: $5 \times 5$ Likelihood vs. Impact heatmap with threat IDs.
7. `mitigation_matrix.png`: Grouped security controls and traceability matrix.
8. `security_vs_privacy.png`: Educational analysis of E2EE scope and limitations.
9. `academic_mapping.png`: Full academic assignment pipeline.
10. `test_results.png`: Terminal output showing all 43 tests passing.

---

## 15. Limitations
1. **Academic Threat Model Prototype**: This system is designed for security analysis, modeling, and demonstration; it does not deploy a real production cryptographic infrastructure.
2. **Synthetic Architecture**: The chatbot architecture and threat data are simulated for educational evaluation and do not represent a specific proprietary commercial service.
3. **Simplified Residual Risk Model**: The residual risk engine applies heuristic percentage reductions based on mitigation status rather than continuous empirical telemetry.

---

## 16. Future Enhancements
1. **Automated Static Code Analysis Integration**: Coupling the threat model with automated SAST tools (e.g., Semgrep, Bandit) to flag vulnerabilities directly from source repositories.
2. **Dynamic Attack Simulation**: Emulating simulated adversarial prompt injection attempts against live sandboxed models to assess guardrail efficacy.
3. **Formal Cryptographic Verification**: Incorporating formal protocol verification tools (e.g., ProVerif or Tamarin) to mathematically prove safety numbers in the Double Ratchet implementation.

---

## 17. Conclusion
This micro-project provides an academically rigorous, mathematically verified, and practical threat-modeling prototype for an End-to-End Encrypted AI Chatbot. By applying the STRIDE taxonomy across 9 architectural components and 4 trust boundaries, the project demonstrates that while E2EE is fundamental for communication privacy, comprehensive security in Generative AI requires a Defense-in-Depth framework spanning hardware confidential compute enclaves, rigorous key lifecycles, and semantic prompt guardrails.

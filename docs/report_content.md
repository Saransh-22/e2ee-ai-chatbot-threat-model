# DAYANANDA SAGAR COLLEGE OF ENGINEERING
**(An Autonomous Institute affiliated to Visvesvaraya Technological University (VTU), Belagavi, Approved by AICTE & UGC, Accredited by NAAC with 'A' Grade & ISO 9001-2015 Certified Institution)**  
**Shavige Malleshwara Hills, Kumaraswamy Layout, Bengaluru - 560 111**  
**DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING**  

---

### ALTERNATE ASSESSMENT TOOL (AAT) — MICRO PROJECT REPORT

## THREAT MODELLING OF AN END-TO-END ENCRYPTED (E2EE) AI CHATBOT

**Submitted by:**  
**SARANSH NEEMA** (USN: **1DS23AI048**)  

**Course Name:** Data Security and Privacy  
**Course Code:** 22AI73  
**Semester:** VII (B.E. in Artificial Intelligence & Machine Learning)  
**Academic Year:** 2026–2027  

**Under the Guidance of:**  
**Dr. Aruna M G**  
Professor, Department of Artificial Intelligence & Machine Learning  
Dayananda Sagar College of Engineering, Bengaluru  

---

## TABLE OF CONTENTS

- **Abstract**
- **Course Outcome (CO) Mapping**
- **Program Outcome (PO) & PSO Mapping**
- **Sustainable Development Goal (SDG) Mapping**
- **1. Introduction**
  - 1.1 Background
  - 1.2 E2EE AI Chatbots
  - 1.3 Security Challenges
- **2. Problem Statement and Objectives**
  - 2.1 Problem Statement
  - 2.2 Objectives
- **3. Proposed Solution / Methodology**
  - 3.1 System Overview
  - 3.2 System Architecture
  - 3.3 Data Flow
  - 3.4 Trust Boundaries
  - 3.5 STRIDE Methodology
- **4. Mathematical Model**
  - 4.1 Threat Risk Model
  - 4.2 Likelihood
  - 4.3 Impact
  - 4.4 Risk Score
  - 4.5 Risk Classification
- **5. Security and Privacy Aspects**
  - 5.1 Spoofing
  - 5.2 Tampering
  - 5.3 Repudiation
  - 5.4 Information Disclosure
  - 5.5 Denial of Service
  - 5.6 Elevation of Privilege
- **6. Implementation and Results**
  - 6.1 Tools and Technologies
  - 6.2 Project Structure
  - 6.3 Threat Engine
  - 6.4 Risk Engine
  - 6.5 Mitigation Engine
  - 6.6 Dashboard
  - 6.7 Results
- **7. Testing and Verification**
- **8. Conclusion and Future Enhancements**
- **9. References**
- **Appendix**

---

## ABSTRACT

The rapid integration of Large Language Models (LLMs) and conversational artificial intelligence into enterprise communications has generated urgent security and data privacy concerns. While standard End-to-End Encryption (E2EE) frameworks (such as the Signal Protocol) guarantee message confidentiality between human peers, deploying an autonomous AI chatbot introduces a fundamental architectural dilemma termed the **"Plaintext Paradox of AI Inference"**: the language model must decrypt and inspect conversational tokens in memory to generate intelligent responses. 

This micro-project presents an academic security threat-modeling and risk-analysis prototype for an End-to-End Encrypted AI Chatbot. Utilizing Microsoft’s **STRIDE** methodology, the system identifies, categorizes, and evaluates 24 realistic threats distributed across 9 chatbot components and 4 explicit trust boundaries. A formal quantitative mathematical model ($\text{Risk Score} = \text{Likelihood} \times \text{Impact}$, on a 1–25 scale) classifies each vulnerability into Low, Medium, High, or Critical severity. A defense-in-depth mitigation strategy is formulated across 9 security control domains, encompassing hardware-enforced confidential computing (AMD SEV-SNP), the Double Ratchet cryptographic protocol, and dual input/output prompt guardrails. An interactive, local **Streamlit** dashboard coupled with 43 automated unit tests validates the model. The project demonstrates that while E2EE is indispensable for communication transit security, comprehensive privacy in Generative AI necessitates robust enclave memory protection, key zeroization, and semantic guardrail isolation.

---

## COURSE OUTCOME (CO) MAPPING

This project directly aligns with the official Course Outcomes defined for **Data Security and Privacy (22AI73)** in the Department of Artificial Intelligence & Machine Learning, DSCE:

| Course Outcome (CO) | Official Institutional Description | Project Activity Justification |
| :--- | :--- | :--- |
| **CO1** | *Use cybersecurity and data privacy principles to identify and mitigate threats like phishing, identity theft, malware, and data breaches using real-world scenarios.* | The project models real-world threats including client identity impersonation (`THR-001`), bearer token theft (`THR-004`), and malware RAM scraping (`THR-015`), defining cryptographic hardware keystores and mTLS controls to mitigate them. |
| **CO2** | *Analyze cybersecurity and data privacy principles to examine, differentiate, mitigate and evaluate threats such as phishing, identity theft, malware, and data breaches using case studies.* | The project applies the STRIDE framework to systematically differentiate between Spoofing, Tampering, Repudiation, Information Disclosure, DoS, and Elevation of Privilege across 9 architecture components. |
| **CO3** | *Demonstrate the use of cryptographic and privacy-preserving mechanisms to secure data and resolve practical security issues in diverse cybersecurity scenarios.* | Demonstrates the practical implementation of Double Ratchet ephemeral key exchange, Authenticated Encryption with Associated Data (AEAD), memory zeroization (`mlock`), and uniform PKCS#7 packet padding to prevent traffic profiling. |
| **CO4** | *Examine security governance frameworks, risk-management practices, and privacy regulations to evaluate organizational resilience and compliance through case-based analysis.* | Implements a formal quantitative risk scoring model ($\text{Risk} = L \times I$), evaluates residual risk postures, and integrates WORM Merkle tree audit logging adhering to DPDP Act 2023 and GDPR data minimization requirements. |

---

## PROGRAM OUTCOME (PO) & PSO MAPPING

### Program Outcomes (POs) Addressed
- **PO1 (Engineering Knowledge)**: Applied mathematical concepts of discrete probability and cryptographic algorithms (ECDH, AEAD, SHA-256 Merkle trees) to model secure communication networks.
- **PO2 (Problem Analysis)**: Formulated the "Plaintext Paradox" of Generative AI inference and systematically analyzed attack vectors using the STRIDE threat matrix.
- **PO3 (Design/Development of Solutions)**: Designed an 11-step confidential communication pipeline incorporating dual prompt guardrails and confidential compute enclaves (AMD SEV-SNP).
- **PO5 (Modern Tool Usage)**: Leveraged modern software engineering tools including Python 3.11, Streamlit, Plotly, Draw.io (diagrams.net), and Pytest.

### Program Specific Outcomes (PSOs) Mapping
- **PSO1 / PSO2**:
  > `[Insert official DSCE AIML PSO wording provided by faculty]`
  - *Technical Relevance*: Demonstrates the intersection of Machine Learning deployment and Cybersecurity by analyzing adversarial prompt injection, KV attention cache tenant cross-bleed, and algorithmic complexity attacks specific to Transformer neural network architectures.

---

## SUSTAINABLE DEVELOPMENT GOAL (SDG) MAPPING

### **SDG 9: Industry, Innovation, and Infrastructure**
*(Target 9.c: Significantly increase access to information and communications technology; Target 9.1: Develop quality, reliable, sustainable, and resilient infrastructure)*

- **Justification**: Modern industrial and enterprise infrastructures increasingly rely on autonomous AI agents and digital messaging networks to process sensitive operational, healthcare, and financial communications. A breach of these communication systems threatens digital infrastructure reliability, citizen privacy, and institutional trust. 
- By developing a formal threat-modeling framework that embeds End-to-End Encryption, confidential enclaves, and rigorous risk quantification into AI communications, this project directly advances **resilient, secure, and privacy-preserving digital infrastructure** (SDG 9).

---

## 1. INTRODUCTION

### 1.1 Background
Digital messaging systems form the backbone of modern collaboration. Over the past decade, End-to-End Encryption (E2EE) protocols—most notably the Signal Protocol, employing the Double Ratchet algorithm—have emerged as the gold standard for confidentiality. In conventional E2EE, cryptographic keys exist solely on the communicating users' devices; intermediate servers act purely as blind packet routers.

### 1.2 E2EE AI Chatbots
The emergence of Large Language Models (LLMs) has shifted chatbots from rigid rule-based scripts to autonomous AI conversational agents. Users increasingly transmit confidential business plans, medical inquiries, financial data, and personal credentials to AI systems. To preserve user confidentiality, architects propose End-to-End Encrypted AI Chatbots, wherein the encryption tunnel terminates directly between the user's client app and the AI inference engine.

### 1.3 Security Challenges: The "Plaintext Paradox"
Introducing an AI model as an endpoint fundamentally disrupts the standard E2EE security model:
1. **The Plaintext Processing Necessity**: Matrix multiplications and attention calculations cannot occur directly over ciphertext under standard cryptographic schemes. The prompt must be decrypted into memory before inference.
2. **Multi-Tenant Memory Bleed**: Transformer architectures utilize Key-Value (KV) attention caches. If GPU memory is multiplexed across sessions, previous tenant prompt fragments can bleed into subsequent user turns.
3. **Semantic Insecurity (Prompt Injection)**: Transport encryption guarantees that data arrives unmodified, but cannot determine whether the prompt itself contains adversarial instructions (jailbreaks) designed to exfiltrate system instructions.
4. **Metadata Leakage**: Because LLM response token lengths vary drastically depending on conversational topic, side-channel packet length profiling allows eavesdroppers to infer private conversational topics even when ciphertext is unbreakable.

---

## 2. PROBLEM STATEMENT AND OBJECTIVES

### 2.1 Problem Statement
How can an organization design, evaluate, and mitigate communication and host security threats in an AI chatbot system where messages must remain confidential in transit, cloud gateways must operate with zero knowledge of message contents, and the AI inference core must remain resilient against adversarial prompt injection, memory scraping, and privilege escalation?

### 2.2 Objectives
1. **Model System Architecture**: Formulate an 11-stage secure communication pipeline with explicit trust boundaries using Draw.io and Mermaid.js.
2. **Catalog STRIDE Threats**: Systematically identify and characterize 24 realistic synthetic threats spanning Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege across 9 chatbot components.
3. **Quantify Risk Posture**: Apply a strict mathematical risk model ($\text{Risk Score} = \text{Likelihood} \times \text{Impact}$) to categorize vulnerabilities into Low, Medium, High, and Critical severity tiers.
4. **Develop Defense Controls**: Map each identified threat to concrete architectural mitigations across 9 security control domains.
5. **Implement an Interactive Dashboard**: Deliver a local, dependency-free Streamlit analysis tool with 43 automated unit tests for practical viva evaluation.

---

## 3. PROPOSED SOLUTION / METHODOLOGY

### 3.1 System Overview
The proposed solution models a synthetic End-to-End Encrypted AI Chatbot comprising 9 core architectural modules operating across 4 distinct trust boundaries. The system implements a defense-in-depth posture combining application-level cryptography (Double Ratchet AEAD), network perimeter controls, confidential computing hardware enclaves, and semantic guardrail filters.

### 3.2 System Architecture
```
[User]
   │ (1. Types Prompt)
   ▼
[Chat Client App]
   │ (2. Key Ratchet Negotiation)
   ▼
[Identity & Authentication (JWT/OAuth2)]
   │ (3. Token Grant)
   ▼
[Encryption / Key Management (Hardware Keystore)]
   │ (4. AEAD Ciphertext Envelope)
   ▼
[Secure Gateway (TLS 1.3 / Ingress WAF)]
   │ (5. Blind Forwarding)
   ▼
[Message Relay Server (Zero-Knowledge Broker)]
   │ (6. Queue Dispatch)
   ▼
[API Layer & Decapsulator (In-Enclave RAM)]
   │ (7. In-Enclave Plaintext Stream)
   ▼
[Input Guardrail ➔ AI LLM Core ➔ Output Guardrail]
   │ (8. Generated Response Tokens)
   ▼
[Response Encryption Engine (Ratchet Re-encryption)]
   │ (9. Ciphertext Envelope)
   ▼
[Message Relay Server ➔ Secure Gateway]
   │ (10. Return Transit)
   ▼
[Chat Client App ➔ User (Decryption & Render)]
```

### 3.3 Data Flow Analysis
The system defines 6 primary data flows:
- **$F_1$ (User $\rightarrow$ Chat Client)**: User inputs prompt and credentials; protected by OS memory zeroization (`mlock`) and biometrics.
- **$F_2$ (Chat Client $\rightarrow$ Secure Gateway)**: E2EE prompt wrapped in outer transport envelope; protected by Double Ratchet AES-256-GCM and TLS 1.3 certificate pinning.
- **$F_3$ (Gateway $\rightarrow$ Message Relay)**: Envelope transit preserving public routing headers; protected by internal mTLS and uniform 4KB packet padding.
- **$F_4$ (Message Relay $\rightarrow$ AI Service)**: Ciphertext blob dispatched to inference queue; protected by SPIFFE/mTLS service mesh into AMD SEV-SNP encrypted memory.
- **$F_5$ (AI Service $\rightarrow$ Response Handler)**: Generated response tokens screened by output DLP guardrails with zero-copy memory transfers.
- **$F_6$ (Response Handler $\rightarrow$ User)**: Re-encrypted response ciphertext pushed back through relay to client UI for local rendering.

### 3.4 Trust Boundaries (TB)
- **`TB-01` (User Client Trust Boundary)**: Untrusted host OS environment; vulnerable to physical theft and memory dump scraping.
- **`TB-02` (Perimeter & Relay DMZ)**: Semi-trusted public transit network; vulnerable to TLS handshake floods and packet size profiling.
- **`TB-03` (Secure AI Processing Enclave)**: High-trust confidential computing enclave; vulnerable to prompt injection, KV attention leaks, and container escapes.
- **`TB-04` (Management & Governance Zone)**: Privileged control plane; vulnerable to IDOR on administrative APIs and audit trail erasure.

### 3.5 STRIDE Methodology
The system applies Microsoft's STRIDE taxonomy:
- **S - Spoofing**: Violates *Authentication*.
- **T - Tampering**: Violates *Integrity*.
- **R - Repudiation**: Violates *Accountability*.
- **I - Information Disclosure**: Violates *Confidentiality*.
- **D - Denial of Service**: Violates *Availability*.
- **E - Elevation of Privilege**: Violates *Authorization*.

---

## 4. MATHEMATICAL MODEL

### 4.1 Threat Risk Model
The threat modeling engine evaluates risk using standard quantitative cybersecurity assessment principles:

$$\text{Risk Score} = \text{Likelihood} \times \text{Impact} \quad \text{--- Equation (1)}$$

### 4.2 Likelihood ($L$)
Likelihood represents the probability of an attack vector being successfully exploited:
- $L = 1$: **Rare** (Requires high-privilege access, physical device possession, or nation-state compute).
- $L = 2$: **Unlikely** (Requires non-trivial specialized tools, internal network access, or custom exploits).
- $L = 3$: **Possible** (Standard exploit kits available; feasible over public networks).
- $L = 4$: **Likely** (Common misconfigurations, automated script attacks, public botnets).
- $L = 5$: **Frequent** (Trivial exploit requiring no specialized technical capability).

### 4.3 Impact ($I$)
Impact represents the technical and operational damage resulting from exploitation:
- $I = 1$: **Negligible** (Minor log noise; zero data loss or operational disruption).
- $I = 2$: **Minor** (Temporary localized failure; non-sensitive metadata exposed).
- $I = 3$: **Moderate** (Single user session affected; temporary denial of service).
- $I = 4$: **Major** (User identity hijacked; confidential prompts or model weights leaked).
- $I = 5$: **Catastrophic** (Host container escape, complete key recovery, multi-tenant database compromise).

### 4.4 Risk Score ($R$)
Because $L \in \{1, 2, 3, 4, 5\}$ and $I \in \{1, 2, 3, 4, 5\}$, the resulting score satisfies:

$$R \in [1, 25]$$

### 4.5 Risk Classification
Threats are classified into four objective tiers without subjective bias:
- **1 – 5**: **Low** (Green) — Periodic monitoring under standard logging.
- **6 – 10**: **Medium** (Yellow) — Moderate risk; baseline defense-in-depth controls required.
- **11 – 15**: **High** (Orange) — Substantial risk; prioritized cryptographic and memory controls.
- **16 – 25**: **Critical** (Red) — Severe breach potential; immediate architectural remediation mandatory.

---

## 5. SECURITY AND PRIVACY ASPECTS

### 5.1 Spoofing (Authentication)
- **Manifestation**: Adversary impersonates a legitimate client (`THR-001`), injects a rogue AI compute node (`THR-002`), or spoofs gateway DNS records (`THR-003`).
- **Mitigation**: Hardware-backed keystores (Android Keystore / iOS Secure Enclave), mutual TLS (mTLS) with SPIFFE workload attestation, and certificate pinning.

### 5.2 Tampering (Integrity)
- **Manifestation**: Modifying ciphertext routing headers in transit (`THR-005`), altering Diffie-Hellman parameters (`THR-006`), or injecting adversarial system prompt instructions (`THR-007`).
- **Mitigation**: Authenticated Encryption with Associated Data (AEAD - AES-256-GCM), Signed Prekey Bundles (X3DH), and Dual-LLM guardrail filters.

### 5.3 Repudiation (Accountability)
- **Manifestation**: User denies sending malicious prompts (`THR-009`), or a privileged administrator erases audit logs to conceal illicit queries (`THR-010`).
- **Mitigation**: Client-side digital signatures with monotonic sequence counters, WORM cloud storage, and cryptographically chained Merkle tree audit logs.

### 5.4 Information Disclosure (Confidentiality)
- **Manifestation**: Eavesdropping on relay queues (`THR-013`), multi-tenant KV attention cache leakage (`THR-014`), RAM key scraping (`THR-015`), or error log data leaks (`THR-016`).
- **Mitigation**: Strict Zero-Knowledge relay routing, AMD SEV-SNP confidential enclaves, per-turn KV attention flushing, memory zeroization (`mlock`), and zero-plaintext logging policies.

### 5.5 Denial of Service (Availability)
- **Manifestation**: TLS handshake exhaustion floods (`THR-017`), recursive combinatorial prompt expansion attacks (`THR-018`), or message buffer saturation (`THR-019`).
- **Mitigation**: Edge stateless SYN-cookies, eBPF XDP rate limiting, token generation quotas, and inference execution timeouts.

### 5.6 Elevation of Privilege (Authorization)
- **Manifestation**: Insecure Direct Object References (IDOR) on management endpoints (`THR-021`), JWT algorithm confusion (`THR-022`), or Python container breakout (`THR-023`).
- **Mitigation**: Attribute-Based Access Control (ABAC), strict JWT algorithm whitelisting (RS256 only), and gVisor microVM container sandboxing.

---

## 6. IMPLEMENTATION AND RESULTS

### 6.1 Tools and Technologies
- **Programming Language**: Python 3.11.9
- **Web Dashboard**: Streamlit 1.65.0
- **Data Analytics & Charts**: Pandas 3.0.6, Plotly 7.1.0
- **Automated Verification**: Pytest 8.4.2
- **Diagramming Tools**: Draw.io (diagrams.net), Mermaid.js

### 6.2 Project Structure
```
e2ee-ai-chatbot-threat-model/
├── app.py                      # Interactive Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive project documentation
├── data/
│   └── threats.json            # 24 synthetic STRIDE threats across 9 components
├── core/
│   ├── __init__.py             # Core package initialization
│   ├── threat_engine.py        # Threat loader, query, and summary engine
│   ├── risk_engine.py          # Mathematical risk calculation & classification
│   ├── mitigation_engine.py    # 9 security control domains & residual risk logic
│   ├── asset_inventory.py      # 9 protected assets with CIA triad ratings
│   ├── data_flow_engine.py     # 6 architectural data flows (F1 to F6)
│   └── security_privacy_engine.py # Conceptual analysis of E2EE scope & limits
├── diagrams/
│   ├── architecture.drawio     # Editable Draw.io XML architecture
│   ├── stride_threat_mapping.drawio # Editable Draw.io STRIDE mapping
│   └── architecture.md         # Detailed architectural documentation
├── tests/
│   └── test_risk_engine.py     # 43 automated unit tests
├── screenshots/
│   └── README.md               # Capture guidelines for presentation
└── docs/
    ├── report_content.md       # Complete college project report
    ├── screenshot_checklist.md # Verification checklist for viva
    ├── demo_script.md          # 5-minute & 2-minute demonstration flow
    └── viva_questions.md       # 25 viva questions with answers
```

### 6.3 Threat Engine
The `ThreatEngine` class loads the 24 synthetic threats from `data/threats.json`, validates their structure, enriches each threat with calculated risk metrics, and provides multi-parameter filtering across STRIDE category, component, risk level, asset, and security property.

### 6.4 Risk Engine
The `risk_engine.py` module strictly implements Equation (1), ensuring that input likelihoods and impacts outside $[1, 5]$ raise appropriate `ValueError` or `TypeError` exceptions, and maps scores to standard color-coded risk tiers.

### 6.5 Mitigation Engine
The `MitigationEngine` organizes controls across the 9 formal security domains and generates a formal mitigation matrix mapping each threat to its recommended control, violated security property, and defense rationale.

### 6.6 Dashboard Implementation
The Streamlit application features 11 dedicated pages:
1. **Dashboard**: Top KPI metric cards, STRIDE distribution bar charts, risk severity donut charts, and automated threat summaries.
2. **System Architecture**: Interactive Mermaid diagram, component role expanders, attack surface tables, and Draw.io downloads.
3. **Data Flow Analysis**: Detailed walkthrough of flows $F_1$ through $F_6$.
4. **Security Asset Inventory**: CIA triad ratings for 9 protected assets.
5. **STRIDE Threat Model**: Searchable catalog with deep-dive inspection cards.
6. **Risk Analysis**: Interactive $5 \times 5$ Risk Heatmap (Impact on Y, Likelihood on X) and risk simulator.
7. **Mitigation Controls**: Grouped controls and formal traceability matrix.
8. **Security vs. Privacy**: Educational analysis of E2EE limitations.
9. **Academic Mapping**: Traceability pipeline for college evaluators.
10. **Testing & Verification**: Direct in-app Pytest test runner with live output streaming.
11. **About Project**: Student credentials and academic disclaimers.

### 6.7 Results
- **Threat Model Balance**: Exactly 24 threats (4 in each STRIDE category).
- **Risk Distribution**: 4 Critical ($16.7\%$), 6 High ($25.0\%$), 11 Medium ($45.8\%$), and 3 Low ($12.5\%$).
- **Mitigation Posture**: $62.5\%$ of threats have verified mitigation architectures, while remaining threats are under active engineering review.

---

## 7. TESTING AND VERIFICATION

The project implements a test suite ([`tests/test_risk_engine.py`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/tests/test_risk_engine.py)) with **43 unit tests**. All 43 tests pass cleanly in $0.09\text{ seconds}$.

### Standardized Testing Table

| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Risk Formula Calculation | $L=3, I=4$ | Score: $12$, Level: High | Score: $12$, Level: High | **PASSED** |
| **TC-02** | Boundary Minimum Check | $L=1, I=1$ | Score: $1$, Level: Low | Score: $1$, Level: Low | **PASSED** |
| **TC-03** | Boundary Maximum Check | $L=5, I=5$ | Score: $25$, Level: Critical | Score: $25$, Level: Critical | **PASSED** |
| **TC-04** | Low Classification Threshold | Score $= 5$ | Level: Low | Level: Low | **PASSED** |
| **TC-05** | Medium Classification Threshold | Score $= 6$ | Level: Medium | Level: Medium | **PASSED** |
| **TC-06** | Medium Classification Cutoff | Score $= 10$ | Level: Medium | Level: Medium | **PASSED** |
| **TC-07** | High Classification Threshold | Score $= 11$ | Level: High | Level: High | **PASSED** |
| **TC-08** | High Classification Cutoff | Score $= 15$ | Level: High | Level: High | **PASSED** |
| **TC-09** | Critical Classification Threshold | Score $= 16$ | Level: Critical | Level: Critical | **PASSED** |
| **TC-10** | Out-of-Bounds Likelihood ($<1$) | $L=0, I=3$ | Raise `ValueError` | `ValueError` raised | **PASSED** |
| **TC-11** | Out-of-Bounds Likelihood ($>5$) | $L=6, I=3$ | Raise `ValueError` | `ValueError` raised | **PASSED** |
| **TC-12** | Out-of-Bounds Impact ($<1$) | $L=3, I=0$ | Raise `ValueError` | `ValueError` raised | **PASSED** |
| **TC-13** | Out-of-Bounds Impact ($>5$) | $L=3, I=6$ | Raise `ValueError` | `ValueError` raised | **PASSED** |
| **TC-14** | Non-Numeric Type Rejection | $L=\text{"high"}, I=4$ | Raise `TypeError` | `TypeError` raised | **PASSED** |
| **TC-15** | Empty Threat Dataset Handling | `threats = []` | Return empty summary; zero crash | Handled gracefully ($0$ threats) | **PASSED** |
| **TC-16** | Dataset Completeness Check | Load `threats.json` | Total count $= 24$ | Total count $= 24$ | **PASSED** |
| **TC-17** | STRIDE Balance Check | Group by STRIDE | Exactly $4$ threats per category | Exactly $4$ threats per category | **PASSED** |
| **TC-18** | Security Property Representation| Query properties | All $6$ properties present | All $6$ properties present | **PASSED** |
| **TC-19** | Text Search Query Filter | Query: "Prompt" | Returns `THR-007`, `THR-018` | Returns matching threats | **PASSED** |
| **TC-20** | Component Filter Check | Component: "Gateway" | Returns only Gateway threats | Returns only Gateway threats | **PASSED** |
| **TC-21** | Summary Analytics Generation | Call summary engine | Returns top assets and controls | Valid summary returned | **PASSED** |
| **TC-22** | Mitigation Matrix Completeness | Generate matrix | $24$ mapped rows returned | $24$ rows returned | **PASSED** |
| **TC-23** | Residual Risk Reduction | Mitigated threat | Residual score $<$ Initial score | Residual score reduced | **PASSED** |
| **TC-24** | Asset Inventory Completeness | Query asset engine | $9$ assets with CIA ratings | $9$ assets with CIA ratings | **PASSED** |
| **TC-25** | Data Flow Engine Verification | Query flow engine | $6$ flows ($F_1$ to $F_6$) verified | $6$ flows verified | **PASSED** |
| **TC-26** | Security vs Privacy Topics | Query topics engine | $9$ educational topics present | $9$ topics present | **PASSED** |

---

## 8. CONCLUSION AND FUTURE ENHANCEMENTS

### 8.1 Conclusion
This micro-project has formulated and implemented a formal threat model for an End-to-End Encrypted AI Chatbot. By applying the STRIDE taxonomy across 9 architecture components and 4 trust boundaries, the study demonstrates that:
1. **E2EE is Necessary but Insufficient**: Encryption secures messages across untrusted transit networks, but offers zero protection against compromised client endpoints, GPU cache attention bleed, or semantic prompt injection.
2. **The Inference Boundary is Paramount**: Because language models require unencrypted tokens to process requests, confidential computing enclaves (AMD SEV-SNP) and dual prompt guardrails represent mandatory additions to any E2EE AI architecture.
3. **Formal Risk Quantification**: Combining STRIDE with a mathematical risk model ($\text{Risk} = L \times I$) enables security teams to prioritize mitigations objectively based on quantitative severity.

### 8.2 Future Enhancements
1. **Automated Static Security Analysis (SAST)**: Integrating automated code scanners (such as Bandit and Semgrep) into the pipeline to detect hardcoded keys and insecure cipher suites in client applications.
2. **Empirical Prompt Injection Fuzzing**: Developing an automated red-teaming fuzzer to test LLM guardrail efficacy against evolving adversarial jailbreak techniques.
3. **Formal Cryptographic Protocol Verification**: Utilizing formal verification tools (e.g., ProVerif or Tamarin) to mathematically prove safety number generation and ephemeral key ratcheting.

---

## 9. REFERENCES

1. **Microsoft Corporation**, *The STRIDE Threat Model*, Microsoft Security Development Lifecycle (SDL), 2009.
2. **OWASP Foundation**, *OWASP Top 10 for Large Language Model Applications*, Version 2025, Open Web Application Security Project.
3. **M. Marlinspike and T. Perrin**, *The Double Ratchet Protocol*, Signal Foundation Specification, 2016.
4. **W. Stallings**, *Cryptography and Network Security: Principles and Practice*, 8th Edition, Pearson Education, 2020.
5. **National Institute of Standards and Technology (NIST)**, *Framework for Improving Critical Infrastructure Cybersecurity (CSF v2.0)*, NIST Special Publication, 2024.
6. **AMD Corporation**, *AMD SEV-SNP: Strengthening VM Isolation with Integrity Protection and More*, White Paper, 2020.
7. **Visvesvaraya Technological University (VTU)**, *Syllabus for Data Security and Privacy (22AI73)*, Department of Artificial Intelligence & Machine Learning, Belagavi.

---

## APPENDIX

### A.1 Architecture Diagram Source (`architecture.drawio`)
The primary architecture diagram is stored in XML format in [`diagrams/architecture.drawio`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/diagrams/architecture.drawio), displaying components, trust boundaries, and data flows.

### A.2 STRIDE Threat Mapping Diagram (`stride_threat_mapping.drawio`)
The second traceability diagram is stored in [`diagrams/stride_threat_mapping.drawio`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/diagrams/stride_threat_mapping.drawio), mapping each component to its STRIDE category, example threat scenario, and defense control.

### A.3 Threat Dataset (`data/threats.json`)
The complete dataset containing all 24 formal STRIDE threats with likelihood, impact, security properties, and mitigations is stored in [`data/threats.json`](file:///c:/Users/saran/OneDrive/Documents/sem7/DSP/e2ee-ai-chatbot-threat-model/data/threats.json).

### A.4 Automated Test Suite Execution Output
```bash
platform win32 -- Python 3.11.9, pytest-8.4.2
collected 43 items
tests/test_risk_engine.py ........................................... [100%]
43 passed in 0.09s
```

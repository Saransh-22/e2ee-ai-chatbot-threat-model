# Academic Project Notes: E2EE AI Chatbot Threat Modeling & Risk Analyzer

- **Subject Code**: 22AI73 - Data Security and Privacy (DSP)
- **Degree / Semester**: B.E. / 7th Semester
- **Student Name**: Saransh Neema
- **USN**: 1DS23AI048
- **Project Title**: Threat Modelling of an E2EE AI Chatbot

---

## 1. Problem Statement & Academic Motivation

Traditional End-to-End Encrypted (E2EE) messaging systems (e.g., Signal, WhatsApp) guarantee that only the communicating human endpoints possess decryption keys. Intermediate servers, telecom operators, and routers only handle opaque ciphertext.

However, when an **Artificial Intelligence (AI) model or LLM agent** acts as a conversational partner, the AI system itself represents a termination point of the encryption tunnel. This creates a critical architectural dilemma known as the **"Plaintext Paradox of AI Inference"**:
- To understand user context, evaluate prompts, and generate relevant responses, the AI inference worker must decrypt the message.
- If this decryption occurs in an untrusted or improperly isolated environment, user privacy, sensitive corporate data, or regulatory compliance (GDPR, HIPAA, DPDP Act 2023) is completely compromised.
- Furthermore, AI models introduce unique attack vectors not present in traditional messaging: **Prompt Injection, KV Cache Attention Bleed, Model Inversion, and Recursive Token DoS attacks**.

This micro-project provides a formal threat modeling prototype applying Microsoft's **STRIDE** methodology and quantitative risk analysis to a synthetic E2EE AI Chatbot architecture.

---

## 2. STRIDE Threat Modeling Methodology

| Category | Definition | Violated Security Property | Primary E2EE AI Vulnerability |
| :--- | :--- | :--- | :--- |
| **S - Spoofing** | Pretending to be someone or something else | **Authentication** | Client identity impersonation, Rogue AI inference worker nodes |
| **T - Tampering** | Modifying data in transit or memory | **Integrity** | Ephemeral key manipulation, Prompt injection attacks |
| **R - Repudiation** | Denying having performed an action | **Accountability** | Denying prompt dispatch, Admin audit log erasure |
| **I - Information Disclosure** | Exposing private data to unauthorized parties | **Confidentiality** | GPU KV cache attention leakage, Client RAM scraping, Traffic analysis |
| **D - Denial of Service** | Depriving legitimate users of access | **Availability** | TLS handshake exhaustion, Algorithmic recursive prompt expansion |
| **E - Elevation of Privilege** | Gaining unauthorized permissions | **Authorization** | Insecure Direct Object References (IDOR), Container/Sandbox escape |

---

## 3. Quantitative Risk Scoring Model

The risk calculation follows standard cybersecurity vulnerability assessment criteria:

$$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$

Where:
- $\text{Likelihood} \in \{1, 2, 3, 4, 5\}$ (1 = Rare, 5 = Almost Certain)
- $\text{Impact} \in \{1, 2, 3, 4, 5\}$ (1 = Negligible, 5 = Catastrophic)
- Resulting $\text{Risk Score} \in [1, 25]$

### Risk Level Classification Matrix:
- **1 – 5**: **Low** (Acceptable risk; monitor periodically)
- **6 – 10**: **Medium** (Moderate risk; implement baseline controls)
- **11 – 15**: **High** (Substantial risk; prioritized remediation required)
- **16 – 25**: **Critical** (Severe breach potential; immediate architectural mitigation mandatory)

---

## 4. Key Defense-in-Depth Mechanisms

1. **Hardware-Backed Cryptography**:
   - Client private keys stored inside Android Keystore / iOS Secure Enclave.
   - Long-term identity keys combined with ephemeral Double Ratchet Diffie-Hellman keys for forward secrecy and post-compromise security.
2. **Confidential Computing (TEE)**:
   - AI inference engine hosted in hardware-isolated Trusted Execution Environments (e.g., AMD SEV-SNP or Intel TDX).
   - Plaintext memory is cryptographically shielded from host OS, hypervisor, and data center administrators.
3. **Dual-Guardrail Architecture**:
   - An independent input guardrail inspects prompts before reaching the LLM core.
   - An output guardrail screens responses for data exfiltration, PII leakage, and hallucinations.
4. **Zero-Knowledge Message Relay**:
   - The relay server operates blindly, using constant-size packet padding (uniform 4KB blocks) to resist traffic volume profiling.

---

## 5. Viva Preparation: Questions & Answers

### Q1: Why can't we use standard Signal protocol directly for an AI chatbot?
**Ans**: In standard Signal protocol, Alice talks to Bob. Neither server has keys. In an AI chatbot, the "recipient" is an automated computational model running on a server cluster. The model requires plaintext prompt representations to execute matrix multiplications in neural network layers. Therefore, the encryption endpoint must terminate inside a hardware-isolated confidential enclave rather than an ordinary user device.

### Q2: What is the difference between Spoofing and Elevation of Privilege?
**Ans**: Spoofing violates *Authenticity* (pretending to be another user or service during authentication). Elevation of Privilege violates *Authorization* (an already authenticated actor successfully accessing features or data reserved for higher privilege levels, e.g., an ordinary user escalating to admin).

### Q3: How do you mitigate prompt injection in an E2EE architecture?
**Ans**: Prompt injection is categorized under **Tampering** (violating semantic Integrity). Because the message is encrypted in transit, inspection cannot occur at intermediate gateways. Mitigation must occur inside the secure enclave using multi-tiered defenses: prompt delimiter sandboxing, structural JSON schemas, and specialized lightweight input guardrail models.

### Q4: How does packet padding mitigate Information Disclosure on an E2EE relay?
**Ans**: Even when ciphertext is completely unbreakable, an eavesdropper can observe packet sizes and frequencies (side-channel traffic analysis). For example, short responses vs. long medical diagnoses leak information. Constant-rate transmission with uniform PKCS#7 block padding prevents side-channel deduction of message contents.

### Q5: How is non-repudiation enforced if messages are encrypted?
**Ans**: Messages are digitally signed client-side with the user's private key before encryption, and the server generates cryptographically chained Merkle tree audit log entries stored in Write-Once-Read-Many (WORM) storage.

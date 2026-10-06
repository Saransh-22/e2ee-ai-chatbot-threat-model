# Practical Demonstration Script for Viva Evaluation

**Course:** Data Security and Privacy (22AI73) — Semester VII  
**Student:** Saransh Neema (USN: **1DS23AI048**)  
**Project Title:** Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot  
**Application URL:** `http://localhost:8501`  

---

## 1. Five-Minute Standard Demonstration Flow (5:00 min)

### **0:00 – 0:30 | Project Introduction & Motivation**
- **Action on Screen**: Open the Streamlit app on `📊 Dashboard`.
- **Spoken Talking Points**:
  > *"Good morning, respected evaluators. My name is Saransh Neema, USN 1DS23AI048. My micro-project for Data Security and Privacy is 'Threat Modelling of an End-to-End Encrypted AI Chatbot'.*
  > *In modern messaging like Signal, E2EE ensures only human endpoints have keys. However, when an AI model acts as a conversational respondent, we encounter the **'Plaintext Paradox of AI Inference'**: the AI model must decrypt the prompt to compute neural network matrix multiplications.*
  > *This creates novel vulnerabilities—from prompt injection and attention cache leaks to memory scraping. Our goal is to formally model these threats using Microsoft's STRIDE framework and quantify them using a mathematical risk model."*

---

### **0:30 – 1:15 | System Architecture & Trust Boundaries**
- **Action on Screen**: Click on `🏛️ System Architecture` in the sidebar. Show the Mermaid diagram tab.
- **Spoken Talking Points**:
  > *"Here is the 11-stage architectural pipeline. The message originates at the Chat Client, establishes ephemeral keys via the Double Ratchet protocol, passes through a TLS 1.3 Secure Gateway, and is routed blindly by a Zero-Knowledge Message Relay Server.*
  > *Crucially, we define **four explicit Trust Boundaries**:*
  > - *`TB-01`: The User Client Zone on an untrusted device.*
  > - *`TB-02`: The Perimeter DMZ handling public transit.*
  > - *`TB-03`: The Secure AI Processing Enclave—this is a hardware-isolated confidential compute environment (AMD SEV-SNP) where prompt decryption occurs exclusively inside protected memory.*
  > - *`TB-04`: The Governance Zone housing administrative APIs and WORM Merkle audit logs.*
  > *We also provide the complete editable Draw.io XML file downloadable directly from this tab."*

---

### **1:15 – 2:15 | STRIDE Threat Model & Deep Dive**
- **Action on Screen**: Click on `🛡️ STRIDE Threat Model`. Filter by STRIDE category (e.g., *Tampering*), then scroll down to the Threat Inspector and select `THR-007`.
- **Spoken Talking Points**:
  > *"Our threat catalog contains 24 formal synthetic threats evenly balanced across all six STRIDE dimensions—exactly four threats per category.*
  > *For example, under **Tampering**, we have `THR-007: Indirect Prompt Injection`. Even if transport encryption is unbreakable, an adversary can embed malicious instruction overrides into the encrypted payload.*
  > *In this inspector, you can see the target component, affected asset, data flow crossing, attack scenario, violated security property (*Integrity*), and the recommended defense: Dual-LLM Guardrail filters that screen prompt semantics prior to core LLM inference."*

---

### **2:15 – 3:15 | Mathematical Risk Model & 5×5 Matrix**
- **Action on Screen**: Click on `📈 Risk Analysis`. Scroll to the 5×5 Risk Matrix Heatmap.
- **Spoken Talking Points**:
  > *"We quantify risk using the objective formula: **Risk Score = Likelihood × Impact**, where Likelihood is rated 1 to 5 and Impact is rated 1 to 5, producing a scale of 1 to 25.*
  > *We enforce strict threshold tiers: 1–5 is Low, 6–10 is Medium, 11–15 is High, and 16–25 is Critical. Notice that threats are classified purely based on calculated mathematics, without subjective bias.*
  > *On this interactive 5×5 matrix, Impact is plotted on the Y-axis and Likelihood on the X-axis. You can see our 4 Critical risks clustered in the top-right score-16 cells—including Prompt Injection (`THR-007`), KV Cache Leakage (`THR-014`), TLS Flooding (`THR-017`), and Recursive Token DoS (`THR-018`). Below, threats are automatically ranked by priority."*

---

### **3:15 – 4:15 | Mitigation Controls & Traceability Matrix**
- **Action on Screen**: Click on `🔐 Mitigation Controls`. Switch to the *Formal Mitigation Traceability Matrix* tab.
- **Spoken Talking Points**:
  > *"We organize defense-in-depth across **nine security control domains**: Authentication, Authorization, Confidentiality, Integrity, Availability, Accountability, Key Management, Logging, and Data Minimization.*
  > *Here is the formal Traceability Matrix mapping each Threat to its Security Control, Violated Security Property, and Technical Rationale.*
  > *For example:*
  > - *Spoofing is mapped to Hardware Keystores and mTLS (*Authentication*).*
  > - *Information Disclosure is mitigated through AMD SEV-SNP enclaves and per-turn KV cache zero-flushing (*Confidentiality*).*
  > - *Repudiation is resolved through WORM storage and Merkle tree hash chaining (*Accountability*)."*

---

### **4:15 – 5:00 | Automated Verification, Testing & Conclusion**
- **Action on Screen**: Click on `🧪 Testing & Verification`. Click the blue **▶️ Execute Pytest Test Suite** button and let the terminal output stream live.
- **Spoken Talking Points**:
  > *"To ensure software engineering rigor, we implemented an automated test suite in Pytest containing 43 unit tests. Let's execute them live.*
  > *[Wait 2 seconds for green banner]*
  > *As you can see, all 43 tests pass in 0.09 seconds. The suite rigorously verifies formula calculations, boundary bounds (1x1 to 5x5), invalid input rejection, empty dataset handling, and dataset completeness.*
  > *In conclusion, this project demonstrates that E2EE is necessary for transit privacy, but true Generative AI security requires Defense-in-Depth spanning confidential enclaves, semantic guardrails, and key zeroization. Thank you, and I am now ready for questions."*

---

## 2. Emergency Two-Minute Quick Version (2:00 min)
*Use this version if the evaluator instructs you to keep it under two minutes.*

- **0:00 – 0:30 | Problem & Architecture**:
  > *"Respected evaluators, my project models security threats in an End-to-End Encrypted AI Chatbot (USN: 1DS23AI048). The core issue is that while messages are encrypted in transit, the AI model must decrypt prompts to process inference. We designed an 11-stage pipeline spanning four trust boundaries, isolating the LLM inside an AMD SEV-SNP confidential compute enclave."*
- **0:30 – 1:00 | STRIDE Model & Risk Formula**:
  > *"We cataloged 24 formal threats across all six STRIDE categories—four per category. Each threat is evaluated using **Risk = Likelihood × Impact** on a 1–25 scale, mapping to Low, Medium, High, and Critical. On our 5x5 heatmap, four threats are flagged as Critical, including Prompt Injection (`THR-007`) and GPU KV Cache Bleed (`THR-014`)."*
- **1:00 – 1:30 | Mitigations & Matrix**:
  > *"We grouped mitigations into 9 domains. For transit, we use Double Ratchet AEAD; for the relay, zero-knowledge routing with 4KB packet padding; for the AI core, dual-guardrails and per-turn attention cache purging; and for governance, WORM Merkle audit logs."*
- **1:30 – 2:00 | Live Test Verification**:
  > *"Our Streamlit prototype includes 43 automated unit tests in Pytest. Clicking execute live: all 43 tests pass in 0.09s, verifying boundary conditions, risk classifications, and dataset integrity. The full report and Draw.io architecture are documented and ready. Thank you."*

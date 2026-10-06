# Comprehensive Viva Questions & Answers

**Course:** Data Security and Privacy (22AI73) — Semester VII  
**Student:** Saransh Neema (USN: **1DS23AI048**)  
**Project:** Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot  

---

### **1. What is End-to-End Encryption (E2EE), and how does it work?**
**Answer:** End-to-End Encryption is a communication security mechanism where only the communicating endpoints possess the cryptographic keys needed to decrypt messages. Intermediary servers, cloud routers, and service providers handle only opaque ciphertext and are unable to access the plaintext message content.

---

### **2. What is the fundamental challenge of applying E2EE to an AI chatbot?**
**Answer:** The **"Plaintext Paradox of AI Inference"**. In standard human-to-human E2EE, both endpoints are humans. In an AI chatbot, the recipient is a neural network model that requires unencrypted prompt representations (token embeddings) to compute attention weights and matrix multiplications. Therefore, encryption must terminate inside the AI server, shifting the threat surface to server memory and confidential enclave boundaries.

---

### **3. What is threat modeling, and why is it performed?**
**Answer:** Threat modeling is a structured engineering process for identifying, quantifying, and mitigating potential security vulnerabilities in a system architecture before development or deployment. It helps prioritize security investments based on calculated risk rather than guesswork.

---

### **4. What does the STRIDE acronym stand for?**
**Answer:** STRIDE is Microsoft’s threat categorization framework representing:
- **S** — Spoofing (violates *Authentication*)
- **T** — Tampering (violates *Integrity*)
- **R** — Repudiation (violates *Accountability*)
- **I** — Information Disclosure (violates *Confidentiality*)
- **D** — Denial of Service (violates *Availability*)
- **E** — Elevation of Privilege (violates *Authorization*)

---

### **5. Why was STRIDE chosen over other threat modeling frameworks like PASTA or DREAD?**
**Answer:** STRIDE maps directly to foundational security properties (CIA + Authentication, Authorization, Accountability), making it ideal for architectural component-level decomposition and academic rigor. DREAD is primarily a legacy scoring method, while PASTA is an extensive enterprise risk methodology exceeding micro-project scope.

---

### **6. Can you give an example of a Spoofing threat in this chatbot architecture?**
**Answer:** `THR-001: Client Identity Impersonation`. An attacker steals an ephemeral session token or clones device biometric tokens to authenticate to the messaging relay, masquerading as a legitimate user.

---

### **7. What is Tampering in an E2EE AI Chatbot context?**
**Answer:** `THR-007: Indirect Prompt Injection`. An adversary crafts adversarial prompt delimiters within the encrypted message to override system instructions and hijack model behavior once decrypted in the AI enclave.

---

### **8. What is Repudiation, and how does it differ from Tampering?**
**Answer:** Tampering alters data; Repudiation is the ability of an actor to **deny having performed an action** due to a lack of indisputable cryptographic evidence. In our project, `THR-009` addresses a user denying having dispatched an abusive prompt.

---

### **9. How does Information Disclosure occur if transit is encrypted?**
**Answer:** Information Disclosure can occur through:
1. **Multi-tenant memory bleed**: Transformer KV attention caches from one tenant leaking into another (`THR-014`).
2. **RAM scraping**: Side-loaded malware reading unpinned session keys from client memory (`THR-015`).
3. **Traffic analysis**: Observing packet size and transmission intervals to infer response lengths (`THR-010`).

---

### **10. What is a Denial of Service (DoS) attack against an AI inference service?**
**Answer:** `THR-018: Algorithmic Token Expansion Attack`. An attacker submits recursive combinatorial prompts designed to force the model into maximum token output generation loops, starving GPU compute cores and exhausting cluster memory.

---

### **11. What is Elevation of Privilege in this architecture?**
**Answer:** `THR-022: JWT Algorithm Confusion`. An adversary switches the token signature algorithm from RS256 to HS256, signing an elevated admin role claim using the public key as HMAC secret, thereby bypassing gateway authorization.

---

### **12. What is a Trust Boundary, and why is it important?**
**Answer:** A trust boundary is a perimeter where data transitions between different security domains with different levels of privilege. It is critical because all data crossing a trust boundary must be validated, authenticated, and sanitized. We defined four: `TB-01` (Client), `TB-02` (Perimeter/DMZ), `TB-03` (AI Enclave), and `TB-04` (Management).

---

### **13. What is an attack surface?**
**Answer:** The attack surface is the sum total of all reachable points and interfaces where an unauthorized user can attempt to inject data, extract information, or exploit a vulnerability. In our system, the attack surface includes client RAM, the gateway TLS port, relay message queues, and admin REST endpoints.

---

### **14. What is the mathematical risk formula used in this project?**
**Answer:** 
$$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$
Where Likelihood $\in \{1, 2, 3, 4, 5\}$ and Impact $\in \{1, 2, 3, 4, 5\}$, producing a score between $1$ and $25$.

---

### **15. How is Likelihood defined and rated?**
**Answer:** Likelihood represents the probability of exploitation on a 1–5 scale:
- 1 = Rare (requires state-level compute or physical possession)
- 2 = Unlikely (requires non-trivial custom exploits)
- 3 = Possible (standard public network exploit kits)
- 4 = Likely (common automated botnet attacks)
- 5 = Frequent (trivial vulnerability requiring zero specialized tools)

---

### **16. How is Impact defined and rated?**
**Answer:** Impact represents the severity of damage resulting from a breach on a 1–5 scale:
- 1 = Negligible (minor log noise)
- 2 = Minor (temporary local glitch)
- 3 = Moderate (single session disrupted)
- 4 = Major (confidential prompts leaked or user identity hijacked)
- 5 = Catastrophic (complete key compromise or container escape)

---

### **17. What are the four Risk Classification tiers?**
**Answer:**
- **1 – 5**: **Low** (Acceptable risk profile; periodic monitoring)
- **6 – 10**: **Medium** (Moderate risk; baseline defense controls)
- **11 – 15**: **High** (Substantial risk; prioritized remediation)
- **16 – 25**: **Critical** (Severe architectural danger; immediate mandatory mitigation)

---

### **18. How do you mitigate the risk of prompt injection in an E2EE architecture?**
**Answer:** Mitigation cannot occur at the transit gateway because the message is encrypted. It must occur inside the secure enclave using a **Dual-LLM Guardrail Architecture**: a dedicated lightweight input guardrail model inspects the decrypted prompt semantics and strips adversarial delimiter patterns before passing tokens to the core LLM.

---

### **19. What is Confidential Computing, and why is it necessary here?**
**Answer:** Confidential Computing utilizes hardware-isolated Trusted Execution Environments (TEEs), such as AMD SEV-SNP or Intel TDX, to encrypt data while in use in system memory. It prevents cloud operators, malicious root administrators, or compromised hypervisors from scraping decrypted prompts or model weights from RAM.

---

### **20. Why does this micro-project use synthetic data rather than real data?**
**Answer:** Because real cryptographic messaging implementations handle personal data protected under regulations like the DPDP Act 2023 and GDPR. Developing an academic threat model using synthetic architectures and simulated threats allows rigorous security analysis without risking real personal data exposure or liability.

---

### **21. Why was Streamlit chosen for the user interface?**
**Answer:** Streamlit allows building interactive, professional, and reproducible cybersecurity analytical tools in pure Python without needing external cloud servers or databases. It enables direct local execution (`streamlit run app.py`) with reactive Plotly charts and live test suite execution.

---

### **22. Why was Draw.io (diagrams.net) chosen for the architecture diagrams?**
**Answer:** Draw.io produces open, standardized, human-readable XML documents that are fully editable and version-controllable. It allows precise visual separation of trust boundaries, data flows, and security zones without proprietary software lock-in.

---

### **23. How does packet padding prevent Information Disclosure?**
**Answer:** In variable-length encryption, an eavesdropper can observe packet sizes and timing (traffic analysis) to infer conversational topics (e.g., short yes/no vs. lengthy medical advice). Uniform PKCS#7 padding standardizes all packet envelopes to uniform 4KB blocks, eliminating side-channel leakage.

---

### **24. What are the primary limitations of this prototype?**
**Answer:**
1. It is an analytical threat modeling prototype, not a production-deployed messaging platform.
2. The residual risk calculation uses heuristic mitigation percentage reductions rather than empirical telemetry.
3. The AI inference engine and guardrails are modeled architecturally rather than executing live multi-billion-parameter neural network weights.

---

### **25. What future enhancements would you propose for this project?**
**Answer:**
1. Integrating automated Static Application Security Testing (SAST) tools to scan client source code for cryptographic vulnerabilities.
2. Building an automated adversarial prompt injection fuzzer to empirically evaluate guardrail resilience.
3. Conducting formal cryptographic protocol verification using tools like ProVerif or Tamarin to mathematically verify key ratcheting security.

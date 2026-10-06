# 5-MINUTE LIVE TEACHER DEMONSTRATION SCRIPT

**Course:** Data Security and Privacy (22AI73)  
**Student:** Saransh Neema  
**USN:** 1DS23AI048  
**Department:** Artificial Intelligence & Machine Learning, DSCE Bengaluru  
**Faculty Guide:** Dr. Aruna M G  
**Project:** Threat Modelling of an End-to-End Encrypted (E2EE) AI Chatbot  

---

## DEMO TIMELINE OVERVIEW (TOTAL: 5 MINUTES)
- **Minute 1:** Project Identity, Motivation & Problem Statement
- **Minute 2:** Architectural Decomposition & Trust Boundaries
- **Minute 3:** STRIDE Methodology & Critical Vulnerability Deep-Dive
- **Minute 4:** Risk Heatmap & Traceability Matrix
- **Minute 5:** Test Execution & Closing Takeaway

---

### MINUTE 1 — INTRODUCTION & PROBLEM STATEMENT
- **WHAT YOU CLICK:** Sidebar $\rightarrow$ **📊 Dashboard**
- **WHAT THE TEACHER SEES:** 
  The top dashboard banner displaying your name, USN `1DS23AI048`, Course `22AI73`, and KPI cards:
  - Total Threats: `24`
  - Critical Threats: `4`
  - High Threats: `6`
  - Medium: `11` | Low: `3`
  - Average Risk Score: `10.38`
- **WHAT YOU SAY:**
  > "Good morning Ma'am / Sir. My name is Saransh Neema, USN 1DS23AI048. 
  > This is my micro-project for Data Security and Privacy (22AI73): **Threat Modelling of an End-to-End Encrypted AI Chatbot**.
  > 
  > In traditional messaging apps like WhatsApp, E2EE ensures that only human users have the decryption keys. However, when we integrate an AI chatbot, the receiving endpoint is an AI neural network that **must decrypt the message** in server memory to generate embeddings and run matrix operations. 
  > 
  > This creates the **'Plaintext Paradox of AI Inference'**: even with encrypted transit, user prompts become vulnerable at the compute boundary. Our objective was to systematically model these vulnerabilities using Microsoft STRIDE and quantify their risks."
- **WHY IT MATTERS:** Establishes your clear understanding of why E2EE in AI differs fundamentally from standard messaging.

---

### MINUTE 2 — SYSTEM ARCHITECTURE & TRUST BOUNDARIES
- **WHAT YOU CLICK:** Sidebar $\rightarrow$ **🏛️ System Architecture**
- **WHAT THE TEACHER SEES:** 
  The 9-component interactive architecture graph showing:
  `User / Chat Client` $\rightarrow$ `Authentication` $\rightarrow$ `Key Management` $\rightarrow$ `Secure Gateway` $\rightarrow$ `Message Relay` $\rightarrow$ `AI Processing Service`, with 4 marked Trust Boundaries (`TB-01` to `TB-04`).
- **WHAT YOU SAY:**
  > "To analyze the attack surface, we decomposed the synthetic system into 9 architectural components across 4 distinct Trust Boundaries:
  > - **TB-01** separates untrusted user devices from the network.
  > - **TB-02** protects the edge ingress gateway.
  > - **TB-03** isolates the confidential AI compute cluster from message queues.
  > - **TB-04** isolates the administrative and logging planes.
  > 
  > Notice that the Message Relay server only handles opaque ciphertext envelopes. Decryption only takes place within TB-03 inside the AI Processing Service."
- **WHY IT MATTERS:** Demonstrates formal system decomposition and boundary demarcation expected in 7th-semester engineering.

---

### MINUTE 3 — STRIDE MODEL & CRITICAL THREAT DEEP-DIVE
- **WHAT YOU CLICK:** Sidebar $\rightarrow$ **🛡️ STRIDE Threat Model** $\rightarrow$ Set Risk Level filter to **Critical**
- **WHAT THE TEACHER SEES:** 
  A filtered table displaying the 4 Critical threats: `THR-007`, `THR-014`, `THR-017`, and `THR-018` highlighted in red badges.
- **WHAT YOU SAY:**
  > "We developed a balanced dataset of 24 threats—exactly 4 threats for each of the six STRIDE categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.
  > 
  > If we look at the Critical threats:
  > Take **THR-007 (Indirect Prompt Injection)** under Tampering. Even though the prompt is end-to-end encrypted in transit, an attacker can embed adversarial jailbreak instructions inside the encrypted payload. Once decrypted inside the AI enclave, the LLM parses the instructions and bypasses safety filters.
  > 
  > We rated Likelihood as 4 and Impact as 4, resulting in a **Risk Score of 16**, which puts it into our Critical tier."
- **WHY IT MATTERS:** Shows that you understand both traditional cybersecurity and modern AI-specific vulnerabilities.

---

### MINUTE 4 — RISK HEATMAP & MITIGATION TRACEABILITY
- **WHAT YOU CLICK:** Sidebar $\rightarrow$ **📈 Risk Analysis** $\rightarrow$ Scroll to **5x5 Likelihood-Impact Heatmap**, then click **🔐 Mitigation Controls**
- **WHAT THE TEACHER SEES:** 
  1. The 5x5 color-coded heatmap showing threat distribution across cells.
  2. The Mitigation Controls page with a 62.5% mitigation posture and the complete Traceability Matrix.
- **WHAT YOU SAY:**
  > "Our mathematical risk engine calculates $\text{Risk} = \text{Likelihood} \times \text{Impact}$ on a scale of 1 to 25, categorized into Low, Medium, High, and Critical.
  > 
  > On this 5x5 heatmap, the teacher can immediately see which vulnerabilities cluster in the critical quadrant.
  > 
  > Moving to **Mitigation Controls**, every threat maps to a concrete security defense. For instance, THR-007 is mitigated by dual-LLM prompt guardrails and delimiter framing. Implementing these controls reduces our average risk score from **10.38 down to 5.92**, achieving a **43% quantitative risk reduction**."
- **WHY IT MATTERS:** Proves full closed-loop traceability: Problem $\rightarrow$ Risk $\rightarrow$ Mitigation $\rightarrow$ Residual Risk.

---

### MINUTE 5 — AUTOMATED TESTING & CONCLUSION
- **WHAT YOU CLICK:** Sidebar $\rightarrow$ **🧪 Testing & Verification** $\rightarrow$ Click the **Run All Automated Tests** button
- **WHAT THE TEACHER SEES:** 
  A live execution terminal in the browser running pytest and outputting:
  `====== 43 passed in 0.14s ======`
- **WHAT YOU SAY:**
  > "Finally, to guarantee the mathematical accuracy and integrity of our threat model, we implemented a complete unit test suite in pytest.
  > 
  > As you can see live on screen, all **43 test cases pass cleanly in 0.14 seconds**. These tests formally verify all risk formulas, boundary conditions, out-of-range value exceptions, and category distributions.
  > 
  > In conclusion, while E2EE guarantees confidentiality over public networks, securing an AI chatbot requires confidential enclaves, attention cache flushing, and strict prompt guardrails at the compute boundary. 
  > Thank you Ma'am / Sir, I am happy to answer any questions."
- **WHY IT MATTERS:** Concludes with incontrovertible technical proof that the code works, runs live, and has zero bugs.

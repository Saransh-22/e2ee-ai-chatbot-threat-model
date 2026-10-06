# System Architecture: End-to-End Encrypted (E2EE) AI Chatbot

## 1. Executive Summary

In a standard End-to-End Encrypted (E2EE) messaging protocol (such as the Signal Protocol), encryption occurs between two human endpoints, and intermediary servers only handle opaque ciphertext. In an **E2EE AI Chatbot**, the AI inference engine is an active communication participant that must decrypt and inspect conversational context to generate intelligent responses, while ensuring:
1. Zero plaintext exposure to intermediate network hops, untrusted transit relays, or unauthorized system operators.
2. Strong cryptographic isolation of session keys, model cache memory, and tenant contexts.
3. Resilience against both conventional network attacks and AI-specific vulnerabilities (such as prompt injection, KV cache bleed, and algorithmic token denial-of-service).

This document outlines the architectural blueprint, trust boundaries, data flows, and STRIDE attack surface represented in `architecture.drawio`.

---

## 2. End-to-End Communication Lifecycle

The communication lifecycle executes in an 11-step pipeline across four defined security domains:

```
[User / Chat Client]
       │ (1. Ephemeral Ratchet Key Agreement)
       ▼
[Encryption / Key Management]
       │ (2. Authenticated Session Token)
       ▼
[Secure Gateway (TLS 1.3 / Ingress WAF)]
       │ (3. Ciphertext Envelope Transit)
       ▼
[Message Relay Server (Zero-Knowledge Queue)]
       │ (4. Confidential Queue Dispatch)
       ▼
[API Layer (AEAD Message Decapsulation)]
       │ (5. In-Memory Plaintext Stream)
       ▼
[AI Processing Service (Confidential LLM Enclave + Guardrails)]
       │ (6. Generated Response Tokens)
       ▼
[Response Encryption Engine (Ratchet Re-encryption)]
       │ (7. Ciphertext Payload)
       ▼
[Message Relay Server]
       │ (8. Push Notification / Stream)
       ▼
[User / Chat Client (Decryption & Rendering)]
```

### Detailed Pipeline Flow
1. **Key Negotiation (`Flow 1`)**: The client application generates an ephemeral Elliptic Curve Diffie-Hellman (ECDH) keypair in its hardware-backed keystore and negotiates a session key ratchet with the AI Enclave.
2. **Authentication Grant (`Flow 2`)**: The client presents its credentials to the Identity Service, receiving an RS256-signed JWT bound to its device fingerprint.
3. **Prompt Encryption & Dispatch (`Flow 3`)**: The user prompt is encrypted client-side using Authenticated Encryption with Associated Data (AEAD, AES-256-GCM / ChaCha20-Poly1305).
4. **Perimeter Ingress (`Flow 4`)**: The Secure Gateway verifies transport TLS, applies DDoS rate-limiting, and forwards the ciphertext envelope.
5. **Zero-Knowledge Queuing (`Flow 5`)**: The Message Relay routes the encrypted payload into message broker queues strictly using outer envelope headers; it never holds decryption keys.
6. **Enclave Ingress & Decryption (`Flow 6`)**: Within the confidential compute boundary, the API layer derives the ratcheted symmetric key, verifies the AEAD authentication tag, and decrypts the prompt payload directly in protected RAM.
7. **Input Guardrail Inspection (`Flow 7`)**: An inline input filter screens the prompt against known jailbreaks, prompt injections, and privilege manipulation payloads.
8. **Sandboxed LLM Inference (`Flow 8`)**: The isolated language model engine generates response tokens within a dedicated per-session memory context.
9. **Output Guardrail & DLP Filter (`Flow 9`)**: Before egress, the generated response is inspected to prevent data loss (PII, credentials, model system prompts).
10. **Ciphertext Re-encryption (`Flow 10`)**: The Response Encryption engine wraps the response in the forward-ratcheted session key.
11. **Client Decryption (`Flow 11`)**: The client receives the response packet, decrypts it in its secure enclave, zeroizes the temporary buffer, and displays the response to the user.

---

## 3. Trust Boundaries (TB)

Threat modeling requires formal boundaries where data crosses between different levels of trust:

| Trust Boundary | Scope | Inherent Trust Level | Key Threats Faced |
| :--- | :--- | :--- | :--- |
| **TB-01: Client Trust Zone** | End-user device, mobile app, local keystore | **Untrusted / Hostile Host** | Client spoofing, physical device theft, RAM scraping, reverse engineering |
| **TB-02: Ingress & Relay DMZ** | Public internet, TLS termination, Message Relay | **Semi-Trusted Transit** | Ingress TLS exhaustion DoS, DNS hijacking, traffic analysis, metadata leakage |
| **TB-03: AI Processing Enclave** | Decapsulation API, LLM inference, Guardrails | **High Trust / Hardened Zone** | Prompt injection, rogue worker nodes, KV cache bleed, container escape |
| **TB-04: Management Zone** | Admin dashboard, audit service, SIEM | **Privileged Governance** | IDOR privilege escalation, audit log tampering, unsigned policy bypass |

---

## 4. Component Analysis & Security Roles

### 4.1 User / Chat Client
- **Role**: Front-end user interface running on Android, iOS, or Web.
- **Security Responsibility**: Client-side cryptography, ephemeral key storage in OS Keystore / Keychain, certificate pinning, and zeroization of plaintext buffers upon UI unmount.

### 4.2 Encryption / Key Management
- **Role**: Cryptographic state management implementing the Double Ratchet Protocol (providing forward secrecy and post-compromise security).
- **Security Responsibility**: Verifying identity keys, rotating ratcheted message keys per message, and preventing replay attacks.

### 4.3 Secure Gateway
- **Role**: Edge ingress reverse proxy.
- **Security Responsibility**: TLS 1.3 termination, IP reputation checking, token-bucket rate limiting, and blocking volumetric SYN / handshake DDoS floods.

### 4.4 Message Relay Server
- **Role**: Asynchronous message broker (e.g., Kafka / NATS / RabbitMQ).
- **Security Responsibility**: Blind routing based solely on public routing tags; packet size padding to uniform boundaries to prevent side-channel traffic analysis.

### 4.5 AI Processing Service & Guardrails
- **Role**: Confidential compute inference worker (AMD SEV-SNP or Intel SGX enclave).
- **Security Responsibility**: Ephemeral memory handling, prompt injection defense, token usage quotas, and isolated KV attention caches.

### 4.6 Logging & Audit Service
- **Role**: Security event tracing and regulatory compliance logging.
- **Security Responsibility**: Storing append-only logs in Write-Once-Read-Many (WORM) storage, cryptographically chaining audit logs with Merkle trees, and strictly redacting any plaintext prompt data.

### 4.7 Administration Interface
- **Role**: Operational portal for security engineers and cluster admins.
- **Security Responsibility**: Enforcing hardware-backed FIDO2 multi-factor authentication, dual-operator approval (four-eyes principle), and strict Attribute-Based Access Control (ABAC).

---

## 5. STRIDE Threat Mapping

| STRIDE Category | Target Components | Vulnerability Pattern | Core Mitigation |
| :--- | :--- | :--- | :--- |
| **Spoofing (S)** | Client, Gateway, AI Worker | Rogue node registration, DNS spoofing, session token theft | mTLS with hardware attestation, cert pinning, SPIFFE identity |
| **Tampering (T)** | Key Exchange, API Layer, AI Inference | DH parameter tampering, header tampering, prompt injection | AEAD integrity tags, dual-LLM guardrails, signed key bundles |
| **Repudiation (R)** | Client, Audit Service, Admin UI | Denying prompt dispatch, deleting audit logs, unsigned config edits | Client digital signing, WORM Merkle logs, FIDO2 action receipts |
| **Information Disclosure (I)**| Relay, Key Storage, AI Memory | Traffic profiling, RAM scraping, KV cache tenant cross-bleed | Uniform packet padding, memory zeroization, enclave isolation |
| **Denial of Service (D)** | Gateway, AI Service, Relay Server | TLS handshake floods, token expansion prompts, buffer overfill | Stateless SYN cookies, token execution timeouts, payload quotas |
| **Elevation of Privilege (E)**| Admin API, Auth Service, API Sandbox | IDOR exploits, JWT algorithm confusion, container escapes | Strict ABAC checks, algorithm pinning, gVisor microVM isolation |

---

## 6. Academic Context (Data Security & Privacy - 22AI73)

This architectural model illustrates that **End-to-End Encryption alone is necessary but not sufficient** when integrating AI models. While transport E2EE protects data in transit, the AI processing enclave becomes the ultimate data boundary. Robust security requires a Defense-in-Depth posture spanning cryptography, confidential compute enclaves, and application-layer AI guardrails.

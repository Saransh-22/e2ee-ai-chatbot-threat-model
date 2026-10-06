"""
Security vs Privacy Conceptual Analysis Engine.
Provides academic analysis explaining that End-to-End Encryption (E2EE) protects data in transit
but does NOT solve every security and privacy challenge in Generative AI systems.
"""

from typing import List, Dict, Any


SECURITY_VS_PRIVACY_TOPICS = [
    {
        "id": "SP-01",
        "topic": "The Endpoint Compromise Fallacy",
        "e2ee_protection": "Protects packets traversing public transit networks against eavesdropping and transit tampering.",
        "limitation": "E2EE provides zero protection if the client device itself is compromised. Key extraction, OS memory scraping, screen capture, or compromised keyboards yield plaintext regardless of cipher strength.",
        "academic_takeaway": "E2EE shifts the threat boundary entirely to the endpoint. Strong hardware keystores (Secure Enclave) and anti-tamper client defenses are non-negotiable prerequisites."
    },
    {
        "id": "SP-02",
        "topic": "The Plaintext Paradox of Server-Side AI Inference",
        "e2ee_protection": "Guarantees intermediate message relays and cloud gateways cannot inspect conversation content.",
        "limitation": "Unlike human-to-human E2EE where only end-users hold keys, an AI chatbot is a computational recipient that must decrypt messages to compute transformer matrix multiplications and attention weights.",
        "academic_takeaway": "Encryption must terminate inside the AI host. The security model depends entirely on Hardware Confidential Computing (AMD SEV-SNP / Intel TDX enclaves) to protect in-memory plaintext from cloud operators and hypervisors."
    },
    {
        "id": "SP-03",
        "topic": "Key Management & Lifecycle Vulnerabilities",
        "e2ee_protection": "Ensures that encrypted packets require mathematically derived session keys for decipherment.",
        "limitation": "Cryptographic security is only as strong as key agreement (ECDH), public-key distribution (identity verification), and key destruction (zeroization). Intercepted prekeys or poorly seeded RNGs undermine the entire scheme.",
        "academic_takeaway": "Robust forward secrecy and post-compromise security require protocols like the Double Ratchet (Signal protocol) and immediate volatile memory zeroization (`mlock`)."
    },
    {
        "id": "SP-04",
        "topic": "Metadata Exposure & Side-Channel Traffic Analysis",
        "e2ee_protection": "Hides message payload plaintext from eavesdroppers.",
        "limitation": "E2EE ciphertext envelopes still reveal communication metadata: sender/recipient endpoints, message frequency, packet burst durations, and payload sizes. LLM responses have distinctive token size profiles.",
        "academic_takeaway": "Confidentiality of content does not equal confidentiality of communication patterns. Defenses require uniform packet padding (PKCS#7 to 4KB blocks) and decoy (chaff) traffic injection."
    },
    {
        "id": "SP-05",
        "topic": "Audit Logging vs. Privacy Conflicts",
        "e2ee_protection": "Guarantees user messages are kept strictly private.",
        "limitation": "Operational debugging, compliance reporting, and threat detection require forensic logs. If application crashes write decrypted stack traces or prompt buffers to central logs, privacy is breached at the audit layer.",
        "academic_takeaway": "Requires Privacy-by-Design logging: append-only WORM Merkle logs for routing events combined with automated scrubbing and zero-plaintext storage policies."
    },
    {
        "id": "SP-06",
        "topic": "The Authentication vs. Confidentiality Gap",
        "e2ee_protection": "Ensures only holders of the private key can decrypt messages.",
        "limitation": "Encryption without rigorous entity authentication (mTLS / device attestation) simply creates an unbreakable encrypted tunnel to an unverified or rogue actor (man-in-the-middle).",
        "academic_takeaway": "Confidentiality and Authenticity are orthogonal properties. E2EE must be coupled with hardware-backed client identity attestation and short-lived signed tokens."
    },
    {
        "id": "SP-07",
        "topic": "Authorization & Enclave Privilege Boundaries",
        "e2ee_protection": "Protects against unauthorized data reading in flight.",
        "limitation": "Once decrypted inside the enclave, the payload must be processed by microservices. Inadequate internal authorization allows low-privilege components to read confidential tenant state.",
        "academic_takeaway": "Defense-in-depth requires microVM sandboxing (gVisor) and Attribute-Based Access Control (ABAC) even within trusted backend environments."
    },
    {
        "id": "SP-08",
        "topic": "AI Service Trust & Model Behavioral Integrity",
        "e2ee_protection": "Guarantees prompts reach the AI model without in-flight modification.",
        "limitation": "E2EE does nothing to protect against what is INSIDE the message. Adversaries can send encrypted prompt injection attacks or jailbreaks that subvert model alignment and trigger data leaks.",
        "academic_takeaway": "Transport cryptography guarantees message integrity, not semantic safety. AI architectures require in-enclave input/output guardrail models."
    },
    {
        "id": "SP-09",
        "topic": "Data Minimization in Generative AI Systems",
        "e2ee_protection": "Protects user data against transit interception.",
        "limitation": "Chatbots retain memory through transformer KV attention caches and multi-turn conversational context windows. Storing residual context across sessions compromises long-term user privacy.",
        "academic_takeaway": "E2EE must be complemented by strict data minimization: per-turn attention cache flushing, ephemeral tenant context lifecycles, and no model fine-tuning on user chat streams."
    }
]


class SecurityPrivacyEngine:
    """
    Manages conceptual security vs. privacy discussions and education.
    """

    @staticmethod
    def get_all_topics() -> List[Dict[str, Any]]:
        """Returns all 9 core security vs privacy analytical dimensions."""
        return list(SECURITY_VS_PRIVACY_TOPICS)

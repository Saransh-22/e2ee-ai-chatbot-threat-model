"""
Data Flow Analysis Engine for E2EE AI Chatbot.
Models each major architectural data flow (F1 to F6) with data types, protection mechanisms,
trust boundary crossings, and mapped STRIDE threats.
"""

from typing import List, Dict, Any


DATA_FLOWS_DATA = [
    {
        "flow_id": "F1",
        "name": "User → Chat Client",
        "source": "End User (Human Principal)",
        "destination": "Chat Client Application (Mobile / Desktop)",
        "data_payload": "Cleartext user prompt query, authentication credentials, and local keystore interaction commands.",
        "protection_mechanism": "Client OS memory isolation, biometric/PIN access control, Secure Enclave / Keystore protection, and volatile RAM buffer zeroization (`mlock`).",
        "trust_boundary": "Crosses into [TB-01: User Client Trust Boundary] from untrusted physical environment.",
        "trust_boundary_desc": "Untrusted physical world to client device execution space.",
        "relevant_threats": [
            {"id": "THR-001", "name": "Client Identity Impersonation", "category": "Spoofing"},
            {"id": "THR-008", "name": "Denial of Malicious Message Dispatch", "category": "Repudiation"},
            {"id": "THR-011", "name": "Client-Side Ephemeral Key Memory Extraction", "category": "Information Disclosure"}
        ]
    },
    {
        "flow_id": "F2",
        "name": "Chat Client → Secure Gateway",
        "source": "Chat Client Application",
        "destination": "Secure Gateway (Ingress Reverse Proxy / WAF)",
        "data_payload": "End-to-end encrypted prompt payload wrapped in outer transport envelope with signed JWT auth token and session routing headers.",
        "protection_mechanism": "Dual-layer cryptography: Inner payload encrypted with AES-256-GCM (Double Ratchet session key); outer transport protected via TLS 1.3 with certificate pinning.",
        "trust_boundary": "Crosses from [TB-01: Client Trust Zone] across untrusted Public Internet into [TB-02: Perimeter & Relay DMZ].",
        "trust_boundary_desc": "Edge device to cloud perimeter over untrusted transit network.",
        "relevant_threats": [
            {"id": "THR-003", "name": "Gateway DNS Spoofing & TLS Interception", "category": "Spoofing"},
            {"id": "THR-013", "name": "Asymmetric TLS & Handshake Exhaustion Attack", "category": "Denial of Service"},
            {"id": "THR-017", "name": "JWT Algorithm Confusion & Role Escalation", "category": "Elevation of Privilege"}
        ]
    },
    {
        "flow_id": "F3",
        "name": "Gateway → Message Relay",
        "source": "Secure Gateway",
        "destination": "Message Relay Server (Zero-Knowledge Message Broker)",
        "data_payload": "Authenticated ciphertext blob with stripped transport headers, preserving only anonymous session queue routing identifiers.",
        "protection_mechanism": "Internal mutual TLS (mTLS), zero-knowledge routing (relay has zero access to message decryption keys), and uniform 4KB packet padding.",
        "trust_boundary": "Operates within [TB-02: Perimeter & Relay DMZ] across isolated perimeter VLAN.",
        "trust_boundary_desc": "Ingress reverse proxy to internal message broker queues.",
        "relevant_threats": [
            {"id": "THR-010", "name": "Traffic Analysis & Message Size Profiling", "category": "Information Disclosure"},
            {"id": "THR-015", "name": "Relay Buffer Overfill with Bogus Ciphertext Blobs", "category": "Denial of Service"}
        ]
    },
    {
        "flow_id": "F4",
        "name": "Message Relay → AI Service",
        "source": "Message Relay Server",
        "destination": "AI Processing Service (Confidential Inference Enclave)",
        "data_payload": "Enqueued ciphertext message blob dequeued for in-enclave decapsulation, verification, and inference processing.",
        "protection_mechanism": "Service mesh mutual authentication (SPIFFE/mTLS), AMD SEV-SNP hardware-encrypted RAM enclave, and ratcheted symmetric key derivation inside enclave.",
        "trust_boundary": "Crosses from [TB-02: Perimeter & Relay DMZ] into [TB-03: Secure AI Processing Enclave].",
        "trust_boundary_desc": "Untrusted message queue to hardware-hardened confidential compute enclave.",
        "relevant_threats": [
            {"id": "THR-002", "name": "Rogue AI Inference Node Registration", "category": "Spoofing"},
            {"id": "THR-004", "name": "Ephemeral Key Exchange Manipulation", "category": "Tampering"},
            {"id": "THR-005", "name": "Encrypted Message Envelope Header Modification", "category": "Tampering"},
            {"id": "THR-006", "name": "Indirect Prompt Injection & Context Manipulation", "category": "Tampering"},
            {"id": "THR-018", "name": "AI Inference Worker Container Escape", "category": "Elevation of Privilege"}
        ]
    },
    {
        "flow_id": "F5",
        "name": "AI Service → Response Handler",
        "source": "AI Processing Service (LLM Engine & Output Guardrail)",
        "destination": "Response Encryption Handler (In-Enclave Cryptographic Engine)",
        "data_payload": "Raw generated response tokens screened by Data Loss Prevention (DLP) output safety filters, ready for cryptographic wrapping.",
        "protection_mechanism": "In-memory zero-copy token transfer, strict KV cache flushing, prompt boundary token isolation, and symmetric Double Ratchet re-encryption.",
        "trust_boundary": "Confined strictly within [TB-03: Secure AI Processing Enclave] memory space.",
        "trust_boundary_desc": "Inference worker to response encryption engine within the confidential compute boundary.",
        "relevant_threats": [
            {"id": "THR-012", "name": "Cross-Session AI KV Cache & Memory Leakage", "category": "Information Disclosure"},
            {"id": "THR-014", "name": "Algorithmic Complexity & Token Expansion Attack", "category": "Denial of Service"}
        ]
    },
    {
        "flow_id": "F6",
        "name": "Response Handler → User",
        "source": "Response Encryption Handler (via Relay & Gateway)",
        "destination": "End User / Chat Client Application UI",
        "data_payload": "Re-encrypted response ciphertext package pushed back to client over websocket/HTTP connection, decrypted into local UI display.",
        "protection_mechanism": "AEAD ciphertext integrity tag verification, client-side Double Ratchet ratchet progression, ephemeral key destruction, and encrypted local view rendering.",
        "trust_boundary": "Crosses from [TB-03: AI Enclave] $\\rightarrow$ [TB-02: DMZ] $\\rightarrow$ Public Internet $\\rightarrow$ [TB-01: Client Trust Zone].",
        "trust_boundary_desc": "Enclave return channel across transit relays back to end-user device.",
        "relevant_threats": [
            {"id": "THR-001", "name": "Client Identity Impersonation", "category": "Spoofing"},
            {"id": "THR-007", "name": "Audit Trail Erasure by Privileged Operator", "category": "Repudiation"},
            {"id": "THR-010", "name": "Traffic Analysis & Message Size Profiling", "category": "Information Disclosure"}
        ]
    }
]


class DataFlowEngine:
    """
    Manages data flow definitions and analysis.
    """

    @staticmethod
    def get_all_flows() -> List[Dict[str, Any]]:
        """Returns all 6 major architectural data flows."""
        return list(DATA_FLOWS_DATA)

    @staticmethod
    def get_flow_by_id(flow_id: str) -> Dict[str, Any]:
        """Returns specific flow by ID (e.g. F1, F2)."""
        for f in DATA_FLOWS_DATA:
            if f["flow_id"].upper() == flow_id.upper():
                return dict(f)
        return {}

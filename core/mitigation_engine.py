"""
Mitigation Engine for E2EE AI Chatbot Threat Modeling.
Maps STRIDE threats to security controls, architectural defenses, mitigation categories, and residual risk calculations.
"""

from typing import List, Dict, Any
from core.risk_engine import calculate_risk


# Standard security properties associated with STRIDE
STRIDE_PROPERTY_MAPPING = {
    "Spoofing": {"property": "Authenticity", "controls": "Mutual Authentication (mTLS), Hardware Keystores, Cryptographic Tokens"},
    "Tampering": {"property": "Integrity", "controls": "AEAD Encryption, Digital Signatures, Input Validation, Guardrails"},
    "Repudiation": {"property": "Non-Repudiation", "controls": "WORM Audit Logs, Merkle Trees, Cryptographic Receipts"},
    "Information Disclosure": {"property": "Confidentiality", "controls": "E2E Encryption (Double Ratchet), Memory Zeroization, Traffic Padding"},
    "Denial of Service": {"property": "Availability", "controls": "Rate Limiting, Handshake Cookies, Token Inference Timeouts"},
    "Elevation of Privilege": {"property": "Authorization", "controls": "Role/Attribute Access Control (RBAC/ABAC), MicroVM Sandboxing"}
}

# The 9 core mitigation categories required by academic standard
MITIGATION_CATEGORIES = [
    "Authentication",
    "Authorization",
    "Confidentiality",
    "Integrity",
    "Availability",
    "Accountability",
    "Key Management",
    "Logging",
    "Data Minimization"
]

MITIGATION_CATEGORY_DESCRIPTIONS = {
    "Authentication": {
        "title": "Authentication Controls",
        "objective": "Verify the claimed identity of users, edge devices, and worker nodes before granting communication or processing rights.",
        "core_mechanisms": "Hardware-backed Keystores (Android Keystore / iOS Secure Enclave), SPIFFE/SPIRE Service Mesh Identity, mTLS, Certificate Pinning."
    },
    "Authorization": {
        "title": "Authorization & Access Controls",
        "objective": "Restrict authenticated principals and processes to the minimum necessary actions and objects (Principle of Least Privilege).",
        "core_mechanisms": "Attribute-Based Access Control (ABAC), Role-Based Access Control (RBAC), MicroVM sandboxing (gVisor), and strict JWT algorithm pinning."
    },
    "Confidentiality": {
        "title": "Confidentiality & Isolation Controls",
        "objective": "Protect plaintext conversational content and AI internal representations against unauthorized disclosure.",
        "core_mechanisms": "Hardware-enforced Confidential Enclaves (AMD SEV-SNP), tenant GPU memory isolation, and per-turn KV attention cache zero-flushing."
    },
    "Integrity": {
        "title": "Integrity & Anti-Tampering Controls",
        "objective": "Guarantee that ciphertext envelopes, routing headers, and prompt semantics remain unaltered during transit and inference.",
        "core_mechanisms": "Authenticated Encryption with Associated Data (AEAD - AES-256-GCM), dual-LLM guardrail sanitizers, and strict structural delimiter framing."
    },
    "Availability": {
        "title": "Availability & Resource Protection",
        "objective": "Ensure continuous system responsiveness against volumetric connection flooding and algorithmic complexity exhaustion.",
        "core_mechanisms": "Stateless SYN cookies, edge eBPF XDP rate limiting, token generation execution quotas, and leaky-bucket queue backpressure."
    },
    "Accountability": {
        "title": "Accountability & Non-Repudiation",
        "objective": "Provide indisputable cryptographic proof of message dispatch and administrative operations.",
        "core_mechanisms": "Client-side private key digital signatures, monotonic sequence counters, and FIDO2-signed dual-custody administrative manifests."
    },
    "Key Management": {
        "title": "Key Management Lifecycle",
        "objective": "Govern generation, negotiation, ephemeral rotation, and zeroization of cryptographic keying material.",
        "core_mechanisms": "Double Ratchet Protocol, Extended Triple Diffie-Hellman (X3DH), ephemeral key zeroization (`mlock`), and out-of-band safety number fingerprints."
    },
    "Logging": {
        "title": "Security Logging & Auditability",
        "objective": "Record security-relevant events without compromising conversational privacy or storing sensitive keys.",
        "core_mechanisms": "Write-Once-Read-Many (WORM) cloud object storage, Merkle tree cryptographic audit chains, and strict Privacy-by-Design log masking."
    },
    "Data Minimization": {
        "title": "Data Minimization & Traffic Obfuscation",
        "objective": "Prevent side-channel intelligence gathering through statistical metadata and payload size profiling.",
        "core_mechanisms": "Uniform PKCS#7 packet padding to fixed 4KB blocks, dummy packet injection (chaff traffic), and ephemeral session retention."
    }
}

# Component-specific standard defense recommendations
COMPONENT_DEFENSES = {
    "User / Chat Client": [
        "Secure Enclave / Keystore protection for private identity keys",
        "Anti-tamper checks, memory protection (`mlock`), and certificate pinning",
        "Mandatory multi-factor authentication (MFA) & biometrics"
    ],
    "Identity & Authentication": [
        "Algorithm-pinned JWT / PASETO with RS256/Ed25519 asymmetric signatures",
        "Short-lived session credentials with cryptographically bound device identifiers",
        "Automated revocation checking via Redis cache / CRLs"
    ],
    "Encryption / Key Management": [
        "Double Ratchet Protocol (Signal standard) with pre-key bundles (X3DH)",
        "Zeroization of session keys immediately after ciphertext decrypt/encrypt",
        "Out-of-band safety number fingerprint verification"
    ],
    "Secure Gateway": [
        "Strict TLS 1.3 only, disabling outdated cipher suites",
        "Stateless SYN-proxy, eBPF DDoS mitigation, and ingress rate limiting",
        "Reverse proxy perimeter with Web Application Firewall (WAF)"
    ],
    "Message Relay Server": [
        "Zero-knowledge routing: relay only inspects outer envelope routing tags",
        "Constant-size ciphertext packet padding (e.g., PKCS#7 to 4KB blocks) to stop traffic analysis",
        "Leaky-bucket queuing with ephemeral retention"
    ],
    "AI Processing Service": [
        "Dual LLM architecture: dedicated Input Filter and Output Guardrail models",
        "Confidential Computing (Trusted Execution Environment / AMD SEV-SNP enclaves)",
        "Strict per-inference context isolation and KV cache zero-flush",
        "Prompt boundary framing with randomized boundary tokens"
    ],
    "API Layer": [
        "Authenticated Encryption with Associated Data (AEAD - AES-GCM-256)",
        "MicroVM sandboxing (gVisor/Firecracker) for code execution components",
        "Strict schema validation on JSON payloads"
    ],
    "Logging / Audit Service": [
        "Write-Once-Read-Many (WORM) cloud object storage with retention locks",
        "Cryptographic Merkle tree hashing to guarantee tamper evidence",
        "Zero logging of plaintext prompts or cryptographic keys (Privacy-by-Design)"
    ],
    "Administration Interface": [
        "Hardware-enforced FIDO2/WebAuthn MFA for all administrator logins",
        "Four-eyes principle (dual authorization) for security-sensitive policy changes",
        "Separation of management plane from data plane network"
    ]
}


class MitigationEngine:
    """
    Analyzes threat mitigations, implementation status, and residual risk posture.
    """

    @staticmethod
    def get_stride_meta(category: str) -> Dict[str, str]:
        """Returns security property and high-level control recommendations for a STRIDE category."""
        return STRIDE_PROPERTY_MAPPING.get(
            category,
            {"property": "General Security", "controls": "Standard Defensive Hardening"}
        )

    @staticmethod
    def get_component_defenses(component: str) -> List[str]:
        """Returns baseline defense recommendations for a given architecture component."""
        return COMPONENT_DEFENSES.get(component, ["Implement defense-in-depth and principle of least privilege."])

    @staticmethod
    def get_mitigation_category_meta(category: str) -> Dict[str, str]:
        """Returns metadata and objectives for a mitigation control category."""
        return MITIGATION_CATEGORY_DESCRIPTIONS.get(
            category,
            {
                "title": f"{category} Controls",
                "objective": "Standard security control implementation.",
                "core_mechanisms": "Defense-in-depth hardening."
            }
        )

    @staticmethod
    def group_threats_by_category(threats: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups threats into the 9 formal mitigation categories.
        """
        grouped = {cat: [] for cat in MITIGATION_CATEGORIES}
        for t in threats:
            cat = t.get("mitigation_category", "Integrity")
            if cat in grouped:
                grouped[cat].append(t)
            else:
                grouped.setdefault(cat, []).append(t)
        return grouped

    @staticmethod
    def calculate_mitigation_posture(threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates implementation statistics across threats.
        """
        total = len(threats)
        if total == 0:
            return {
                "total": 0,
                "mitigated": 0,
                "in_progress": 0,
                "under_review": 0,
                "identified": 0,
                "completion_rate": 0.0
            }

        counts = {
            "Mitigated": 0,
            "In Progress": 0,
            "Under Review": 0,
            "Identified": 0
        }

        for t in threats:
            st = t.get("status", "Identified")
            if st in counts:
                counts[st] += 1
            else:
                counts["Identified"] += 1

        completion_rate = round((counts["Mitigated"] / total) * 100, 1)

        return {
            "total": total,
            "mitigated": counts["Mitigated"],
            "in_progress": counts["In Progress"],
            "under_review": counts["Under Review"],
            "identified": counts["Identified"],
            "completion_rate": completion_rate
        }

    @staticmethod
    def compute_residual_risk(threat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimates residual risk after applying controls based on threat status:
        - Mitigated: Likelihood decreases by 2 (min 1), Impact decreases by 1 (min 1)
        - In Progress: Likelihood decreases by 1 (min 1)
        - Under Review / Identified: Unchanged
        """
        orig_l = threat.get("likelihood", 1)
        orig_i = threat.get("impact", 1)
        status = threat.get("status", "Identified")

        if status == "Mitigated":
            res_l = max(1, orig_l - 2)
            res_i = max(1, orig_i - 1)
        elif status == "In Progress":
            res_l = max(1, orig_l - 1)
            res_i = orig_i
        else:
            res_l = orig_l
            res_i = orig_i

        orig_calc = calculate_risk(orig_l, orig_i)
        res_calc = calculate_risk(res_l, res_i)

        return {
            "initial_score": orig_calc["risk_score"],
            "initial_level": orig_calc["risk_level"],
            "residual_likelihood": res_l,
            "residual_impact": res_i,
            "residual_score": res_calc["risk_score"],
            "residual_level": res_calc["risk_level"],
            "risk_reduction_pct": round(
                ((orig_calc["risk_score"] - res_calc["risk_score"]) / orig_calc["risk_score"]) * 100, 1
            )
        }

    @staticmethod
    def get_mitigation_matrix(threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Builds formal mitigation traceability matrix:
        Threat ID, Threat Name, STRIDE Category, Security Control, Security Property, Reason/Explanation.
        """
        matrix = []
        for t in threats:
            matrix.append({
                "id": t.get("id"),
                "threat_name": t.get("threat_name"),
                "stride_category": t.get("stride_category"),
                "security_control": t.get("security_control", t.get("mitigation")),
                "security_property": t.get("security_property", "Integrity"),
                "mitigation_category": t.get("mitigation_category", "Integrity"),
                "reason": t.get("mitigation_reason", "Neutralizes attack vector and ensures operational resilience."),
                "status": t.get("status", "Identified")
            })
        return matrix

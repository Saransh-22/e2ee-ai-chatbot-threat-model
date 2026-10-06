"""
E2EE AI Chatbot Threat Modeling & Risk Analyzer
College Micro-Project: Data Security and Privacy (22AI73)
Student: Saransh Neema | USN: 1DS23AI048 | 7th Semester B.E.
"""

import os
import sys
import subprocess
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.threat_engine import (
    ThreatEngine,
    STRIDE_CATEGORIES,
    SECURITY_PROPERTIES
)
from core.risk_engine import calculate_risk, RISK_LEVEL_COLORS, get_risk_summary
from core.mitigation_engine import (
    MitigationEngine,
    MITIGATION_CATEGORIES,
    MITIGATION_CATEGORY_DESCRIPTIONS,
    COMPONENT_DEFENSES
)
from core.asset_inventory import AssetInventoryEngine
from core.data_flow_engine import DataFlowEngine
from core.security_privacy_engine import SecurityPrivacyEngine


# Configure Streamlit Page
st.set_page_config(
    page_title="E2EE AI Chatbot Threat Modeler",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished academic appearance
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.4rem;
    }
    .kpi-card {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .kpi-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #475569;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .badge-critical {
        background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem;
    }
    .badge-high {
        background-color: #fd7e14; color: white; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem;
    }
    .badge-medium {
        background-color: #ffc107; color: #212529; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem;
    }
    .badge-low {
        background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem;
    }
    .security-callout {
        background-color: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 15px 0;
        color: #1e3a8a;
    }
    .academic-step {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_threat_engine():
    """Cached loader for ThreatEngine."""
    return ThreatEngine()


engine = get_threat_engine()
all_threats = engine.get_all_threats()
summary = get_risk_summary(all_threats)
model_summary = engine.get_threat_model_summary()
posture = MitigationEngine.calculate_mitigation_posture(all_threats)


# Sidebar Header & Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=60)
    st.markdown("### E2EE AI Chatbot Security")
    st.caption("Threat Modeler & Risk Analyzer")
    
    st.markdown("---")
    nav_selection = st.radio(
        "Navigation Menu",
        [
            "📊 Dashboard",
            "🏛️ System Architecture",
            "🔀 Data Flow Analysis",
            "🗄️ Security Asset Inventory",
            "🛡️ STRIDE Threat Model",
            "📈 Risk Analysis",
            "🔐 Mitigation Controls",
            "⚖️ Security vs. Privacy",
            "🎓 Academic Mapping",
            "🧪 Testing & Verification",
            "ℹ️ About Project"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("**Academic Information**")
    st.text("USN: 1DS23AI048")
    st.text("Student: Saransh Neema")
    st.text("Course: DSP (22AI73)")
    st.text("Semester: VII (AI & DS)")
    st.caption("College Micro-Project Prototype")


# ==============================================================================
# 1. DASHBOARD PAGE
# ==============================================================================
if nav_selection == "📊 Dashboard":
    st.markdown('<div class="main-title">E2EE AI Chatbot Threat Modeling Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Quantitative Security &amp; Risk Overview for Synthetic Chatbot Architecture</div>', unsafe_allow_html=True)

    # 7 Core KPI Cards
    k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Threats</div>
            <div class="kpi-value">{summary['total_threats']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Critical</div>
            <div class="kpi-value" style="color: #dc3545;">{summary['critical_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">High</div>
            <div class="kpi-value" style="color: #fd7e14;">{summary['high_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Medium</div>
            <div class="kpi-value" style="color: #d97706;">{summary['medium_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Low</div>
            <div class="kpi-value" style="color: #28a745;">{summary['low_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">STRIDE Classes</div>
            <div class="kpi-value" style="color: #2563eb;">{len(engine.get_categories())}</div>
        </div>
        """, unsafe_allow_html=True)
    with k7:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Components</div>
            <div class="kpi-value" style="color: #7c3aed;">{len(engine.get_components())}</div>
        </div>
        """, unsafe_allow_html=True)

    # Short Security Summary Callout
    st.markdown(f"""
    <div class="security-callout">
        <b>Security Posture Summary:</b> The synthetic architecture currently models <b>{summary['total_threats']} threats</b> across <b>{len(engine.get_components())} components</b>.
        <b>Critical risks ({summary['critical_count']})</b> require immediate mitigation because their calculated risk score is 16 or higher, presenting direct threats to model integrity and host boundary isolation. 
        <b>High risks ({summary['high_count']})</b> demand prioritized cryptographic and memory controls. Current mitigation implementation rate stands at <b>{posture['completion_rate']}%</b>.
    </div>
    """, unsafe_allow_html=True)

    # Charts Row 1: STRIDE Distribution & Risk Level Breakdown
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Threats by STRIDE Category")
        stride_counts = engine.get_distribution_by_stride()
        df_stride = pd.DataFrame(list(stride_counts.items()), columns=["STRIDE Category", "Threat Count"])
        fig_stride = px.bar(
            df_stride,
            x="STRIDE Category",
            y="Threat Count",
            color="STRIDE Category",
            text="Threat Count",
            color_discrete_sequence=px.colors.qualitative.Safe,
            title="Balanced Distribution Across STRIDE Categories (4 per Category)"
        )
        fig_stride.update_layout(showlegend=False, xaxis_title="", yaxis_title="Number of Threats")
        st.plotly_chart(fig_stride, use_container_width=True)

    with c2:
        st.subheader("2. Threats by Risk Level")
        risk_counts = summary["counts_by_level"]
        df_risk = pd.DataFrame(list(risk_counts.items()), columns=["Risk Level", "Count"])
        fig_risk = px.pie(
            df_risk,
            names="Risk Level",
            values="Count",
            color="Risk Level",
            color_discrete_map=RISK_LEVEL_COLORS,
            hole=0.45,
            title="Distribution by Risk Level (Likelihood × Impact)"
        )
        fig_risk.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_risk, use_container_width=True)

    # Chart 3: Threats by Component
    st.subheader("3. Threats by Architecture Component")
    comp_counts = engine.get_distribution_by_component()
    df_comp = pd.DataFrame(list(comp_counts.items()), columns=["Component", "Threat Count"]).sort_values(by="Threat Count", ascending=True)
    fig_comp = px.bar(
        df_comp,
        x="Threat Count",
        y="Component",
        orientation="h",
        color="Threat Count",
        color_continuous_scale="Blues",
        text="Threat Count",
        title="Threat Density Across Chatbot Components"
    )
    fig_comp.update_layout(xaxis_title="Number of Identified Threats", yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    # Automatically Generated Threat Model Summary Block
    st.markdown("---")
    st.subheader("📋 Automatically Generated Threat Model Summary")
    sum1, sum2 = st.columns(2)
    with sum1:
        st.markdown("#### Most Frequently Affected Assets")
        df_top_assets = pd.DataFrame(model_summary["top_affected_assets"], columns=["Protected Asset", "Threat Count"])
        st.dataframe(df_top_assets, use_container_width=True, hide_index=True)

        st.markdown("#### Most Frequently Recommended Security Controls")
        df_top_ctrls = pd.DataFrame(model_summary["top_recommended_controls"], columns=["Security Control", "Frequency"])
        st.dataframe(df_top_ctrls, use_container_width=True, hide_index=True)

    with sum2:
        st.markdown("#### Highest Calculated Risks (Top 5 Priority)")
        df_top_risks = pd.DataFrame([
            {
                "ID": t["id"],
                "Threat Name": t["threat_name"],
                "STRIDE": t["stride_category"],
                "Risk Score": t["risk_score"],
                "Risk Level": t["risk_level"]
            }
            for t in model_summary["highest_risks"]
        ])
        st.dataframe(df_top_risks, use_container_width=True, hide_index=True)

        st.markdown("#### Distribution by Security Property")
        prop_dist = engine.get_distribution_by_security_property()
        df_prop = pd.DataFrame(list(prop_dist.items()), columns=["Security Property", "Threats"])
        st.dataframe(df_prop, use_container_width=True, hide_index=True)


# ==============================================================================
# 2. SYSTEM ARCHITECTURE PAGE
# ==============================================================================
elif nav_selection == "🏛️ System Architecture":
    st.markdown('<div class="main-title">System Architecture &amp; Trust Boundaries</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">End-to-End Encrypted AI Chatbot Component Topology &amp; Attack Surfaces</div>', unsafe_allow_html=True)

    st.subheader("Component Flow Sequence")
    st.info("""
    **Core Pipeline Flow:**  
    `User` ➔ `Chat Client` ➔ `Authentication` ➔ `Encryption / Key Management` ➔ `Secure Gateway` ➔ `Message Relay` ➔ `AI Processing Service` ➔ `Response Encryption` ➔ `User`
    """)

    # Interactive tabs for visual diagram and component roles
    tab_diagram, tab_components, tab_surface, tab_drawio = st.tabs([
        "📊 Architecture Diagram (Mermaid)",
        "🧩 Component Breakdown",
        "🎯 Potential Attack Surface",
        "📥 Editable Draw.io File"
    ])

    with tab_diagram:
        st.subheader("Interactive Architectural Blueprint")
        st.markdown("""
```mermaid
graph TD
    subgraph TB01 ["TB-01: User Client Zone (Untrusted Device)"]
        User(["👤 User"])
        Client["📱 Chat Client"]
        KeyMgmt["🔑 Encryption / Key Management (Hardware Keystore)"]
    end

    subgraph TB02 ["TB-02: Perimeter & Relay DMZ (Untrusted Transit)"]
        Auth["🪪 Identity & Authentication (JWT/OAuth2)"]
        Gateway["🛡️ Secure Gateway (TLS 1.3 / Ingress WAF)"]
        Relay["📬 Message Relay Server (Zero-Knowledge Broker)"]
    end

    subgraph TB03 ["TB-03: Secure AI Enclave (Confidential Compute)"]
        APILayer["🔌 API Layer & Decapsulator"]
        InputGuard["🛡️ Input Prompt Guardrail"]
        AIService["🧠 AI Processing Service (LLM Engine)"]
        OutputGuard["🛡️ Output Safety & DLP Guardrail"]
        RespEnc["🔐 Response Encryption Engine"]
    end

    subgraph TB04 ["TB-04: Management Zone"]
        Admin["⚙️ Admin Interface (FIDO2 MFA)"]
        Audit["📜 Logging / Audit Service (WORM Merkle Tree)"]
    end

    User -->|1. Types Prompt| Client
    Client -->|2. Key Agreement| KeyMgmt
    Client -->|3. Session Request| Auth
    KeyMgmt -->|4. AEAD Ciphertext| Gateway
    Gateway -->|5. Blind Transit| Relay
    Relay -->|6. Enqueue Ciphertext| APILayer
    APILayer -->|7. Decrypted Plaintext| InputGuard
    InputGuard -->|8. Filtered Tokens| AIService
    AIService -->|9. Generated Tokens| OutputGuard
    OutputGuard -->|10. Inspected Response| RespEnc
    RespEnc -->|11. Re-encrypted Ciphertext| Relay
    Relay -->|12. Push Response| Client
    Client -->|13. Decrypt & Render| User

    Gateway -.->|Audit Trails| Audit
    APILayer -.->|Inference Logs| Audit
    Admin -.->|Signed Policies| Gateway
```
        """)

    with tab_components:
        st.subheader("Component Roles & Responsibilities")
        components_info = [
            ("User", "The human interacting with the chatbot.", "Provides prompts and receives generated responses via UI."),
            ("Chat Client", "Front-end mobile/web/desktop application.", "Renders UI, handles local memory buffers, zeroizes plaintext RAM, and pins gateway certificates."),
            ("Identity & Authentication", "Centralized auth service (OAuth2 / PASETO / JWT).", "Validates user credentials, issues cryptographically signed RS256 tokens, and manages device attestation."),
            ("Encryption / Key Management", "Cryptographic state engine (Double Ratchet Protocol).", "Generates ephemeral ECDH keys, rotates ratcheted symmetric keys, and securely stores keys in hardware keystores."),
            ("Secure Gateway", "Perimeter reverse proxy and WAF.", "Terminates public TLS 1.3, executes stateless SYN-cookie DDoS rate limiting, and forwards opaque ciphertext."),
            ("Message Relay Server", "Zero-knowledge asynchronous message broker.", "Dispatches and routes encrypted message packets using public routing headers without holding decryption keys."),
            ("API Layer", "Internal ingress decapsulation point.", "Authenticates inner AEAD tags, enforces rate quotas, and decapsulates ciphertext envelopes within protected enclave memory."),
            ("AI Processing Service", "Confidential compute LLM engine (AMD SEV-SNP enclave).", "Runs neural network inference, applies input prompt injection filters, and purges attention KV caches per turn."),
            ("Response Encryption", "In-enclave symmetric re-encryption module.", "Wraps generated response tokens using the client's ratcheted session key before egress to the relay."),
            ("Logging / Audit Service", "Tamper-evident audit store (WORM / Merkle trees).", "Records administrative and security events without recording cleartext conversational prompts (Privacy-by-Design)."),
            ("Administration Interface", "Governance portal for platform operators.", "Enforces dual-operator authorization (four-eyes principle), FIDO2 hardware MFA, and Attribute-Based Access Control.")
        ]
        for name, role, details in components_info:
            with st.expander(f"📌 **{name}** — {role}"):
                st.write(details)

    with tab_surface:
        st.subheader("🎯 Potential Attack Surface Breakdown")
        st.write("Each component introduces specific threat exposures that must be accounted for in the threat model:")
        
        surface_table = [
            {"Component": "User / Chat Client", "Trust Boundary": "TB-01 Client", "Attack Surfaces": "Physical device theft, side-loaded malware, debugger RAM scraping, local cache extraction."},
            {"Component": "Identity & Authentication", "Trust Boundary": "TB-02 Perimeter", "Attack Surfaces": "JWT signature confusion (alg: none / HS256), token replay, brute force login."},
            {"Component": "Encryption / Key Management", "Trust Boundary": "TB-01 / TB-03", "Attack Surfaces": "Diffie-Hellman downgrade, weak RNG seeds, key reuse, unpinned RAM key leaks."},
            {"Component": "Secure Gateway", "Trust Boundary": "TB-02 Perimeter", "Attack Surfaces": "TLS handshake flooding, slowloris DoS, DNS spoofing, proxy header injection."},
            {"Component": "Message Relay Server", "Trust Boundary": "TB-02 Perimeter", "Attack Surfaces": "Traffic volume/size analysis, buffer overflow with bogus blobs, queue starvation."},
            {"Component": "API Layer", "Trust Boundary": "TB-03 AI Enclave", "Attack Surfaces": "Envelope tampering, unvalidated payload headers, container escapes, microVM breakouts."},
            {"Component": "AI Processing Service", "Trust Boundary": "TB-03 AI Enclave", "Attack Surfaces": "Prompt injection, jailbreaks, KV attention cache tenant leaks, algorithmic token exhaustion."},
            {"Component": "Response Encryption", "Trust Boundary": "TB-03 AI Enclave", "Attack Surfaces": "Nonce reuse in AEAD ciphers, key desynchronization with client ratchet."},
            {"Component": "Logging / Audit Service", "Trust Boundary": "TB-04 Management", "Attack Surfaces": "Privileged log deletion, log injection, sensitive data leakage into logs."},
            {"Component": "Administration Interface", "Trust Boundary": "TB-04 Management", "Attack Surfaces": "Insecure Direct Object References (IDOR), session hijacking, unsigned policy overrides."}
        ]
        st.dataframe(pd.DataFrame(surface_table), use_container_width=True, hide_index=True)

    with tab_drawio:
        st.subheader("Download Editable Draw.io Diagrams (diagrams.net)")
        st.write("Two formal editable Draw.io XML diagrams are provided for your college project documentation and report:")

        dc1, dc2 = st.columns(2)
        with dc1:
            st.markdown("#### 1. System Architecture & Trust Boundaries")
            drawio_path1 = os.path.join(ROOT_DIR, "diagrams", "architecture.drawio")
            if os.path.exists(drawio_path1):
                with open(drawio_path1, "r", encoding="utf-8") as f1:
                    content1 = f1.read()
                st.download_button(
                    label="📥 Download architecture.drawio",
                    data=content1,
                    file_name="e2ee_ai_chatbot_architecture.drawio",
                    mime="application/xml",
                    key="dl_arch"
                )
                st.caption("Displays the 11-step pipeline, 4 trust boundaries, and component attack surfaces.")
            else:
                st.error("architecture.drawio not found.")

        with dc2:
            st.markdown("#### 2. STRIDE Threat & Mitigation Mapping")
            drawio_path2 = os.path.join(ROOT_DIR, "diagrams", "stride_threat_mapping.drawio")
            if os.path.exists(drawio_path2):
                with open(drawio_path2, "r", encoding="utf-8") as f2:
                    content2 = f2.read()
                st.download_button(
                    label="📥 Download stride_threat_mapping.drawio",
                    data=content2,
                    file_name="stride_threat_mapping.drawio",
                    mime="application/xml",
                    key="dl_stride"
                )
                st.caption("Displays the Component ➔ STRIDE Category ➔ Threat Scenario ➔ Defense Control flow.")
            else:
                st.error("stride_threat_mapping.drawio not found.")

        st.info("💡 **How to edit**: Open [diagrams.net](https://app.diagrams.net/) in your web browser, click 'Open Existing Diagram', and select either XML file to edit or export as high-resolution SVG/PNG for your college report.")


# ==============================================================================
# 3. DATA FLOW ANALYSIS
# ==============================================================================
elif nav_selection == "🔀 Data Flow Analysis":
    st.markdown('<div class="main-title">Data Flow Analysis &amp; Boundary Crossings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed Examination of Flows F1 through F6 Across Architectural Trust Boundaries</div>', unsafe_allow_html=True)

    flows = DataFlowEngine.get_all_flows()

    for flow in flows:
        fid = flow["flow_id"]
        fname = flow["name"]
        with st.expander(f"🔹 Flow {fid}: {fname}", expanded=True):
            fc1, fc2 = st.columns([1, 1])
            with fc1:
                st.markdown(f"**Origin / Source:** `{flow['source']}`")
                st.markdown(f"**Destination:** `{flow['destination']}`")
                st.markdown(f"**Data Payload:**\n> {flow['data_payload']}")
                st.markdown(f"**Trust Boundary Crossing:**\n> 🌐 *{flow['trust_boundary']}*")
            with fc2:
                st.markdown(f"**Protection Mechanism:**\n> 🛡️ {flow['protection_mechanism']}")
                st.markdown("**Relevant STRIDE Threats:**")
                for th in flow["relevant_threats"]:
                    st.markdown(f"- **`{th['id']}`** ({th['category']}): {th['name']}")


# ==============================================================================
# 4. SECURITY ASSET INVENTORY
# ==============================================================================
elif nav_selection == "🗄️ Security Asset Inventory":
    st.markdown('<div class="main-title">Security Asset Inventory &amp; CIA Requirements</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Identification and Protection Objectives of Chatbot Information Assets</div>', unsafe_allow_html=True)

    assets = AssetInventoryEngine.get_all_assets()
    
    table_rows = []
    for a in assets:
        threat_str = ", ".join([t["id"] for t in a["primary_threats"]])
        table_rows.append({
            "Asset": a["asset"],
            "Description": a["description"],
            "Confidentiality": a["confidentiality"],
            "Integrity": a["integrity"],
            "Availability": a["availability"],
            "Primary Threat IDs": threat_str
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Asset Deep Dive & Threat Exposure")

    selected_asset_name = st.selectbox("Select Asset to inspect CIA requirements:", [a["asset"] for a in assets])
    sel_asset = AssetInventoryEngine.get_asset_by_name(selected_asset_name)

    if sel_asset:
        ac1, ac2 = st.columns([1, 1])
        with ac1:
            st.markdown(f"### Asset: `{sel_asset['asset']}`")
            st.write(sel_asset["description"])
            st.markdown("#### Primary Associated Threats:")
            for pt in sel_asset["primary_threats"]:
                st.markdown(f"- ⚠️ **`{pt['id']}`**: {pt['name']}")
        with ac2:
            st.markdown("#### Security Requirements (CIA Triad)")
            st.markdown(f"**Confidentiality:** `{sel_asset['confidentiality']}`")
            st.caption(sel_asset["confidentiality_desc"])
            st.markdown(f"**Integrity:** `{sel_asset['integrity']}`")
            st.caption(sel_asset["integrity_desc"])
            st.markdown(f"**Availability:** `{sel_asset['availability']}`")
            st.caption(sel_asset["availability_desc"])


# ==============================================================================
# 5. STRIDE THREAT MODEL PAGE
# ==============================================================================
elif nav_selection == "🛡️ STRIDE Threat Model":
    st.markdown('<div class="main-title">STRIDE Threat Catalog &amp; Model Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Interactive Threat Catalog with Exact Multi-Parameter Filters (24 Formal Threats)</div>', unsafe_allow_html=True)

    # Required Filters
    with st.expander("🔍 Filter & Search Threats", expanded=True):
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1:
            q_search = st.text_input("Search Threat / Keyword", placeholder="e.g. Prompt, Key, JWT...")
        with f2:
            q_stride = st.selectbox("STRIDE Category", ["All"] + engine.get_categories())
        with f3:
            q_comp = st.selectbox("Component", ["All"] + engine.get_components())
        with f4:
            q_prop = st.selectbox("Security Property", ["All"] + engine.get_security_properties())
        with f5:
            q_risk = st.selectbox("Risk Level", ["All", "Low", "Medium", "High", "Critical"])

    filtered_threats = engine.filter_threats(
        query=q_search,
        stride_category=q_stride,
        component=q_comp,
        risk_level=q_risk,
        security_property=q_prop
    )

    st.write(f"Showing **{len(filtered_threats)}** matching threats:")

    # Required Table Columns
    table_data = [
        {
            "ID": t["id"],
            "Component": t["component"],
            "STRIDE": t["stride_category"],
            "Threat": t["threat_name"],
            "Description": t["description"],
            "Likelihood": t["likelihood"],
            "Impact": t["impact"],
            "Risk Score": t["risk_score"],
            "Risk Level": t["risk_level"],
            "Mitigation": t["mitigation"]
        }
        for t in filtered_threats
    ]
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    # Expandable Threat Details
    st.markdown("---")
    st.subheader("Expandable Threat Details Inspector")
    if filtered_threats:
        selected_id = st.selectbox(
            "Select Threat ID to inspect full analysis:",
            [f"{t['id']} - {t['threat_name']} ({t['stride_category']})" for t in filtered_threats]
        )
        sel_id_clean = selected_id.split(" - ")[0]
        selected_threat = engine.get_threat_by_id(sel_id_clean)

        if selected_threat:
            d1, d2 = st.columns([2, 1])
            with d1:
                st.markdown(f"### `{selected_threat['id']}`: {selected_threat['threat_name']}")
                st.markdown(f"**Target Component:** `{selected_threat['component']}` | **Affected Asset:** `{selected_threat.get('asset', 'N/A')}`")
                st.markdown(f"**Data Flow:** `{selected_threat.get('data_flow', 'N/A')}` | **Trust Boundary:** `{selected_threat.get('trust_boundary', 'N/A')}`")
                st.markdown(f"**Threat Description:**\n{selected_threat['description']}")
                st.markdown(f"**Attack Scenario:**\n> {selected_threat['attack_scenario']}")
                st.markdown(f"**Security Impact:**\n> 💥 {selected_threat.get('security_impact', 'Impact on system.')}")
                st.markdown(f"**Recommended Mitigation:**\n> 🛡️ {selected_threat['mitigation']}")
            with d2:
                st.markdown("#### Risk & Security Property")
                level = selected_threat['risk_level']
                score = selected_threat['risk_score']
                st.markdown(f"**STRIDE Category:** `{selected_threat['stride_category']}`")
                st.markdown(f"**Security Property:** `{selected_threat['security_property']}`")
                st.markdown(f"**Likelihood:** {selected_threat['likelihood']} / 5")
                st.markdown(f"**Impact:** {selected_threat['impact']} / 5")
                st.markdown(f"**Risk Score:** `{score}` (Likelihood × Impact)")
                st.markdown(f"**Risk Level:** <span class='badge-{level.lower()}'>{level}</span>", unsafe_allow_html=True)
                st.markdown(f"**Mitigation Category:** `{selected_threat.get('mitigation_category', 'General')}`")
                st.markdown(f"**Status:** `{selected_threat['status']}`")


# ==============================================================================
# 6. RISK ANALYSIS PAGE
# ==============================================================================
elif nav_selection == "📈 Risk Analysis":
    st.markdown('<div class="main-title">Risk Scoring &amp; Matrix Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Quantitative Risk Model Evaluation Based Strictly on Defined Mathematics</div>', unsafe_allow_html=True)

    # Formula Display
    st.markdown("""
    <div class="security-callout">
        <b>Mathematical Risk Model:</b><br>
        $$\\text{Risk Score} = \\text{Likelihood} \\times \\text{Impact}$$
        Where $\\text{Likelihood} \\in \\{1, 2, 3, 4, 5\\}$ and $\\text{Impact} \\in \\{1, 2, 3, 4, 5\\}$, resulting in $\\text{Risk Score} \\in [1, 25]$.<br>
        <b>Strict Classification Thresholds:</b> 
        <b>Low</b> (1–5) | <b>Medium</b> (6–10) | <b>High</b> (11–15) | <b>Critical</b> (16–25).
    </div>
    """, unsafe_allow_html=True)

    # 5x5 Matrix: Impact on Y-axis (1 to 5), Likelihood on X-axis (1 to 5)
    st.subheader("Interactive 5×5 Risk Matrix (Impact on Y-axis, Likelihood on X-axis)")
    
    matrix_counts = [[0 for _ in range(5)] for _ in range(5)]
    matrix_labels = [["" for _ in range(5)] for _ in range(5)]

    for t in all_threats:
        l_idx = t["likelihood"] - 1
        i_idx = t["impact"] - 1
        matrix_counts[i_idx][l_idx] += 1
        tid = t["id"].replace("THR-", "T")
        if matrix_labels[i_idx][l_idx]:
            matrix_labels[i_idx][l_idx] += f", {tid}"
        else:
            matrix_labels[i_idx][l_idx] = tid

    annotations_text = []
    z_scores = []
    for i in range(5):
        row_ann = []
        row_z = []
        for l in range(5):
            score = (l + 1) * (i + 1)
            count = matrix_counts[i][l]
            lbl = matrix_labels[i][l]
            cell_text = f"Score: {score}<br><b>{count} threat(s)</b>"
            if count > 0:
                cell_text += f"<br><span style='font-size:10px;'>[{lbl}]</span>"
            row_ann.append(cell_text)
            row_z.append(score)
        annotations_text.append(row_ann)
        z_scores.append(row_z)

    fig_matrix = go.Figure(data=go.Heatmap(
        z=z_scores,
        x=["1 (Rare)", "2 (Unlikely)", "3 (Possible)", "4 (Likely)", "5 (Frequent)"],
        y=["1 (Negligible)", "2 (Minor)", "3 (Moderate)", "4 (Major)", "5 (Catastrophic)"],
        text=annotations_text,
        texttemplate="%{text}",
        colorscale=[
            [0.0, "#28a745"],
            [0.2, "#85e085"],
            [0.4, "#ffc107"],
            [0.6, "#fd7e14"],
            [1.0, "#dc3545"]
        ],
        showscale=True,
        colorbar=dict(title="Risk Score")
    ))
    fig_matrix.update_layout(
        xaxis_title="Likelihood (X-Axis: 1 to 5)",
        yaxis_title="Impact (Y-Axis: 1 to 5)",
        height=520
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

    # Top Risks & Sorting
    st.markdown("---")
    st.subheader("Top Risks (Sorted by Highest Risk Score)")
    sorted_threats = sorted(all_threats, key=lambda x: (x["risk_score"], x["impact"], x["likelihood"]), reverse=True)
    
    df_sorted = pd.DataFrame([
        {
            "Rank": idx + 1,
            "ID": t["id"],
            "Threat Name": t["threat_name"],
            "STRIDE": t["stride_category"],
            "Component": t["component"],
            "Likelihood": t["likelihood"],
            "Impact": t["impact"],
            "Risk Score": t["risk_score"],
            "Risk Level": t["risk_level"],
            "Status": t["status"]
        }
        for idx, t in enumerate(sorted_threats)
    ])
    st.dataframe(df_sorted, use_container_width=True, hide_index=True)


# ==============================================================================
# 7. MITIGATION CONTROLS PAGE
# ==============================================================================
elif nav_selection == "🔐 Mitigation Controls":
    st.markdown('<div class="main-title">Mitigation Controls &amp; Traceability Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Systematic Defense Categorization Across the 9 Academic Security Control Domains</div>', unsafe_allow_html=True)

    tab_cat, tab_matrix = st.tabs(["📂 Grouped Mitigation Domains", "📋 Formal Mitigation Traceability Matrix"])

    with tab_cat:
        grouped_threats = MitigationEngine.group_threats_by_category(all_threats)
        selected_mit_cat = st.selectbox("Select Mitigation Category to inspect:", MITIGATION_CATEGORIES)
        cat_meta = MitigationEngine.get_mitigation_category_meta(selected_mit_cat)
        cat_threats = grouped_threats.get(selected_mit_cat, [])

        st.markdown(f"""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 8px 0; color: #1e293b;">{cat_meta['title']}</h3>
            <p style="margin: 0 0 6px 0;"><b>Objective:</b> {cat_meta['objective']}</p>
            <p style="margin: 0; color: #475569;"><b>Standard Mechanisms:</b> {cat_meta['core_mechanisms']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write(f"Associated Threats in **{selected_mit_cat}** ({len(cat_threats)}):")
        for t in cat_threats:
            with st.expander(f"🛡️ `{t['id']}`: {t['threat_name']} — Control: **{t.get('security_control', 'Standard Control')}**", expanded=True):
                mc1, mc2 = st.columns([1, 1])
                with mc1:
                    st.markdown(f"**Threat:** {t['threat_name']}")
                    st.markdown(f"**Component:** `{t['component']}`")
                    st.markdown(f"**STRIDE Category:** `{t['stride_category']}`")
                    st.markdown(f"**Security Control:**\n> 🔒 **{t.get('security_control', t['mitigation'])}**")
                with mc2:
                    st.markdown(f"**Reason for Control:**\n> 💡 {t.get('mitigation_reason', 'Neutralizes attack vector.')}")
                    st.markdown(f"**Expected Security Property:** `{t['security_property']}`")
                    st.markdown(f"**Implementation Status:** `{t['status']}`")

    with tab_matrix:
        st.subheader("Formal Mitigation Traceability Matrix")
        st.markdown("""
        **STRIDE Mapping Rules:**
        - **Spoofing** ➔ Authentication Control ➔ *Authentication*
        - **Tampering** ➔ Integrity Protection / AEAD ➔ *Integrity*
        - **Repudiation** ➔ WORM / Merkle Audit Records ➔ *Accountability*
        - **Information Disclosure** ➔ E2EE / Memory Zeroization / Data Minimization ➔ *Confidentiality*
        - **Denial of Service** ➔ Rate Limiting / Token Timeouts ➔ *Availability*
        - **Elevation of Privilege** ➔ RBAC / ABAC / MicroVM Sandboxing ➔ *Authorization*
        """)
        matrix_rows = MitigationEngine.get_mitigation_matrix(all_threats)
        df_matrix = pd.DataFrame(matrix_rows)
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)


# ==============================================================================
# 8. SECURITY VS PRIVACY DISCUSSION PAGE
# ==============================================================================
elif nav_selection == "⚖️ Security vs. Privacy":
    st.markdown('<div class="main-title">Security vs. Privacy Conceptual Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Why End-to-End Encryption (E2EE) Alone Does Not Solve Every Security and Privacy Problem</div>', unsafe_allow_html=True)

    st.warning("""
    ⚠️ **Crucial Academic Realization:**  
    **End-to-End Encryption guarantees confidentiality of message content in transit. It does NOT guarantee complete security, integrity, or privacy across the system lifecycle.**  
    In an AI chatbot, the AI model is a participant that requires plaintext to process queries. Security requires Defense-in-Depth.
    """)

    topics = SecurityPrivacyEngine.get_all_topics()
    for top in topics:
        with st.expander(f"📌 {top['id']}: **{top['topic']}**", expanded=True):
            p1, p2 = st.columns([1, 1])
            with p1:
                st.markdown(f"**What E2EE Achieves:**\n> 🛡️ {top['e2ee_protection']}")
                st.markdown(f"**Inherent Limitation of E2EE:**\n> ⚠️ {top['limitation']}")
            with p2:
                st.markdown(f"**Academic Defense & Recommendation:**\n> 💡 {top['academic_takeaway']}")


# ==============================================================================
# 9. ACADEMIC TRACEABILITY PAGE
# ==============================================================================
elif nav_selection == "🎓 Academic Mapping":
    st.markdown('<div class="main-title">Academic Pipeline Traceability</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">College Micro-Project Assignment Flow: Problem ➔ Design ➔ Prototype ➔ Evaluation</div>', unsafe_allow_html=True)

    steps = [
        ("1. Problem Identification", "Identify critical communication and security vulnerabilities in an AI chatbot where messages are encrypted end-to-end but inference requires plaintext token inspection."),
        ("2. Objectives Formulation", "Analyze trust boundaries, map synthetic threats to the STRIDE framework, quantify risks using a formal mathematical model, and formulate architectural mitigations."),
        ("3. System Architecture Design", "Construct an 11-stage secure communication pipeline with 4 explicit trust boundaries (TB-01 to TB-04), 9 architecture components, and 6 data flows (F1 to F6)."),
        ("4. STRIDE Threat Modeling", "Systematically catalog 24 realistic synthetic threats evenly balanced across Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege."),
        ("5. Mathematical Risk Evaluation", "Apply the quantitative model: Risk = Likelihood (1-5) × Impact (1-5) on a 1-25 scale, categorizing risks into Low, Medium, High, and Critical without subjective bias."),
        ("6. Mitigation Architecture", "Formulate defense-in-depth controls across 9 domains (Authentication, Key Management, Integrity, Enclaves, Guardrails, Rate Limiting, WORM Auditing)."),
        ("7. Automated Testing & Verification", "Implement 43 automated unit tests in pytest to verify mathematical formulas, boundary guards, invalid types, and empty dataset handlers."),
        ("8. Evaluation & Viva Results", "Deliver a polished, local, dependency-free Streamlit prototype ready for practical viva demonstration and project defense.")
    ]

    for title, desc in steps:
        st.markdown(f"""
        <div class="academic-step">
            <h4 style="margin: 0 0 6px 0; color: #1e3a8a;">{title}</h4>
            <p style="margin: 0; color: #334155;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 10. TESTING & VERIFICATION PAGE
# ==============================================================================
elif nav_selection == "🧪 Testing & Verification":
    st.markdown('<div class="main-title">Automated Verification &amp; Unit Tests</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Rigorous Verification of Risk Formulas, Bounds, Filters, and Empty Datasets</div>', unsafe_allow_html=True)

    st.write("""
    The test suite executes via `pytest` to guarantee mathematical correctness of the Risk Scoring formula 
    ($$Score = Likelihood \\times Impact$$), input boundary checks, and full coverage of the 9 mitigation domains and asset inventories.
    """)

    if st.button("▶️ Execute Pytest Test Suite", type="primary"):
        with st.spinner("Running automated unit tests..."):
            try:
                res = subprocess.run(
                    [sys.executable, "-m", "pytest", "tests/test_risk_engine.py", "-v"],
                    cwd=ROOT_DIR,
                    capture_output=True,
                    text=True
                )
                if res.returncode == 0:
                    st.success("🎉 All 43 Unit Tests Passed Successfully! (100% test pass rate)")
                else:
                    st.error("Some tests failed.")
                st.code(res.stdout, language="bash")
            except Exception as e:
                st.error(f"Error running pytest: {e}")

    st.markdown("### Test Coverage Areas")
    st.markdown("""
    - ✅ **Risk Calculation**: Validates $L \\times I$ formula across full boundary domain.
    - ✅ **Classification Thresholds**: Verifies exact cuts at 5 (Low), 10 (Med), 15 (High), and 16+ (Critical).
    - ✅ **Invalid Inputs**: Enforces error handling for $L, I \\notin [1, 5]$ and non-numeric types.
    - ✅ **Empty Datasets**: Ensures enricher, summaries, and engines handle empty datasets gracefully without crashing.
    - ✅ **STRIDE Filtering**: Verifies filtering across all 6 STRIDE categories and components.
    - ✅ **Asset Inventory**: Verifies 9 protected assets with CIA ratings.
    - ✅ **Data Flows**: Verifies 6 data flows (F1 to F6) with trust boundary definitions.
    - ✅ **Security vs. Privacy Engine**: Verifies all 9 analytical topics.
    - ✅ **Mitigation Traceability Matrix**: Verifies all 24 mapped rows.
    """)


# ==============================================================================
# 11. ABOUT PROJECT PAGE
# ==============================================================================
elif nav_selection == "ℹ️ About Project":
    st.markdown('<div class="main-title">About This Academic Micro-Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">College Micro-Project Submission for Data Security and Privacy (22AI73)</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Project Credentials
    - **Course Name**: Data Security and Privacy (Course Code: **22AI73**)
    - **Academic Year / Semester**: 2026 / 7th Semester B.E. (AI & DS)
    - **Student Name**: **Saransh Neema**
    - **University Seat Number (USN)**: **1DS23AI048**
    - **Project Title**: **Threat Modelling of an E2EE AI Chatbot**

    ---

    ### Project Objectives
    1. **Analyze Security Boundaries**: Map communication and security trust boundaries in an End-to-End Encrypted AI Chatbot.
    2. **Apply STRIDE Threat Taxonomy**: Systematically identify Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege vectors across 9 chatbot components.
    3. **Formal Risk Quantification**: Evaluate likelihood ($1-5$) and impact ($1-5$) using quantitative risk matrices.
    4. **Formulate Defense-in-Depth Mitigations**: Recommend state-of-the-art protections across the 9 formal security control domains.
    5. **Model Assets and Data Flows**: Catalog 9 critical protected assets and 6 architectural data flows.
    6. **Academic Traceability**: Demonstrate the complete engineering lifecycle from problem definition to automated verification.

    ---

    ### Academic Disclaimer
    > **Note for Evaluators**: This application is an **academic threat-modeling prototype** designed for security evaluation and viva demonstration. It utilizes synthetic architecture schemas and simulated threat datasets. It is not intended to operate as a live production messaging system.
    """)

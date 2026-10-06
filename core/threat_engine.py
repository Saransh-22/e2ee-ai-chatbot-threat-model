"""
Threat Engine for E2EE AI Chatbot Threat Modeling.
Loads, searches, filters, and analyzes synthetic STRIDE threats with full academic traceability.
"""

import json
import os
from typing import List, Dict, Any, Optional
from collections import Counter
from core.risk_engine import enrich_threats_with_risk


DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "threats.json"
)

# Formal 6 STRIDE Categories
STRIDE_CATEGORIES = [
    "Spoofing",
    "Tampering",
    "Repudiation",
    "Information Disclosure",
    "Denial of Service",
    "Elevation of Privilege"
]

# Formal 6 Primary Security Properties
SECURITY_PROPERTIES = [
    "Authentication",
    "Integrity",
    "Accountability",
    "Confidentiality",
    "Availability",
    "Authorization"
]


class ThreatEngine:
    """
    Manages loading, filtering, querying, and summarizing threats.
    """

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or DEFAULT_DATA_PATH
        self._threats: List[Dict[str, Any]] = []
        self.load_threats()

    def load_threats(self) -> List[Dict[str, Any]]:
        """
        Loads threat entries from JSON file and enriches each with risk score & level.
        Handles missing or corrupted file gracefully.
        """
        if not os.path.exists(self.data_path):
            self._threats = []
            return self._threats

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if not isinstance(raw_data, list):
                self._threats = []
                return self._threats
            self._threats = enrich_threats_with_risk(raw_data)
        except Exception as e:
            print(f"Error loading threats from {self.data_path}: {e}")
            self._threats = []

        return self._threats

    def get_all_threats(self) -> List[Dict[str, Any]]:
        """Returns all enriched threats."""
        return list(self._threats)

    def get_threat_by_id(self, threat_id: str) -> Optional[Dict[str, Any]]:
        """Returns a single threat by its ID, or None if not found."""
        for t in self._threats:
            if t.get("id", "").strip().upper() == threat_id.strip().upper():
                return dict(t)
        return None

    def get_categories(self) -> List[str]:
        """Returns list of distinct STRIDE categories in standard order."""
        return list(STRIDE_CATEGORIES)

    def get_components(self) -> List[str]:
        """Returns sorted list of distinct architecture components."""
        return sorted(list({t.get("component", "") for t in self._threats if t.get("component")}))

    def get_assets(self) -> List[str]:
        """Returns sorted list of distinct affected assets."""
        return sorted(list({t.get("asset", "") for t in self._threats if t.get("asset")}))

    def get_security_properties(self) -> List[str]:
        """Returns list of distinct security properties."""
        return list(SECURITY_PROPERTIES)

    def get_statuses(self) -> List[str]:
        """Returns sorted list of distinct mitigation statuses."""
        return sorted(list({t.get("status", "") for t in self._threats if t.get("status")}))

    def filter_threats(
        self,
        query: Optional[str] = None,
        stride_category: Optional[str] = None,
        component: Optional[str] = None,
        risk_level: Optional[str] = None,
        asset: Optional[str] = None,
        security_property: Optional[str] = None,
        status: Optional[str] = None,
        min_score: int = 1,
        max_score: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Filters threat list based on search terms, STRIDE category, component, risk level, asset, and status.
        """
        results = self._threats

        if query:
            q = query.strip().lower()
            results = [
                t for t in results
                if q in t.get("threat_name", "").lower()
                or q in t.get("description", "").lower()
                or q in t.get("attack_scenario", "").lower()
                or q in t.get("mitigation", "").lower()
                or q in t.get("id", "").lower()
                or q in t.get("component", "").lower()
                or q in t.get("asset", "").lower()
                or q in t.get("security_control", "").lower()
            ]

        if stride_category and stride_category != "All":
            results = [t for t in results if t.get("stride_category") == stride_category]

        if component and component != "All":
            results = [t for t in results if t.get("component") == component]

        if risk_level and risk_level != "All":
            results = [t for t in results if t.get("risk_level") == risk_level]

        if asset and asset != "All":
            results = [t for t in results if t.get("asset") == asset]

        if security_property and security_property != "All":
            results = [t for t in results if t.get("security_property") == security_property]

        if status and status != "All":
            results = [t for t in results if t.get("status") == status]

        results = [
            t for t in results
            if min_score <= t.get("risk_score", 1) <= max_score
        ]

        return results

    def get_distribution_by_stride(self) -> Dict[str, int]:
        """Returns threat count per STRIDE category."""
        counts = {cat: 0 for cat in STRIDE_CATEGORIES}
        for t in self._threats:
            cat = t.get("stride_category")
            if cat in counts:
                counts[cat] += 1
            else:
                counts[cat] = 1
        return counts

    def get_distribution_by_component(self) -> Dict[str, int]:
        """Returns threat count per component."""
        counts: Dict[str, int] = {}
        for t in self._threats:
            comp = t.get("component", "Unknown")
            counts[comp] = counts.get(comp, 0) + 1
        return counts

    def get_distribution_by_security_property(self) -> Dict[str, int]:
        """Returns threat count per security property."""
        counts = {prop: 0 for prop in SECURITY_PROPERTIES}
        for t in self._threats:
            prop = t.get("security_property")
            if prop in counts:
                counts[prop] += 1
            else:
                counts[prop] = 1
        return counts

    def get_threat_model_summary(self) -> Dict[str, Any]:
        """
        Generates an automated summary of the threat model:
        - Total threats
        - Threats by STRIDE
        - Threats by component
        - Threats by risk level
        - Highest calculated risks
        - Most frequently affected assets
        - Most frequently recommended controls
        """
        total = len(self._threats)
        if total == 0:
            return {
                "total_threats": 0,
                "stride_distribution": {},
                "component_distribution": {},
                "risk_distribution": {"Low": 0, "Medium": 0, "High": 0, "Critical": 0},
                "highest_risks": [],
                "top_affected_assets": [],
                "top_recommended_controls": []
            }

        stride_dist = self.get_distribution_by_stride()
        comp_dist = self.get_distribution_by_component()
        
        # Risk distribution
        risk_dist = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        for t in self._threats:
            lvl = t.get("risk_level", "Low")
            if lvl in risk_dist:
                risk_dist[lvl] += 1

        # Highest calculated risks
        highest_risks = sorted(
            self._threats,
            key=lambda x: (x.get("risk_score", 0), x.get("impact", 0), x.get("likelihood", 0)),
            reverse=True
        )[:5]

        # Most frequently affected assets
        asset_counts = Counter([t.get("asset") for t in self._threats if t.get("asset")])
        top_assets = asset_counts.most_common(5)

        # Most frequently recommended controls
        control_counts = Counter([t.get("security_control") for t in self._threats if t.get("security_control")])
        top_controls = control_counts.most_common(5)

        return {
            "total_threats": total,
            "stride_distribution": stride_dist,
            "component_distribution": comp_dist,
            "risk_distribution": risk_dist,
            "highest_risks": highest_risks,
            "top_affected_assets": top_assets,
            "top_recommended_controls": top_controls
        }

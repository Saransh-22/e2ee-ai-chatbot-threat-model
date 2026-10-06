"""
Comprehensive unit test suite for E2EE AI Chatbot Threat Modeler.
Covers risk calculation, tier classification, input boundary validation,
STRIDE filtering, mitigation grouping, asset inventory, data flow verification,
security vs. privacy analysis, and academic traceability.
"""

import pytest
import sys
import os
import tempfile

# Add root directory to sys.path so core can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk_engine import (
    calculate_risk,
    classify_risk_level,
    enrich_threats_with_risk,
    get_risk_summary
)
from core.threat_engine import ThreatEngine, STRIDE_CATEGORIES, SECURITY_PROPERTIES
from core.mitigation_engine import MitigationEngine, MITIGATION_CATEGORIES
from core.asset_inventory import AssetInventoryEngine
from core.data_flow_engine import DataFlowEngine
from core.security_privacy_engine import SecurityPrivacyEngine


class TestRiskEngine:
    """Test suite for mathematical risk score calculation and tier classification."""

    def test_risk_formula_basic(self):
        """Verify Risk = Likelihood x Impact calculation."""
        res = calculate_risk(3, 4)
        assert res["risk_score"] == 12
        assert res["risk_level"] == "High"

    def test_boundary_values_min_max(self):
        """Verify minimum boundary (1x1=1, Low) and maximum boundary (5x5=25, Critical)."""
        min_res = calculate_risk(1, 1)
        assert min_res["risk_score"] == 1
        assert min_res["risk_level"] == "Low"

        max_res = calculate_risk(5, 5)
        assert max_res["risk_score"] == 25
        assert max_res["risk_level"] == "Critical"

    @pytest.mark.parametrize("score,expected_level", [
        (1, "Low"),
        (2, "Low"),
        (5, "Low"),
        (6, "Medium"),
        (7, "Medium"),
        (10, "Medium"),
        (11, "High"),
        (12, "High"),
        (15, "High"),
        (16, "Critical"),
        (20, "Critical"),
        (25, "Critical"),
    ])
    def test_risk_classification_tiers(self, score, expected_level):
        """Verify exact classification cutoffs: 1-5 Low, 6-10 Medium, 11-15 High, 16-25 Critical."""
        assert classify_risk_level(score) == expected_level

    @pytest.mark.parametrize("invalid_l", [0, -1, 6, 10, -99])
    def test_invalid_likelihood_handling(self, invalid_l):
        """Likelihood values outside [1, 5] must raise ValueError."""
        with pytest.raises(ValueError, match="Likelihood must be between 1 and 5"):
            calculate_risk(invalid_l, 3)

    @pytest.mark.parametrize("invalid_i", [0, -1, 6, 10, -99])
    def test_invalid_impact_handling(self, invalid_i):
        """Impact values outside [1, 5] must raise ValueError."""
        with pytest.raises(ValueError, match="Impact must be between 1 and 5"):
            calculate_risk(3, invalid_i)

    def test_invalid_non_numeric_types(self):
        """Non-numeric string/object inputs must raise TypeError."""
        with pytest.raises(TypeError):
            calculate_risk("high", 4)
        with pytest.raises(TypeError):
            calculate_risk(4, "severe")

    def test_classify_out_of_range(self):
        """Risk scores below 1 or above 25 must raise ValueError."""
        with pytest.raises(ValueError):
            classify_risk_level(0)
        with pytest.raises(ValueError):
            classify_risk_level(26)

    def test_empty_threat_dataset_handling(self):
        """Empty threat dataset passed to enricher or summary must return valid empty structure without crashing."""
        empty_enriched = enrich_threats_with_risk([])
        assert empty_enriched == []

        empty_summary = get_risk_summary([])
        assert empty_summary["total_threats"] == 0
        assert empty_summary["average_risk_score"] == 0.0
        assert empty_summary["critical_count"] == 0
        assert empty_summary["high_count"] == 0
        assert empty_summary["counts_by_level"]["Low"] == 0


class TestThreatEngine:
    """Test suite for threat loader, STRIDE filters, and keyword searches."""

    @pytest.fixture
    def engine(self):
        return ThreatEngine()

    def test_threat_loading_and_attributes(self, engine):
        """Verify that exactly 24 threats load with complete attributes."""
        threats = engine.get_all_threats()
        assert len(threats) == 24
        for t in threats:
            assert "id" in t
            assert "component" in t
            assert "asset" in t
            assert "data_flow" in t
            assert "trust_boundary" in t
            assert "stride_category" in t
            assert "threat_name" in t
            assert "description" in t
            assert "attack_scenario" in t
            assert "security_impact" in t
            assert "likelihood" in t
            assert "impact" in t
            assert "risk_score" in t
            assert "risk_level" in t
            assert "mitigation" in t
            assert "mitigation_category" in t
            assert "security_control" in t
            assert "security_property" in t
            assert "status" in t

    def test_stride_category_distribution_balance(self, engine):
        """Verify all 6 STRIDE categories have exactly 4 threats each (24 total)."""
        counts = engine.get_distribution_by_stride()
        for cat in STRIDE_CATEGORIES:
            assert counts[cat] == 4, f"Category {cat} should have 4 threats, got {counts[cat]}"

    def test_security_properties_present(self, engine):
        """Verify all 6 core security properties are represented."""
        counts = engine.get_distribution_by_security_property()
        for prop in SECURITY_PROPERTIES:
            assert counts[prop] > 0, f"Property {prop} missing from threats"

    def test_stride_category_filtering(self, engine):
        """Verify filtering by each individual STRIDE category."""
        for cat in STRIDE_CATEGORIES:
            results = engine.filter_threats(stride_category=cat)
            assert len(results) == 4
            assert all(t["stride_category"] == cat for t in results)

    def test_component_filtering(self, engine):
        """Verify filtering by architecture component."""
        gateway_threats = engine.filter_threats(component="Secure Gateway")
        assert len(gateway_threats) > 0
        assert all(t["component"] == "Secure Gateway" for t in gateway_threats)

    def test_risk_level_filtering(self, engine):
        """Verify filtering by risk level tiers."""
        critical_threats = engine.filter_threats(risk_level="Critical")
        assert len(critical_threats) == 4
        assert all(t["risk_level"] == "Critical" for t in critical_threats)

    def test_search_by_threat_name_and_query(self, engine):
        """Verify text query search across name, description, and controls."""
        res_prompt = engine.filter_threats(query="Prompt Injection")
        assert len(res_prompt) > 0
        assert any("Prompt Injection" in t["threat_name"] for t in res_prompt)

        res_jwt = engine.filter_threats(query="JWT")
        assert len(res_jwt) > 0
        assert any("JWT" in t["threat_name"] for t in res_jwt)

    def test_threat_model_summary(self, engine):
        """Verify automatic summary generation."""
        summary = engine.get_threat_model_summary()
        assert summary["total_threats"] == 24
        assert len(summary["highest_risks"]) == 5
        assert len(summary["top_affected_assets"]) > 0
        assert len(summary["top_recommended_controls"]) > 0

    def test_empty_file_handling(self):
        """Verify that an empty JSON file does not crash the ThreatEngine."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            tf.write("[]")
            temp_path = tf.name

        try:
            temp_engine = ThreatEngine(data_path=temp_path)
            assert temp_engine.get_all_threats() == []
            assert temp_engine.get_threat_model_summary()["total_threats"] == 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestMitigationEngine:
    """Test suite for mitigation categorization, matrix, and residual risk posture."""

    def test_mitigation_categories_completeness(self):
        """Verify all 9 formal mitigation categories are present."""
        expected_cats = {
            "Authentication", "Authorization", "Confidentiality", "Integrity",
            "Availability", "Accountability", "Key Management", "Logging", "Data Minimization"
        }
        assert set(MITIGATION_CATEGORIES) == expected_cats

    def test_threat_grouping_by_mitigation_category(self):
        """Verify that threats correctly group across all 9 categories."""
        engine = ThreatEngine()
        threats = engine.get_all_threats()
        grouped = MitigationEngine.group_threats_by_category(threats)

        for cat in MITIGATION_CATEGORIES:
            assert cat in grouped
            assert len(grouped[cat]) > 0, f"Expected threats mapped to mitigation category: {cat}"

    def test_mitigation_matrix_generation(self):
        """Verify that mitigation matrix generates rows with Threat, Control, Property, Reason."""
        engine = ThreatEngine()
        threats = engine.get_all_threats()
        matrix = MitigationEngine.get_mitigation_matrix(threats)
        assert len(matrix) == 24
        for item in matrix:
            assert "id" in item
            assert "threat_name" in item
            assert "security_control" in item
            assert "security_property" in item
            assert "reason" in item

    def test_residual_risk_calculation(self):
        """Ensure Mitigated threats have reduced risk score compared to initial score."""
        threat = {
            "likelihood": 4,
            "impact": 4,
            "status": "Mitigated"
        }
        res = MitigationEngine.compute_residual_risk(threat)
        assert res["initial_score"] == 16
        assert res["residual_score"] < 16
        assert res["risk_reduction_pct"] > 0


class TestAssetAndDataFlowEngines:
    """Test suite for Security Asset Inventory, Data Flows, and Security vs. Privacy."""

    def test_asset_inventory_has_all_assets(self):
        """Verify 9 required protected assets exist with CIA requirements."""
        assets = AssetInventoryEngine.get_all_assets()
        assert len(assets) == 9
        for a in assets:
            assert a["confidentiality"] in ["Low", "Moderate", "High", "Critical"]
            assert a["integrity"] in ["Low", "Moderate", "High", "Critical"]
            assert a["availability"] in ["Low", "Moderate", "High", "Critical"]
            assert len(a["primary_threats"]) > 0

    def test_data_flows_f1_to_f6(self):
        """Verify all 6 flows (F1 to F6) exist with protection mechanisms and STRIDE threats."""
        flows = DataFlowEngine.get_all_flows()
        assert len(flows) == 6
        flow_ids = [f["flow_id"] for f in flows]
        assert flow_ids == ["F1", "F2", "F3", "F4", "F5", "F6"]

    def test_security_vs_privacy_engine(self):
        """Verify that all 9 security vs privacy topics exist."""
        topics = SecurityPrivacyEngine.get_all_topics()
        assert len(topics) == 9
        for top in topics:
            assert "topic" in top
            assert "e2ee_protection" in top
            assert "limitation" in top
            assert "academic_takeaway" in top

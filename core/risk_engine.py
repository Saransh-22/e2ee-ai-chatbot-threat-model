"""
Risk Engine for E2EE AI Chatbot Threat Modeling.
Computes risk scores based on Likelihood and Impact metrics according to academic DSP standards.
"""

from typing import Dict, Any, List, Tuple


RISK_LEVEL_COLORS = {
    "Low": "#28a745",
    "Medium": "#ffc107",
    "High": "#fd7e14",
    "Critical": "#dc3545"
}


def classify_risk_level(risk_score: int) -> str:
    """
    Classifies a numeric risk score into standard qualitative tiers:
    1 - 5   : Low
    6 - 10  : Medium
    11 - 15 : High
    16 - 25 : Critical
    """
    if not isinstance(risk_score, int):
        try:
            risk_score = int(risk_score)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid risk score '{risk_score}': must be an integer.")

    if risk_score < 1:
        raise ValueError(f"Risk score {risk_score} is below minimum allowed value of 1.")
    elif risk_score <= 5:
        return "Low"
    elif risk_score <= 10:
        return "Medium"
    elif risk_score <= 15:
        return "High"
    elif risk_score <= 25:
        return "Critical"
    else:
        raise ValueError(f"Risk score {risk_score} exceeds maximum allowed value of 25.")


def calculate_risk(likelihood: int, impact: int) -> Dict[str, Any]:
    """
    Calculates Risk Score = Likelihood x Impact.
    Both parameters must be integers in the range [1, 5].
    Returns a dictionary containing 'risk_score' and 'risk_level'.
    """
    if not isinstance(likelihood, int) or not isinstance(impact, int):
        try:
            likelihood = int(likelihood)
            impact = int(impact)
        except (ValueError, TypeError):
            raise TypeError("Likelihood and Impact must be integers between 1 and 5.")

    if not (1 <= likelihood <= 5):
        raise ValueError(f"Likelihood must be between 1 and 5 inclusive. Got: {likelihood}")

    if not (1 <= impact <= 5):
        raise ValueError(f"Impact must be between 1 and 5 inclusive. Got: {impact}")

    risk_score = likelihood * impact
    risk_level = classify_risk_level(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }


def enrich_threats_with_risk(threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Takes a list of threat records and attaches 'risk_score' and 'risk_level' to each.
    """
    enriched: List[Dict[str, Any]] = []
    for threat in threats:
        item = dict(threat)
        l = item.get("likelihood", 1)
        i = item.get("impact", 1)
        calc = calculate_risk(l, i)
        item["risk_score"] = calc["risk_score"]
        item["risk_level"] = calc["risk_level"]
        enriched.append(item)
    return enriched


def get_risk_summary(threats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes aggregated risk statistics across all threats.
    """
    if not threats:
        return {
            "total_threats": 0,
            "average_risk_score": 0.0,
            "counts_by_level": {"Low": 0, "Medium": 0, "High": 0, "Critical": 0},
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0
        }

    counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    scores = []

    for t in threats:
        score = t.get("risk_score")
        level = t.get("risk_level")
        if score is None or level is None:
            calc = calculate_risk(t.get("likelihood", 1), t.get("impact", 1))
            score = calc["risk_score"]
            level = calc["risk_level"]
        scores.append(score)
        if level in counts:
            counts[level] += 1

    return {
        "total_threats": len(threats),
        "average_risk_score": round(sum(scores) / len(scores), 2),
        "counts_by_level": counts,
        "critical_count": counts["Critical"],
        "high_count": counts["High"],
        "medium_count": counts["Medium"],
        "low_count": counts["Low"]
    }

"""
Node 3: Risk Assessment Scenario Matrix
Description: Evaluates organizational click and reporting ratios against established 
             corporate baselines to determine the workforce security posture level.
"""

from typing import Dict, Any, Tuple

# Corporate Security Performance Benchmarks (Adjust to align with specific compliance requirements)
HIGH_CLICK_THRESHOLD: float = 5.0
HIGH_REPORT_THRESHOLD: float = 20.0


def determine_risk_profile(is_high_click: bool, is_high_report: bool) -> Tuple[str, str, str, str]:
    """
    Evaluates multi-quadrant engagement parameters using corporate threshold conditions
    to classify the workforce behavior into distinct risk profiles.
    
    Returns:
        Tuple containing: (scenario_title, descriptive_text, risk_tier, visual_indicator)
    """
    if is_high_report and not is_high_click:
        return (
            "High Report / Low Click",
            "Ideal behavior – users identify and report the threat without interacting.",
            "Low Risk",
            "🟢"
        )
        
    elif is_high_click and not is_high_report:
        return (
            "High Click / Low Report",
            "High-risk behavior – users fall for the phishing attempt and fail to report it.",
            "High Risk",
            "🔴"
        )
        
    elif is_high_click and is_high_report:
        return (
            "High Click / High Report",
            "Mixed behavior – users interact but also demonstrate active reporting traits.",
            "Medium Risk",
            "🟡"
        )
        
    else:
        return (
            "Low Click / Low Report",
            "Low engagement – users neither interact with nor report the security incident.",
            "Moderate Risk",
            "⚪"
        )


def main(click_rate_input: Any, reporting_rate_input: Any) -> Dict[str, Any]:
    """
    Main entrypoint orchestration function executing multi-variable calculation logic 
    to evaluate enterprise data matrices.
    """
    try:
        # 1. Enforce rigorous datatype cleansing and float mappings
        click_rate_value = float(click_rate_input) if click_rate_input is not None else 0.0
        reporting_rate_value = float(reporting_rate_input) if reporting_rate_input is not None else 0.0

        # 2. Assert systemic states based on organizational target boundaries
        is_high_click = click_rate_value >= HIGH_CLICK_THRESHOLD
        is_high_report = reporting_rate_value >= HIGH_REPORT_THRESHOLD

        # 3. Classify organizational performance vector
        scenario, description, risk_level, emoji = determine_risk_profile(is_high_click, is_high_report)

        # 4. Synthesize structural markers for database dashboard visualization feeds
        label = f"{emoji} {risk_level}"

        return {
            "scenario": scenario,
            "description": description,
            "risk_level": risk_level,
            "risk_emoji": emoji,
            "label": label,
            "click_rate_value": round(click_rate_value, 2),
            "reporting_rate_value": round(reporting_rate_value, 2),
            "threshold_click": HIGH_CLICK_THRESHOLD,
            "threshold_report": HIGH_REPORT_THRESHOLD
        }

    except Exception as e:
        return {
            "scenario": "Unknown",
            "description": f"Critical analytical anomaly processing threat metrics: {str(e)}",
            "risk_level": "Unknown",
            "risk_emoji": "⚪",
            "label": "⚪ Unknown",
            "click_rate_value": 0.0,
            "reporting_rate_value": 0.0,
            "threshold_click": 0.0,
            "threshold_report": 0.0
        }

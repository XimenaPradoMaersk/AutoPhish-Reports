"""
Risk Classification Module

This script classifies phishing risk based on:
- Click rate
- Reporting rate

It assigns:
- Scenario
- Risk level
- Description
- Visual label (for dashboards)

This represents logic originally implemented in a Dify code node.
"""


def normalize_rate(rate):
    """
    Convert rate to float (handles strings like '25%')
    """
    if isinstance(rate, str):
        return float(rate.replace("%", "").strip())
    return float(rate)


def classify_risk(click_rate, reporting_rate):
    """
    Classify phishing risk based on click and reporting rates

    :param click_rate: Click rate (%)
    :param reporting_rate: Reporting rate (%)
    :return: Dictionary with risk classification
    """

    # ✅ Normalize inputs
    click_rate_value = normalize_rate(click_rate)
    reporting_rate_value = normalize_rate(reporting_rate)

    # ✅ Thresholds
    HIGH_CLICK_THRESHOLD = 10
    HIGH_REPORT_THRESHOLD = 20

    is_high_click = click_rate_value >= HIGH_CLICK_THRESHOLD
    is_high_report = reporting_rate_value >= HIGH_REPORT_THRESHOLD

    # ✅ Scenario logic
    if is_high_report and not is_high_click:
        scenario = "High Report / Low Click"
        description = "✅ Ideal behavior – users identify and report the threat without interacting"
        risk_level = "Low Risk"
        emoji = "🟢"

    elif is_high_click and not is_high_report:
        scenario = "High Click / Low Report"
        description = "🚨 High-risk behavior – users fall for the phishing attempt and fail to report it"
        risk_level = "High Risk"
        emoji = "🔴"

    elif is_high_click and is_high_report:
        scenario = "High Click / High Report"
        description = "⚖️ Mixed behavior – users interact but also report the email"
        risk_level = "Medium Risk"
        emoji = "🟡"

    else:
        scenario = "Low Click / Low Report"
        description = "⚠️ Low engagement – users neither interact nor report"
        risk_level = "Moderate Risk"
        emoji = "⚪"

    # ✅ Label (useful for dashboards / slides)
    label = f"{emoji} {risk_level}"

    return {
        "scenario": scenario,
        "description": description,
        "risk_level": risk_level,
        "risk_emoji": emoji,
        "label": label,
        "click_rate": click_rate_value,
        "reporting_rate": reporting_rate_value,
        "threshold_click": HIGH_CLICK_THRESHOLD,
        "threshold_report": HIGH_REPORT_THRESHOLD
    }


def main():
    # ✅ Example usage
    click_rate = 25
    reporting_rate = 60

    result = classify_risk(click_rate, reporting_rate)

    print("✅ Scenario:", result["scenario"])
    print("✅ Risk Level:", result["label"])
    print("✅ Description:", result["description"])


if __name__ == "__main__":
    main()

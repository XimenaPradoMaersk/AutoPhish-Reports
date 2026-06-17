from data_preprocessing import main as preprocess
from metrics_calculation import calculate_click_metrics
from reporting_metrics import calculate_reporting_metrics
from risk_classification import classify_risk


def run_pipeline(excel_file, reporting_file):
    # Step 1: Preprocess data
    data_result = preprocess(excel_file)
    clean_data = data_result["data"]

    # Step 2: Click metrics
    click_metrics = calculate_click_metrics(clean_data)

    # Step 3: Reporting metrics
    reporting_metrics = calculate_reporting_metrics(
        reporting_file,
        click_metrics["total_users"]
    )

    # Step 4: Risk classification
    risk = classify_risk(
        click_metrics["click_rate"],
        reporting_metrics["reporting_rate"]
    )

    return {
        "click_metrics": click_metrics,
        "reporting_metrics": reporting_metrics,
        "risk": risk
    }

"""
Main Orchestrator
Description: Simulates the Dify workflow engine locally. It pipes data through 
             Node 1 (Deduplication), Node 2 (Reporting), Node 3 (Risk Matrix),
             and Node 4 (Template Formatting) to generate a unified cybersecurity report.
"""

import os
import json

# Import node logic
import node1_deduplication
import node2_reporting_metrics
import node3_risk_matrix
import node4_template_formatting   


def run_pipeline(campaign_file_path: str, reporting_file_path: str) -> None:
    """
    Orchestrates the execution of all nodes, handling variable pass-through 
    and printing both technical and executive-friendly outputs.
    """

    print("=" * 60)
    print("⚡ STARTING PHISHING SIMULATION ANALYTICS PIPELINE ⚡")
    print("=" * 60)

    # --- FILE INPUT SIMULATION ---
    campaign_input_payload = {
        "url": os.path.abspath(campaign_file_path),
        "name": os.path.basename(campaign_file_path),
        "extension": ".csv"
    }

    reporting_input_payload = {
        "url": os.path.abspath(reporting_file_path),
        "name": os.path.basename(reporting_file_path),
        "extension": ".csv"
    }

    # =========================================================================
    # NODE 1: DEDUPLICATION & CORE METRICS
    # =========================================================================
    print("\n[Node 1] Processing Raw Campaign Logs & Eliminating Duplicates...")

    node1_output = node1_deduplication.main(campaign_input_payload)

    if "Error" in node1_output.get("summary_text", ""):
        print(f"❌ Pipeline Aborted at Node 1: {node1_output['summary_text']}")
        return

    print(f"✅ Node 1 Success: {node1_output['final_rows']} unique users")
    print(f"   - Open Rate: {node1_output['open_rate_percentage']}%")
    print(f"   - Click Rate: {node1_output['click_rate_percentage']}%")

    # =========================================================================
    # NODE 2: REPORTING METRICS
    # =========================================================================
    print("\n[Node 2] Analyzing Phishing Reports Telemetry...")

    node2_output = node2_reporting_metrics.main(
        reporting_file_array=reporting_input_payload,
        total_unique_users=node1_output["final_rows"]
    )

    if "Error" in node2_output.get("summary_text", ""):
        print(f"❌ Pipeline Aborted at Node 2: {node2_output['summary_text']}")
        return

    print(f"✅ Node 2 Success")
    print(f"   - Reporting Rate: {node2_output['reporting_rate_percentage']}%")

    # =========================================================================
    # NODE 3: RISK MATRIX
    # =========================================================================
    print("\n[Node 3] Evaluating Risk Posture...")

    node3_output = node3_risk_matrix.main(
        click_rate_input=node1_output["click_rate_percentage"],
        reporting_rate_input=node2_output["reporting_rate_percentage"]
    )

    print("✅ Node 3 Success")

    # =========================================================================
    # NODE 4: TEMPLATE FORMATTING
    # =========================================================================
    print("\n[Node 4] Formatting Executive Report...")

    template_input = {
        "Total_Users": node1_output["final_rows"],
        "Total_Opens": node1_output["total_opens"],
        "Open_Rate": node1_output["open_rate_percentage"],
        "Total_Clicks": node1_output["total_clicks"],
        "Click_Rate": node1_output["click_rate_percentage"],
        "Total_Reports": node2_output["total_reports"],
        "Reporting_Rate": node2_output["reporting_rate_percentage"],
        "Scenario": node3_output["scenario"],
        "Risk_Level": node3_output["label"]
    }

    formatted_report = node4_template_formatting.format_phishing_report(template_input)

    print("✅ Node 4 Success: Report formatted")

    # =========================================================================
    # FINAL OUTPUTS
    # =========================================================================
    print("\n" + "=" * 60)
    print("📊 TECHNICAL JSON OUTPUT")
    print("=" * 60)

    final_json_report = {
        "metrics": template_input,
        "risk_context": {
            "description": node3_output["description"]
        }
    }

    print(json.dumps(final_json_report, indent=4, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("🧾 EXECUTIVE REPORT (FINAL OUTPUT)")
    print("=" * 60)

    print(formatted_report)

    print("=" * 60)
    print("🚀 PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":

    CAMPAIGN_CSV_SAMPLE = "data_samples/campaign_data.csv"
    REPORTING_CSV_SAMPLE = "data_samples/reporting_data.csv"

    try:
        run_pipeline(CAMPAIGN_CSV_SAMPLE, REPORTING_CSV_SAMPLE)
    except Exception as global_err:
        print(f"\n[Environment Warning] {global_err}")

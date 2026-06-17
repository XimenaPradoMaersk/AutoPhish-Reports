"""
Main Orchestrator
Description: Simulates the Dify workflow engine locally. It pipes data through 
             Node 1 (Deduplication), Node 2 (Reporting), and Node 3 (Risk Matrix)
             to generate a unified cybersecurity report.
"""

import os
import json
# Import the main functions from your clean node files
import node1_deduplication
import node2_reporting_metrics
import node3_risk_matrix


def run_pipeline(campaign_file_path: str, reporting_file_path: str) -> None:
    """
    Orchestrates the execution of all nodes, handling variable pass-through 
    and printing a beautiful executive summary.
    """
    print("=" * 60)
    print("⚡ STARTING PHISHING SIMULATION ANALYTICS PIPELINE ⚡")
    print("=" * 60)

    # --- SIMULATE DIFY FILE UPLOAD STRUCTURE ---
    # Dify wraps local file uploads inside metadata structures with a dummy local path or URL.
    # We pass the absolute path here to simulate Dify locating your files.
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
    # NODE 1: DEDUPLICATION & CORE ENGAGEMENT METRICS
    # =========================================================================
    print("\n[Node 1] Processing Raw Campaign Logs & Eliminating Duplicates...")
    
    # We intercept fetch_and_parse_csv locally by overriding the requests.get or mocking it.
    # To keep code execution clean locally, Node 1's fetch can fall back to local open if 'http' is absent.
    # Since our nodes are built to read files, ensure you test them in an environment that handles file path parsing.
    node1_output = node1_deduplication.main(campaign_input_payload)
    
    if "Error" in node1_output.get("summary_text", ""):
        print(f"❌ Pipeline Aborted at Node 1: {node1_output['summary_text']}")
        return

    print(f"✅ Node 1 Success: Reduced rows to {node1_output['final_rows']} unique users.")
    print(f"   - Click Rate: {node1_output['click_rate_percentage']}%")
    print(f"   - Open Rate: {node1_output['open_rate_percentage']}%")

    # =========================================================================
    # NODE 2: TELEMETRY REPORTING RATES
    # =========================================================================
    print("\n[Node 2] Analyzing Phishing Reports Telemetry...")
    
    # Pass Node 1's dynamic 'final_rows' output directly into Node 2
    node2_output = node2_reporting_metrics.main(
        reporting_file_array=reporting_input_payload,
        total_unique_users=node1_output["final_rows"]
    )
    
    if "Error" in node2_output.get("summary_text", ""):
        print(f"❌ Pipeline Aborted at Node 2: {node2_output['summary_text']}")
        return

    print(f"✅ Node 2 Success: Calculated user compliance indicators.")
    print(f"   - Reporting Rate: {node2_output['reporting_rate_percentage']}%")

    # =========================================================================
    # NODE 3: RISK ASSESSMENT MATRIX
    # =========================================================================
    print("\n[Node 3] Evaluating Organizational Security Risk Posture...")
    
    # Pass calculated ratios from Node 1 and Node 2 into Node 3
    node3_output = node3_risk_matrix.main(
        click_rate_input=node1_output["click_rate_percentage"],
        reporting_rate_input=node2_output["reporting_rate_percentage"]
    )
    
    print("✅ Node 3 Success: Corporate risk profile successfully evaluated.")

    # =========================================================================
    # CONSOLIDATED END RESPONSE REPORT
    # =========================================================================
    print("\n" + "=" * 60)
    print("📊 CONSOLIDATED EXECUTIVE CYBERSECURITY REPORT")
    print("=" * 60)
    
    final_json_report = {
        "pipeline_metadata": {
            "initial_log_records": node1_output["original_rows"],
            "cleaned_unique_targets": node1_output["final_rows"],
            "inflated_records_purged": node1_output["removed_duplicates"]
        },
        "performance_metrics": {
            "email_open_rate": f"{node1_output['open_rate_percentage']}%",
            "link_click_rate": f"{node1_output['click_rate_percentage']}%",
            "employee_reporting_rate": f"{node2_output['reporting_rate_percentage']}%"
        },
        "security_posture": {
            "assigned_scenario": node3_output["scenario"],
            "risk_tier": node3_output["label"],
            "posture_description": node3_output["description"]
        }
    }
    
    print(json.dumps(final_json_report, indent=4, ensure_ascii=False))
    print("=" * 60)
    print("🚀 PIPELINE EXECUTED SUCCESSFULLY WITHOUT CHARACTER LIMIT OVERHEAD")
    print("=" * 60)


if __name__ == "__main__":
    # --- LOCAL RUNTIME ENVIRONMENT SETUP ---
    # Ensure you create these dummy or sample CSVs inside your project folder to test!
    CAMPAIGN_CSV_SAMPLE = "data_samples/campaign_data.csv"
    REPORTING_CSV_SAMPLE = "data_samples/reporting_data.csv"
    
    # To run this script locally outside of Dify servers, you can mock or adjust 
    # the 'requests.get' method in Node 1 and 2 to point to built-in open() functions,
    # or test the JSON payloads inside an automated PyTest suite.
    
    # Example simulation execution:
    try:
        run_pipeline(CAMPAIGN_CSV_SAMPLE, REPORTING_CSV_SAMPLE)
    except Exception as global_err:
        print(f"\n[Environment Warning] Local test require mocking the network 'requests.get' function to bypass server downloads: {global_err}")

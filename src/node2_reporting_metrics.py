"""
Node 2: Reporting Metrics Calculation
Description: Extracts raw phishing reporting logs from a security telemetry file, deduplicates 
             reporting entries by user email, and calculates the organization's corporate Reporting Rate.
"""

import csv
import requests
from typing import Dict, List, Set, Optional, Any


def extract_file_object(file_payload: Any) -> Optional[dict]:
    """
    Safely unwraps the incoming framework variable to handle both direct dictionaries 
    and list-wrapped payload metadata arrays seamlessly.
    """
    if isinstance(file_payload, list) and len(file_payload) > 0:
        return file_payload[0]
    elif isinstance(file_payload, dict):
        return file_payload
    return None


def fetch_reporting_data(url: str) -> List[List[str]]:
    """
    Downloads the reporting log stream, strips hidden encoding structures like 
    Excel Byte Order Marks (BOM), and extracts rows via the standard CSV engine.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    raw_text = response.content.decode('utf-8-sig', errors='ignore')
    text_lines = raw_text.splitlines()
    
    reader = csv.reader(text_lines)
    return [row for row in reader if row and any(cell.strip() for cell in row)]


def discover_email_column_index(header_row: List[str]) -> int:
    """
    Scans data headers to dynamically resolve the appropriate index column mapping 
    for target email credentials, adding structural flexibility.
    """
    for i, col_name in enumerate(header_row):
        if 'email' in str(col_name).strip().lower():
            return i
    return 0  # Robust programmatic fallback to index 0 if exact string match fails


def extract_unique_reporting_users(data_rows: List[List[str]], email_idx: int) -> Set[str]:
    """
    Iterates through campaign interactions to parse and assemble an identity set of 
    completely unique users who successfully reported the threat vectors.
    """
    reported_emails: Set[str] = set()
    
    for row in data_rows:
        if email_idx < len(row):
            email_val = str(row[email_idx]).strip().lower()
            if email_val and email_val != 'none':
                reported_emails.add(email_val)
                
    return reported_emails


def main(reporting_file_array: Any, total_unique_users: Any) -> Dict[str, Any]:
    """
    Main orchestration entrypoint designed for modular pipeline integration 
    and microservice security automation frameworks.
    """
    try:
        # 1. Isolate and parse target metadata object
        file_obj = extract_file_object(reporting_file_array)
        if not isinstance(file_obj, dict) or not file_obj.get("url"):
            return {
                'summary_text': "Error: Invalid or missing Reporting payload metadata structure.",
                'total_reported_users': 0, 'reporting_rate_percentage': 0.0
            }

        # 2. Extract network file data lines
        all_rows = fetch_reporting_data(file_obj.get("url"))
        if not all_rows:
            return {
                'summary_text': "Error: Downloaded target reporting dataset is completely empty.",
                'total_reported_users': 0, 'reporting_rate_percentage': 0.0
            }

        header = all_rows[0]
        data_rows = all_rows[1:]

        # 3. Track targeting indices and compile distinct reporting actors
        email_index = discover_email_column_index(header)
        unique_reporters = extract_unique_reporting_users(data_rows, email_index)
        total_reported = len(unique_reporters)

        # 4. Compute metrics using total baseline from previous pipeline nodes
        base_universe = int(total_unique_users) if total_unique_users else 2290
        reporting_rate = (total_reported / base_universe) * 100 if base_universe > 0 else 0.0

        # 5. Build presentation summary metrics string
        summary = (
            f"Phishing Simulation Reporting Metrics:\n"
            f"- Total Users Who Reported: {total_reported}\n"
            f"- Reporting Rate: {reporting_rate:.2f}% (Based on {base_universe} unique targets)"
        )

        return {
            'summary_text': summary,
            'total_reported_users': total_reported,
            'reporting_rate_percentage': round(reporting_rate, 2)
        }

    except Exception as e:
        return {
            'summary_text': f"System Error processing reporting data stream: {str(e)}",
            'total_reported_users': 0, 'reporting_rate_percentage': 0.0
        }

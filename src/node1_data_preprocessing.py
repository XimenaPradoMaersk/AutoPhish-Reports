"""
Node 1: Deduplication & Core Metrics
Description: Extracts raw phishing logs from a dynamic storage URL, deduplicates data using 
             a priority-based interaction matrix, and computes primary campaign KPIs.
"""

import csv
import io
import requests
from typing import Dict, List, Optional, Any


def find_file_url(obj: Any) -> Optional[str]:
    """
    Recursively scans the input object structure to dynamically locate the file download URL,
    making the pipeline resilient to variations in low-code platform payload schemas.
    """
    if isinstance(obj, dict):
        if "url" in obj and obj["url"]:
            return obj["url"]
        for val in obj.values():
            result = find_file_url(val)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_file_url(item)
            if result:
                return result
    return None


def fetch_and_parse_csv(url: str) -> List[List[str]]:
    """
    Downloads the remote CSV binary stream, handles bytecode decoding, and parses 
    it safely into a structured multidimensional list of row strings.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    # Decodes handling hidden Excel Byte Order Mark (BOM) patterns gracefully
    raw_text = response.content.decode('utf-8-sig', errors='ignore')
    text_lines = raw_text.splitlines()
    
    reader = csv.reader(text_lines, delimiter=',')
    return [row for row in reader if row and any(cell.strip() for cell in row)]


def extract_highest_priority_interactions(data_rows: List[List[str]], email_idx: int, response_idx: int) -> List[List[str]]:
    """
    Applies the core business logic to eliminate transaction duplicates. 
    Maintains only the highest-value conversion milestone per unique employee.
    
    Hierarchy Matrix: Link clicked (3) > Mail opened (2) > Delivered (1) > Bounced/Other (0)
    """
    best_rows: Dict[str, tuple] = {}

    for row in data_rows:
        if email_idx >= len(row):
            continue
            
        email = str(row[email_idx]).strip().lower()
        if not email or email in ['none', '']:
            continue

        response_val = str(row[response_idx]).strip().lower() if response_idx < len(row) else ''

        # Map current action to priority levels
        if 'click' in response_val:
            current_priority = 3
        elif 'open' in response_val:
            current_priority = 2
        elif 'deliver' in response_val:
            current_priority = 1
        else:
            current_priority = 0

        # Enforce transaction supremacy inside the user dictionary map
        if email not in best_rows or current_priority > best_rows[email][0]:
            best_rows[email] = (current_priority, row)

    return [item[1] for item in best_rows.values()]


def chunk_output_text(csv_string: str, chunk_size: int = 100000) -> List[str]:
    """
    Splits a large string payload into smaller bounded segments to comply 
    with variable length constraint boundaries of low-code workflow platforms.
    """
    return [csv_string[i:i + chunk_size] for i in range(0, len(csv_string), chunk_size)]


def main(arg1: Any) -> Dict[str, Any]:
    """
    Main orchestration function compatible with serverless workflows and Dify Python steps.
    """
    try:
        # 1. Resolve storage resource location
        file_url = find_file_url(arg1)
        if not file_url:
            return {
                'output': [], 'removed_duplicates': 0, 'final_rows': 0, 'original_rows': 0,
                'total_clicks': 0, 'total_opens': 0, 'click_rate_percentage': 0, 'open_rate_percentage': 0,
                'summary_text': f"Error: No valid download URL detected in input object framework."
            }

        # 2. Acquire and structure source dataset
        all_rows = fetch_and_parse_csv(file_url)
        if not all_rows:
            return {
                'output': [], 'removed_duplicates': 0, 'final_rows': 0, 'original_rows': 0,
                'total_clicks': 0, 'total_opens': 0, 'click_rate_percentage': 0, 'open_rate_percentage': 0,
                'summary_text': 'Error: Downloaded target CSV file contains no valid rows.'
            }

        header = all_rows[0]
        data_rows = all_rows[1:]
        original_count = len(data_rows)

        # Verified schema indices matching standard telemetry files
        EMAIL_INDEX = 1
        RESPONSE_INDEX = 4

        # 3. Process records and deduplicate
        unique_rows = extract_highest_priority_interactions(data_rows, EMAIL_INDEX, RESPONSE_INDEX)
        final_count = len(unique_rows)
        removed_count = original_count - final_count

        # 4. Aggregate core behavioral analytics metrics
        clicks_count = 0
        opens_count = 0
        
        for row in unique_rows:
            res_val = str(row[RESPONSE_INDEX]).strip().lower() if RESPONSE_INDEX < len(row) else ''
            if 'click' in res_val:
                clicks_count += 1
                opens_count += 1
            elif 'open' in res_val:
                opens_count += 1

        click_rate = (clicks_count / final_count) * 100 if final_count > 0 else 0.0
        open_rate = (opens_count / final_count) * 100 if final_count > 0 else 0.0

        # 5. Build presentation metrics text
        summary = (
            f"Phishing Simulation Analytics Report:\n"
            f"- Total Unique Target Users Evaluated: {final_count}\n"
            f"- Email Open Successes: {opens_count} ({open_rate:.2f}% Open Rate)\n"
            f"- Phishing Links Clicked: {clicks_count} ({click_rate:.2f}% Click Rate)"
        )

        # 6. Re-serialize clean target array into text bytes stream
        output_stream = io.StringIO()
        writer = csv.writer(output_stream, delimiter=',')
        writer.writerow(header)       
        writer.writerows(unique_rows)  
        
        # 7. Package and segment telemetry to prevent workflow limit overhead exceptions
        chunks_list = chunk_output_text(output_stream.getvalue())

        return {
            'output': chunks_list,
            'removed_duplicates': removed_count,
            'final_rows': final_count,
            'original_rows': original_count,
            'total_clicks': clicks_count,
            'total_opens': opens_count,
            'click_rate_percentage': round(click_rate, 2),
            'open_rate_percentage': round(open_rate, 2),
            'summary_text': summary
        }

    except Exception as e:
        return {
            'output': [], 'removed_duplicates': 0, 'final_rows': 0, 'original_rows': 0,
            'total_clicks': 0, 'total_opens': 0, 'click_rate_percentage': 0, 'open_rate_percentage': 0,
            'summary_text': f"Critical processing failure on Node 1 thread: {str(e)}"
        }

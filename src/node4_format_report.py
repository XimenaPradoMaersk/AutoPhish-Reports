def format_phishing_report(data):
    """
    Formats phishing metrics into a structured report.
    """

    try:
        report = f"""
📊 Phishing Analytics Report:

• Total Users: {data.get('Total_Users', 0)}
• Total Opens: {data.get('Total_Opens', 0)}
• Open Rate: {data.get('Open_Rate', 0)}%

• Total Clicks: {data.get('Total_Clicks', 0)}
• Click Rate: {data.get('Click_Rate', 0)}%

• Total Reports: {data.get('Total_Reports', 0)}
• Reporting Rate: {data.get('Reporting_Rate', 0)}%

• Scenario: {data.get('Scenario', 'N/A')}
• Risk Level: {data.get('Risk_Level', 'Unknown')}
"""
        return report.strip()

    except Exception as e:
        return f"Error generating report: {str(e)}"

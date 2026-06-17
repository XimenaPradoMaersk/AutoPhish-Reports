"""
Metrics Calculation Module

This script calculates key phishing metrics from processed data:
- Total users
- Clicked users
- Click rate

This represents logic originally implemented in a Dify code node.
"""


def calculate_click_metrics(data):
    """
    Calculate click-related metrics from phishing dataset

    :param data: List of dictionaries (processed user data)
    :return: Dictionary with calculated metrics
    """

    if not data:
        return {
            "total_users": 0,
            "clicked_users": 0,
            "click_rate": 0
        }

    total_users = len(data)
    clicked_users = 0

    for row in data:
        response = str(row.get("Response", "")).strip().lower()

        if response == "link clicked":
            clicked_users += 1

    click_rate = (clicked_users / total_users) * 100 if total_users > 0 else 0

    return {
        "total_users": total_users,
        "clicked_users": clicked_users,
        "click_rate": round(click_rate, 2)
    }


def main():
    # ✅ Example test data (for demo purposes)
    sample_data = [
        {"Email": "user1@test.com", "Response": "Link clicked"},
        {"Email": "user2@test.com", "Response": "Opened"},
        {"Email": "user3@test.com", "Response": "Delivered"},
        {"Email": "user4@test.com", "Response": "Link clicked"},
    ]

    results = calculate_click_metrics(sample_data)

    print("✅ Total Users:", results["total_users"])
    print("✅ Clicked Users:", results["clicked_users"])
    print("✅ Click Rate:", f"{results['click_rate']}%")



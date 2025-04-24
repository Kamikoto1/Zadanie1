import mysql.connector
import csv
import sys
from datetime import datetime, timedelta

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root",
        database="mydatabase"
    )

def parse_date_range():
    if len(sys.argv) != 3:
        print("Usage: python aggregate_logs.py <start_date> <end_date>")
        print("Example: python aggregate_logs.py 2024-04-01 2024-04-30")
        sys.exit(1)

    try:
        start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)

    if start_date > end_date:
        print("Start date must be before end date.")
        sys.exit(1)

    return start_date, end_date

def aggregate_data(start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    results = []
    prev_total_topics = 0

    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)

        # New accounts
        cursor.execute("""
            SELECT COUNT(*) FROM user_logs 
            WHERE action_type = 'registration' AND action_datetime BETWEEN %s AND %s
        """, (current_date, next_date))
        registrations = cursor.fetchone()[0]

        # All messages
        cursor.execute("""
            SELECT COUNT(*) FROM user_logs 
            WHERE action_type = 'post_message' AND action_datetime BETWEEN %s AND %s
        """, (current_date, next_date))
        total_messages = cursor.fetchone()[0]

        # Anonymous messages
        cursor.execute("""
            SELECT COUNT(*) FROM user_logs 
            WHERE action_type = 'post_message' AND user_id IS NULL AND action_datetime BETWEEN %s AND %s
        """, (current_date, next_date))
        anon_messages = cursor.fetchone()[0]

        anon_percent = (anon_messages / total_messages * 100) if total_messages > 0 else 0

        # Total topics (cumulative by that day)
        cursor.execute("""
            SELECT COUNT(*) FROM user_logs 
            WHERE action_type = 'create_topic' AND action_datetime <= %s
        """, (next_date,))
        total_topics = cursor.fetchone()[0]

        # Relative topic growth
        if prev_total_topics == 0:
            topic_growth_percent = 0.0
        else:
            topic_growth_percent = ((total_topics - prev_total_topics) / prev_total_topics) * 100

        results.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "new_accounts": registrations,
            "anonymous_message_percent": round(anon_percent, 2),
            "total_messages": total_messages,
            "topic_growth_percent": round(topic_growth_percent, 2)
        })

        prev_total_topics = total_topics
        current_date = next_date

    cursor.close()
    conn.close()
    return results

def write_to_csv(data, filename="aggregated_forum_data.csv"):
    with open(filename, mode="w", newline="") as csv_file:
        fieldnames = ["date", "new_accounts", "anonymous_message_percent", "total_messages", "topic_growth_percent"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Data written to {filename}")

if __name__ == "__main__":
    start_date, end_date = parse_date_range()
    aggregated = aggregate_data(start_date, end_date)
    write_to_csv(aggregated)
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def create_date_frequency_graph(json_data):
    # Extract dates from the JSON data
    dates = [entry['date'] for entry in json_data]

    # Convert dates to datetime objects
    dates = pd.to_datetime(dates)

    # Count frequency of each date
    date_counts = dates.value_counts().sort_index()

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Create bar plot
    ax = date_counts.plot(kind='bar')

    # Customize the plot
    plt.title('Number of Executive Orders by Date (January 2025)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Executive Orders', fontsize=12)

    # Format x-axis labels to show only dates
    ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in date_counts.index], rotation=45, ha='right')
    # Rotate x-axis labels for better readability
    # plt.xticks(rotation=45, ha='right')

    # Add grid lines
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot
    plt.savefig('executive_orders_by_date.png')
    print(f"Created graph showing {len(json_data)} executive orders across {len(date_counts)} dates")
    print(f"Date distribution:")
    for date, count in date_counts.items():
        print(f"{date.strftime('%Y-%m-%d')}: {count} orders")

# Example usage
if __name__ == "__main__":
    import json

    # Load the JSON data
    with open('./documents_scraped.json', 'r') as f:
        data = json.load(f)

    create_date_frequency_graph(data)

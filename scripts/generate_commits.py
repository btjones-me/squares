#!/usr/bin/env python3
"""
Generate realistic commit timestamps across the last 400 days.
Weekday-biased distribution (more commits on weekdays).
"""

import json
import random
from datetime import datetime, timedelta


def generate_commits(num_commits=30, days_back=400):
    """
    Generate commit timestamps with weekday bias.
    
    Args:
        num_commits: Number of commits to generate
        days_back: How many days back to look
    
    Returns:
        List of commit dictionaries with date, timestamp, and message
    """
    commits = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Generate all possible dates in the range
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date.date())
        current_date += timedelta(days=1)
    
    # Weight weekdays more heavily (Mon-Fri: 5x, Sat-Sun: 1x)
    weighted_dates = []
    for date in all_dates:
        weekday = date.weekday()  # 0=Monday, 6=Sunday
        weight = 5 if weekday < 5 else 1
        weighted_dates.extend([date] * weight)
    
    # Select random dates with replacement (allows multiple commits per day)
    selected_dates = random.choices(weighted_dates, k=num_commits)
    
    # Generate timestamps for each date
    for date in selected_dates:
        # Random time during work hours (9 AM - 6 PM) with some variation
        hour = random.randint(9, 24)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        timestamp = datetime.combine(date, datetime.min.time().replace(
            hour=hour, minute=minute, second=second
        ))
        
        commits.append({
            "date": date.isoformat(),
            "timestamp": timestamp.isoformat(),
            "message": "update data.csv"
        })
    
    # Sort by timestamp
    commits.sort(key=lambda x: x["timestamp"])
    
    return commits


def main():
    """Generate commits.json file."""
    commits = generate_commits(num_commits=30, days_back=400)
    
    output_file = "commits.json"
    with open(output_file, "w") as f:
        json.dump(commits, f, indent=2)
    
    print(f"Generated {len(commits)} commits and saved to {output_file}")
    print(f"Date range: {commits[0]['date']} to {commits[-1]['date']}")


if __name__ == "__main__":
    main()


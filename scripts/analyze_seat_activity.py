#!/usr/bin/env python3
"""
Seat Activity Analyzer

This script analyzes seat activity CSV files and calculates the percentage
of active users. A user is considered active if they have activity within the last 60 days.
"""

import csv
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def analyze_seat_activity(csv_path: str) -> dict:
    """
    Analyze a seat activity CSV file.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Dictionary containing analysis results
    """
    total_users = 0
    active_users = 0
    inactive_users = 0
    
    # Calculate the cutoff date (60 days ago from now)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=60)
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            total_users += 1
            last_activity = row.get('Last Activity At', '').strip()
            
            if last_activity and last_activity.lower() != 'none':
                try:
                    # Parse the ISO 8601 date format (e.g., "2025-12-01T19:59:43Z")
                    activity_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                    
                    if activity_date >= cutoff_date:
                        active_users += 1
                    else:
                        inactive_users += 1
                except (ValueError, AttributeError):
                    # If date parsing fails, consider as inactive
                    inactive_users += 1
            else:
                inactive_users += 1
    
    active_percentage = (active_users / total_users * 100) if total_users > 0 else 0
    inactive_percentage = (inactive_users / total_users * 100) if total_users > 0 else 0
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'active_percentage': active_percentage,
        'inactive_percentage': inactive_percentage,
        'cutoff_date': cutoff_date
    }


def main():
    """Main function to run the analysis."""
    # Default CSV file path
    script_dir = Path(__file__).parent
    csv_file = script_dir / 'seat-activity.csv'
    
    # Allow custom CSV path as command line argument
    if len(sys.argv) > 1:
        csv_file = Path(sys.argv[1])
    
    if not csv_file.exists():
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)
    
    print(f"Analyzing: {csv_file.name}")
    print("-" * 60)
    
    results = analyze_seat_activity(str(csv_file))
    
    cutoff_date_str = results['cutoff_date'].strftime('%Y-%m-%d')
    print(f"\nActivity cutoff date: {cutoff_date_str} (60 days ago)")
    print(f"\nTotal Users:      {results['total_users']:,}")
    print(f"Active Users:     {results['active_users']:,} ({results['active_percentage']:.2f}%)")
    print(f"Inactive Users:   {results['inactive_users']:,} ({results['inactive_percentage']:.2f}%)")
    print("-" * 60)
    print(f"\n✓ Active user percentage: {results['active_percentage']:.2f}%")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Debug script to test date validation logic
"""

from datetime import date, datetime

# Test current date
print("=== Date Validation Debug ===")
print(f"Local date.today(): {date.today()}")
print(f"Local datetime.now(): {datetime.now()}")

# Test the specific dates we're trying
test_dates = ['2024-12-20', '2024-12-25', '2025-01-15']
print("\n=== Testing specific dates ===")
for date_str in test_dates:
    test_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    print(f"Test date: {test_date}")
    print(f"Is {test_date} < {date.today()}? {test_date < date.today()}")
    print(f"Comparison: {test_date} vs {date.today()}")
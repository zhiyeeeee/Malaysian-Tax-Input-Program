import pandas as pd
import os

# Constants for tax relief caps
MAX_CHILDREN = 12
MAX_MEDICAL = 8000
MAX_LIFESTYLE = 2500
MAX_EDUCATION = 7000
MAX_PARENTAL = 5000
FILENAME = "tax_records.csv"

# ---------------- User Functions ---------------- #

def verify_user(ic_number, password):
    """Verify password by matching last 4 digits of IC number."""
    return len(ic_number) == 12 and password == ic_number[-4:]

def is_user_registered(ic_number,FILENAME):
    """Check if user IC exists in CSV file."""
    if os.path.isfile(FILENAME):
        df = pd.read_csv(FILENAME)
        return ic_number in df['IC Number'].astype(str).values
    return False

def remove_existing_ic(ic_number):
    """Remove existing IC record from CSV (used before saving new)."""
    FILENAME= "tax_records.csv"
    if os.path.isfile(FILENAME):
        df = pd.read_csv(FILENAME)
        df = df[df['IC Number'].astype(str) != (ic_number)]
        df.to_csv(FILENAME, index=False)

# ---------------- Tax Logic ---------------- #

def calculate_tax():
    """Prompt user for reliefs and calculate tax."""
    income = float(input("Enter your annual income (RM): "))

    print("👉 Answer the following to calculate your tax relief:")

    individual = 9000
    spouse = int(input("Spouse with income < RM4,000? (1 = Yes, 0 = No): ")) * 4000
    children = min(int(input(f"Number of children (max {MAX_CHILDREN}): ")), MAX_CHILDREN) * 8000
    medical = min(float(input(f"Medical expenses (max {MAX_MEDICAL}): ")), MAX_MEDICAL)
    lifestyle = min(float(input(f"Lifestyle items (max {MAX_LIFESTYLE}): ")), MAX_LIFESTYLE)
    education = min(float(input(f"Education fees (max {MAX_EDUCATION}): ")), MAX_EDUCATION)
    parental = min(float(input(f"Parental care (max {MAX_PARENTAL}): ")), MAX_PARENTAL)

    total_relief = individual + spouse + children + medical + lifestyle + education + parental
    taxable_income = max(0, income - total_relief)

    tax_payable = calculate_malaysian_tax(taxable_income)
    return income, total_relief, tax_payable

def calculate_malaysian_tax(income):
    """Apply Malaysia progressive tax rates."""
    brackets = [
        (5000, 0.01), (15000, 0.03), (15000, 0.06), (15000, 0.11),
        (20000, 0.19), (30000, 0.25), (50000, 0.26),
        (100000, 0.28), (float('inf'), 0.30)
    ]

    tax = 0
    remaining = income

    for amount, rate in brackets:
        if remaining <= 0:
            break
        taxable = min(remaining, amount)
        tax += taxable * rate
        remaining -= taxable

    return tax

# ---------------- CSV Handling ---------------- #

def save_to_csv(data,FILENAME):
    """Append new tax data to CSV file."""
    df = pd.DataFrame([data])
    if not os.path.isfile(FILENAME):
        df.to_csv(FILENAME, index=False)
    else:
        df.to_csv(FILENAME, mode='a', header=False, index=False)

def file_read_from_csv(FILENAME):
    """Read all tax records from CSV."""
    if os.path.isfile(FILENAME):
        return pd.read_csv(FILENAME,dtype={'IC Number':str})
    else:
        return None

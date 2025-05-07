import pandas as pd
import os

# Verifies user by checking IC number and last 4 digits as password
def verify_user(ic_number, password):
    return len(ic_number) == 12 and password == ic_number[-4:]

def is_user_registered(ic_number, filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        return ic_number in df['IC Number'].astype(str).values
    return False


# Calculates tax relief and tax payable based on Malaysian income tax rates
def calculate_tax():
    income = float(input("Enter your annual income (RM): "))
    
    print("Answer the following to calculate your tax relief:")

    individual = 9000
    spouse = int(input("Spouse with income < RM4,000? (1 = Yes, 0 = No): ")) * 4000
    children = min(int(input("Number of children (max 12)? ")), 12) * 8000
    medical = min(float(input("Medical expenses (max 8000): ")), 8000)
    lifestyle = min(float(input("Lifestyle items (max 2500): ")), 2500)
    education = min(float(input("Education fees (max 7000): ")), 7000)
    parental = min(float(input("Parental care (max 5000): ")), 5000)

    total_relief = individual + spouse + children + medical + lifestyle + education + parental
    taxable_income = income - total_relief
    taxable_income = max(0, taxable_income)

    # Malaysia LHDN Tax Brackets (2023–2025)
    tax_payable = 0
    remaining = taxable_income

    brackets = [
        (5000, 0.01),
        (15000, 0.03),
        (15000, 0.06),
        (15000, 0.11),
        (20000, 0.19),
        (30000, 0.25),
        (50000, 0.26),
        (100000, 0.28),
        (float('inf'), 0.30)
    ]

    for amount, rate in brackets:
        if remaining <= 0:
            break
        taxable = min(remaining, amount)
        tax_payable += taxable * rate
        remaining -= taxable

    return income, total_relief, tax_payable

# Saves data (as dictionary) to a CSV file using pandas
def save_to_csv(data, filename):
    df = pd.DataFrame([data])
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# Reads CSV file and returns data as DataFrame
def file_read_from_csv(filename):
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return None

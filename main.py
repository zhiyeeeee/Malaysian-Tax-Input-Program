from functions import verify_user, is_user_registered, calculate_tax, save_to_csv, file_read_from_csv
import pandas as pd
import os

FILENAME = "tax_records.csv"

# Optional: Ensure old IC data is removed before saving new
def remove_existing_ic(ic_number):
    if os.path.isfile(FILENAME):
        df = pd.read_csv(FILENAME)
        df = df[df['IC Number'].astype(str) != str(ic_number)]
        df.to_csv(FILENAME, index=False)

def main():
    print("📌 Welcome to Malaysian Tax Input Program")

    # Step 1: Prompt for User ID and password
    ic = input("Enter your User ID (12-digit IC number): ").strip()
    pwd = input("Enter your password (last 4 digits of IC): ").strip()

    # Step 2: Validate IC format
    if not ic.isdigit() or len(ic) != 12:
        print("❌ Invalid IC format. Must be 12 digits.")
        return

    # Step 3: Check registration and verify user
    if is_user_registered(ic, FILENAME):
        if not verify_user(ic, pwd):
            print("❌ Incorrect password. Access denied.")
            return
        else:
            print("✅ Login successful.")
            remove_existing_ic(ic)  # Remove old record if updating
    else:
        if verify_user(ic, pwd):
            print("✅ Registration successful.")
        else:
            print("❌ Registration failed. Password must match last 4 digits of IC.")
            return

    # Step 4: Income & Tax Input
    income, relief, tax = calculate_tax()

    # Step 5: Display Summary
    print(f"\n📄 Summary for {ic}:")
    print(f"🧾 Income: RM {income:.2f}")
    print(f"📉 Tax Relief: RM {relief:.2f}")
    print(f"💰 Tax Payable: RM {tax:.2f}")

    # Step 6: Save to CSV (overwrite if exists)
    data = {
        "IC Number": ic,
        "Income (RM)": income,
        "Tax Relief (RM)": relief,
        "Tax Payable (RM)": round(tax, 2)
    }

    save_to_csv(data, FILENAME)
    print("\n✅ Tax record saved successfully.")

    # Step 7: Display all tax records
    print("\n📊 All Tax Records:")
    df = file_read_from_csv(FILENAME)
    if df is not None:
        print(df.to_string(index=False))
    else:
        print("No records found.")

if __name__ == "__main__":
    main()

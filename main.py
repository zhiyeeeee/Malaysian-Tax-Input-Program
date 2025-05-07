from functions import verify_user, is_user_registered, calculate_tax, save_to_csv, file_read_from_csv

FILENAME = "tax_records.csv"

def main():
    print("📌 Welcome to Malaysian Tax Input Program")

     # Step 1: Prompt for User ID and password
    ic_number = input("Enter your User ID (12-digit IC number): ").strip()
    password = input("Enter your password (last 4 digits of IC): ").strip()

    # Step 2: Check registration
    if is_user_registered(ic_number, FILENAME):
        # User exists, verify password
        if verify_user(ic_number, password):
            print("✅ Login successful.")
        else:
            print("❌ Incorrect password. Access denied.")
            return
    else:
        # User not registered, ask for registration
        print("🔒 You are not registered. Let's register you.")
        if password == ic_number[-4:]:
            print("✅ Registration successful.")
        else:
            print("❌ Registration failed. Password must match last 4 digits of IC.")
            return

    # Step 3: User enter income and Calculate tax
    income, relief, tax = calculate_tax()

    # Step 4: Display summary
    print(f"\n📄 Summary for {ic_number}:")
    print(f"🧾 Income: RM {income:.2f}")
    print(f"📉 Tax Relief: RM {relief:.2f}")
    print(f"💰 Tax Payable: RM {tax:.2f}")

    # Step 5: Save tax records to CSV
    tax_data = {
        "IC Number": ic_number,
        "Income (RM)": income,
        "Tax Relief (RM)": relief,
        "Tax Payable (RM)": round(tax, 2)
    }

    save_to_csv(tax_data, FILENAME)
    print("\n✅ Tax record saved.")

    # Step 6: Display all tax records
    print("\n📊 All Tax Records:")
    df = file_read_from_csv(FILENAME)
    if df is not None:
        print(df.to_string(index=False))
    else:
        print("No records found.")

if __name__ == "__main__":
    main()

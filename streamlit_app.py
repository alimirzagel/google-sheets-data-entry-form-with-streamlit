import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title
st.title("Vendor Management Portal")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Login Section
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "your_username" and password == "your_password":  # Replace with actual username and password
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
else:
    # Display Action Options
    action = st.selectbox("Choose an Action", ["Summary", "Entry"])

    # Account Heads Dropdown Options
    ACCOUNT_HEADS = [
        "Site Expense - Local Purchase",
        "Site Expenses - Safety",
        "Office - Safety",
        "Site Transport - 4 Wheeler Hire Charges",
        "Site Expenses-Others - Consultancy - Professional Services",
        "Site Expenses-Survey",
        "Site Maintenance - Repair & Maintenance",
        "Site Expenses - Freight & Transport Charges",
        "Site Expenses - Packing & Forwarding",
        "Site Expenses - EPC Full I&C",
        "Site Expenses-System Config.",
        "Site Expenses-Mobilisation",
        "Site Expenses-Inspection",
        "Site Expenses-Electrical - Supply, Installation, Comissioning & Testing",
        "Site Expenses-Civil-Construction,Installation",
        "Site Expenses - Statutory Expense",
        "Site Expenses-Security",
        "Site Expenses-Labour",
        "Site Expenses-Rental Charges (JCB, Hydra, etc.)",
        "Office - Freight & Transport Charges",
        "Site Guest House - Rent",
        "Site Guest House - Maintenance",
        "Site Guest House - Electricity Bill",
        "Site Travel",
        "Site Travel - Accommodation",
        "Site Travel - Food",
        "Site Expenses - Printing & Stationary",
        "Site Expenses - Postage & Courier Charges",
        "Site Expenses - Communication Expense",
        "Site Expenses - Staff Welfare",
        "Site Expenses - Training",
        "Office - Printing & Stationary",
        "Office - Postage & Courier Charges",
        "Office - Staff Welfare",
        "Office - Training",
        "Office - Travel",
        "Office - Accommodation",
        "Office - Food",
        "Office - Toll, Parking",
        "Site Expenses-Credit Report and Facility Management",
        "Office - Legal & Compliance Expenses GL Code",
        "Site Expenses - CRM"
    ]

    # Summary Page
    if action == "Summary":
        st.header("Summary Page")
        st.dataframe(existing_data)

    # Entry Page
    elif action == "Entry":
        st.header("Entry Page")
        with st.form(key="entry_form"):
            name = st.text_input("Name")
            purchase_period = st.date_input("Purchase for Period")
            total_amount = st.number_input("Total Amount", min_value=0.0)
            st.markdown("### Entry Details")
            entry_table = st.empty()
            entry_data = []
            if st.button("Add Row"):
                entry_data.append({
                    "Sr. No.": len(entry_data) + 1,
                    "Bill No": st.text_input(f"Bill No {len(entry_data) + 1}"),
                    "Date": st.date_input(f"Date {len(entry_data) + 1}"),
                    "Name of the Vendor": st.text_input(f"Name of the Vendor {len(entry_data) + 1}"),
                    "Description": st.text_input(f"Description {len(entry_data) + 1}"),
                    "Account Head": st.selectbox(f"Account Head {len(entry_data) + 1}", ACCOUNT_HEADS),
                    "GL code": st.text_input(f"GL code {len(entry_data) + 1}"),
                    "Type": st.text_input(f"Type {len(entry_data) + 1}"),
                    "Amount": st.number_input(f"Amount {len(entry_data) + 1}", min_value=0.0),
                    "Bill Status": st.text_input(f"Bill Status {len(entry_data) + 1}"),
                    "Upload Bill": st.file_uploader(f"Upload Bill {len(entry_data) + 1}")
                })
                entry_table.write(pd.DataFrame(entry_data))

            if st.form_submit_button("Submit"):
                if not name or not purchase_period or not total_amount or not entry_data:
                    st.warning("Please fill in all required fields.")
                else:
                    # Prepare data for Google Sheets
                    new_data = pd.DataFrame([{
                        "Name": name,
                        "Purchase Period": purchase_period.strftime("%Y-%m"),
                        "Total Amount": total_amount,
                        **{f"Row {i+1}": entry for i, entry in enumerate(entry_data)}
                    }])
                    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                    conn.update(worksheet="Entries", data=updated_df)
                    st.success("Entry successfully submitted!")
                    st.experimental_rerun()

# Logout
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

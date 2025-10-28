import pandas as pd
import streamlit as st

st.title("Dealer Duplicate Checker")

# --- Upload files ---
potential_file = st.file_uploader("Upload Potential Dealers file", type=["csv", "xls", "xlsx"])
current_file = st.file_uploader("Upload Current Dealers file", type=["csv", "xls", "xlsx"])

# --- Helper: read any Excel or CSV file safely ---
def read_any(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# --- Helper: find likely column name from list of keywords ---
def find_col(df, keywords):
    for col in df.columns:
        name = col.lower().strip()
        for word in keywords:
            if word in name:
                return col
    return None

# --- Main logic ---
if potential_file and current_file:
    potential = read_any(potential_file)
    current = read_any(current_file)

    # Normalize column names (remove spaces, lowercase)
    potential.columns = potential.columns.str.strip().str.lower()
    current.columns = current.columns.str.strip().str.lower()

    # Detect likely email and company columns
    potential_email_col = find_col(potential, ["email", "e-mail"])
    current_email_col = find_col(current, ["email", "e-mail"])

    potential_company_col = find_col(potential, ["company", "dealer", "shop", "store", "business"])
    current_company_col = find_col(current, ["company", "dealer", "shop", "store", "business"])

    # Optional: try to find helpful context columns for email personalization
    contact_name_col = find_col(potential, ["contact", "owner", "manager", "name"])
    city_col = find_col(potential, ["city", "town"])
    state_col = find_col(potential, ["state", "province", "region"])
    website_col = find_col(potential, ["website", "url"])

    if not potential_email_col or not current_email_col:
        st.error("Could not find an email column in one or both files.")
    else:
        # Extract email domains
        potential["domain"] = potential[potential_email_col].fillna("").str.lower().str.split("@").str[-1]
        current["domain"] = current[current_email_col].fillna("").str.lower().str.split("@").str[-1]

        # Flag duplicates
        potential["duplicate_domain"] = potential["domain"].isin(current["domain"])

        # Optional: flag company duplicates
        if potential_company_col and current_company_col:
            potential["duplicate_company"] = potential[potential_company_col].str.lower().isin(
                current[current_company_col].str.lower()
            )
        else:
            potential["duplicate_company"] = False

        # Combine both checks
        potential["duplicate_flag"] = potential["duplicate_domain"] | potential["duplicate_company"]

        st.success(f"Found {potential['duplicate_flag'].sum()} potential duplicates.")

        # --- 👇 NEW: columns to keep for your ChatGPT email agent ---
        selected_columns = [
            potential_company_col,
            contact_name_col,
            potential_email_col,
            city_col,
            state_col,
            website_col,
            "domain",
            "duplicate_domain",
            "duplicate_company",
            "duplicate_flag"
        ]

        # Remove missing ones (None values)
        selected_columns = [c for c in selected_columns if c in potential.columns]

        cleaned = potential[selected_columns]

        # Show results table in Streamlit
        st.dataframe(cleaned[cleaned["duplicate_flag"]])

        # Downloadable CSV (only selected columns)
        csv = cleaned.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results", csv, "Cleaned_Dealers.csv", "text/csv")

else:
    st.info("Please upload both dealer files to start.")

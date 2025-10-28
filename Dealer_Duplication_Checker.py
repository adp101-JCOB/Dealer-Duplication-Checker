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

    # --- Detect key columns automatically ---
    email_col = find_col(potential, ["email", "e-mail", "mail"])
    company_col = find_col(potential, ["company", "dealer", "shop", "store", "business"])
    website_col = find_col(potential, ["website", "url", "web"])
    contact_name_col = find_col(potential, ["contact", "name", "manager", "owner", "rep"])
    contact_title_col = find_col(potential, ["title", "position", "role"])
    phone_col = find_col(potential, ["phone", "telephone", "mobile"])
    linkedin_col = find_col(potential, ["linkedin", "linkdn", "li"])
    state_col = find_col(potential, ["state", "province", "region"])
    country_col = find_col(potential, ["country", "nation"])

    # --- Duplicate detection (optional) ---
    if not email_col:
        st.error("Could not find an email column in the potential dealers file.")
    else:
        # Extract email domain for comparison
        potential["domain"] = potential[email_col].fillna("").str.lower().str.split("@").str[-1]
        current["domain"] = current[find_col(current, ["email", "e-mail"])].fillna("").str.lower().str.split("@").str[-1]

        potential["duplicate_domain"] = potential["domain"].isin(current["domain"])
        potential["duplicate_flag"] = potential["duplicate_domain"]

        st.success(f"Found {potential['duplicate_flag'].sum()} potential duplicates.")

        # --- Create cleaned export for ChatGPT agent ---
        output_cols = {
            company_col: "Shop Name",
            website_col: "Website",
            email_col: "Email",
            contact_name_col: "Contact Name",
            contact_title_col: "Contact Title",
            phone_col: "Main Phone",
            linkedin_col: "LinkedIn",
            state_col: "State",
            country_col: "Country"
        }

        # Build cleaned dataframe with consistent headers
        cleaned = pd.DataFrame()

        for original, new_name in output_cols.items():
            if original in potential.columns:
                cleaned[new_name] = potential[original]
            else:
                cleaned[new_name] = ""  # blank if not found

        # Show final cleaned data table
        st.dataframe(cleaned)

        # --- Download cleaned, formatted CSV ---
        csv = cleaned.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned Dealers CSV", csv, "Cleaned_Dealers.csv", "text/csv")

else:
    st.info("Please upload both dealer files to start.")

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

    # --- Detect columns in "potential" dataset ---
    col_map = {
        "Shop Name": find_col(potential, ["shop", "dealer", "store", "company", "business", "name"]),
        "Website": find_col(potential, ["website", "url", "web"]),
        "Email": find_col(potential, ["email", "e-mail", "mail"]),
        "Contact Name": find_col(potential, ["contact", "owner", "manager", "person", "rep"]),
        "Contact Title": find_col(potential, ["title", "position", "role"]),
        "Main Phone": find_col(potential, ["phone", "telephone", "mobile"]),
        "State": find_col(potential, ["state", "province", "region"]),
        "Country": find_col(potential, ["country", "nation"]),
    }

    # --- Duplicate detection (optional) ---
    email_col = col_map["Email"]
    if not email_col:
        st.error("Could not find an email column in the potential dealers file.")
    else:
        # Extract email domains to compare
        potential["domain"] = potential[email_col].fillna("").str.lower().str.split("@").str[-1]
        current_email_col = find_col(current, ["email", "e-mail"])
        if current_email_col:
            current["domain"] = current[current_email_col].fillna("").str.lower().str.split("@").str[-1]
            potential["duplicate_flag"] = potential["domain"].isin(current["domain"])
        else:
            potential["duplicate_flag"] = False

        st.success(f"Found {potential['duplicate_flag'].sum()} potential duplicates.")

        # --- Build the cleaned export ---
        cleaned = pd.DataFrame()

        # Always include all 8 requested columns (fill blanks if not found)
        for nice_name, original_col in col_map.items():
            if original_col and original_col in potential.columns:
                cleaned[nice_name] = potential[original_col]
            else:
                cleaned[nice_name] = ""  # blank if not found

        # --- Display and download ---
        st.dataframe(cleaned)
        csv = cleaned.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned Dealers CSV", csv, "Cleaned_Dealers.csv", "text/csv")

else:
    st.info("Please upload both dealer files to start.")

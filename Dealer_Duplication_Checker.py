import pandas as pd
import streamlit as st

st.title("🔍 Dealer Duplicate Checker")

# Upload files
potential_file = st.file_uploader("Upload Potential Dealers CSV", type=["csv"])
current_file = st.file_uploader("Upload Current Dealers CSV", type=["csv"])

if potential_file and current_file:
    potential = pd.read_csv(potential_file)
    current = pd.read_csv(current_file)

    # Make domain columns
    potential["Domain"] = potential["Email"].fillna("").str.lower().str.split("@").str[-1]
    current["Domain"] = current["Email"].fillna("").str.lower().str.split("@").str[-1]

    # Check duplicates
    potential["Domain_Duplicate"] = potential["Domain"].isin(current["Domain"])

    # Show summary
    num_duplicates = potential["Domain_Duplicate"].sum()
    st.success(f"✅ Found {num_duplicates} duplicate domains!")

    # Show duplicates
    st.dataframe(potential[potential["Domain_Duplicate"]])

    # Download option
    csv = potential.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Cleaned CSV", csv, "Clean_Potential_Dealers.csv", "text/csv")
else:
    st.info("👆 Please upload both CSV files to start.")

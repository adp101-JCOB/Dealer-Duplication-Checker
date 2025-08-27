# The apps we are bringing in
import pandas as pd  # bring in the Excel superpowers
from fuzzywuzzy import fuzz


#                                           --- SETTING UP PANDAS DATAFRAMES ---

#STEP 1: Ask the user to type the file paths
POTENTIAL_DEALERS_FILE_PATH = "Potential Dealers (08.24.2025).csv"
CURRENT_DEALERS_FILE_PATH = "Current Dealers (08.24.2025).csv"

#STEP 2: load file paths into pandas: Dataframes gets saved into variables
potential = pd.read_csv(POTENTIAL_DEALERS_FILE_PATH)
current = pd.read_csv(CURRENT_DEALERS_FILE_PATH)

#STEP 3: Show column names
print("POTENTIAL DEALERS: columns")
print(list(potential.columns))
print("CURRENT DEALERS: columns")
print(list(current.columns))



#                                       --- REMOVE DUPLICATE EMAIL DOMAINS ---

#STEP 4: Grab the email domains (the part after "@") from both current and potential dealer lists
current_domains = set(current["Email"].dropna().str.lower().apply(lambda x: x.split("@")[-1]))
potential_domains = set(potential["Email"].dropna().str.lower().apply(lambda x: x.split("@")[-1]))

#STEP 5: Find the overlap between them (domains that show up in BOTH lists = duplicates) 
combined_unclean_domains = current_domains.intersection(potential_domains)

#STEP 6: Build a clean potential dealer list by removing any rows with those duplicate domains
clean_potential = potential[~potential["Email"].str.lower().apply(lambda x: x.split("@")[-1]).isin(combined_unclean_domains)]
i


#                       --- PRINTING CSV OF CLEAN TABLE + ANOTHER TAB WITH DUPLICATE EMAIL DOMAINS ---

#STEP 7: Exporting results into an Excel file with multiple tabs.
with pd.ExcelWriter("Dealer_Clean_Output.xlsx", engine="xlsxwriter") as writer:
    clean_potential.to_excel(writer, sheet_name="Cleaned_Potential", index=False)
    pd.DataFrame({"Duplicate_Domains": list(combined_unclean_domains)}).to_excel(writer, sheet_name="Duplicate_Domains", index=False)



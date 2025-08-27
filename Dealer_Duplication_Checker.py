# The apps we are bringing in
import pandas as pd  # bring in the Excel superpowers
from fuzzywuzzy import fuzz


#                                                  --- EXACT MATCHING SCRIPT ---

# Ask the user to type the file paths
POTENTIAL_DEALERS_FILE_PATH = "Potential Dealers (08.24.2025).csv"
CURRENT_DEALERS_FILE_PATH = "Current Dealers (08.24.2025).csv"

# load file paths into pandas: Dataframes gets saved into variables
potential = pd.read_csv(POTENTIAL_DEALERS_FILE_PATH)
current = pd.read_csv(CURRENT_DEALERS_FILE_PATH)

# Show column names
print("POTENTIAL DEALERS: columns")
print(list(potential.columns))
print("CURRENT DEALERS: columns")
print(list(current.columns))

# Get those current dealers and now pull only unique email domains  
current_domains = set(current["Email"].dropna().str.lower().apply(lambda x: x.split("@")[-1]))





# Dealer Duplicate Checker

A Streamlit app that helps JCOB Cycling identify and remove duplicate dealer leads, ensuring outreach efforts stay focused and efficient.

**Live App:** [dealer-duplication-checker.streamlit.app](https://dealer-duplication-checker-xgnsn77beyumpn829aqepc.streamlit.app)

---

## Overview

As JCOB expands its dealer network, keeping outreach lists clean is essential.  
This tool compares new potential dealer files against the current dealer list and flags overlaps based on email domain or company name.

---

## Features

- Upload two CSVs: Potential Dealers and Current Dealer Base  
- Automatic duplicate detection by email domain  
- Clean results table with download option  
- Works in any browser with no setup required  

---

## Tech Stack

- [Streamlit](https://streamlit.io/) - user interface  
- [Pandas](https://pandas.pydata.org/) - data cleaning  
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) - fuzzy matching  
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel support  

---

## Developer Notes

To run locally:

```bash
git clone https://github.com/adp101-JCOB/Dealer-Duplication-Checker.git
cd Dealer-Duplication-Checker
pip install -r requirements.txt
streamlit run Dealer_Duplication_Checker.py

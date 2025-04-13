Must update the following from line 223 to 228

# Update to your actual directory path where the data is being held.
base_directory = r"C:\Users\samue\Documents\Year_2_AUT\M3\Assignment\data"
# Update to desired directory path where you wish to output
output_directory = r"C:\Users\samue\Documents\Year_2_AUT\M3\Assignment"
# Change to desired year to analyze
year_to_analyze = 2023

Assumptions

All JSON files in the base_directory follow the required schema.
Dates in the visit_date field are valid and in the YYYY-MM-DD format.
The follow_up_needed field can have True/False, or be missing (assumed False).
The analysis is limited to the specified year (year_to_analyze).

Error Handling

Invalid JSON Format: If a file contains invalid JSON, an error message will be displayed, and the file will be skipped.
No Data for Year: If no valid records are found for the specified year, the script will raise a ValueError.
Unexpected Data Formats: If the script encounters unexpected data types, a warning will be printed, and the data will be ignored.

Generated Outputs

JSON Report:
	Total records processed.
	Department-level summaries (e.g., total visits, common diagnoses and treatments, average 	treatment duration).
	Monthly trends in visits and follow-ups.
	Overall patient outcomes (e.g., improved, no change, worsened).

Text Summary:
	Overall statistics.
	Monthly trends in visits and follow-ups.
	Busiest month for each department, diagnosis, and treatment.

References (Both in README.txt and .py file):

Python Software Foundation, os — Miscellaneous operating system interfaces, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/os.html. [Accessed: Nov. 24-25, 2024].
Python Software Foundation, json — JSON encoder and decoder, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/json.html. [Accessed: Nov. 24-25, 2024].
Python Software Foundation, 8. Errors and Exceptions, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/tutorial/errors.html. [Accessed: Nov. 25-26-28-29, 2024].
Python Software Foundation, datetime — Basic date and time types, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/datetime.html. [Accessed: Nov. 25-26-27-29, 2024].
The pandas development team, pandas: Python Data Analysis Library, v2.1.1 Documentation. [Online]. Available: https://pandas.pydata.org/pandas-docs/stable/. [Accessed: Nov. 25-26-27-28-29, 2024].

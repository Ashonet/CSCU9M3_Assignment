import os
import json
from datetime import datetime
import pandas as pd

# Traverses the directory and collects the data from all the .json files
def collect_traverse_data(base_dir):
    all_data = []
    for root, i, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                        elif isinstance(data, dict):
                            all_data.append(data)  # Apends directly if it's a single dictionary
                        else:
                            print(f"Unexpected data format in {file_path}: {data}")
                    except json.JSONDecodeError as er:
                        print(f"Error decoding JSON in file {file_path}: {er}")
    return all_data

# Aggregates data by department, monthly trends, and overall outcomes
def aggregate_data(data, year):
    # Validates records and filters for the given year
    valid_records = [
        record for record in data if isinstance(record, dict) and 'visit_date' in record
    ]

    # Filters records by year
    year_data = [
        record for record in valid_records if datetime.strptime(record['visit_date'], "%Y-%m-%d").year == year
    ]
    print(f"Records for year {year}: {len(year_data)}")
    if not year_data:
        raise ValueError(f"No valid records found for the year {year}.")

    # Converts to DataFrame
    df = pd.DataFrame(year_data)

    total_records = len(df)

    # Department level aggregation
    department_summaries = []

    for department, group in df.groupby('department'):
        diagnoses = group['diagnosis'].value_counts()
        treatments = group['treatment'].value_counts()
        avg_duration = group['treatment_duration'].mean()

        department_summary = {
            "department_name": department,
            "total_visits": len(group),
            "common_diagnoses": [{"diagnosis": d, "frequency": f} for d, f in diagnoses.items()],
            "common_treatments": [{"treatment": t, "frequency": f} for t, f in treatments.items()],
            "average_treatment_duration": round(avg_duration, 2),
        }
        department_summaries.append(department_summary)

    # Chronological order of months in a year
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    df['month'] = pd.Categorical(
        df['visit_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%B")),
        categories=month_order,
        ordered=True
    )
    df['follow_up_needed'] = df['follow_up_needed'].fillna(False).astype(bool)

    # Monthly summary of overall record counts and follow-up visits
    monthly_summary = (
        df.groupby('month', observed = False)
        .agg(record_count=('visit_date', 'count'), follow_up_visits=('follow_up_needed', 'sum'))
        .reset_index()
        .sort_values('month')
        .to_dict(orient='records')
    )

    department_monthly_visits = (
        df.groupby(['department', 'month'], observed = False)['visit_date']
        .count()
        .reset_index(name='visit_count')
    )

    # Busiest month by department
    department_peak_months = (
        department_monthly_visits.loc[
            department_monthly_visits.groupby('department')['visit_count'].idxmax()
        ][['department', 'month']]
        .rename(columns={'month': 'busiest_month'})
        .to_dict(orient='records')
    )
    
    diagnosis_monthly_visits = (
        df.groupby(['diagnosis', 'month'], observed = False)['visit_date']
        .count()
        .reset_index(name='visit_count')
    )

    # Busiest month diagnosis wise
    diagnosis_peak_months = (
        diagnosis_monthly_visits.loc[
            diagnosis_monthly_visits.groupby('diagnosis')['visit_count'].idxmax()
        ][['diagnosis', 'month']]
        .rename(columns={'month': 'most_likely_month'})
        .to_dict(orient='records')
    )

    # Treatment monthly visits
    treatment_monthly_visits = (
        df.groupby(['treatment', 'month'], observed = False)['visit_date']
        .count()
        .reset_index(name='visit_count')
    )

    # Busiest month treatment-wise
    treatment_peak_months = (
        treatment_monthly_visits.loc[
            treatment_monthly_visits.groupby('treatment')['visit_count'].idxmax()
        ][['treatment', 'month']]
        .rename(columns={'month': 'most_likely_month'})
        .to_dict(orient='records')
    )

    # Overall outcomes of patients
    outcomes = df['outcome'].value_counts().to_dict()
    overall_outcomes = {
        "improved": outcomes.get("Improved", 0),
        "no_change": outcomes.get("No Change", 0),
        "worsened": outcomes.get("Worsened", 0),
    }

    # Core report for JSON
    core_report = {
        "year": year,
        "total_records": total_records,
        "departments": department_summaries,
        "monthly_summary": monthly_summary,
        "overall_outcomes": overall_outcomes,
        
    }

    # Extra data only for text report
    extra_data = {
        "department_peak_months": department_peak_months,
        "diagnosis_peak_months": diagnosis_peak_months,
        "treatment_peak_months": treatment_peak_months,
    }

    return core_report, extra_data

# Save aggregated report as a JSON file
def save_json_report(core_report, year, output_dir):
    output_path = os.path.join(output_dir, f"{year}_annual_report.json")
    with open(output_path, 'w') as f:
        json.dump(core_report, f, indent=4)
    print(f"Report saved to: {output_path}")

# Creates a text summary for the annual report and saves to a .txt file.
def save_txt_summary(core_report, extra_data, year, output_dir):
    output_path = os.path.join(output_dir, f"{year}_summary.txt")
    with open(output_path, 'w') as f:
        f.write(f"Annual Summary Report - {year}\n")
        f.write("=" * 50 + "\n\n")

        # Overall Statistics
        f.write(f"Overall Statistics:\n")
        f.write(f"  Total Records Processed: {core_report['total_records']}\n")
        overall_outcomes = core_report["overall_outcomes"]
        f.write(f"  Outcomes Summary:\n")
        f.write(f"      Improved: {overall_outcomes['improved']}\n")
        f.write(f"      No Change: {overall_outcomes['no_change']}\n")
        f.write(f"      Worsened: {overall_outcomes['worsened']}\n\n")

        # Department Statistics
        f.write(f"Department Insights:\n")
        for department in core_report["departments"]:
            f.write(f"  {department['department_name']}:\n")
            f.write(f"      Total Visits: {department['total_visits']}\n")
            f.write(f"          Common Diagnoses:\n")
            for diag in department["common_diagnoses"]:
                f.write(f"              {diag['diagnosis']}: {diag['frequency']} visits\n")
            f.write(f"          Common Treatments:\n")
            for treat in department["common_treatments"]:
                f.write(f"              {treat['treatment']}: {treat['frequency']} visits\n")
            f.write(f"  Average Treatment Duration: {department['average_treatment_duration']} days\n\n")

        # Monthly Trends
        f.write(f"Monthly Trends:\n")
        for month in core_report["monthly_summary"]:
            f.write(f"  {month['month']}:\n")
            f.write(f"      Total Visits: {month['record_count']}\n")
            f.write(f"      Follow-up Visits Needed: {month['follow_up_visits']}\n")
        f.write("\n")

        # Notable Insights as stated in 2. Text Summary
        f.write("Notable Insights:\n")

        # Adds busiest month per department
        f.write("  Busiest Month by Department:\n")
        for dept in extra_data["department_peak_months"]:
            f.write(f"      {dept['department']} saw the most visits in {dept['busiest_month']}.\n")

        # Adds most likely month per diagnosis
        f.write("\n  Busiest Month by Diagnosis:\n")
        for diag in extra_data["diagnosis_peak_months"]:
            f.write(f"      {diag['diagnosis']} was most commonly reported in {diag['most_likely_month']}.\n")

        # Adds busiest month per treatment
        f.write("\n  Busiest Month by Treatment:\n")
        for treat in extra_data["treatment_peak_months"]:
            f.write(f"      {treat['treatment']} was most commonly administered in {treat['most_likely_month']}.\n")


    print(f"Text summary saved to: {output_path}")

# Update to your actual directory path where the data is being held.
base_directory = r"C:\Users\samue\Documents\Year_2_AUT\M3\Assignment\data"
# Update to desired directory path where you wish to output
output_directory = r"C:\Users\samue\Documents\Year_2_AUT\M3\Assignment"
# Change to desired year to analyze
year_to_analyze = 2022

print("Collecting data...")
collected_data = collect_traverse_data(base_directory)
print(f"Total records collected: {len(collected_data)}")

print("Aggregating data...")
try:
    core_report, extra_data = aggregate_data(collected_data, year_to_analyze)
    save_json_report(core_report, year_to_analyze, output_directory)
    save_txt_summary(core_report, extra_data, year_to_analyze, output_directory)
except ValueError as er:
    print(f"Error during aggregation: {er}")

"""
References (Both in README.txt and .py file):

Python Software Foundation, os — Miscellaneous operating system interfaces, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/os.html. [Accessed: Nov. 24-25, 2024].
Python Software Foundation, json — JSON encoder and decoder, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/json.html. [Accessed: Nov. 24-25, 2024].
Python Software Foundation, 8. Errors and Exceptions, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/tutorial/errors.html. [Accessed: Nov. 25-26-28-29, 2024].
Python Software Foundation, datetime — Basic date and time types, Python 3.12.0 Documentation. [Online]. Available: https://docs.python.org/3/library/datetime.html. [Accessed: Nov. 25-26-27-29, 2024].
The pandas development team, pandas: Python Data Analysis Library, v2.1.1 Documentation. [Online]. Available: https://pandas.pydata.org/pandas-docs/stable/. [Accessed: Nov. 25-26-27-28-29, 2024].
"""
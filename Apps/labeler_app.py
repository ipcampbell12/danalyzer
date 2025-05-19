import pandas as pd
import os
import sys
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager
from docxtpl import DocxTemplate
from glob import glob



manager = DataTaskManager()
ode_folder = manager.return_folders()["ode"]
subfolder1 = "Historical Assessment Data" 
subfolder2 = "Historical OSAS Results"  # Replace with the actual subfolder name
path = os.path.join(ode_folder, subfolder1, subfolder2)
cur_school_path = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\Current School Info.xlsx"

cols_to_keep = [
    "DistStdntID",
    "AttndSchlInstID",
    "LglLNm",
    "LglFNm",
    "EnrlGrdCd",
     "TstYr",
     "TstDtTxt",
     "SbjctCd",
     "PLGScore",
]

school_lookup = {
     796: "Nellie",
     797: "Washington",
     1267: "Lincoln",
     1359: "Heritage",
     4230: "Arthur Academy",
     1268: "French Prairie",
     1360: "Valor",
     800: "WHS",
     4544: "Success",
     95: "WCP - HS Students",
     4540: "AIS",
     4543: "WACA",
     4541: "WEBSS",
     4542: "WAAST",
}

subject_mapping = {
    "CE":"ELA",
    "CM":"Math",
    "NS":"Science",
    "SC":"Science",
}


def process_date_text(rowValue):
    if pd.isna(rowValue):  # Check if the value is NaN
        return ""
    
    rowValue = str(rowValue).strip()  # Ensure it's a string and strip whitespace
    
    if len(rowValue) == 7:
        month = "0" + rowValue[0]
        day = rowValue[1:3]
        year = rowValue[-4:]
    elif len(rowValue) == 8:
        month = rowValue[:2]
        day = rowValue[2:4]
        year = rowValue[-4:]
    else:
        return ""
    
    return f"{month}/{day}/{year}"


def proper_case(text):
    return text.title() if isinstance(text, str) else text


def combine_and_process_school_year_files(school_years, path):
    """
    Combines and processes all Excel files for each school year into a single processed file.

    Args:
        school_years (dict): A dictionary where keys are school years and values are lists of file names.
        path (str): The directory path where the files are located.
    """
    all_years_combined_data = pd.DataFrame()  # Create an empty DataFrame to hold data for all years

    for year, files in school_years.items():
        combined_data = pd.DataFrame()  # Create an empty DataFrame to hold the combined data for the current year
        for file in files:
            file_path = os.path.join(path, file)  # Construct the full file path
            try:
                # Read and process each file
                data = pd.read_excel(file_path)
                data = data[cols_to_keep]
                data["school"] = data["AttndSchlInstID"].map(school_lookup)
                data = data[data["school"].notna() & (data["school"] != "")]
                data = data[data["PLGScore"].notna() & (data["PLGScore"] != "")]
                data["Test Date"] = data["TstDtTxt"].apply(process_date_text)
                data["LglLNm"] = data["LglLNm"].apply(proper_case)
                data["LglFNm"] = data["LglFNm"].apply(proper_case)
                data["Subjects"] = data["SbjctCd"].map(subject_mapping)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
                print(f"Processed and added file: {file}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

        # Ensure "Test Date" is in datetime format
        combined_data["Test Date"] = pd.to_datetime(combined_data["Test Date"], errors="coerce")

        # Sort by Test Date to ensure the most recent date is used
        combined_data = combined_data.sort_values("Test Date").drop_duplicates(
            subset=["DistStdntID", "AttndSchlInstID", "school", "LglLNm", "LglFNm", "EnrlGrdCd", "TstYr", "Subjects"],
            keep="last"
        )

        # Pivot table to include both PLGScore and Test Date for each subject
        combined_data = combined_data.pivot_table(
            index=["DistStdntID", "AttndSchlInstID", "school", "LglLNm", "LglFNm", "EnrlGrdCd"],
            columns="Subjects",
            values=["PLGScore", "Test Date","TstYr"],
            aggfunc="first",
            fill_value=""
        )

        combined_data = combined_data.reset_index()

        # Flatten the MultiIndex columns
        combined_data.columns = [
            f"{col[1]} {col[0]}" if isinstance(col, tuple) else col for col in combined_data.columns
        ]

        # Ensure all "PLGScore" columns are treated as strings
        for col in combined_data.columns:
            if "PLGScore" in col:
                combined_data[col] = combined_data[col].apply(
                    lambda x: str(int(float(x))) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() and float(x).is_integer()
                    else str(x) if pd.notna(x) else ""
                )
                
        # Append the processed data for the current year to the all_years_combined_data DataFrame
        all_years_combined_data = pd.concat([all_years_combined_data, combined_data], ignore_index=True)
        print("Processed and combined data for year:", year)
   
    # Save the final combined data for all years to a single Excel file
    if not all_years_combined_data.empty:
        # Normalize column names to avoid case or whitespace issues
        all_years_combined_data.columns = all_years_combined_data.columns.str.strip().str.lower()

        # Ensure required columns exist before proceeding
        required_columns = ["ela test date", "math test date", "science test date"]
        missing_columns = [col for col in required_columns if col not in all_years_combined_data.columns]
        if missing_columns:
            print(f"Error: Missing columns in all_years_combined_data: {missing_columns}")
            print("Available columns:", all_years_combined_data.columns.tolist())
        else:
            # Add a new column for the most recent test date
            all_years_combined_data["most_recent_test_date"] = all_years_combined_data[required_columns].max(axis=1)

            # Find the row index corresponding to the most recent test date per student
            idx = all_years_combined_data.groupby("diststdntid")["most_recent_test_date"].idxmax()

            # Retrieve the school for each student's most recent test
            most_recent_school = (
                all_years_combined_data.loc[idx, ["diststdntid", "school"]]
                .set_index("diststdntid")["school"]
            )

            # Map the most recent school back to the original DataFrame
            all_years_combined_data["most_recent_school"] = all_years_combined_data["diststdntid"].map(most_recent_school)

        
        # Save the final combined data to an Excel file
        output_file = os.path.join(path, "Processed OSAS Results Combined.xlsx")
        all_years_combined_data.to_excel(output_file, index=False, sheet_name="All Years OSAS")
        adjust_column_widths(output_file)
        print(f"Final combined file saved: {output_file}")
    else:
        print("No data to save for all years")


# Main logic
school_years = {year: [] for year in ["2016-2017",
                                      "2017-2018",
                                      "2018-2019",
                                      "2021-2022",
                                      "2022-2023"]}
for year in school_years.keys():
    school_years[year] = [file for file in os.listdir(path) if file.endswith(".xlsx") and year in file]



def distribute_by_school(data_path):
    """
    Distributes the processed data by school into separate Excel files.
    """

    merged_data = pd.read_excel(data_path)

    dest_folder= r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\Historical OSAS Results\Processed Results"

    for school in school_lookup.values():
        school_data = merged_data[merged_data["most_recent_school"] == school]
        school_data = school_data.sort_values(["lgllnm", "lglfnm",], ascending=True)
        if not school_data.empty:
            output_file = os.path.join(dest_folder, f"Processed OSAS Results {school}.xlsx")
            
            # Ensure date columns are formatted as mm/dd/yyyy
            date_columns = [col for col in school_data.columns if "date" in col.lower()]
            for col in date_columns:
                school_data[col] = pd.to_datetime(school_data[col], errors="coerce").dt.strftime("%m/%d/%Y")
            
            # Save to Excel with the desired date format
            school_data.to_excel(output_file, index=False, sheet_name=school)
            adjust_column_widths(output_file)
            print(f"Distributed file saved for {school}: {output_file}")
        else:
            print(f"No data available for {school}")





def create_labels_from_excel(template_path, excel_path, output_path):
    # Load template
    doc = DocxTemplate(template_path)

    # Read Excel
    df = pd.read_excel(excel_path)
    df.fillna("", inplace=True)  # Replace NaNs with empty strings

    # Convert DataFrame to list of dictionaries
    label_data = df.to_dict(orient="records")

    # Render the template with all rows
    context = {"labels": label_data}
    doc.render(context)
    doc.save(output_path)

def generate_labels():
    template = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\Labels\OSAS Labels Template.docx"
    dest_folder= r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\Historical OSAS Results\Processed Results"
    excel_files = glob(os.path.join(dest_folder, "*.xlsx"))
    output_dir = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\Historical OSAS Results\Processed Results\Labels"
    os.makedirs(output_dir, exist_ok=True)

    for excel_file in excel_files:
        base_name = os.path.splitext(os.path.basename(excel_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}_labels.docx")
        create_labels_from_excel(template, excel_file, output_file)
        print(f"Created: {output_file}")


def merge_with_current(combined_data_path,current_school_path=cur_school_path):
    combined_data = pd.read_excel(combined_data_path)
    curent_school_df = pd.read_excel(current_school_path)

    # Perform the merge
    merged_data = pd.merge(combined_data, curent_school_df, how="left", on="diststdntid", suffixes=("", "_new"))
    print('Merged current school data with combined data')

    # Update 'most_recent_school' only where the merge found a match
    if "most_recent_school_new" in merged_data.columns:
        merged_data["most_recent_school"].update(merged_data["most_recent_school_new"])
        merged_data.drop(columns=["most_recent_school_new"], inplace=True)

    print('Updated most_recent_school with merged values where applicable')
    
    merged_data.to_excel(combined_data_path, index=False, sheet_name="All Years OSAS")
    adjust_column_widths(combined_data_path)
    print("Merged data written to spreadsheet and column widths adjusted")


# combine_and_process_school_year_files(school_years, path)
# merge_with_current(os.path.join(path, "Processed OSAS Results Combined.xlsx"), cur_school_path)
distribute_by_school(os.path.join(path, "Processed OSAS Results Combined.xlsx"))
# generate_labels()

import pandas as pd
import subprocess
from datetime import date
import calendar
from Helpers.columns import adjust_column_widths



def monitor_el_graduation(grades_path, els_path, failed_path,processed_el_graduation_folder):
    # Read the original Excel file
    # grades_path = powerschool_folder /"12-17 Historical Grades.xlsx"
    # els_path = powerschool_folder /"12-17 HS ELs.xlsx"
    # failed_path = powerschool_folder / "12-17 Failed Classes.xlsx"
    grades_df = pd.read_excel(grades_path)
    els_df= pd.read_excel(els_path)
    failed_df= pd.read_excel(failed_path)
    current_date = pd.Timestamp('today')
    current_month = calendar.month_name[date.today().month]
    current_year = date.today().year

    # Ensure the columns are spelled correctly
    print(grades_df.columns)

    # Dictionary mapping grade levels to ideal credits
    grade_credits_dict = {
        9: 0,
        10: 6,
        11: 12,
        12: 18
    }

    # Apply the dictionary to create the 'ideal_credits' column
    grades_df["ideal_credits"] = grades_df["Grade Level"].apply(lambda value: grade_credits_dict.get(value, 0))

    # Add 'isDeficient' column to check credit deficiency
    grades_df["isDeficient"] = grades_df.apply(lambda x: "Yes" if x["Sum Earnedcrhrs"] < x["ideal_credits"] else "No", axis=1)

    # Sort values by 'Grade Level'
    grades_df.sort_values(by=["Grade Level","Sum Earnedcrhrs"], inplace=True)
    grades_df = grades_df.rename(columns={'Student Number': 'student_number'})
    grades_df = grades_df.merge(els_df,how="left",on="student_number")
    grades_df = grades_df[grades_df["S_OR_STU_X.ELFg"]==1]
    print(grades_df.columns)
    grades_df = grades_df[['student_number','Lastfirst','Grade Level','Sum Earnedcrhrs','ideal_credits','isDeficient','S_OR_STU_X.ELFg','S_OR_STU_LEP_X.StartDt']]
    grades_df['Years as EL'] = current_date - grades_df['S_OR_STU_LEP_X.StartDt']
    grades_df['Years as EL'] = round(grades_df['Years as EL'].dt.days/365.25)
    pivot_grades = grades_df.groupby(['Grade Level', "isDeficient"]).size().unstack(fill_value=0).reset_index()
    failed_pivot = failed_df.groupby(['Credit Type','Grade']).size().unstack(fill_value=0).reset_index()
    failed_pivot = failed_pivot.sort_values(by="F",ascending=False)
    failed_course_pivot = failed_df.groupby(['Course Name','Grade']).size().unstack(fill_value=0).reset_index()
    failed_course_pivot = failed_course_pivot.sort_values(by="F",ascending=False)



    # Debugging outputs
    print(pivot_grades)
    print(list(pivot_grades.columns))

    # Strip whitespace from column names
    pivot_grades.rename(columns=lambda x: x.strip() if isinstance(x, str) else x, inplace=True)

    # Ensure index name is removed
    pivot_grades.columns.name = None

    # Calculate Deficient Percentage safely
    pivot_grades["Deficient Percentage"] = pivot_grades.apply(
        lambda x: round(x["Yes"] / (x["Yes"]+x["No"]) * 100) if x.get("Yes", 0) > 0 else 0,
        axis=1
    )

    print(pivot_grades)

    grades_df['S_OR_STU_LEP_X.StartDt'] = grades_df['S_OR_STU_LEP_X.StartDt'].dt.strftime('%m/%d/%Y')
    high_profile_df = grades_df[grades_df['Sum Earnedcrhrs'] + 4 < grades_df['ideal_credits']]
    high_profile_df = high_profile_df[['student_number','Lastfirst','Grade Level','Sum Earnedcrhrs','ideal_credits','isDeficient','S_OR_STU_LEP_X.StartDt','Years as EL']]
    are_deficient_df = grades_df[grades_df['isDeficient']=='Yes']
    final_path = processed_el_graduation_folder / f"{current_month}, {current_year} Credit Deficient.xlsx"

    el_years_df = are_deficient_df['Years as EL'].value_counts().reset_index()

    # Rename the columns for clarity
    el_years_df.columns = ['Years as EL', 'Number of Students (Credit Defficient)']

    with pd.ExcelWriter(final_path, engine='openpyxl') as writer:
    # Save the resulting DataFrame to an Excel file
        high_profile_df.to_excel(writer, sheet_name="High Concern", index=False, startrow=0)
        are_deficient_df.to_excel(writer, sheet_name="Credit Deficient", index=False, startrow=0)
        pivot_grades.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
        el_years_df.to_excel(writer,sheet_name="Summary", index=False, startrow=7)
        grades_df.to_excel(writer, sheet_name="All ELs", index=False, startrow=0)
        failed_pivot.to_excel(writer, sheet_name="Failed by Credit Type", index=False, startrow=0)
        failed_course_pivot.to_excel(writer, sheet_name="Failed by Course", index=False, startrow=0)


    adjust_column_widths(final_path)

    subprocess.run(["start", "excel", final_path], shell=True)
    # os.system(f"start EXCEL.EXE {final_path}")
import pandas as pd
import os
from columns import adjust_column_widths
import subprocess

file_path = "5-16 Fastbridge Upload.xlsx"

fasbridge_df = pd.read_excel(file_path)

cols = [
    ['State', ''],
    ['SchoolDistrict', 'Woodburn School District'],
    ['School', ''],
    ['Grade', ''],
    ['Course', ''],
    ['Section', ''],
    ['StudentID', ''],
    ['StudentStateID', ''],
    ['StudentFirstName', ''],
    ['StudentLastName', ''],
    ['TeacherID', ''],
    ['TeacherFirstName', ''],
    ['TeacherLastName', ''],
    ['TeacherEmail', ''],
    ['StudentGender', ''],
    ['StudentBirthDate', ''],
    ['StudentRace', ''],
    ['MealStatus', ''],
    ['EnglishProficiency', ''],
    ['NativeLanguage', ''],
    ['ServiceCode', ''],
    ['PrimaryDisabilityType', ''],
    ['IEPReading', ''],
    ['IEPMath', ''],
    ['IEPBehavior', ''],
    ['GiftedAndTalented', ''],
    ['Section504', ''],
    ['Mobility', '']
]

print(fasbridge_df.columns)
# headers = ["Course Name","Instructor Last Name","Expression"]

# classes_df = math_df.groupby(headers).size().reset_index(name="Students")

# final_path = "Sections.xlsx"

# classes_df.to_excel(final_path,index=False)

# adjust_column_widths(final_path)

# subprocess.run(["start", "excel", final_path], shell=True)
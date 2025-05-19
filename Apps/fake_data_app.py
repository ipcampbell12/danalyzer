import pandas as pd
import random
import openpyxl
from faker import Faker
import subprocess
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths

manager = DataTaskManager()
output_folder = manager.return_folders()["fake_data_folder"]
# Constants
ETHNICITY_NAME_MAP = {
    "Hispanic": {
        "first_names": ["Alejandro", "Carlos", "Diego", "Emilio", "Fernando", "Javier", "José", "Luis", "Manuel", "Ricardo",
                        "Camila", "Daniela", "Gabriela", "Isabella", "Lucia", "Marisol", "Natalia", "Rosa", "Sofia", "Valeria"],
        "last_names": ["Ramirez", "Lopez", "Garcia", "Martinez", "Rodriguez", "Alvarez", "Sanchez", "Reyes", "Cruz", "Mendoza"]
    },
    "Asian": {
        "first_names": ["Wei", "Linh", "Nguyen", "Hiroshi", "Dae-Jung", "Chen", "Yasmin", "Amara", "Mina", "Raj"],
        "last_names": ["Nguyen", "Chang", "Lee", "Nakamura", "Kim", "Chen", "Singh", "Patel", "Kumar"]
    },
    "Black": {
        "first_names": ["Jamal", "Kwame", "Aisha", "Fatima", "Youssef", "Kofi", "Ans su"],
        "last_names": ["Okafor", "Osei", "Hussain", "Rahman", "Ali"]
    },
    "White": {
        "first_names": ["Billy", "Sergio", "Elena", "Mikhail", "Mateo", "Isabella", "Leila"],
        "last_names": ["Smith", "Williams", "Jensen", "Larsen", "Kowalski", "Dubois", "Rossi"]
    },
    "Middle Eastern": {
        "first_names": ["Aliya", "Youssef", "Mina", "Zara", "Anika"],
        "last_names": ["Al-Farsi", "Rahman", "Hussain", "Ali"]
    },
    "Mixed": {
        "first_names": ["Diego", "Sofia", "Lucia", "Jamal", "Aarav"],
        "last_names": ["Rodriguez", "Martinez", "Hernandez", "Singh", "Ali"]
    },
    "Native American": {
        "first_names": ["Quetzalcoatl", "Ruben", "Belinda"],
        "last_names": ["Sales", "De Jesus"]
    },
    "Pacific Islander": {
        "first_names": ["Emmanuel"],
        "last_names": ["Godinez"]
    }
}

SCHOOLS = {
    "Maplecrest Elementary School": ["1", "", "3", "4", "5"],
    "Maplecrest Middle School": ["6", "7", "8"],
    "Maplecrest High School": ["9", "10", "11", "12"]
}

# Adjusted function to generate data
def generate_fake_data(num_students=200):
    """
    Generates a student dataset with logically mapped names, ethnicities, and date relationships.

    :param num_students: Number of students to generate.
    """
    
    # Initialize Faker for generating fake data
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    # Ethnicities with weights
    ethnicities = list(ETHNICITY_NAME_MAP.keys())
    ethnicity_weights = [60, 3, 4, 23, 3, 5, 1, 1]  # Approximate percentage distribution

    # Gender with weights
    genders = ["Male", "Female", "Non-Binary"]
    gender_weights = [48, 49, 3]  # Approximate percentages

    # Generate student data
    data = []
    for _ in range(num_students):
        # Generate ethnicity and names
        ethnicity = random.choices(ethnicities, weights=ethnicity_weights)[0]
        first_name = random.choice(ETHNICITY_NAME_MAP[ethnicity]["first_names"])
        last_name = random.choice(ETHNICITY_NAME_MAP[ethnicity]["last_names"])
        
        # Generate student ID (8 digits long)
        student_id = str(fake.unique.random_int(min=10000000, max=99999999))

        # Generate date of birth and corresponding grade level/school mapping
        dob = fake.date_of_birth(minimum_age=5, maximum_age=18)
        grade_level, school = map_grade_level_school(dob)

        # Gender and other student attributes
        gender = random.choices(genders, weights=gender_weights)[0]
        gpa = round(random.uniform(0.0, 4.0), 2)
        achievement_quintile = random.randint(1, 5)
        attendance_rate = round(random.uniform(70, 100), 2)
        enrollment_date = fake.date_between(start_date=dob.replace(year=dob.year + 5), end_date="today")
        special_ed_status = random.choice(["Y", "N"])
        english_learner_status = random.choice(["Y", "N"])
        lep_start_date = fake.date_between(start_date=dob.replace(year=dob.year + 5), end_date=enrollment_date)

        data.append([first_name, last_name, student_id, dob, gender, ethnicity, gpa, achievement_quintile,
                     attendance_rate, grade_level, enrollment_date, special_ed_status, english_learner_status, lep_start_date,
                     school, "Maplecrest School District"])

    # Create DataFrame
    columns = [
        "First Name", "Last Name", "Student ID", "Date of Birth", "Gender", "Ethnicity",
        "GPA", "Achievement Quintile", "Attendance Rate", "Grade Level", "Enrollment Date",
        "Special Education Status", "LEP Flag", "LEP Start Date", "School", "School District"
    ]
    
    df = pd.DataFrame(data, columns=columns)

    # Ensure date columns are datetime objects
    date_columns = ["Date of Birth", "Enrollment Date", "LEP Start Date"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col]).dt.strftime("%m/%d/%Y")

    # Save Data
    manager = DataTaskManager()
    output_folder = manager.return_folders()["fake_data_folder"]
    output_path = output_folder / "fake_data.xlsx"

    df.to_excel(output_path, index=False)
    adjust_column_widths(output_path)
    
    print(f"Fake data generated and saved to {output_path}")
    return df
    # subprocess.run(["start", "excel", output_path], shell=True)

# Mapping DOB to grade level and school
def map_grade_level_school(dob):
    """
    Maps a student's date of birth to a grade level and school.
    """
    current_year = pd.to_datetime("today").year
    age = current_year - dob.year

    # Determine grade level and school based on age
    if age == 5:
        return "KG", "Maplecrest Elementary School"
    elif age >= 6 and age <= 10:
        grade = age - 5  # 1st through 5th grade
        return f"{grade}", "Maplecrest Elementary School"
    elif age >= 11 and age <= 13:
        grade = age - 5  # 6th through 8th grade
        return f"{grade}", "Maplecrest Middle School"
    elif age >= 14 and age <= 18:
        grade = min(age - 5, 12)  # Cap grade at 12th grade
        return f"{grade}", "Maplecrest High School"
    else:
        return "N/A", "N/A"

def mess_up_data(df,path):
    df_copy = df.copy()

    # Duplicate Records
    duplicate_count = random.randint(1, 5)
    for _ in range(duplicate_count):
        duplicate_row = df_copy.sample(1)
        df_copy = pd.concat([df_copy, duplicate_row], ignore_index=True)

    # Formatting Inconsistencies
    name_columns = ["First Name", "Last Name"]
    for col in name_columns:
        for index, row in df_copy.iterrows():
            if random.random() < 0.2:  # 20% chance to mess up the capitalization
                df_copy.at[index, col] = row[col].lower() if random.random() < 0.5 else row[col].upper()

    # Missing or Incorrect Data
    for col in ["Date of Birth", "Student ID"]:
        for index, row in df_copy.iterrows():
            if random.random() < 0.1:  # 10% chance to mess up data
                if col == "Date of Birth":
                    df_copy.at[index, col] = None if random.random() < 0.5 else "01/01/2023"
                else:
                    df_copy.at[index, col] = str(random.randint(10000000, 99999999)) if random.random() < 0.5 else None

    # LEP Flag and LEP Start Date Inconsistencies
    for index, row in df_copy.iterrows():
        if random.random() < 0.15:  # 15% chance to mess up LEP data
            lep_flag = row["LEP Flag"]
            lep_start_date = row["LEP Start Date"]
            if lep_flag == "Y" and lep_start_date is None:
                df_copy.at[index, "LEP Start Date"] = pd.to_datetime("today").strftime("%m/%d/%Y")
            elif lep_flag == "N" and lep_start_date:
                df_copy.at[index, "LEP Flag"] = "Y"  # Create inconsistency

    # Randomly introduce some missing LEP Flags and LEP Start Dates
    for index, row in df_copy.iterrows():
        if random.random() < 0.05:  # 5% chance of missing LEP flag or start date
            if random.choice([True, False]):
                df_copy.at[index, "LEP Flag"] = None
            else:
                df_copy.at[index, "LEP Start Date"] = None

    # Ensure DOB makes sense with Grade Level
    grade_level_dob_mapping = {
        "KG": (-6, -5),  # KG: age 5-6
        "1": (-7, -6),  # 1st grade: age 6-7
        "2": (-8, -7),  # 2nd grade: age 7-8
        "3": (-9, -8),  # 3rd grade: age 8-9
        "4": (-10, -9),  # 4th grade: age 9-10
        "5": (-11, -10),  # 5th grade: age 10-11
        "6": (-12, -11),  # 6th grade: age 11-12
        "7": (-13, -12),  # 7th grade: age 12-13
        "8": (-14, -13),  # 8th grade: age 13-14
        "9": (-15, -14),  # 9th grade: age 14-15
        "10": (-16, -15),  # 10th grade: age 15-16
        "11": (-17, -16),  # 11th grade: age 16-17
        "12": (-18, -17),  # 12th grade: age 17-18
    }

    for index, row in df_copy.iterrows():
        # Check if Grade Level and DOB are valid
        grade_level = row["Grade Level"]
        dob = pd.to_datetime(row["Date of Birth"], errors='coerce')
        
        # Skip rows with invalid Grade Level or DOB (e.g., 'N/A', empty, etc.)
        if grade_level in ['N/A', None] or pd.isna(dob):
            continue
        
        # If DOB is valid, check if it aligns with the grade level
        if pd.notna(dob):
            # Calculate age based on the current year
            current_year = pd.to_datetime("today").year
            age = current_year - dob.year

            # If age does not make sense for grade level, intentionally create errors
            if age not in range(grade_level_dob_mapping.get(grade_level, (0, 0))[0], 
                               grade_level_dob_mapping.get(grade_level, (0, 0))[1] + 1):
                # 10% chance to create inconsistency
                if random.random() < 0.1:
                    # Introduce an incorrect DOB for the student to not match the grade level
                    incorrect_dob = pd.to_datetime(f"{current_year - random.randint(5, 25)}-01-01")
                    df_copy.at[index, "Date of Birth"] = incorrect_dob.strftime("%m/%d/%Y")

    df_copy.to_excel(path,index=False)
    adjust_column_widths(path)
    print(f"Fake data MESSED UP and saved ${path}")
    subprocess.run(["start", "excel", path], shell=True)


# Call the function
fake_df = generate_fake_data()

output_path = output_folder / "2-24 Excel Task Spreadsheet.xlsx"
mess_up_data(fake_df,output_path)


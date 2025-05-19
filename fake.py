import pandas as pd
import random
import openpyxl
from faker import Faker
from task_manager import DataTaskManager
from columns import adjust_column_widths
import subprocess

# Initialize Faker for generating fake data
fake = Faker()
Faker.seed(42)
random.seed(42)

# Diverse list of first and last names
first_names = [
    "Sergio", "Billy", "Ans su", "Fatima", "Kofi", "Wei", "Amara", "Nguyen", "Raj", "Yasmin",
    "Aisha", "Dae-Jung", "Linh", "Hiroshi", "Elena", "Jamal", "Mina", "Youssef", "Zara", "Chen",
    "Mateo", "Aarav", "Sofia", "Kwame", "Anika", "Mikhail", "Aliya", "Diego", "Isabella", "Leila","Alejandro", "Carlos", "Diego", "Emilio", "Fernando", "Javier", "José", "Luis", "Manuel", "Ricardo",
    "Camila", "Daniela", "Gabriela", "Isabella", "Lucia", "Marisol", "Natalia", "Rosa", "Sofia", "Valeria"
]

last_names = [
    "Lopez", "Nguyen", "Kyit", "Kim", "Okafor", "Chang", "Singh", "Patel", "Kumar", "Al-Farsi",
    "Dubois", "Rossi", "Petrov", "Ali", "Smith", "Garcia", "Williams", "Hernandez", "Kowalski",
    "Rahman", "Hussain", "Chen", "Lee", "Nakamura", "Osei", "Jensen", "Larsen", "Rodriguez", "Martinez",  "Alvarez", "Castillo", "Cruz", "Delgado", "Fernandez", "Gonzalez", "Herrera", "Jimenez", 
    "Mendoza", "Morales", "Ortiz", "Ramirez", "Reyes", "Rivera", "Sanchez","Godinez","Sales"
]

# School and district details
schools = [
    "Hogwarts Elementary School of Magic",
    "Hogwarts Middle School of Magic",
    "Hogwarts High School of Magic"
]
district = "The Enchanted Learning District"

# Grade levels for each school type
grade_levels = {
    "Hogwarts Elementary School of Magic": ["1st", "2nd", "3rd", "4th", "5th"],
    "Hogwarts Middle School of Magic": ["6th", "7th", "8th"],
    "Hogwarts High School of Magic": ["9th", "10th", "11th", "12th"]
}

# Ethnicities with weights
ethnicities = [
    "Hispanic", "Asian", "Black", "White", "Mixed", "Middle Eastern", "Native American", "Pacific Islander"
]
ethnicity_weights = [60, 3, 4, 23, 5, 3, 1, 1]  # Percent-based weights


# Gender with weights
genders = ["Male", "Female", "Non-Binary"]
gender_weights = [48, 49, 3]  # Percent-based weights

# Generate 200 rows of data
data = []
for _ in range(200):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    student_id = fake.unique.random_int(min=1000, max=9999)
    dob = fake.date_of_birth(minimum_age=5, maximum_age=18)
    gender = random.choices(genders, weights=gender_weights)[0]
    ethnicity = random.choices(ethnicities, weights=ethnicity_weights)[0]
    gpa = round(random.uniform(0.0, 4.0), 2)
    achievement_quintile = random.randint(1, 5)
    attendance_rate = round(random.uniform(70, 100), 2)
    school = random.choice(schools)
    grade = random.choice(grade_levels[school])
    enrollment_date = fake.date_between(start_date="-10y", end_date="today")
    special_ed_status = random.choice(["Yes", "No"])
    english_learner_status = random.choice(["Yes", "No"])

    data.append([
        first_name, last_name, student_id, dob, gender, ethnicity, gpa, achievement_quintile,
        attendance_rate, grade, enrollment_date, special_ed_status, english_learner_status,
        school, district
    ])

# Create DataFrame
columns = [
    "First Name", "Last Name", "Student ID", "Date of Birth", "Gender", "Ethnicity",
    "GPA", "Achievement Quintile", "Attendance Rate", "Grade Level", "Enrollment Date",
    "Special Education Status", "English Learner Status", "School", "School District"
]

df = pd.DataFrame(data, columns=columns)

manager = DataTaskManager()
output_folder = manager.return_folders()["fake_data_folder"]
# Save to CSV
output_path = output_folder / "fake_data.xlsx"
df.to_excel(output_path, index=False)
adjust_column_widths(output_path)
print(f"Data saved to {output_path}")
subprocess.run(["start", "excel", output_path], shell=True)
import pandas as pd


def validate_avid_file(df):
     df["isAvid"] =df["Elective"].apply(lambda x: "AVID" in str(x).upper())
     print("Created isAvid column")

     course_columns = [
        'Math',
        'Science',
        "Health",
        'Social Studies',
        'Physical Education',
        'Language Arts',
        'Elective',
     ]

     df["isADC"] = df.apply(
        lambda row: (
            "College" in str(row['Schools Attended']) or
            "Willamette Career Academy" in str(row['Schools Attended']) or
            (row['Vocational Count'] > 0) or
            any("AP " in str(row[col]).upper() or "IB " in str(row[col]).upper() for col in course_columns)
        ),
        axis=1
    )
     print("Created isADC column")

     print(df[course_columns].head())  # Check the relevant columns
     print(df["isADC"].value_counts())  # Verify the distribution of True/False

     notPass = ["F", "I", "W", "NC", "NP", "N/A"]

     # df["allCredits"] = df["All Grades"].apply(
     #      lambda row: (
     #           all(grade not in str(row).upper() for grade in notPass) 
     #      )
     # )

     print("Created allCredits column")
     df["twoCTE"] = df["Vocational Count"].apply(lambda x: x >= 2)

     # df["tookAPTest"] = df["AP Test"].apply( lambda x: any(True in str(x).upper()))
     return df
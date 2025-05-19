import pandas as pd
import random
import openpyxl
from faker import Faker
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess


def interview_tester(submission_file,check_file):
     
     check_df = pd.read_excel(check_file,sheet_name="Data Analysis Answers")
     test_df = pd.read_excel(submission_file,sheet_name="Data Analysis Answers")

     check_answers = check_df["Answer"].tolist()
     test_answers = test_df["Answer"].tolist()

     print(check_answers)
     print(test_answers)

     correct_answers = []
     wrong_answers =[]
     for idx,answer in enumerate(test_answers):
          if answer == check_answers[idx]:
               correct_answers.append(answer)
          else:
               wrong_answers.append(answer)

     right_string = f"Boby got {len(correct_answers)} questions right"
     print(right_string)
     wrong_string = f"Bob got {len(wrong_answers)} questions wrong"
     print(wrong_string)

     return [right_string,wrong_string]
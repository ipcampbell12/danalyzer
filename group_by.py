import pandas as pd
import os
from columns import adjust_column_widths
import subprocess

# file_path = "9th Grade Math Classes.xlsx"

def group_by_spreadsheet(file_path,headers,new_name,new_file_name):
     basic_df = pd.read_excel(file_path)

     # headers = ["Course Name","Instructor Last Name","Expression"]

     group_df = basic_df.groupby(headers).size().reset_index(name="Students")

     final_path = new_file_name + ".xlsx"

     group_df.to_excel(final_path,index=False)

     adjust_column_widths(final_path)

     subprocess.run(["start", "excel", final_path], shell=True)
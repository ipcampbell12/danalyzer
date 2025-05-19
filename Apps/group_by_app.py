import pandas as pd
import os
from Helpers.columns import adjust_column_widths
import subprocess
from task_manager import DataTaskManager

manager = DataTaskManager()

file_path = r"C:\Users\inpcampbell\Desktop\ODE\24-25 Recent Arrviers Production Download.xlsx"


def group_by_spreadsheet(file_path,headers,filter_col,filter_vals,new_name,new_file_name):
     basic_df = pd.read_excel(file_path)

     # headers = ["Course Name","Instructor Last Name","Expression"]

     basic_df = basic_df[basic_df[filter_col].isin(filter_vals)]
     # print(basic_df.head(20))
     group_df = basic_df.groupby(headers).size().reset_index(name=new_name)

     group_df =group_df.sort_values(by=new_name,ascending=False)

     group_df["Language Name"]=group_df["LangOrgnCd"].apply(lambda x: manager.lookup_language(x))
     print(group_df.columns)
     final_path = new_file_name + ".xlsx"
     
     group_df.to_excel(final_path,index=False)


     adjust_column_widths(final_path)

     subprocess.run(["start", "excel", final_path], shell=True)


# group_by_spreadsheet(file_path,["LangOrgnCd"],"EnrlGrdCd",[6,7,8,9,10,11,12],"Students by Country","Recent Arrivers by Country")
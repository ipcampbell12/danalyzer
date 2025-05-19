import pandas as pd
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess

manager = DataTaskManager()
folder = manager.return_folders()["powerschool_folder"]
high_school_path = folder / "1-22 Sum Success Credits.xlsx"
stamp_path = folder / "1-22 Succes STAMP Credits.xlsx"
non_taught_path = folder / "1-22 All Success Credits.xlsx"
work_path = folder / "1-22 SUccess Work Experience.xlsx"


high_school_df = pd.read_excel(high_school_path).sort_values(by=['First Name','Last Name'])
stamp_df = pd.read_excel(stamp_path).sort_values(by=['First Name','Last Name'])
non_taught_df = pd.read_excel(non_taught_path,sheet_name="Non Taught Credits").sort_values(by=['First Name','Last Name'])
all_credits_df = pd.read_excel(non_taught_path,sheet_name="All Credits").sort_values(by=['First Name','Last Name'])


if "Grade Level" in all_credits_df.columns:
     all_credits_df=all_credits_df.drop("Grade Level",axis=1)

if "MTW Status" in non_taught_df.columns:
     non_taught_df=non_taught_df.drop("MTW Status",axis=1)

group_cols = ['First Name','Last Name','Student Number',"Teacher Name","Course Name","Earnedcrhrs","Datestored","Term"]
conflicting_credits = find_conflicting_credits_from_excel(non_taught_df,group_cols)

work_df = pd.read_excel(work_path).sort_values(by=['First Name','Last Name'])
# Extract the first two digits, append '00', and convert it back to a number
high_school_df['Yearid'] = high_school_df['Termid'].astype(str).str[:2] + '00'

# Convert the result back to a numeric type
high_school_df['Yearid'] = pd.to_numeric(high_school_df['Yearid'])

# grouped_df = high_school_df.groupby(['Lastfirst','Student Number','Yearid'])
grouped_stamp = stamp_df.groupby(['First Name','Last Name','Student Number'])

grouped_non_taught = non_taught_df.groupby(['First Name','Last Name','Student Number'])

grouped_work = work_df.groupby(['First Name','Last Name','Student Number',"Termid"])

# credits_df = grouped_df["Sum Earnedcrhrs"].sum().reset_index()
stamp_credits_df = grouped_stamp["Earnedcrhrs"].sum().reset_index().sort_values(by=['First Name','Last Name'])
non_taught_credits_df = grouped_non_taught["Earnedcrhrs"].sum().reset_index().sort_values(by=['First Name','Last Name'])
total_work_df = grouped_work["Sum Earnedcrhrs"].sum().reset_index().sort_values(by=['First Name','Last Name'])

stamp_credits_df = stamp_credits_df[stamp_credits_df["Earnedcrhrs"]>2]
concern_df = high_school_df[high_school_df['Sum Earnedcrhrs']>8]
non_taught_credits_df = non_taught_credits_df[non_taught_credits_df["Earnedcrhrs"]>5]

stamp_credits_df =stamp_credits_df.rename(columns={"Earnedcrhrs":"Credits Earned from STAMP"})
overall_red_flag_df = stamp_credits_df.merge(concern_df,on="Student Number",how="outer")
final_path = manager.return_folders()["audits_folder"] / "Success Audit.xlsx"

with pd.ExcelWriter(final_path,engine='openpyxl') as writer:
     # overall_red_flag_df.to_excel(writer,sheet_name="Overall Red Flag",index=False)
     concern_df.to_excel(writer,sheet_name="Credits Red Flags",index=False)
     stamp_credits_df.to_excel(writer,sheet_name="STAMP Red Flag",index=False)
     non_taught_credits_df.to_excel(writer,sheet_name="Non Taught Credits Red Flag",index=False)
     conflicting_credits.to_excel(writer,sheet_name="Dual Credits Red Flag",index=False)
     high_school_df.to_excel(writer, sheet_name="Total Credits for Students",index=False)
     all_credits_df.to_excel(writer,sheet_name="Individual Credits for Students",index=False)
     total_work_df.to_excel(writer,sheet_name="Total Work Credits",index=False)
     stamp_df.to_excel(writer,sheet_name="STAMP Credit",index=False)
     non_taught_df.to_excel(writer,sheet_name="Non Taught Credits",index=False)
     

adjust_column_widths(final_path)


subprocess.run(["start", "excel", final_path], shell=True)
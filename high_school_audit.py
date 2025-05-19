import pandas as pd
from task_manager import DataTaskManager
from columns import adjust_column_widths
import subprocess


manager = DataTaskManager()
folder = manager.return_folders()["powerschool_folder"]
high_school_path = folder / "12-20 Succes Credits.xlsx"
stamp_path = folder / "12-20 PS STAMP.xlsx"
# Sample data
high_school_df = pd.read_excel(high_school_path)
stamp_df = pd.read_excel(stamp_path)

# Extract the first two digits, append '00', and convert it back to a number
high_school_df['Yearid'] = high_school_df['Termid'].astype(str).str[:2] + '00'

# Convert the result back to a numeric type
high_school_df['Yearid'] = pd.to_numeric(high_school_df['Yearid'])

grouped_df = high_school_df.groupby(['Lastfirst','Student Number','Yearid'])
grouped_stamp = stamp_df.groupby(['Lastfirst','Student Number'])

credits_df = grouped_df["Sum Earnedcrhrs"].sum().reset_index()
stamp_credits_df = grouped_stamp["Earnedcrhrs"].sum().reset_index()
stamp_credits_df = stamp_credits_df[stamp_credits_df["Earnedcrhrs"]>2]
concern_df = credits_df[credits_df['Sum Earnedcrhrs']>8]
stamp_credits_df =stamp_credits_df.rename(columns={"Earnedcrhrs":"Credits Earned from STAMP"})
overall_red_flag_df = stamp_credits_df.merge(concern_df,on="Student Number",how="outer")
final_path = "Success High School Credits.xlsx"

with pd.ExcelWriter(final_path,engine='openpyxl') as writer:
     # overall_red_flag_df.to_excel(writer,sheet_name="Overall Red Flag",index=False)
     concern_df.to_excel(writer,sheet_name="Credits Red Flags",index=False)
     stamp_credits_df.to_excel(writer,sheet_name="STAMP Red Flag",index=False)
     credits_df.to_excel(writer, sheet_name="Credits for All Students",index=False)
     stamp_df.to_excel(writer,sheet_name="STAMP Credit",index=False)


adjust_column_widths(final_path)


subprocess.run(["start", "excel", final_path], shell=True)
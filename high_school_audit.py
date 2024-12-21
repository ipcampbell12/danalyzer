import pandas as pd
from task_manager import DataTaskManager
from columns import adjust_column_widths
import subprocess

manager = DataTaskManager()
folder = manager.return_folders()["powerschool_folder"]
high_school_path = folder / "12-20 Succes Credits.xlsx"
# Sample data
high_school_df = pd.read_excel(high_school_path)

# Extract the first two digits, append '00', and convert it back to a number
high_school_df['Yearid'] = high_school_df['Termid'].astype(str).str[:2] + '00'

# Convert the result back to a numeric type
high_school_df['Yearid'] = pd.to_numeric(high_school_df['Yearid'])

grouped_df = high_school_df.groupby(['Lastfirst','Student Number','Yearid'])

credits_df = grouped_df["Sum Earnedcrhrs"].sum().reset_index()
concern_df = credits_df[credits_df['Sum Earnedcrhrs']>=7]

final_path = "Success High School Credits.xlsx"

with pd.ExcelWriter(final_path,engine='openpyxl') as writer:
     concern_df.to_excel(writer,sheet_name="Red Flag Students",index=False)
     credits_df.to_excel(writer, sheet_name="Credits for All Students",index=False)


adjust_column_widths(final_path)
subprocess.run(["start", "excel", final_path], shell=True)
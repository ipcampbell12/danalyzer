import pandas as pd
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess

manager = DataTaskManager()
audits_folder = manager.return_folders()["audits_folder"]
stamp_folder = manager.return_folders()["stamp_folder"]
output_path = manager.return_folders()["audits_output_folder"] / "HS Audit.xlsx"

cols_to_sort = ['Lastfirst','Student Number']

#Data frames
credits_df = pd.read_excel(audits_folder / "2-5 HS Audit Data - Credits.xlsx").sort_values(by=cols_to_sort)
cur_classes_df = pd.read_excel(audits_folder / "2-5 HS Audit Data - 24-25 Classes.xlsx")
prev_classes_df = pd.read_excel(audits_folder / "2-5 HS Audit Data - 23-24 Classes.xlsx")
cur_att_df = pd.read_excel(audits_folder / "24-25 Attendance Data.xlsx")
prev_att_df = pd.read_excel(audits_folder / "23-24 Attendance Data.xlsx")
stamp_scores_df=pd.read_excel(stamp_folder / "ODS Stamp Score Report.xlsx")

# print(credits_df.columns)
# print(prev_classes_df.columns)

#Concatenated data frames for attendance and classes
classes_df = pd.concat([cur_classes_df,prev_classes_df],ignore_index=True).sort_values(by=['Student Last, First','Student Number'])
att_df = pd.concat([cur_att_df,prev_att_df],ignore_index=True).sort_values(by=['Student Name'])

schools_to_check = ['Woodburn High School','Woodburn Success High School']
credits_df = credits_df[credits_df['Schoolname'].isin(schools_to_check)&credits_df['Earnedcrhrs']>0]
# Merge credits_df with classes_df to find unmatched credits
non_taught_df = credits_df[
    (credits_df['Course Name'].str.contains('Essential')==True) |
    (credits_df['Teacher Name']=='-') |
    (credits_df['Course Number']=='-')
]
non_taught_df = non_taught_df.drop(columns=['Schoolid','Grade','Current Schoolid','Course Number'])
# Filter for rows where the class in credits_df was not found in classes_df
# non_taught_df = non_taught_df[non_taught_df['_merge'] == 'left_only']

# # Drop the merge indicator column as it's no longer needed
# non_taught_df = non_taught_df.drop(columns=['_merge'])



#Show stutdents who got more then 2 years of STAMP credit
stamp_cols = ['Student Number','Lastfirst','Schoolname','Grade Level','Teacher Name','Course Name','Earnedcrhrs','Datestored','Termid']
stamp_df =credits_df[credits_df["Teacher Name"].str.contains("STAMP")][stamp_cols]
# print(stamp_df.columns)

#Show studnets who go inadequate score for STAMP test
selected_columns = ['Student ID', 'Test Score','Test Language','Test Subject','Test Date']
stamp_scores_df = stamp_scores_df[selected_columns]
stamp_scores_df =stamp_scores_df[stamp_scores_df["Test Language"]!="English"]
stamp_scores_df =stamp_scores_df[stamp_scores_df["Test Subject"]=="Composite"]
stamp_scores_df =stamp_scores_df.rename(columns={"Student ID":"Student Number"})
stamp_scores_df = pd.merge(stamp_df,stamp_scores_df,on="Student Number")

grouped_stamp_df = stamp_df.groupby(['Student Number','Lastfirst','Schoolname','Grade Level'])
grouped_stamp_df = grouped_stamp_df["Earnedcrhrs"].sum().reset_index().sort_values(by=['Lastfirst'])

concerning_stamp_df = stamp_df[
    (stamp_df["Course Name"] == "Spanish Composition")|
    (pd.to_datetime(stamp_df["Datestored"]) > pd.Timestamp("2024-11-01")) 
]


#Show students who have more then 8 credits
credits_df['Yearid'] = credits_df['Termid'].astype(str).str[:2] + '00'
credits_df['Yearid'] = pd.to_numeric(credits_df['Yearid'])
grouped_credits_df = credits_df.groupby(['Student Number','Lastfirst','Schoolname','Grade Level','Yearid'])
grouped_credits_df = grouped_credits_df["Earnedcrhrs"].sum().reset_index().sort_values(by=['Lastfirst'])
concerning_credit_df = grouped_credits_df[grouped_credits_df["Earnedcrhrs"]>8]
#Show students who have more then 5 non-taught credits
#Show students with work experience credits
work_df = credits_df[credits_df["Course Name"].str.contains("Work Experience")]
work_df = work_df.drop(columns=['Schoolid','Teacher Name','Grade','Current Schoolid','Course Number'])
work_total_df = work_df.groupby(['Student Number','Lastfirst','Schoolname','Grade Level','Yearid'])
work_total_df = work_total_df["Earnedcrhrs"].sum().reset_index().sort_values(by=['Lastfirst'])
att_df = att_df[["SID","Student Attendance Percent","Absence Days",'Yearid']]
print(att_df.columns)
print(work_total_df.columns)
work_total_df = work_total_df.merge(att_df,how='left',left_on=['Student Number','Yearid'],right_on=['SID','Yearid'])
concerning_work_df = work_total_df[work_total_df["Student Attendance Percent"]<90]

with pd.ExcelWriter(output_path,engine='openpyxl') as writer:
     concerning_credit_df.to_excel(writer,sheet_name="Concerning Credits Amounts",index=False)
     concerning_work_df.to_excel(writer,sheet_name="Concerning Work Credits",index=False)
     concerning_stamp_df.to_excel(writer,sheet_name="Concerning STAMP Credits",index=False)
     non_taught_df.to_excel(writer,sheet_name="Concerning Classes",index=False)
     # stamp_scores_df.to_excel(writer,sheet_name="STAMP Scores",index=False)
     stamp_df.to_excel(writer,sheet_name="STAMP Credits",index=False)
     # grouped_stamp_df.to_excel(writer,sheet_name="Grouped STAMP Credits",index=False)
     # grouped_credits_df.to_excel(writer,sheet_name="Total Credits",index=False) 
     
     work_df.to_excel(writer,sheet_name="Work Experience Credits",index=False)
     # work_total_df.to_excel(writer,sheet_name="Grouped Work Experience Credits",index=False)
     


adjust_column_widths(output_path)
subprocess.run(["start", "excel", output_path], shell=True)
import sys
import os
from task_manager import DataTaskManager
from Apps.ods_validator_app import validate_ods
from Apps.eld_enrollment_app import validate_eld_enrollment
from Apps.el_graduation_app import monitor_el_graduation
from Apps.class_size_app import generate_class_size_lists
from Apps.discipline_app import audit_discipline_discrepancies
from Apps.transcript_app import proccess_transcript
from Apps.mail_merge_app import create_mail_merge
from Apps.interview_runner_app import interview_tester
from Apps.group_by_app import group_by_spreadsheet
from Apps.clipboard_app import process_clipboard_to_excel_and_text
from Apps.Map_Analyzer.growth_analyzer_app import process_map_growth_data
from Apps.kinder_analyzer_app import analyzer_kinder_data
from Apps.Map_Analyzer.fluency_analyzer_app import process_fluency_data
from Apps.row_to_cols import process_course_data
from Apps.update_standards_app import update_standards
from Apps.course_pivoting_app import pivot_courses
from Apps.eighth_grade_credits_app import process_math_credits


manager = DataTaskManager()
folders = manager.return_folders()

# Dictionary of scripts and their required source folder keys
SCRIPTS = {
     "Process 8th Grade Credits":{
        "function": process_math_credits,
        "source_folders": [
             (folders['powerschool_folder'], 1)  
        ],
        "helper_messages": [
             "Select the 8th grade math export file",     
        ],
        "destination_folders": [
             folders["general_output_folder"]
        ]
     }
     ,
     "Pivot Courses":{
        "function": pivot_courses,
        "source_folders": [
             (folders['avid_folder'], 1)  
        ],
        "helper_messages": [
             "Add courses file",     
        ],
        "destination_folders": [
             folders["avid_folder"]
        ]
     },
      "Updated Standards Imports/Exports":{
        "function": update_standards,
        "source_folders": [
             (folders['powerschool_folder'], 1)  
        ],
        "helper_messages": [
             "Select the standards download file",     
        ],
        "destination_folders": [
             folders["desktop"]
        ]
     },
     "Process Course Requests":{
        "function": process_course_data,
        "source_folders": [
             (folders['powerschool_folder'], 2)  
        ],
        "helper_messages": [
             "Select the student file",
             "Select the course requests file",      
        ],
        "destination_folders": [
             folders["general_output_folder"]
        ] 
     },
     "Analyze Kinder Data":{
        "function": analyzer_kinder_data,
        "source_folders": [
             (folders["map_folder"],4),
             (folders['powerschool_folder'], 2),
             (folders["clever_folder"],1)
             
        ],
        "helper_messages": [
             "Select the Fall MAP Growth File",
             "Select the Winter MAP Growth File",
             "Select the Fall MAP Fluency File",
             "Select the Winter MAP Fluency File",
             "Select the PowerSchool Quick Export File",
             "Select the PowerSchool Reading Levels File",
             "Select the mClass file"
             
        ],
        "destination_folders": [
             folders["general_output_folder"]
        ] 
     }
     ,
     "Handle Email/Username Imports": {
        "function": process_clipboard_to_excel_and_text,
        "source_folders": [
             (folders['powerschool_folder'], 1)
        ],
        "helper_messages": [
             "Select the EMAIL IMPORTER FILE only"
        ],
        "destination_folders": [
             folders["imports_folder"]
        ]
     },
     "Disaggregate MAP Growth Data": {
        "function": process_map_growth_data,
        "source_folders": [
            (folders['map_folder'], 3),
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "Select the Fall MAP Growth file to process",
            "Select the Winter MAP Growth file to process",
            "Select the Spring MAP Growth file to process",
            "Select PowerSchool demographics file",
            "Select PowerSchool language program file"
        ],
        "destination_folders": [folders['map_output_folder']]
     },
     "Disaggregate MAP Fluency Data": {
        "function": process_fluency_data,
        "source_folders": [
            (folders['map_folder'], 3),
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "Select the Fall MAP Fluency file to process",
            "Select the Winter MAP Fluency file to process",
            "Select the Spring MAP Fluency file to process",
            "Select PowerSchool demographics file",
            "Select PowerSchool language program file"
        ],
        "destination_folders": [folders['map_output_folder']]
     },
     "General Dissag Function": {
           "function": process_map_growth_data,
        "source_folders": [
            (folders['map_folder'], 1),
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "Select the MAP Growth file to process",
            "Select PowerSchool demographics file",
            "Select PowerSchool language program file"
        ],
        "destination_folders": [folders['map_output_folder']]
     },
    "Validate ELD Enrollment": {
        "function": validate_eld_enrollment,
        "source_folders": [
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "EL Students file",
            "ELD Classes file",
        ],
        "destination_folders": [folders['eld_enrollment_folder']]
    },
    "Audit ELD Graduation": {
        "function": monitor_el_graduation,
        "source_folders": [
            (folders['powerschool_folder'], 3)
        ],
        "helper_messages": [
            "Historical grades file",
            "EL students file",
            "Failed classes file",
        ],
        "destination_folders": [folders['el_graduation_folder']]
    },
    "Validate ODS": {
        "function": validate_ods,
        "source_folders": [
            (folders['ods_folder'], 1),
            (folders['powerschool_folder'], 1)
        ],
        "helper_messages": [
            "ODS student data.",
            "PowerSchool student data"
        ],
        "destination_folders": [folders['ods_validations_folder']]
    },
    "Audit Discipline Discrepancies": {
        "function": audit_discipline_discrepancies,
        "source_folders": [
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "Discipline Incidents file",
            "Absences file"
        ],
        "destination_folders": [folders['discipline_folder']]
    },
    "Proccess Transcripts": {
        "function": proccess_transcript,
        "source_folders": [
            (folders['transcripts_folder'], 1)
        ],
        "helper_messages": [
            "Select transcript to process",
        ],
        "destination_folders": [folders['sealed_transcripts_folder']]
    },
    "Audit Class Size": {
        "function": generate_class_size_lists,
        "source_folders": [
            (folders['powerschool_folder'],2),
            (folders['ode'],1)
        ],
        "helper_messages": [
            "Primary enrollments file",
            "Secondary enrollments file",
            "Course Name file",
        ],
        "destination_folders": [folders['class_size_folder']]
    },
    "Create Mail Merge": {
        "function": create_mail_merge,
        "source_folders": [
            (folders['powerschool_folder'],3)
        ],
        "helper_messages": [
            "Juaquina download",
            "ELs Download",
            "ELA Class Download",
        ],
        "destination_folders": [folders["elpa_cards"]]
    },
    "Check Interview Answers": {
        "function": interview_tester,
        "source_folders": [
            (folders['fake_data_folder'],2)
        ],
        "helper_messages": [
            "Check sheet",
            "Submission sheet"
        ],
        "destination_folders": []
    },
    "Group a Spreadsheet": {
        "function": group_by_spreadsheet,
        "source_folders": [
            (folders['powerschool_folder'],1)
        ],
        "helper_messages": [
            "File to group",
        ],
        "destination_folders": [folders["grouped_folder"]],
        "additioanal_inputs":[
             {
               "type": "multi-dropdown", 
               "label": "Select Columns to Group By", 
               "var_name": "selected_columns",
               "options": ["Student Name", "Grade", "Test Score", "Percentile", "School"]
             },
        ]
    },
 

}

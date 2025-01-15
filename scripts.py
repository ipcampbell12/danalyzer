import sys
import os
from task_manager import DataTaskManager
from ods_validator_app import validate_ods
from eld_enrollment_app import validate_eld_enrollment
from el_graduation_app import monitor_el_graduation
from class_size_app import generate_class_size_lists
from discipline_app import audit_discipline_discrepancies
from transcript_app import proccess_transcript
from mail_merge_app import create_mail_merge
from interview_runner import interview_tester
from group_by import group_by_spreadsheet

manager = DataTaskManager()
folders = manager.return_folders()

# Dictionary of scripts and their required source folder keys
SCRIPTS = {
    "Validate ELD Enrollment": {
        "function": validate_eld_enrollment,
        "source_folders": [
            (folders['powerschool_folder'], 2)
        ],
        "helper_messages": [
            "EL Students file",
            "ELD Classes file"
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
            (folders['powerschool_folder'],3)
        ],
        "helper_messages": [
            "Primary enrollments file",
            "Secondary enrollments file",
            "IUID file",
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
        "destination_folders": [folders["grouped_folder"]]
    },
}

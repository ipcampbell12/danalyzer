import pyperclip
from pathlib import Path
import pandas as pd

class DataTaskManager:
    def __init__(self):

        self.folders = {
            "dessa_folder":Path(r"C:\Users\inpcampbell\Desktop\DESSA"),
            "clever_folder":Path(r"C:\Users\inpcampbell\Desktop\Clever"),
            "audits_output_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Audits Folder"),
            "transcripts_folder": Path(r"C:\Users\inpcampbell\Desktop\Transcripts"),
            "assets_folder": Path(r"C:\Users\inpcampbell\Desktop\Danalyzer\Assets"),
            "sealed_transcripts_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Processed Transcripts"),
            "powerschool_folder": Path(r"C:\Users\inpcampbell\Desktop\PowerSchool"),
            "ods_folder": Path(r"C:\Users\inpcampbell\Desktop\ODS"),
            "ods_validations_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\ODS Validation"),
            "class_size_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Master Schedule with Class Size"),
            "sports_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Sports Attendance"),
            "el_graduation_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\EL Graduation Progress"),
            "yearly_numbers_folder ": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Yearly Numbers"),
            "discipline_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Discipline Discrepancies"),
            "aperture_folder": Path(r"C:\Users\inpcampbell\Desktop\Aperture"),
            "general_output_folder": Path(r"C:\Users\inpcampbell\Desktop\Processing Output\General Output"),
            # "dessa_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\DESSA Reports"),
            "downloads_folder":Path(r"C:\Users\inpcampbell\Downloads"),
            "elpa_cards":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\ELPA Testing Cards"),
            "eld_enrollment_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\ELD Class Enrollment"),
            "fake_data_folder":Path(r"C:\Users\inpcampbell\Desktop\Fake Data"),
            "grouped_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Grouped Files"),
            "stamp_folder":Path(r"C:\Users\inpcampbell\Desktop\STAMP"),
            "audits_folder":Path(r"C:\Users\inpcampbell\Desktop\Audits"),
            "imports_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\Email Imports"),
            "map_folder":Path(r"C:\Users\inpcampbell\Desktop\MAP"),
            "map_output_folder":Path(r"C:\Users\inpcampbell\Desktop\Processing Output\MAP Analysis"),
            "desktop":Path(r"C:\Users\inpcampbell\Desktop"),
            "ode":Path(r"C:\Users\inpcampbell\Desktop\ODE"),
            "avid_folder":Path(r"C:\Users\inpcampbell\Desktop\PowerSchool\AVID Data Analysis"),
        }
        self.language_lookup = Path(r"C:\Users\inpcampbell\Desktop\ODE\Language Codes.xlsx")
        # Dictionary containing complex properties for each task
        self.task_dict = {
            "Find Discipline Discrepancies": {
                "script": "discipline_app.py",
                "fields": "discipline_fields",
                "query": "discipline_query",
                "folders": ["powerschool_folder", "discipline_folder"]
            },
            "Validate ELD Enrollment": {
                "script": "eld_enrollment_app.py",
                "fields": "eld_fields",
                "query": "eld_query",
                "folders": ["eld_folder1", "eld_folder2"]
            },
            "Audit ELD Graduation": {
                "script": "el_graduation_app.py",
                "fields": "student_number \n State_StudentNumber \n grade_level \n ^([schools]name) \n S_OR_STU_X.ELFg \n S_OR_STU_LEP_X.StartDt",
                "query": "S_OR_STU_X.ELFg=1;grade_level>=9",
                "folders": ['powerschool_folder','el_graduation_folder']
            },
            "Find Yearly Numbers": {
                "script": "yearly_numbers_app.py",
                "fields": "yearly_fields",
                "query": "yearly_query",
                "folders": ["yearly_folder1", "yearly_folder2"]
            },
            "Validate ODS": {
                "script": "ods_validator_app.py",
                "fields": "ods_fields",
                "query": "ods_query",
                "folders": ["ods_folder1", "ods_folder2"]
            },
            "Audit Class Size": {
                "script": "class_size_app.py",
                "fields": "class_size_fields",
                "query": "class_size_query",
                "folders": ["powerschool_folder", "class_size_folder"]
            },
            "Group By App": {
                "script": "group_by_app.py",
                "fields": "group_by_fields",
                "query": "class_size_query",
                "folders": ["powerschool_folder"]
            },
        }

    def get_script(self, task_name):
        """Retrieve the script file associated with the given task name."""
        task = self.task_dict.get(task_name)
        if task:
            return task["script"]
        else:
            return "Script not found."
    
    def lookup_language(self, code):
        try:
            language_df = pd.read_excel(self.language_lookup,sheet_name='Code Tables')
            result = language_df.loc[language_df['Code'] == code, 'Description']
            
            if result.empty:
                raise ValueError(f"No language found for code: {code}")
            print("The language is: ", result.values[0])
            return result.values[0]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_fields(self, task_name):
        """Retrieve the fields associated with the given task name."""
        task = self.task_dict.get(task_name)
        if task:
            return task["fields"]
        else:
            return "Fields not found."

    def get_query(self, task_name):
        """Retrieve the query associated with the given task name."""
        task = self.task_dict.get(task_name)
        if task:
            return task["query"]
        else:
            return "Query not found."

    def get_folders(self, task_name):
        """Retrieve the folder paths associated with the given task name."""
        task = self.task_dict.get(task_name)
        if task:
            # Retrieve folder names from the task
            folder_names = task["folders"]
            # Map folder names to actual folder paths using self.folders
            folder_paths = {folder_name: str(self.folders[folder_name]) for folder_name in folder_names}
            return folder_paths
        else:
            return "Folders not found."
    def return_folders(self):
        return self.folders

    def copy_to_clipboard(self, task_name):
        """Copy the script, fields, query, and folder paths to the clipboard."""
        task = self.task_dict.get(task_name)
        
        if task:
            content = f"Script: {task['script']}\n" \
                      f"Fields: {task['fields']}\n" \
                      f"Query: {task['query']}\n" \
                      f"Folders: {', '.join(task['folders'])}"
            pyperclip.copy(content)
            print(f"Task '{task_name}' content has been copied to the clipboard:\n{content}")
        else:
            print(f"Task '{task_name}' not found.")



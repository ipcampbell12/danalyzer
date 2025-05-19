<<<<<<< HEAD
# import subprocess
# import os
# import ttkbootstrap as tb
# from ttkbootstrap import Style
# from functools import partial
# from ttkbootstrap.constants import *
# from ttkbootstrap.dialogs import Messagebox
# from other_funcs import delete_files_in_directory
# import pyperclip
# from task_manager import DataTaskManager
# from Apps.ods_validator_app import validate_ods
# from eld_enrollment_app import validate_eld_enrollment
# from Apps.el_graduation_app import monitor_el_graduation
# from class_size_app import generate_class_size_lists

# manager = DataTaskManager()
# folders = manager.return_folders()

# # Folder and script dictionaries
# source_dict = {
#     "PowerSchool":folders['powerschool_folder'],
#     "ODS": folders['ods_folder'],
#     "Transcripts": folders['transcripts_folder']
# }

# dest_dict = {
#     "Validate ELD Enrollment":folders['eld_enrollment_folder'] ,
#     "Audit ELD Graduation":folders['el_graduation_folder'],
#     "Validate ODS": folders['ods_validations_folder'],
#     "Audit Class Size": folders['class_size_folder'],
# }

# script_dict = {
#     "Audit Class Size": generate_class_size_lists,
#     "Validate ELD Enrollment": validate_eld_enrollment,
#     "Audit ELD Graduation": monitor_el_graduation,
#     "Validate ODS": validate_ods,
# }

# clipboard_dict = {
    
# }


# # Create root window with ttkbootstrap style
# root = tb.Window(themename="flatly")
# root.title("Danalyzer App")
# root.geometry("500x500")

# # Add a style for better visuals
# style = Style()

# # Labels and Comboboxes

# app_label = tb.Label(root, text="Select a script to run:", font=("Helvetica", 12))
# app_label.pack(padx=10, pady=10)

# app_combo = tb.Combobox(root, values=list(script_dict.keys()), width=50)
# app_combo.pack(padx=10, pady=10)

# # Function to handle selection change
# def on_select(event):
#     selected_key = combo.get()
#     print(f"Selected key: '{selected_key}'")
#     print(f"Available keys: {list(source_dict.keys())}")
#     folder_select = source_dict[selected_key]
#     print(f"You selected folder: {folder_select}")


# def clear_downloads():
#     delete_files_in_directory(downloads_folder)
#     return [True,"Downloads folder cleared!"]

# def copyToClipBoard():
#     Queries_And_Fields.copy_to_clipboard(clipboard_dict)
#     return [True,"Fields copied!"]

# def run_script():
#     selected_key = app_combo.get().strip()
#     print(f"The key is {selected_key}")
#     if selected_key in script_dict:
#         script_path = script_dict[selected_key]
#         print(f"The script path is {script_path}")
#         if os.path.exists(script_path):
#             try:
#                 result = subprocess.run(
#                     ["python", script_path],
#                     capture_output=True,
#                     text=True,
#                     check=True
#                 )
#                 Messagebox.show_info(result.stdout, title="Output")
#                 return True  # Indicate success
#             except subprocess.CalledProcessError as e:
#                 Messagebox.show_error(f"Script failed:\n{e.stderr}", title="Error")
#                 return False
#             except Exception as e:
#                 Messagebox.show_error(f"An error occurred:\n{e}", title="Error")
#                 return False
#         else:
#             Messagebox.show_error(f"Script file not found: {script_path}", title="Error")
#             return False
#     else:
#         Messagebox.show_error("Please select a valid script.", title="Error")
#         return False

# # Function to display success message after running script
# def on_button_click(function):
#     success = function()
#     if success[0]:
#         success_label = tb.Label(root, text=f"Success! {success[1]}", bootstyle=SUCCESS, font=("Helvetica", 12))
#         success_label.pack(pady=20)
#         root.after(3500, success_label.destroy)

# # Bind event for combo selection
# combo.bind("<<ComboboxSelected>>", on_select)

# # Run button
# run_button = tb.Button(root, text="Run Script", command=partial(on_button_click,run_script), bootstyle=PRIMARY)
# run_button.pack(padx=10, pady=20)

# run_button = tb.Button(root, text="Clear Downloads", command=partial(on_button_click,clear_downloads), bootstyle=DANGER)
# run_button.pack(padx=10, pady=20)

# run_button = tb.Button(root, text="Clear Downloads", command=partial(on_button_click,copyToClipBoard), bootstyle=INFO)
# run_button.pack(padx=10, pady=20)



# # Start the application
# root.mainloop()
=======
import subprocess
import os
import ttkbootstrap as tb
from ttkbootstrap import Style
from functools import partial
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from other_funcs import delete_files_in_directory
import pyperclip
from Scripts.task_manager import DataTaskManager
from ods_validator_app import validate_ods
from eld_enrollment_app import validate_eld_enrollment
from el_graduation_app import monitor_el_graduation
from class_size_app import generate_class_size_lists

manager = DataTaskManager()
folders = manager.return_folders()

# Folder and script dictionaries
source_dict = {
    "PowerSchool":folders['powerschool_folder'],
    "ODS": folders['ods_folder'],
    "Transcripts": folders['transcripts_folder']
}

dest_dict = {
    "Validate ELD Enrollment":folders['eld_enrollment_folder'] ,
    "Audit ELD Graduation":folders['el_graduation_folder'],
    "Validate ODS": folders['ods_validations_folder'],
    "Audit Class Size": folders['class_size_folder'],
}

script_dict = {
    "Audit Class Size": generate_class_size_lists,
    "Validate ELD Enrollment": validate_eld_enrollment,
    "Audit ELD Graduation": monitor_el_graduation,
    "Validate ODS": validate_ods,
}

clipboard_dict = {
    
}


# Create root window with ttkbootstrap style
root = tb.Window(themename="flatly")
root.title("Danalyzer App")
root.geometry("500x500")

# Add a style for better visuals
style = Style()

# Labels and Comboboxes

app_label = tb.Label(root, text="Select a script to run:", font=("Helvetica", 12))
app_label.pack(padx=10, pady=10)

app_combo = tb.Combobox(root, values=list(script_dict.keys()), width=50)
app_combo.pack(padx=10, pady=10)

# Function to handle selection change
def on_select(event):
    selected_key = combo.get()
    print(f"Selected key: '{selected_key}'")
    print(f"Available keys: {list(source_dict.keys())}")
    folder_select = source_dict[selected_key]
    print(f"You selected folder: {folder_select}")


def clear_downloads():
    delete_files_in_directory(downloads_folder)
    return [True,"Downloads folder cleared!"]

def copyToClipBoard():
    Queries_And_Fields.copy_to_clipboard(clipboard_dict)
    return [True,"Fields copied!"]

def run_script():
    selected_key = app_combo.get().strip()
    print(f"The key is {selected_key}")
    if selected_key in script_dict:
        script_path = script_dict[selected_key]
        print(f"The script path is {script_path}")
        if os.path.exists(script_path):
            try:
                result = subprocess.run(
                    ["python", script_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                Messagebox.show_info(result.stdout, title="Output")
                return True  # Indicate success
            except subprocess.CalledProcessError as e:
                Messagebox.show_error(f"Script failed:\n{e.stderr}", title="Error")
                return False
            except Exception as e:
                Messagebox.show_error(f"An error occurred:\n{e}", title="Error")
                return False
        else:
            Messagebox.show_error(f"Script file not found: {script_path}", title="Error")
            return False
    else:
        Messagebox.show_error("Please select a valid script.", title="Error")
        return False

# Function to display success message after running script
def on_button_click(function):
    success = function()
    if success[0]:
        success_label = tb.Label(root, text=f"Success! {success[1]}", bootstyle=SUCCESS, font=("Helvetica", 12))
        success_label.pack(pady=20)
        root.after(3500, success_label.destroy)

# Bind event for combo selection
combo.bind("<<ComboboxSelected>>", on_select)

# Run button
run_button = tb.Button(root, text="Run Script", command=partial(on_button_click,run_script), bootstyle=PRIMARY)
run_button.pack(padx=10, pady=20)

run_button = tb.Button(root, text="Clear Downloads", command=partial(on_button_click,clear_downloads), bootstyle=DANGER)
run_button.pack(padx=10, pady=20)

run_button = tb.Button(root, text="Clear Downloads", command=partial(on_button_click,copyToClipBoard), bootstyle=INFO)
run_button.pack(padx=10, pady=20)



# Start the application
root.mainloop()
>>>>>>> 8a62c288c787e2496f36739d0a2a3a91789d9b12

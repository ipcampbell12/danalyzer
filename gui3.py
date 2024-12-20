import os
import ttkbootstrap as tb
from tkinter import messagebox
from scripts import SCRIPTS
from task_manager import DataTaskManager

# Initialize the DataTaskManager to get the folders
manager = DataTaskManager()
folders = manager.return_folders()

# Function to update file dropdowns based on the selected script
def update_file_dropdowns(event):
    selected_script = script_combobox.get()
    script_info = SCRIPTS[selected_script]
    source_requirements = script_info["source_folders"]
    helper_messages = script_info["helper_messages"]
    print(helper_messages)

    # Clear any existing dropdowns
    for widget in file_frame.winfo_children():
        widget.destroy()

    # Clear the previous file_comboboxes list
    file_comboboxes.clear()

    # Create dropdowns for each source folder requirement
    for index, (folder_path, num_files) in enumerate(source_requirements):
        if not os.path.exists(folder_path):
            tb.Label(file_frame, text=f"Folder '{folder_path}' not found!", bootstyle="warning").pack(pady=2)
            continue
        print(num_files)
        # List files in the folder
        try:
            files = os.listdir(folder_path)
        except FileNotFoundError:
            files = []
            tb.Label(file_frame, text="Folder not found!", bootstyle="danger").pack(pady=2)

        # For each file to be selected, create a file selector and its helper message
        for i in range(num_files):
            file_label = f"Select file {i+1} from {folder_path}:"
            print(file_label)
            print(folder_path)
            tb.Label(file_frame, text=file_label).pack(pady=2)

            # Create the helper message
            tb.Label(file_frame, text=helper_messages[i], bootstyle="info").pack(pady=2)

            # File combobox for file selection
            file_combobox = tb.Combobox(file_frame, values=files, bootstyle="info",width=50)
            file_combobox.pack(pady=5)
            file_comboboxes.append((file_combobox, folder_path))

    # Handle the destination folders (no file selection needed)
    dest_requirements = script_info["destination_folders"]
    for folder_path in dest_requirements:
        tb.Label(file_frame, text=f"Destination folder: {folder_path}").pack(pady=2)

# Function to handle button click and display success messages
def on_button_click(function):
    success = function()
    if success[0] and success[1] == "Check Interview Answers":
        correct_label = tb.Label(root, text=f"{success[2][0]}", bootstyle="success", font=("Helvetica", 12,"bold"))
        correct_label.pack(pady=20)
        wrong_label = tb.Label(root, text=f"{success[2][1]}", bootstyle="danger", font=("Helvetica", 12,"bold"))
        wrong_label.pack(pady=20)
        root.after(3500, success_label.destroy)
    elif success[0]:
        success_label = tb.Label(root, text=f"Success! {success[1]}", bootstyle="success", font=("Helvetica", 12))
        success_label.pack(pady=10)
        root.after(3500, success_label.destroy)

# Function to run the selected script with selected files
def run_script():
    script_name = script_combobox.get()
    script_info = SCRIPTS.get(script_name)

    if not script_name or not script_info:
        messagebox.showwarning("Warning", "Please select a script.")
        return

    # Get selected file paths for source folders
    file_paths = []
    for combobox, folder_path in file_comboboxes:
        file_name = combobox.get()
        if not file_name:
            messagebox.showwarning("Warning", "Please select all required files in the correct order.")
            return
        file_paths.append(os.path.join(folder_path, file_name))

    # Handle destination folders (no file selection needed)
    dest_folders = script_info["destination_folders"]

    # Execute the script function with the selected files using on_button_click
    def execute():
        try:
            if script_name == "Check Interview Answers":
                results = script_info["function"](*file_paths, *dest_folders)
                print(results)
                return (True, script_name, results)
            else:
                script_info["function"](*file_paths, *dest_folders)
                return (True, f"{script_name} executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error executing script: {e}")
            return (False, "")

    on_button_click(execute)

# Function to clear script selection and dynamically generated dropdowns
def clear_selection():
    # Clear script combobox selection
    script_combobox.set('')

    # Clear dynamically generated file selection dropdowns
    for widget in file_frame.winfo_children():
        widget.destroy()

    # Clear the file_comboboxes list
    file_comboboxes.clear()

# Create the main window using ttkbootstrap
root = tb.Window(themename="flatly")
root.title("WSD Data Cookbook")
root.geometry("600x500")

# Dropdown for selecting a script
tb.Label(root, text="Select a Script:", font=("Helvetica", 12)).pack(pady=5)
script_combobox = tb.Combobox(root, values=list(SCRIPTS.keys()), bootstyle="primary")
script_combobox.pack(pady=5)
script_combobox.bind("<<ComboboxSelected>>", update_file_dropdowns)

# Frame to hold file dropdowns
file_frame = tb.Frame(root)
file_frame.pack(pady=20)

# File combobox list
file_comboboxes = []

# Clear button
clear_button = tb.Button(root, text="Clear", bootstyle="secondary", command=clear_selection)
clear_button.pack(pady=10)

# Run button
run_button = tb.Button(root, text="Run Script", bootstyle="success", command=run_script)
run_button.pack(pady=10)

root.mainloop()

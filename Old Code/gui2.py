import os
import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, WARNING, DANGER
from tkinter import messagebox
from Scripts.scripts import SCRIPTS
from Scripts.task_manager import DataTaskManager

# Initialize the DataTaskManager to get the folders
manager = DataTaskManager()
folders = manager.return_folders()

# Function to update file dropdowns based on the selected script
def update_file_dropdowns(event):
    selected_script = script_combobox.get()
    script_info = SCRIPTS[selected_script]
    source_requirements = script_info["source_folders"]

    # Clear any existing dropdowns
    for widget in file_frame.winfo_children():
        widget.destroy()

    # Clear the previous file_comboboxes list
    file_comboboxes.clear()

    # Create dropdowns for each source folder requirement
    for folder_path, num_files in source_requirements:
        if not os.path.exists(folder_path):
            tb.Label(file_frame, text=f"Folder '{folder_path}' not found!", bootstyle=WARNING).pack(pady=2)
            continue

        # Label for the source folder
        tb.Label(file_frame, text=f"Select {num_files} file(s) from {folder_path}:").pack(pady=2)

        # List files in the folder
        try:
            files = os.listdir(folder_path)
        except FileNotFoundError:
            files = []
            tb.Label(file_frame, text="Folder not found!", bootstyle=DANGER).pack(pady=2)

        # Create dropdowns based on the required number of files
        for i in range(num_files):
            file_combobox = tb.Combobox(file_frame, values=files, bootstyle="info")
            file_combobox.pack(pady=5)
            file_comboboxes.append((file_combobox, folder_path))

    # Handle the destination folders (no file selection required)
    dest_requirements = script_info["destination_folders"]
    for folder_path in dest_requirements:
        tb.Label(file_frame, text=f"Destination folder: {folder_path}").pack(pady=2)

# Function to handle button click and display success messages
def on_button_click(function):
    success = function()
    if success[0]:
        success_label = tb.Label(root, text=f"Success! {success[1]}", bootstyle=SUCCESS, font=("Helvetica", 12))
        success_label.pack(pady=20)
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
            messagebox.showwarning("Warning", "Please select all required files.")
            return
        file_paths.append(os.path.join(folder_path, file_name))

    # Handle destination folders (no file selection needed)
    dest_folders = script_info["destination_folders"]

    # Execute the script function with the selected files using on_button_click
    def execute():
        try:
            script_info["function"](*file_paths, *dest_folders)
            return (True, f"{script_name} executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error executing script: {e}")
            return (False, "")

    on_button_click(execute)

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
root.title("Script Runner")
root.geometry("600x500")

# Dropdown for selecting a script
tb.Label(root, text="Select a Script:", font=("Helvetica", 12)).pack(pady=5)
script_combobox = tb.Combobox(root, values=list(SCRIPTS.keys()), bootstyle="primary")
script_combobox.pack(pady=5)
script_combobox.bind("<<ComboboxSelected>>", update_file_dropdowns)

# Frame to hold file dropdowns
file_frame = tb.Frame(root)
file_frame.pack(pady=10)

# Store file dropdowns
file_comboboxes = []

# Button to run the selected script
run_button = tb.Button(root, text="Run Script", bootstyle="success", command=run_script)
run_button.pack(pady=20)

# Button to clear the selection
clear_button = tb.Button(root, text="Clear Selection", bootstyle="danger", command=clear_selection)
clear_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()

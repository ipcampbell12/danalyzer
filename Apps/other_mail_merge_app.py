import os
import pandas as pd
import win32com.client as win32

# Step 1: Split the Excel workbook into separate files for each sheet
def split_excel_sheets(excel_file, dest_folder):
    excel_data = pd.ExcelFile(excel_file)
    excel_files = []
    for sheet_name in excel_data.sheet_names:
        sheet_data = excel_data.parse(sheet_name)
        sheet_file = os.path.join(dest_folder, f'{sheet_name}_data.xlsx')
        sheet_data.to_excel(sheet_file, index=False)
        excel_files.append(sheet_file)
    print("Excel sheets have been split into separate files.")
    return excel_files

# Step 2: Perform the mail merge in Word for each Excel sheet
def run_mail_merge(excel_file, label_template, output_file):
    word = win32.Dispatch("Word.Application")
    word.Visible = False  # Set to True if you want to see the process
    
    try:
        # Open the label template
        doc = word.Documents.Open(label_template)
        
        # Perform the mail merge
        doc.MailMerge.OpenDataSource(Name=excel_file)
        doc.MailMerge.Execute()
        
        # Save the generated document
        doc.SaveAs(output_file)
        doc.Close()
        print(f"Mail merge completed for {excel_file}, saved as {output_file}")
    except Exception as e:
        print(f"An error occurred during mail merge: {e}")
    finally:
        word.Quit()

# Step 3: Cleanup the temporary Excel files
def cleanup_excel_files(excel_files):
    for file in excel_files:
        os.remove(file)
        print(f"Deleted temporary file: {file}")

# Step 4: Automate the entire process for each tab in the Excel file
def automate_mail_merge(excel_file, label_template, dest_folder):
    # Step 1: Split the Excel sheets into separate files
    excel_files = split_excel_sheets(excel_file, dest_folder)

    # Step 2: Run the mail merge for each Excel sheet
    for sheet_file in excel_files:
        sheet_name = os.path.splitext(os.path.basename(sheet_file))[0].replace('_data', '')
        output_file = os.path.join(dest_folder, f'{sheet_name}_labels.docx')
        run_mail_merge(sheet_file, label_template, output_file)

    # Step 3: Cleanup the temporary Excel files
    cleanup_excel_files(excel_files)

# Example usage
excel_file = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\ELPA Labels\All ELPA - Cols.xlsx"  # Your Excel file
label_template = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\ELPA Labels\ELPA Labels Template.doc"  # Your Word label template
dest_folder = r"C:\Users\inpcampbell\Desktop\ODE\Historical Assessment Data\ELPA Labels"
# automate_mail_merge(excel_file, label_template, dest_folder)
split_excel_sheets(excel_file,dest_folder)
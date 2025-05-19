import pandas as pd



def update_standards(standards_path,dest_folder):
    
    active=False
#     active = False
    # Read the tab-delimited file into a DataFrame
    standards_df = pd.read_csv(standards_path, delimiter="\t",encoding="latin-1")
    print(standards_df.head())

    # Update IsActive column based on the active flag
    if not active:
        standards_df["IsActive"] = standards_df["IsActive"].replace(1, 0)
    else:
        standards_df["IsActive"] = standards_df["IsActive"].replace(0, 1)

    # Save the updated DataFrame back to a tab-delimited file
    output_path = dest_folder / "standards_import.txt"
    standards_df.to_csv(output_path, sep="\t", index=False)

    print("File saved as standards_import.txt")
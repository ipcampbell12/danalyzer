import pandas as pd
import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager

def pivot_rows_to_cols(df, mapping, new_col, map_col, index_cols, val_cols, multi_index=False):
    """
    Pivots rows to columns based on a mapping and allows for flexible index and value columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        mapping (dict): A dictionary to map values in `map_col` to new column names.
        new_col (str): The name of the new column created from the mapping.
        map_col (str): The column to apply the mapping to.
        index_cols (list): A list of columns to use as the index.
        val_cols (list): A list of columns to use as values.
        multi_index (bool): Whether to keep a multi-level index (default is False).

    Returns:
        pd.DataFrame: The pivoted DataFrame.
    """
    # Map the values in the specified column
    df[new_col] = df[map_col].map(mapping)

    # Perform the pivot operation
    df = df.pivot_table(
        index=index_cols,
        columns=new_col,
        values=val_cols,
        aggfunc=lambda x: ', '.join(map(str, x)),
        fill_value=""
    )

    # Flatten the multi-level columns if multi_index is False
    if not multi_index:
        df.columns = [
            f"{col[1]} {col[0]}" if isinstance(col, tuple) else col for col in df.columns
        ]
        df = df.reset_index()

    return df


# Example usage
manager = DataTaskManager()
ps_folder = manager.return_folders()["powerschool_folder"]
dest_folder = manager.return_folders()["general_output_folder"]
data_path = os.path.join(ps_folder, "23-24 WHS Credits.xlsx")
data_df = pd.read_excel(data_path)

new_col = "Student Grades"
map_col = "Grade"
index_cols = ["Lastfirst", "Student Number"]
val_cols = ["Grade"]

# new_df = pivot_rows_to_cols(
#     data_df,
#     mapping={"A": "A", "B": "B", "C": "C", "D": "D", "F": "F"},
#     new_col=new_col,
#     map_col=map_col,
#     index_cols=index_cols,
#     val_cols=val_cols,
#     multi_index=False
# )
def concatenate_grades(df, group_by_col, grade_col):
    """
    Concatenates all grades for each unique value in the group_by_col into a single string.

    Args:
        df (pd.DataFrame): The input DataFrame.
        group_by_col (str): The column to group by (e.g., "Student Number").
        grade_col (str): The column containing grades to concatenate.

    Returns:
        pd.DataFrame: A DataFrame with the grouped column and concatenated grades.
    """
    # Ensure all values in the grade column are strings
    df[grade_col] = df[grade_col].astype(str)

    # Group by the specified column and concatenate grades into a single string
    concatenated_df = df.groupby(group_by_col)[grade_col].apply(lambda x: ', '.join(x)).reset_index()
    concatenated_df.rename(columns={grade_col: "All Grades"}, inplace=True)

    # Identify bad grades (F, I, NP)
    concatenated_df["Bad Grades"] = concatenated_df["All Grades"].apply(
        lambda x: ', '.join([grade for grade in ["F", "I", "NP"] if grade in x])
    )
    concatenated_df["NotGotBadGrade?"] = concatenated_df["All Grades"].apply(
        lambda x: not any(grade in x for grade in ["F", "I", "NP"])
    )
    return concatenated_df

new_df = concatenate_grades(data_df, "Student Number", "Grade")
# Save the pivoted DataFrame to an Excel file
output_path = os.path.join(dest_folder, "Pivoted_Data.xlsx")
new_df.to_excel(output_path, index=False)
adjust_column_widths(output_path)

subprocess.run(["start", "excel", output_path], shell=True)

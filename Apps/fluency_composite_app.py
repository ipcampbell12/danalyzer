import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess

def get_fluency_composite(fluency_df, term):
    demo_cols = [  
        'SchoolName',
        'TermName', 
        'StudentLastName',
        'StudentFirstName', 
        'StudentID', 
        'Grade'
    ]

    performance_mapping = {
        'Meets Expectation': 3,
        'Below Expectation': 1,
        'Approaching Expectation': 2,
        'Exceeds Expectation': 4,
    }

    performance_cols = [col for col in fluency_df.columns.to_list() if "PerformanceLevel" in col]

    # Filter the DataFrame to include only the columns in demo_cols and performance_cols
    fluency_df = fluency_df[demo_cols + performance_cols]

    # Map performance levels to numerical values
    for col in performance_cols:
        fluency_df[col] = fluency_df[col].map(performance_mapping)

    # Create a new column for the total score
    fluency_df[f'{term} MapFluencyCompositeScore'] = fluency_df[performance_cols].sum(axis=1)

    # Create a new column for the quartile numbers
    fluency_df['QuartileNumber'] = pd.qcut(fluency_df[f'{term} MapFluencyCompositeScore'], 4, labels=[1, 2, 3, 4])

    # Create a new column for the quartile text labels using the keys from performance_mapping
    sorted_labels = sorted(performance_mapping, key=performance_mapping.get)
    fluency_df[f'{term} MAPFluencyCompositeLevel'] = fluency_df['QuartileNumber'].map(lambda x: sorted_labels[int(x) - 1])

    # Aggregate to keep only the row with the highest score for each StudentID
    idx = fluency_df.groupby('StudentID')[f'{term} MapFluencyCompositeScore'].idxmax()
    fluency_df = fluency_df.loc[idx]
    
    print(f"The fluency df cols are {fluency_df.columns}")
    return fluency_df

# Example usage
# fluency_df = pd.read_excel("path_to_fluency_data.xlsx")
# term = "Fall"
# updated_fluency_df = get_fluency_composite(fluency_df, term)
# updated_fluency_df.to_excel("Updated_MAP_Fluency_Download.xlsx", index=False)
# adjust_column_widths("Updated_MAP_Fluency_Download.xlsx")
# subprocess.run(["start", "excel", "Updated_MAP_Fluency_Download.xlsx"], shell=True)
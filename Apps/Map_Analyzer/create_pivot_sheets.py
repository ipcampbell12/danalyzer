import pandas as pd
import os
from Helpers.map_config import ethnicity_columns, other_columns, column_order,race_cols
from Helpers.other_funcs import row_order_getter

# print(os.listdir())
import os
# print("Current Working Directory:", os.getcwd())

from .map_growth_pivot_app import create_ordered_pivot_table

# Create an Excel writer object outside the loops

def create_pivot_sheets(map_df, output_pivot_file):
     print("Creating pivot sheets")
     grades = [1, 2, 3, 4, 5, 6,7,8,9]
     terms = ["Fall", "Winter","Spring"]
     subjects = ["Reading","Reading (Spanish)"]
  
     with pd.ExcelWriter(output_pivot_file) as writer:
          for subject in subjects:
               for term in terms:
                    sheet_name = f"{term} term, {subject}"
                    start_row = 1  # Initialize the starting row
                    for grade in grades:
                         row_order_list = row_order_getter(grade)
                         print("There is it is in the pivot sheets function")
                         print(map_df.shape)
                         result_pivot_df = create_ordered_pivot_table(
                              map_df, term, subject, grade, row_order=row_order_list, column_order=column_order,
                              ethnicity_cols=ethnicity_columns, other_cols=other_columns,race_cols=race_cols
                         )
                         
                         


                         # Write the pivot table to the specified sheet with the correct starting row
                         result_pivot_df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=True)
                         

                         print(f"Created and wrote pivot table for {grade},{term} and {subject}")
                         

                         # Add some space between pivot tables, assuming each pivot table is about 15 rows tall
                         start_row += len(result_pivot_df) + 2
                    
   
     
    

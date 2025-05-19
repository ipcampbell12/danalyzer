import pandas as pd

def create_ordered_pivot_table(
    df,
    term,
    subject,
    grade_level=0,
    row_order=None,
    column_order=None,
    ethnicity_cols=None,
    other_cols=None,
    race_cols=None,
    risk_mapping=None,
    term_column_map=None,  # <-- renamed parameter
    risk_col_name="RiskLevel"
):
    print("Pivot function running")
    print("Here it is before filtering")
    print(df.shape)
    print(f"Size before filtering: {df.shape}")

    filtered_df = df[df["EnrlGrdCd"] == grade_level]
    print(f"After filtering by EnrlGrdCd: {filtered_df.shape}")
    print(filtered_df[['EnrlGrdCd', 'TermName', 'Course']].head())  # Preview rows

    filtered_df = filtered_df[filtered_df["TermName"].str.contains(term, na=False)]
    print(f"After filtering by TermName: {filtered_df.shape}")
    print(filtered_df[['EnrlGrdCd', 'TermName', 'Course']].head())

    filtered_df = filtered_df[filtered_df["Course"] == subject]
    print(f"After filtering by Course: {filtered_df.shape}")
    print(filtered_df[['EnrlGrdCd', 'TermName', 'Course']].head())

    # Check if filtered_df is empty
    if filtered_df.empty:
        print(f"No data found for grade_level={grade_level}, term={term}, subject={subject}")
        return pd.DataFrame()  # Return an empty DataFrame if no data matches the criteria

    print("The df was not empty")
    print("Here it is after filtering")
    print(filtered_df.shape)

    # --- Dynamic RiskLevel assignment ---
    # Set defaults if not provided
    if risk_mapping is None:
        risk_mapping = {
            'High': 'Low Risk',
            'HiAvg': 'Low Risk',
            'Avg': 'Some Risk',
            'LoAvg': 'Some Risk',
            'Low': 'High Risk'
        }
    if term_column_map is None:
        term_column_map = {
            "Fall": "AchievementQuintile",
            "Winter": "FallToWinterGrowthQuintile",
            "Spring": "FallToSpringGrowthQuintile"
        }

    # Assign risk level to a dynamic column name
    filtered_df[risk_col_name] = filtered_df[term_column_map[term]].map(risk_mapping)
    # --- End dynamic RiskLevel assignment ---

    # Create MoreThanOneRace column
    filtered_df['MoreThanOneRace'] = filtered_df[race_cols].sum(axis=1) >= 2
    filtered_df['MoreThanOneRace'] = filtered_df['MoreThanOneRace'].astype(int)
    print(f"Here is some more shapes: {filtered_df.shape}")
    # Define melt columns, including 'WhiteNotHisp' and 'MoreThanOneRace'
    melt_columns = ethnicity_cols + other_cols + ['WhiteNotHisp', 'MoreThanOneRace']

    print(ethnicity_cols)
    print(other_cols)
    # Melt the filtered dataframe for categorical columns including 'WhiteNotHisp' and 'MoreThanOneRace'
    melted_categorical = filtered_df.melt(
        id_vars=[risk_col_name],
        value_vars=melt_columns,
        var_name='Category',
        value_name='Value'
    )
    print(melted_categorical.shape)

    # Replace long category names with aliases
    melted_categorical['Category'] = melted_categorical['Category'].replace({
        'AmerIndianAlsknNtvRaceFg': 'American Indian/Alaska Native',
        'AsianRaceFg': 'Asian',
        'BlackRaceFg': 'Black or African American',
        'HispEthnicFg': 'Hispanic/Latino',
        'PacIslndrRaceFg': 'Native Hawaiian/Pacific Islander',
        'WhiteRaceFg': 'White',
        'StudentOfColorFg':"Student of Color",
        'SpEdFg': 'SpEd',
        'TAGFg': 'TAG',
        'ELFg': 'EL',
        "Sect504Fg":"Section 504",
        "MigrntEdFg": "Migrant",
        'EconDsvntgFg': 'EconDisadvantaged',
        'MoreThanOneRace': 'Two or More Races',
        'WhiteNotHisp': 'White Not Hispanic',
        "InDualFg":"In Dual Language Program"
    })

    # Create a pivot table for categorical columns with sum aggregation
    pivot_categorical = melted_categorical.pivot_table(
        index='Category',
        columns=risk_col_name,
        values='Value',
        aggfunc='sum',
        fill_value=0
    )

    # Convert pivot table values to integers
    pivot_categorical = pivot_categorical.astype(int)
    print(pivot_categorical.shape)
    # Calculate total students for the entered grade level by risk level
    grade_level_risk = filtered_df.pivot_table(
        index=["EnrlGrdCd"],
        columns=risk_col_name,
        aggfunc='size',
        fill_value=0
    )
    print("THe code got this far")
    # Rename the index from grade_level to 'Total Students'
    grade_level_risk.index = [f'All Grade {grade_level} students']
    
    # Ensure all risk levels from the mapping are present
    expected_risk_levels = set(risk_mapping.values())
    for col in expected_risk_levels:
        if col not in grade_level_risk.columns:
            grade_level_risk[col] = 0

    # Concatenate 'Total Students' row with pivot_categorical
    pivot_combined = pd.concat([grade_level_risk, pivot_categorical])

    # Ensure all categories in row_order are present in pivot_combined index
    if row_order:
        row_order_filtered = [cat for cat in row_order if cat in pivot_combined.index]
        pivot_combined = pivot_combined.loc[row_order_filtered]

    # Ensure all columns in column_order are present in pivot_combined columns
    if column_order:
        column_order_filtered = [col for col in column_order if col in pivot_combined.columns]
        pivot_combined = pivot_combined[column_order_filtered]

    # Add a total column
    pivot_combined["Total"] = pivot_combined.sum(axis=1)
    print(pivot_combined.head())
    return pivot_combined

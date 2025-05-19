ethnicity_columns = [
        'AmerIndianAlsknNtvRaceFg',
        'AsianRaceFg',
        'BlackRaceFg',
        'HispEthnicFg',
        'PacIslndrRaceFg',
        'WhiteRaceFg'
    ]

other_columns = [
        'SpEdFg',
        'ELFg',
        'EconDsvntgFg',
        'TAGFg',
        'MigrntEdFg',
        "Sect504Fg",
        'StudentOfColorFg',
        'InDualFg'
    ]

rows_to_highlight =[
    'SpEd',
    "Section 504",
    "Migrant",
    "Student of Color",
    "In Dual Language Program",
    'EL'
]

columns_to_keep = [
    'TermName', 'DistrictName', 'SchoolName', 'StudentID', 'Student_StateID', 'Subject', 'Course', "TestName",
    "TestRITScore", "AchievementQuintile", "FallToWinterConditionalGrowthIndex", "FallToWinterGrowthQuintile", "FallToWinterConditionalGrowthPercentile",
    "FallToSpringConditionalGrowthIndex", "FallToSpringGrowthQuintile", "FallToSpringConditionalGrowthPercentile"
]

fluency_cols = [
    'TermName',
    'StudentID',
    'Grade',
    'TestLanguage',
    'ListeningComprehensionPerformanceLevel',
    'PictureVocabPerformanceLevel',
    'PhonologicalAwarenessPerformanceLevel',
    'PhonicsWordRecognitionPerformanceLevel',
    'SentenceReadingFluencyPerformanceLevel',
    'OralReadingRatePerformanceLevel',
    'OralReadingAccuracyPerformanceLevel',
    'LiteralComprehensionPerformanceLevel',
    # 'MapFluencyCompositeScore'
]

fluency_level_cols = [
    'ListeningComprehensionPerformanceLevel',
    'PictureVocabPerformanceLevel',
    'PhonologicalAwarenessPerformanceLevel',
    'PhonicsWordRecognitionPerformanceLevel',
    'SentenceReadingFluencyPerformanceLevel',
    'OralReadingRatePerformanceLevel',
    'OralReadingAccuracyPerformanceLevel',
    'LiteralComprehensionPerformanceLevel',
    # 'MapFluencyCompositeScore'
]


ps_cols = [
    "EnrlGrdCd",
    'AmerIndianAlsknNtvRaceFg',
    'AsianRaceFg',
    'BlackRaceFg',
    'HispEthnicFg',
    'PacIslndrRaceFg',
    'WhiteRaceFg',
    'SpEdFg',
    'ELFg',
    'MigrntEdFg',
    "Sect504Fg",
    'StudentOfColorFg',
    'InDualFg',
    'EconDsvntgFg',
    'InDualFg',
    'DistStdntID',
    'TAGFg'
]


column_order = ["Low Risk", "Some Risk", "High Risk"] 

other_cols = [
    "DistStdntID",
    "GndrCd",
    "LangOrgnCd",
    "EnrlGrdCd",
    "InDualFg"

]

race_cols = [
    "AmerIndianAlsknNtvRaceFg",
    "AsianRaceFg",
    "WhiteRaceFg",
    "BlackRaceFg",
    "PacIslndrRaceFg",
]

y_and_n_cols = [
    "HispEthnicFg",
    "EconDsvntgFg",
    "SpEdFg",
    "Sect504Fg",
    "MigrntEdFg",
    "IndianEdFg",
    "ELFg",
    "TAGFg",
    "InDualFg"
]

isk_mapping = {
        'High': 'Low Risk',
        'HiAvg': 'Low Risk',
        'Avg': 'Some Risk',
        'LoAvg': 'Some Risk',
        'Low': 'High Risk'
    }

quintile_select = {
    "Fall": "AchievementQuintile",
    "Winter": "FallToWinterGrowthQuintile",
    "Spring": "FallToSpringGrowthQuintile"
}
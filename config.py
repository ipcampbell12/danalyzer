ssid_cols=['ChkDigitStdntID', 'DistStdntID', 'ResdDistInstID', 'ResdSchlInstID',
       'AttndDistInstID', 'AttndSchlInstID', 'InstFill', 'LglLNm', 'LglFNm',
       'LglMNm', 'GnrtnCd', 'PrfrdLNm', 'PrfrdFNm', 'PrfrdMNm', 'BirthDtTxt',
       'GndrCd', 'HispEthnicFg', 'AmerIndianAlsknNtvRaceFg', 'AsianRaceFg',
       'BlackRaceFg', 'WhiteRaceFg', 'PacIslndrRaceFg', 'RaceFill',
       'LangOrgnCd', 'SSN', 'EnrlGrdCd', 'Addr', 'City', 'ZipCd', 'Zip4Cd',
       'ResdCntyCd', 'Phn', 'TchrFill', 'HSEntrySchlYr', 'Fill',
       'EconDsvntgFg', 'Ttl1Fg', 'SpEdFg', 'Sect504Fg', 'MigrntEdFg',
       'IndianEdFg', 'ELFg', 'DstncLrnFg', 'HomeSchlFg', 'TrnstnProgFg',
       'AltEdProgFg', 'TrbAfflnCd', 'TAGFg', 'AddnLangCd', 'DemogFill']

class_size_excluded = [
    "Advisory",
    "Freshman Victory",
    "Student Services",
    "1st Lunch",
    "2nd Lunch",
    "3rd Lunch",
    "Early College High School",
    "See Counselor",
    "Early Release",
    "Willamette Career Academy AM",
    "Willamette Career Academy PM",
    "Credit Recovery",
    "Boys Soccer",
    "Cheer Team",
    "Cross Country",
    "Football",
    "Girls Soccer",
    "Volleyball",
    "Advisory 6",
    "Advisory 7",
    "Advisory 8",
    "Lunch 6",
    "Lunch 7",
    "Lunch 8",
    "Student Assistant"
]

race_cols=[
       'HispEthnicFg',
       'AmerIndianAlsknNtvRaceFg', 
       'AsianRaceFg',
       'BlackRaceFg', 
       'WhiteRaceFg', 
       'PacIslndrRaceFg',
]

ods_cols=[
     'Student ID', 'Student Name', 'Address', 'City', 'State', 'Zip Code',
       'Email Address', 'Mobile Phone', 'Home Phone', 'Birthday',
       'Correspondence Language', 'Race/Ethnicity', 'Current Grade',
       'High School Entry Year', 'Special Ed. Indicator', 'ESL Indicator',
       'LEP Indicator', 'Gender', 'Homeless Indicator', 'Language',
       'Migrant Indicator', 'Talented and Gifted', 'School Name', 'Entry Date',
       'Withdrawal Date', 'Resident District', 'Resident School']

filtered_ssid_cols =[
       'GndrCd', 
       'LangOrgnCd',
       'SpEdFg', 
       'MigrntEdFg',
       'ELFg',
       'TAGFg'
]


filtered_ods_cols =[
     'Gender',
     'Language', 
     'Special Ed. Indicator',
     'Migrant Indicator',
     'LEP Indicator', 
     'Talented and Gifted', 
]

schools_dict = {
     95:"WSD Continuation Programs",
     796: "Nellie Muir Elementary",
     797:"Washington Elementary",
     800:"Woodburn High School",
     1267:"Lincoln Elementary",
     1268:"French Prairie Middle School",
     1359:"Heritage Elementary",
     1360:"Valor Middle School",
     4230:"Arthur Academy",
     4544:"Woodburn Success High School"

}

language_dict = {
     1290:"English",
     4260:"Spanish",
     3830:"Russian",
     5030:"Mam"
}

elpa_testing_card_col_elementary = ['LastFirst',
                          'student_number',
                          'SSID', 
                          'grade_level', 
                            'S_OR_STU_LEP_X.RecTypCd', 
                            'EL_Student', 
                            'School',
                            'Teacher',
                            'ELPA_Accessibility_Supports',
                              'IEP_Date', 
                              'IEP_or_504', 
                              'Exemptions' ]

elpa_testing_card_col_middle = ['LastFirst',
                          'student_number',
                          'SSID', 
                          'grade_level', 
                            'S_OR_STU_LEP_X.RecTypCd', 
                            'EL_Student', 
                            'School',
                            'Teacher',
                            'ELPA_Accessibility_Supports',
                              'IEP_Date', 
                              'IEP_or_504', 
                              'Exemptions', 
                              'Expression']

elpa_testing_card_col_high = ['LastFirst',
                          'student_number',
                          'SSID', 
                          'grade_level', 
                            'S_OR_STU_LEP_X.RecTypCd', 
                            'EL_Student', 
                            'School',
                            'ELPA_Accessibility_Supports',
                              'IEP_Date', 
                              'IEP_or_504', 
                              'Exemptions']
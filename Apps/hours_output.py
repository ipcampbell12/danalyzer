from datetime import datetime, timedelta

def get_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), "%m/%d/%Y")
        except ValueError:
            print("Please enter the date in MM/DD/YYYY format.")

def subtract_holiday_days(start, end, holidays):
    """Subtract days from the date range that overlap with holidays."""
    total_days = 0
    current = start
    while current <= end:
        if current.weekday() < 5 and current.date() not in holidays:
            total_days += 1
        current += timedelta(days=1)
    return total_days

def calculate_teacher_hours():
    # Fixed school schedule
    start_time = datetime.strptime("7:55 AM", "%I:%M %p")
    end_time = datetime.strptime("2:20 PM", "%I:%M %p")
    student_contact_days = 165  # Hardcoded student contact days

    # User input for non-instructional periods
    specials_minutes = 45
    lunch_recess_minutes = 40
    eld_minutes = 30
    # Total school day in minutes
    total_day_minutes = (end_time - start_time).seconds / 60

    # Instructional minutes
    regular_instruction_minutes = total_day_minutes - specials_minutes - lunch_recess_minutes - eld_minutes
    daily_regular_hours = regular_instruction_minutes / 60
    daily_eld_hours = eld_minutes / 60

    reg_mult_val= round(daily_regular_hours,2)
    eld_mult_val= round(daily_eld_hours,2)
    print(f"Reuglar hours:{reg_mult_val} hours")
    print(f"ELD hours:{eld_mult_val} hours")
    # Yearly totals
    yearly_regular_hours = round(daily_regular_hours * student_contact_days)
    yearly_eld_hours = round(daily_eld_hours * student_contact_days)

    # Define holiday ranges for 2024 and 2025
    christmas_start_2024 = datetime(2024, 12, 23)
    christmas_end_2024 = datetime(2024, 12, 31)
    spring_start_2025 = datetime(2025, 3, 24)
    spring_end_2025 = datetime(2025, 3, 28)

    # Set of holiday dates (only weekdays considered)
    holidays = set()

    # Add Christmas holidays (2024)
    current = christmas_start_2024
    while current <= christmas_end_2024:
        if current.weekday() < 5:  # Only weekdays
            holidays.add(current.date())
        current += timedelta(days=1)

    # Add Spring holidays (2025)
    current = spring_start_2025
    while current <= spring_end_2025:
        if current.weekday() < 5:  # Only weekdays
            holidays.add(current.date())
        current += timedelta(days=1)

    print(f"Configured Holidays: {sorted(holidays)}\n")  # Debug: Show the holiday dates

    print("\nDid the teacher have a long-term sub? (yes or no)")
    long_term_sub = input().strip().lower()

    if long_term_sub == "yes":
        num_ranges = int(input("How many date ranges (due to long-term subs) would you like to enter? "))
        date_ranges = []

        total_days = 0
        for i in range(num_ranges):
            print(f"\nEnter date range #{i + 1}:")
            start = get_date("  Start date (MM/DD/YYYY): ")
            end = get_date("  End date (MM/DD/YYYY): ")

            # Subtract holidays and count weekdays
            days = subtract_holiday_days(start, end, holidays)
            total_days += days
            date_ranges.append((i + 1, days))

            print(f"Date Range #{i+1}: {days} days after excluding holidays.")  # Debug: Check the days after holiday subtraction

        # Total excess days (difference between total calculated days and student contact days)
        excess_days = total_days - student_contact_days
        if excess_days > 0:
            print(f"\nThere are {excess_days} excess days to be subtracted from the calculated hours.")

            # Proportional subtraction of excess days
            total_days_in_ranges = sum([days for _, days in date_ranges])

            print("\nInstructional Hour Breakdown with Adjustments:")
            total_reg = 0
            total_eld = 0
            for i, days in date_ranges:
                # Calculate the original total hours based on the number of days in each range
                total_range_regular_hours = round((days / total_days_in_ranges) * yearly_regular_hours)
                total_range_eld_hours = round((days / total_days_in_ranges) * yearly_eld_hours)

                # Proportional subtraction of excess days
                proportion = days / total_days_in_ranges
                excess_hours = round((excess_days * proportion))
                total_range_regular_hours -= excess_hours
                total_range_eld_hours -= round(excess_hours * (total_range_eld_hours / total_range_regular_hours))  # Maintain ratio of regular to ELD hours

                # Calculate adjusted days after subtraction of proportional excess days
                adjusted_days = days - round(excess_days * proportion)

                total_reg += total_range_regular_hours
                total_eld += total_range_eld_hours

                print(f"Date Range #{i}: {adjusted_days} days → Regular: {round(adjusted_days*reg_mult_val)} hrs | ELD: {round(adjusted_days*eld_mult_val)} hrs")

            print(f"\nTotal Hours → Regular: {total_reg} hrs | ELD: {total_eld} hrs")
        else:
            print("\nNo excess days. Using original calculations without adjustments.")
            # No need for adjustments, output the regular values
            total_reg = yearly_regular_hours
            total_eld = yearly_eld_hours
            print(f"\nInstructional Hour Breakdown:")
            print(f"Regular: {total_reg} hours")
            print(f"ELD/ESOL: {total_eld} hours")
            print(f"Full Time Hours: {total_reg + total_eld} hours")
    else:
        print("\nYearly Instructional Hours (no long-term sub):")
        print(f"Regular: {yearly_regular_hours} hours")
        print(f"ELD/ESOL: {yearly_eld_hours} hours")
        print(f"Full Time Hours: {yearly_regular_hours + yearly_eld_hours} hours")

# Run it
calculate_teacher_hours()


from datetime import datetime, timedelta

def count_weekdays(start, end, weekday_name):
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4
    }

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    counts = {day: 0 for day in weekdays}

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in weekdays.values():
            for day, num in weekdays.items():
                if current_date.weekday() == num:
                    counts[day] += 1
        current_date += timedelta(days=1)

    if weekday_name.lower() == "all":
        return counts
    elif weekday_name.lower() in weekdays:
        return {weekday_name.lower(): counts[weekday_name.lower()]}
    else:
        raise ValueError("Invalid weekday. Enter a full weekday name (e.g., 'Monday') or 'all'.")

# # ---- User interaction zone ----
# if __name__ == "__main__":
#     print("📅 Weekday Counter 3000+ 📅")
#     start = input("Enter the start date (YYYY-MM-DD): ")
#     end = input("Enter the end date (YYYY-MM-DD): ")
#     weekday = input("Enter a weekday (e.g., Monday, Friday) or 'all' to count every weekday: ")

#     try:
#         result = count_weekdays(start, end, weekday)
#         print("\nHere’s your weekday count:")
#         for day, count in result.items():
#             print(f"  {day.capitalize()}: {count}")
#     except Exception as e:
#         print(f"\n⚠️ Error: {e}")

import datetime
import holidays


def main():
    """
    Generates a string of dates for a given year, including dates every
    11 days and all Austrian public holidays.
    """
    year = datetime.datetime.now().year
    start_date = datetime.datetime(year, 1, 1, 8, 0)

    # 1. Generate all "eleventh days" for the year
    eleventh_days = set()
    i = 0
    while True:
        current_date = start_date + datetime.timedelta(days=i * 11)
        if current_date.year == year:
            # Store only the date part for comparison
            eleventh_days.add(current_date.date())
            i += 1
        else:
            break

    # 2. Get all Austrian public holidays for the year
    austrian_holidays = holidays.AT(year)

    # 3. Combine dates and format them according to the rules
    # Use a dictionary to store final dates to handle duplicates and precedence
    processed_dates = {}

    # Add eleventh days first with their specific format
    for d in sorted(list(eleventh_days)):
        dt = datetime.datetime.combine(d, start_date.time())
        processed_dates[d] = dt.strftime("%Y-%m-%d: %H:%M-00:00")

        # Add the day AFTER the eleventh day with its own rules
        day_after = d + datetime.timedelta(days=1)

        # Only process if it's in the same year and not an eleventh day itself
        if day_after.year == year and day_after not in eleventh_days:
            time_str = ""
            # Sunday or public holiday
            if day_after.weekday() == 6 or day_after in austrian_holidays:
                time_str = "00:00-08:00"
            # Saturday
            elif day_after.weekday() == 5:
                time_str = "00:00-12:00"
            # Working day
            else:
                time_str = "00:00-18:00"
            processed_dates[day_after] = day_after.strftime(f"%Y-%m-%d: {time_str}")

    # Add holidays that are NOT eleventh days
    for d in sorted(austrian_holidays.keys()):
        if d not in eleventh_days and d - datetime.timedelta(days=1) not in eleventh_days:
            processed_dates[d] = d.strftime("%Y-%m-%d: x")

    # 3.5. Add special handling for Dec 24 and Dec 31
    special_dates_to_check = [
        datetime.date(year, 12, 24),
        datetime.date(year, 12, 31),
    ]
    for d in special_dates_to_check:
        # If it's an eleventh day, it's already formatted correctly. Skip.
        if d in eleventh_days:
            continue

        day_before = d - datetime.timedelta(days=1)
        # If it follows an eleventh day
        if day_before in eleventh_days:
            processed_dates[d] = d.strftime("%Y-%m-%d: 00:00-12:00")
        # Else, it's the default case for these special dates
        else:
            processed_dates[d] = d.strftime("%Y-%m-%d: 08:00-12:00")

    # 4. Sort the final list by date and print
    final_output = [processed_dates[d] for d in sorted(processed_dates.keys())]
    print(", ".join(final_output))


if __name__ == "__main__":
    main()

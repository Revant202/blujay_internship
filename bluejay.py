# run python bluejay.py to see results in console

import pandas as pd

# Reading the Excel file into a DataFrame
file_path = 'Assignment_Timecard.xlsx'
df = pd.read_excel(file_path)

# Defining a dictionary to specify how to handle missing values for each column
fillna_values = {
    'Time': pd.to_datetime('1970-01-01'),  # Replace missing Time values with a specific date
    'Time Out': pd.to_datetime('1970-01-01'),  # Replace missing Time Out values with a specific date
    'Timecard Hours (as Time)': 0  # Replace missing Timecard Hours (as Time) with 0
}

# Filling missing values based on the specified dictionary
df.fillna(value=fillna_values, inplace=True)

# Converting 'Timecard Hours (as Time)' to float
df['Timecard Hours (as Time)'] = df['Timecard Hours (as Time)'].str.extract(r'(\d+)').astype(float)

# Function to check if an employee has worked for 7 consecutive days
def worked_for_7_consecutive_days(employee_df):
    sorted_df = employee_df.sort_values('Time')
    date_range = sorted_df['Time'].dt.date
    min_date = date_range.min()
    max_date = date_range.max()
    if (max_date - min_date).days >= 6:  # 6 days because we include the start date
        return True
    return False

# Function to check if an employee has less than 10 hours of time between shifts but greater than 1 hour
def time_between_shifts(employee_df):
    sorted_df = employee_df.sort_values('Time')
    time_diff = sorted_df['Time'].diff().dt.total_seconds() / 3600  # Convert seconds to hours
    return any((time_diff > 1) & (time_diff < 10))

# Function to check if an employee has worked for more than 14 hours in a single shift
def worked_for_more_than_14_hours(employee_df):
    return any(employee_df['Timecard Hours (as Time)'] > 14)

# Grouping the data by 'Employee Name'
grouped = df.groupby('Employee Name')
consecutiveDays = []
shifts = []
moreThan14Hours = []

for name, employee_df in grouped:
    if worked_for_7_consecutive_days(employee_df):
        consecutiveDays.append(name)
    if time_between_shifts(employee_df):
        shifts.append(name)
    if worked_for_more_than_14_hours(employee_df):
        moreThan14Hours.append(name)

print("Worked for 7 consecutive days: \n","\n ".join(consecutiveDays),"\n")
print("Less than 10 hours of time between shifts but greater than 1 hour: \n","\n ".join(shifts),"\n")
print("Worked for more than 14 hours in a single shift: \n","\n ".join(moreThan14Hours),"\n")
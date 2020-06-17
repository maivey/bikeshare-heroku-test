# Import dependencies
import time
import pandas as pd
import numpy as np
import datetime
import json

# Create a dictionary that maps the city name to the corresponding .csv file
CITY_DATA = { 'chicago': 'data/chicago.csv',
              'new york city': 'data/new_york_city.csv',
              'washington': 'data/washington.csv' }

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Capitilize month and day in order to use dt.month_name() and dt.day_name() functions
    if month != 'all':
        month = month.capitalize()
    if day !='all':
        day = day.capitalize()
    
    # If neither month nor day is "all", filter by month and day
    if (month!='all') and (day!='all'):
        df = df.loc[(df['Start Time'].dt.month_name()==month) & (df['Start Time'].dt.day_name()==day)]
    # Else if month is "all" and day is not "all", filter only by day
    elif (month=='all') and (day !='all'):
        df = df.loc[df['Start Time'].dt.day_name()==day]
    # Else if day is "all" and month is not "all", filter only by month
    elif (month!='all') and (day =='all'):
        df = df.loc[df['Start Time'].dt.month_name()==month]
    # Else if both month and day is "all", apply no month or day filter

    return df
def filtered_choice(df):
    common_months = df['Start Time'].dt.month_name().value_counts()
    common_days = df['Start Time'].dt.day_name().value_counts()
    # If there is only one month and one day in the DataFrame, the filter is both
    if (len(common_days)==1) and (len(common_months)==1):
        filtered = 'Both'
    # Else if there only one month and more than one day in the DataFrame, the filter is month
    elif (len(common_days)!=1) and (len(common_months)==1):
        filtered = 'Month'
    # Else if there only one day and more than one month in the DataFrame, the filter is day
    elif (len(common_days)==1) and (len(common_months)!=1):
        filtered = 'Day'
    # Else the filter is none
    else:
        filtered = 'None'
    return filtered

def time_stats_day(df,filtered):
    """Computes and displays statistics on the most frequent day of travel."""
    common_days = df['Start Time'].dt.day_name().value_counts()
    most_common_day = common_days.index[0]
    day_count = common_days.values[0]
    return common_days, most_common_day, day_count
    print(f'Most common day of the week : {str(most_common_day)}, Count : {str(day_count)}, Filter : {filtered}\n')
    
    
def time_stats_month(df,filtered):
    """Computes and displays statistics on the most frequent month of travel."""
    common_months = df['Start Time'].dt.month_name().value_counts()
    most_common_month = common_months.index[0]
    month_count = common_months.values[0]
    return common_months, most_common_month, month_count
    print(f'Most common month : {str(most_common_month)}, Count : {str(month_count)}, Filter : {filtered}\n')
    # month_count = df['Start Time'].dt.month_name().value_counts().values[0]

def time_stats_hour(df,filtered):
    """Computes and displays statistics on the most frequent hour of travel."""
    common_hours = df['Start Time'].dt.hour.value_counts()
    most_common_hour = df['Start Time'].dt.hour.value_counts().index[0]
    hour_count = df['Start Time'].dt.hour.value_counts().values[0]

    # Display the proper time in non-military time, considering AM and PM
    if (most_common_hour >12) and (most_common_hour <24):
        most_common_hour -=12
        most_common_hour_str = f'{str(most_common_hour)}:00 PM'
    elif most_common_hour == 12:
        most_common_hour_str = f'{str(most_common_hour)}:00 PM'
    elif most_common_hour ==24:
        most_common_hour -=12
        most_common_hour_str = f'{str(most_common_hour)}:00 AM'
    else:
        most_common_hour_str = f'{str(most_common_hour)}:00 AM'
    print(f'Most common start hour : {most_common_hour_str}, Count : {str(hour_count)}, Filter : {filtered}\n')
    return common_hours, most_common_hour_str, hour_count

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Get the user's filter choice ('Month', 'Day', 'Both', or 'None')
    filtered = filtered_choice(df)

    # If the filter is 'Both', display the most common start hour
    if filtered == 'Both':
        # Display the most common start hour
        common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
        return common_hours, most_common_hour_str, hour_count
    # If the filter is month, display the most common day and start hour
    elif filtered == 'Month':
        # Display the most common day of week
        common_days, most_common_day, day_count = time_stats_day(df,filtered)
        # Display the most common start hour
        common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
    # If the filter is 'Day', display the most common month and start hour
    elif filtered == 'Day':
        # Display the most common month
        common_months, most_common_month, month_count = time_stats_month(df,filtered)
        # Display the most common hour
        common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
    # Else the filter is none, display the most common month, day, and start hour
    elif filtered == 'None':
        # Display the most common month
        common_months, most_common_month, month_count = time_stats_month(df,filtered)
        # Display the most common day of week
        common_days, most_common_day, day_count = time_stats_day(df,filtered)
        # Display the most common start hour
        common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def most_common(df,col_name):
    ''' 
    Returns the most frequent value in a column and the number of occurances for that most frequent value.
    
    Args:
        df - dataframe to analyze
        (str) col_name - name of column to get most frequent value, count of that value
    Returns:
        (str) common - the most common value in col_name column of df DataFrame
        (int/float) freq - the frequency of the most common value in col_name column of df DataFrame
    '''
    common = df[col_name].value_counts().index[0]
    freq = df[col_name].value_counts().values[0]
    return common,freq

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Get the user's filter choice ('Month', 'Day', 'Both', or 'None')
    filtered = filtered_choice(df)

    # Display most commonly used start station
    common_start, freq_start = most_common(df,'Start Station')
    print(f'Most commonly used Start Station : {str(common_start)}, Count : {str(freq_start)}, Filter : {filtered}\n')

    # Display most commonly used end station
    common_end, freq_end = most_common(df,'End Station')
    print(f'Most commonly used End Station : {str(common_end)}, Count : {str(freq_end)}, Filter : {filtered}\n')

    # Display most frequent combination of start station and end station trip
    combo = pd.value_counts(list(zip(df['Start Station'], df['End Station'])))
    combo_names = combo.index[0]
    combo_count = combo.values[0]
    print(f'Most frequent combination of start and end station : {str(combo_names)}, Count : {str(combo_count)}, Filter : {filtered}\n')
    return common_start, freq_start, common_end, freq_end, combo_names, combo_count



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Get the user's filter choice ('Month', 'Day', 'Both', or 'None')
    filtered = filtered_choice(df)

    # Display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    count_trip_duration = df['Trip Duration'].count()

    # Display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print(f'Total Duration : {str(total_trip_duration)}, Count : {str(count_trip_duration)}, Avg Duration : {str(average_trip_duration)} , Filter : {filtered}\n')

    return total_trip_duration, count_trip_duration, average_trip_duration
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Get the user's filter choice ('Month', 'Day', 'Both', or 'None')
    filtered = filtered_choice(df)

    # Display counts of user types
    print('Calculating user types...')
    subs = df['User Type'].value_counts().index[0] + "s"
    sub_count = df['User Type'].value_counts().values[0]
    users = df['User Type'].value_counts().index[1] + "s"
    user_count = df['User Type'].value_counts().values[1]
    print(f'{subs} : {sub_count}, {users} : {user_count}, Filter : {filtered} \n')

    # If city is NYC or Chicago, display gender and birth year statistics
    if (city.lower() =='new york city') or (city.lower() =='chicago'):
        # Display counts of gender
        print('Calculating gender..')
        m = df['Gender'].value_counts().index[0]
        m_count = df['Gender'].value_counts().values[0]
        f = df['Gender'].value_counts().index[1]
        f_count = df['Gender'].value_counts().values[1]
        print(f'{m} : {m_count}, {f} : {f_count}, Filter : {filtered} \n')

        # Display earliest, most recent, and most common year of birth
        print('Calculating birth year...')
        # Calculate and display earliest birth year
        earliest_birth = int(df['Birth Year'].min())
        earliest_count = len(df.loc[df['Birth Year']==earliest_birth])
        print(f'Earliest birth year : {earliest_birth}, Count : {earliest_count}, Filter : {filtered}')
        
        # Calculate and display most recent birth year
        recent_birth = int(df['Birth Year'].max())
        recent_count = len(df.loc[df['Birth Year']==recent_birth])
        print(f'Most recent birth year : {recent_birth}, Count : {recent_count}, Filter : {filtered}')

        # Calculate and display most common birth year
        common, freq = most_common(df,'Birth Year')
        common = int(common)
        print(f'Most common birth year : {common}, Count : {freq}, Filter : {filtered}\n')
        return subs, sub_count, users, user_count, m, m_count, f, f_count, earliest_birth, earliest_count, recent_birth, recent_count, common, freq
    else:
        return subs, sub_count, users, user_count


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw(df):
    ''' 
    Prompt the user whether they would like want to see the raw data. 
    If the user answers 'yes,' print 5 rows of the data at a time, 
    then ask the user if they would like to see 5 more rows of the data.
    Continue prompting and printing the next 5 rows at a time 
    until the user chooses 'no,' they do not want any more raw data to be displayed.
    '''
    # Prompt the user whether they would like want to see the raw data. 
    display_raw = input('Would you like to see the raw data? \n')

    # If the user answers 'yes,' print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data.
    # Continue prompting and printing the next 5 rows at a time until the user chooses 'no,' they do not want any more raw data to be displayed.
    
    # Ensure the user inputs a valid input ('yes' or 'no)
    if display_raw.lower() not in ['yes','no']:
        print("Please enter a valid input. Valid inputs are 'yes' or 'no'.")
        display_raw = input('Would you like to see the raw data? \n')
    temp1 = 0
    temp2 = 5
    df = df.rename(columns={'Unnamed: 0': ''})
    df['Start Time'] =df['Start Time'].astype('str')
    # While the user inputs 'yes', print 5 rows, and then increase temp1 and temp2 to print the next 5 rows
    while display_raw.lower() == 'yes':
        five = df[temp1:temp2].to_dict('records')
        print(json.dumps(five, indent=0))
        temp1 +=5
        temp2+=5
        display_raw = input('Would you like to see the 5 more rows of the raw data? \n')
        # If the user says no, break the loop
        if display_raw.lower() =='no':
            break
        # Ensure the user inputs a valid input ('yes' or 'no')
        elif display_raw.lower() not in ['yes','no']:
            print("Please enter a valid input. Valid inputs are 'yes' or 'no'.")
            display_raw = input('Would you like to see the raw data? \n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Ask the user if they want to display rows of the data after displaying statistics
        print_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

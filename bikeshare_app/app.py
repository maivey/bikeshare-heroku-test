import flask
from flask import Flask, render_template, url_for
from flask import request
from flask import jsonify
from flask import send_from_directory
import os.path
# from bikeshare_flask.py import load_data, filtered_choice, time_stats_day, time_stats_month, time_stats_hour, most_common, station_stats, trip_duration_stats, user_stats
import pandas as pd
import time
import pandas as pd
import numpy as np
import datetime
import json

# =================================
# FUNCTIONS FROM BIKESHARE_FLASK.PY
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
    # CITY_DATA = { 'chicago': '/data/chicago.csv',
    #           'new york city': '/data/new_york_city.csv',
    #           'washington': '/data/washington.csv' }
    CITY_DATA = { 'chicago': 'https://raw.githubusercontent.com/maivey/bikeshare-heroku-test/master/bikeshare_app/data/chicago.csv',
              'new york city': 'https://raw.githubusercontent.com/maivey/bikeshare-heroku-test/master/bikeshare_app/data/new_york_city.csv',
              'washington': 'https://raw.githubusercontent.com/maivey/bikeshare-heroku-test/master/bikeshare_app/data/washington.csv' }
    df = pd.read_csv(CITY_DATA[city.lower()],sep=",")
    # df = pd.read_csv(CITY_DATA[city.lower()])
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
# =================================
# ENDS FUNCTIONS FROM BIKESHARE_FLASK.PY
# =================================


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(flask.render_template('index.html'))
    if request.form["btn"]== "stats":
        if request.method == 'POST':
            city = str(request.form['my_city']).lower()
            
            print(city)
            month_day = str((request.form['month_day'])).lower()
            print(month_day)
            
            if month_day =='both':
                month = str((request.form['month'])).lower()
                day = str((request.form['day'])).lower()
            elif month_day =='month':
                month = str((request.form['month'])).lower()
                day = 'all'
            elif month_day == 'day':
                day = str((request.form['day'])).lower()
                month = 'all'
            elif month_day == 'none':
                month = 'all'
                day = 'all'
            else:
                month='temp'
                day = 'temp'
            
            # INPUT CHECKS
            if (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']) and (month not in ['january','february','march','april','may','june','all']) and (day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter',
                                 monthError = 'Please Enter a Valid Month',
                                 dayError = 'Please Enter a Valid Day')
            elif (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']) and (month not in ['january','february','march','april','may','june','all']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter',
                                 monthError = 'Please Enter a Valid Month')
            elif (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter')
            elif city not in ['chicago','washington','new york city']:
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City')
            elif month_day not in ['both','month','day','none']:
                return flask.render_template('index.html', 
                                filterError = 'Please Enter a Valid Filter')
            elif month not in ['january','february','march','april','may','june','all']:
                return flask.render_template('index.html', 
                                monthError = 'Please Enter a Valid Month')
            elif day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']:
                return flask.render_template('index.html', 
                                dayError = 'Please Enter a Valid Day')


            print(month)
            print(day)

            df = load_data(city, month, day)

            filtered = filtered_choice(df)
            print(filtered)
            common_start, freq_start, common_end, freq_end, combo_names, combo_count = station_stats(df)
            total_trip_duration, count_trip_duration, average_trip_duration = trip_duration_stats(df)
            print(city not in ['new york city','chicago'])
            if city not in ['new york city','chicago']:
                if (filtered == 'Both'):
                # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                elif filtered == 'Month':
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                # If the filter is 'Day', display the most common month and start hour
                elif filtered == 'Day':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                # Else the filter is none, display the most common month, day, and start hour
                elif filtered == 'None':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
            else:
                if (filtered == 'Both'):
            # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count, m, m_count, f, f_count, earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                elif filtered == 'Month':
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count, m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                # If the filter is 'Day', display the most common month and start hour
                elif filtered == 'Day':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count,  m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                # Else the filter is none, display the most common month, day, and start hour
                elif filtered == 'None':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count,  m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('index.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
    if request.form["btn"]== "graphs":
        if request.method == 'POST':
            city = str(request.form['my_city']).lower()
            print(city)
            month_day = str((request.form['month_day'])).lower()
            print(month_day)
            if month_day =='both':
                month = str((request.form['month'])).lower()
                day = str((request.form['day'])).lower()
            elif month_day =='month':
                month = str((request.form['month'])).lower()
                day = 'all'
            elif month_day == 'day':
                day = str((request.form['day'])).lower()
                month = 'all'
            elif month_day == 'none':
                month = 'all'
                day = 'all'
            else:
                month='temp'
                day = 'temp'

            # INPUT CHECKS
            if (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']) and (month not in ['january','february','march','april','may','june','all']) and (day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter',
                                 monthError = 'Please Enter a Valid Month',
                                 dayError = 'Please Enter a Valid Day')
            elif (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']) and (month not in ['january','february','march','april','may','june','all']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter',
                                 monthError = 'Please Enter a Valid Month')
            elif (city not in ['chicago','washington','new york city']) and (month_day not in ['both','month','day','none']):
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City',
                                filterError = 'Please Enter a Valid Filter')
            elif city not in ['chicago','washington','new york city']:
                return flask.render_template('index.html', 
                                cityError = 'Please Enter a Valid City')
            elif month_day not in ['both','month','day','none']:
                return flask.render_template('index.html', 
                                filterError = 'Please Enter a Valid Filter')
            elif month not in ['january','february','march','april','may','june','all']:
                return flask.render_template('index.html', 
                                monthError = 'Please Enter a Valid Month')
            elif day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']:
                return flask.render_template('index.html', 
                                dayError = 'Please Enter a Valid Day')
            print(month)
            print(day)

            df = load_data(city, month, day)
            # if city == 'chicago':
            #     df.to_csv('outputData/chicago_filtered.csv')
            # elif city == 'new york city':
            #     df.to_csv('outputData/nyc_filtered.csv')
            # elif city == 'washington':
            #     df.to_csv('outputData/washington_filtered.csv')
            filtered = filtered_choice(df)
            print(filtered)
            common_start, freq_start, common_end, freq_end, combo_names, combo_count = station_stats(df)
            total_trip_duration, count_trip_duration, average_trip_duration = trip_duration_stats(df)
            print(city not in ['new york city','chicago'])
            if city not in ['new york city','chicago']:
                if (filtered == 'Both'):
                # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                elif filtered == 'Month':
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                # If the filter is 'Day', display the most common month and start hour
                elif filtered == 'Day':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
                # Else the filter is none, display the most common month, day, and start hour
                elif filtered == 'None':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count)
            else:
                if (filtered == 'Both'):
            # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count, m, m_count, f, f_count, earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                elif filtered == 'Month':
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count, m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                # If the filter is 'Day', display the most common month and start hour
                elif filtered == 'Day':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count,  m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
                # Else the filter is none, display the most common month, day, and start hour
                elif filtered == 'None':
                    # Display the most common month
                    common_months, most_common_month, month_count = time_stats_month(df,filtered)
                    # Display the most common day of week
                    common_days, most_common_day, day_count = time_stats_day(df,filtered)
                    # Display the most common start hour
                    common_hours, most_common_hour_str, hour_count = time_stats_hour(df,filtered)
                    subs, sub_count, users, user_count,  m, m_count, f, f_count,earliest_birth, earliest_count, recent_birth, recent_count, common, freq = user_stats(df, city)
                    return flask.render_template('graphs.html', 
                                myFilter = filtered,
                                myCity = city,
                                myMonth = month,
                                myDay = day,
                                most_common_hour_str = most_common_hour_str,
                                hour_count = hour_count,
                                most_common_month = most_common_month,
                                month_count = month_count,
                                most_common_day = most_common_day,
                                day_count = day_count,
                                common_start=common_start, 
                                freq_start=freq_start, 
                                common_end=common_end, 
                                freq_end=freq_end, 
                                combo_names=combo_names, 
                                combo_count=combo_count,
                                total_trip_duration=total_trip_duration, 
                                count_trip_duration=count_trip_duration, 
                                average_trip_duration=average_trip_duration,
                                subs=subs, 
                                sub_count=sub_count, 
                                users=users, 
                                user_count=user_count,
                                m=m, 
                                m_count=m_count, 
                                f=f, 
                                f_count=f_count,
                                earliest_birth=earliest_birth, 
                                earliest_count=earliest_count, 
                                recent_birth=recent_birth, 
                                recent_count=recent_count, 
                                common=common, 
                                freq=freq)
        # return flask.render_template('graphs.html')

# @app.route("/chicago")
# def chicago():
#     chicago_df= pd.read_csv('data/chicago.csv')
#     # chicago_df = chicago_df.to_json(orient='records')
#     chicago_df = chicago_df.to_dict(orient='records')
#     # chicago = {'data':chicago}
#     # chicago_df = json.dumps(chicago_df, indent=2)
#     data = {'data': chicago_df}

#     return jsonify(data)

# @app.route("/nyc")
# def nyc():
#     nyc_df= pd.read_csv('data/new_york_city.csv')
#     nyc_df = nyc_df.to_dict(orient='records')
#     return jsonify(nyc_df)

# @app.route("/washington")
# def washington():
#     washington_df= pd.read_csv('data/washington.csv')
#     washington_df = washington_df.to_dict(orient='records')
#     return jsonify(washington_df)

Data_folder = os.path.join(app.root_path, 'data')
print(app.root_path)
@app.route('/data/<path:filename>')
def data(filename):
  # Add custom handling here.
  # Send a file download response.
  return send_from_directory(Data_folder, filename)

# outputData_folder = os.path.join(app.root_path, 'outputData')
# print(app.root_path)
# @app.route('/outputData/<path:filename>')
# def OutputData(filename):
#   # Add custom handling here.
#   # Send a file download response.
#   return send_from_directory(outputData_folder, filename)


if __name__ == "__main__":
    app.run(debug=True) 



import flask
from flask import Flask, render_template, url_for
from flask import request
from flask import jsonify
from flask import send_from_directory
import os.path
from bikeshare_flask import load_data, filtered_choice, time_stats_day, time_stats_month, time_stats_hour, most_common, station_stats, trip_duration_stats, user_stats
import pandas as pd
import time
import pandas as pd
import numpy as np
import datetime
import json

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
            if city == 'chicago':
                df.to_csv('outputData/chicago_filtered.csv')
            elif city == 'new york city':
                df.to_csv('outputData/nyc_filtered.csv')
            elif city == 'washington':
                df.to_csv('outputData/washington_filtered.csv')
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

outputData_folder = os.path.join(app.root_path, 'outputData')
print(app.root_path)
@app.route('/outputData/<path:filename>')
def OutputData(filename):
  # Add custom handling here.
  # Send a file download response.
  return send_from_directory(outputData_folder, filename)


if __name__ == "__main__":
    app.run(debug=True) 



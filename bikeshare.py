import pandas as pd
import time
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:

        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = fn_city()
    month, day = fn_filtermdn()
    return city, month, day


def fn_city():
    """
    Get user input for city (chicago, new york city, washington).
    """
    city = ''
    while city not in ('chicago', 'new york', 'washington'):

        city = input("Would you like to see the data for Chicago, New York or Washington?  \n")
        city = city.lower().strip()
        print("You have selected {} to analyze  ".format(city))
        if city not in ('chicago', 'new york', 'washington'):
            print("Chicago or New York or Washington are the valid options")
    return city


def fn_filtermdn():
    """ Asks the user input for month,day,both or none to analyse"""

    filtermdn = ''
    day = 'all'
    month = 'all'

    while filtermdn not in ('month', 'day', 'both', 'none'):
        filtermdn = input(
            "How Would you like to filter the data: month,day,both or none? Type none for no time filter \n")

        filtermdn = filtermdn.lower().strip()
        print("you have selected {}  to analyse ".format(filtermdn))
        if filtermdn not in ('month', 'day', 'both', 'none'):
            print("Enter the valid option month , day , both , none ")
    if filtermdn == 'month':
        month = fn_month()
    if filtermdn == 'day':
        day = fn_day()
    if filtermdn == 'both':
        month = fn_month()
        day = fn_day()
    return month, day


def fn_month():
    """ Asks the user input for month to analyse data
        (january, february, ... , june)
    """
    month = ''
    while month not in ('january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Which month? January , February , March , April , May or June.  Please Type full month name\n")
        month = month.lower().strip()
        print("you have selected {} month to analyse".format(month))
        if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print("January , February , March , April , May or June are the valid options")
    return month


def fn_day():
    """Asks the user input for day to analyse data
    (1,2...7)
    """
    dayint = 0
    while True:
        try:
            dayint = int(input("which day(1-7)?  Please enter number 1 for sunday\n"))
            if (dayint >= 1 and dayint <= 7):
                break
            else:
                print('Invalid Input. Try again.')
        except ValueError:
            print('Invalid Input. Try again.')
    if (dayint == 1):
        day = 'sunday'
    elif (dayint == 2):
        day = 'monday'
    elif (dayint == 3):
        day = 'tuesday'
    elif (dayint == 4):
        day = 'wednesday'
    elif (dayint == 5):
        day = 'thursday'
    elif (dayint == 6):
        day = 'friday'
    elif (dayint == 7):
        day = 'saturday'
    print('{} is selected'.format(day))
    return day


def load_data(city, month, day):
    """ Loads data with user input for city ,month and day"""
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        # use the index of the months list to get the corresponding int
        df['month'] = df['Start Time'].dt.month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if month == 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # Display the most common month
        df['month'] = df['Start Time'].dt.month_name()
        most_cm = df['month'].mode()[0]
        print("\nMost common month is: {} ".format(most_cm))

    if day == 'all':
        #  Display the most common day of week
        df['day'] = df['Start Time'].dt.day_name()
        most_day = df['day'].mode()[0]
        print("\nMost common day is: {} ".format(most_day))

    #  Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_hour = df['hour'].mode()[0]
    print("\nMost common start hour is : {} ".format(most_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  Display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['difference'] = df['End Time'] - df['Start Time']
    trip_dur = df['difference'].sum()
    counttr = df['Trip Duration'].value_counts().sum()
    print("\nTotal trip duration is {} \nCount : {} ".format(trip_dur, counttr))
    trip_avg = df['difference'].mean()
    print("\nAverage Trip duration is {}".format(trip_avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counting_user = (df['User Type'].value_counts())
    print("\nCount of User Type  ")
    for i in range(len(counting_user.index.values)):
        print(counting_user.index.values[i], ':', list(counting_user)[i])

    if ("Gender" in df.columns and "Birth Year" in df.columns):
        # Display counts of gender
        gendercount = (df['Gender'].value_counts())
        print("\nCount of Gender")
        for i in range(len(gendercount.index.values)):
            print(gendercount.index.values[i], ' : ', list(gendercount)[i])

        # Display earliest, most recent, and most common year of birth
        mostrecent = int(df['Birth Year'].max())
        earliest = int(df['Birth Year'].min())
        common = int(df['Birth Year'].mode())
        print("\nMost recent Birth Year: {}  Earliest Birth Year : {}  Common Birth Year : {} ".format(mostrecent,
                                                                                                       earliest,
                                                                                                       common))
    else:
        print("\nNo Gender and Birth Year data to Display ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Most common start station
    st_station = df['Start Station'].mode()[0]
    countst = df['Start Station'].value_counts().max()
    print("\nMost common start station is : {}  \nCount : {} ".format(st_station, countst))
    # Most common end station
    ed_station = df['End Station'].mode()[0]
    counted = df['End Station'].value_counts().max()
    print("\nMost common End station is : {}  \nCount : {}".format(ed_station, counted))
    # Most common trip from start to end (i.e., most frequent combination of start station and end station trip)
    df['combine'] = df['Start Station'] + df['End Station']
    most_common = df['combine'].mode()[0]
    countco = df['combine'].value_counts().max()
    print("\nMost common trip from start to end station is : {} \nCount : {}".format(most_common, countco))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(city):
    """To see 5 lines of Raw Data"""

    rawdf = pd.read_csv(CITY_DATA[city])
    rawdata = ''
    while (rawdata.lower() not in ('yes', 'no')):
        rawdata = input('\nWould you like to see five lines of raw data? Enter yes or no.\n')
        i = 0
        if (rawdata.lower() not in ('yes', 'no')):
            print("Please enter the option as yes or no")
        if rawdata.lower() == 'no':
            break
    while (rawdata.lower() == 'yes' and i + 5 < rawdf.shape[0]):

        for n in range(i, i + 5, 1):
            print(rawdf.iloc[n])
            print('\n')

        i = i + 5

        """ To see five more lines following the previous data"""
        rawdata = input('\nWould you like to see five more lines of raw data? Enter yes or no.\n')
        while (rawdata.lower() not in ('yes', 'no')):
            print("Please enter the option as yes or no")
            rawdata = input('\nWould you like to see five more lines of raw data? Enter yes or no.\n')

            if rawdata.lower() == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

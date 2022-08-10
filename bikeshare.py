from ast import While
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose the city to analyze from (chicago, new york city, washington): \n').lower()

    while city not in ['chicago', 'new york city', 'washington'] :
        city = input('Enter a valid city from (chicago, new york city, washington): \n').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('Choose the month to filter by from (all, january, february, ... , june): \n').lower()

    while month not in ['all', 'january', 'february','march','april','may','june'] :
        month = input('Enter a valid month from (all, january, february, ... , june): \n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Choose the day of week to filter by from (all, monday, tuesday, ... sunday): \n').lower()

    while day not in ['all', 'monday', 'tuesday','wednesday','thursday','Friday','Saturday','sunday'] :
        day = input('Enter a valid day of week from (all, monday, tuesday, ... sunday): \n').lower()


    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month_name()
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all' :
        df = df[df['Month'] == month.title()]

    if day != 'all' :
        df = df[df['Day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['Month'] = df['Start Time'].dt.month_name()
    print('   --The most common month is : {}'.format(df['Month'].mode()))

    # display the most common day of week
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    print('   --The most common day is : {}'.format(str(df['Day_of_week'].mode())))


    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    print('   --The most common start hour is : {}'.format(int(df['Start Hour'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    start_stations = {}
    for station in df['Start Station'] :
        if station in start_stations :
            start_stations[station] += 1
        else :
            start_stations[station] = 1
    
    print('   --The most commonly used start station *** ')
    for station, use_num in start_stations.items() :
        if use_num == max(start_stations.values()) :
            print('      --' + station + ' : ' + str(use_num) + ' Times')
            break

    # display most commonly used end station
    end_stations = {}
    for station in df['End Station'] :
        if station in end_stations :
            end_stations[station] += 1
        else :
            end_stations[station] = 1
    
    print('   --The most commonly used end station *** ')
    for station, use_num in end_stations.items() :
        if use_num == max(end_stations.values()) :
            print('      --' + station + ' : ' + str(use_num) + ' Times')
            break

    # display most frequent combination of start station and end station trip
    compin_stations = {}
    for trip in np.array(df['Start Station']+'$'+df['End Station']) :
        if trip in compin_stations :
            compin_stations[trip] += 1
        else :
            compin_stations[trip] = 1


    print('   --The most frequent combination of start station and end station trip ***')
    for trip, use_num in compin_stations.items() :
        if use_num == max(compin_stations.values()) :
            print('      --Trip from {} to {} : {} Trips\n'.format(trip.split('$')[0],trip.split('$')[0],str(use_num)))
            break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    total_trips_time = 0
    for duration in df['Trip Duration'] :
        total_trips_time += duration

    print('   --Total travel time is : {} Seconds.'.format(total_trips_time))

    # display mean travel time
    print('   --Mean travel time is : {} Seconds.'.format(total_trips_time/len(df['Trip Duration'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = {}
    for user in df['User Type'] :
        if user in user_types :
            user_types[user] += 1
        else :
            user_types[user] = 1

    print('   --User Types Count *** ')
    for _type, count in user_types.items() :
        print('      --{} Users : {}.'.format(_type,count))

    # Display counts of gender
    print('   --Users Gender Count ***')
    if 'Gender' in df:
        males = 0
        females = 0
        for user in df['Gender'] :
            if user == 'Male' :
                males += 1
            else :
                females += 1

        print('      --1. Females : {} Users.'.format(females))
        print('      --2. Males : {} Users.'.format(males))
    else :
        print('      $$ there is no Gender data for this City.')

    # Display earliest, most recent, and most common year of birth
    print('   --Users year of birth stats ***')
    if 'Birth Year' in df:
        print('     --Earliest year of birth is : {}'.format(int(df['Birth Year'].min())))
        print('     --Most recent year of birth is : {}'.format(int(df['Birth Year'].max())))
        print('     --Most common year of birth is : {}'.format(int(df['Birth Year'].mode())))
    else :
        print('      $$ there is no year of birth data for this City.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    restart = input('\nWould you like to view 5 rows of trip data? Enter yes or no.\n').lower()
    count = 0
    while restart != 'no':
        print(df[count : count+5])
        count += 5
        restart = input('\nView more 5 rows... Enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

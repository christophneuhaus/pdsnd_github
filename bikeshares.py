import time
import pandas as pd
import numpy as np

# this dictionary contains the data that can be loaded
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
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

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # inputs

    while True:
        city = input('Please select a city (chicago, new york city or washington): ').lower()
        if city in CITY_DATA.keys():
            print('you selected ' + city + '.\n')
            break
        else:
            print('city input not available, please select from (chicago, new york city, washington). ')

    # TO DO: get user input for month (all, january, february, ... , june)
    possible_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('Please select a month (all, january, february, march, april, may, june): ').lower()
        if month in possible_months:
            print('you selected ' + month + '.\n')
            break
        else:
            print('month input not available, please select from (all, january, february, march, april, may, june).')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    possible_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('Please select a day (all, monday, tuesday, ... sunday): ').lower()
        if day in possible_days:
            print('you selected ' + day + '.\n')
            break
        else:
            print('day input not available, please select from (all, monday, tuesday, ... sunday).')

    print('-' * 40)
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

    # ==============================================================
    #
    # THE FOLLOWING CODE I COPIED FROM ONE SOLUTION TO ONE OF THE PREVIOUS QUIZZES
    #
    # ==============================================================

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # also add a column with start hour
    df['start_hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # index must be "+1" because January = 1, february = 2, .....
        month = months.index(month) + 1

        # filter by month to create the new dataframe,
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    possible_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('most popular month: ', popular_month, ', corresponds to', possible_months[popular_month])

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('most popular day of week: ', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    print('most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station: ', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('most commonly used end station: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # Create an new column with the trip data:
    df['start_to_stop'] = df['Start Station'] + ' to  ' + df['End Station']
    popular_combination = df['start_to_stop'].mode()[0]
    print('most frequent combination of start station and end station: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts(dropna=False))

    user_types = df['User Type'].unique()
    print('Count of user types: ', len(user_types), '(List of Types:', user_types, ')\n')

    print('\nInformation about gender: ')

    # check if gender column exists:
    if 'Gender' in df:
        gender_types = df['Gender'].unique()

        # message-string
        message_gender = 'Count of genders'

        if df['Gender'].isnull().values.any():
            message_gender += ' (gender data contains one or more NaN!)'

        print(message_gender + ':')
        print(df['Gender'].value_counts(dropna=False))  # also print data with nan

    else:
        print('Sorry, dataset does not contain Gender data of Customers.')

    # TO DO: Display earliest, most recent, and most common year of birth
    # print message about year of birth:
    print('\nInformation about year of birth: ')

    # check if Birth Year included in dataset
    if 'Birth Year' in df:

        earliest_birth = int((df['Birth Year'].min()))  # make sure year of birth is type integer
        print('erliest year of birth: ', earliest_birth)

        most_recent_birth = int((df['Birth Year'].max()))  # make sure year of birth is type integer
        print('most recent year of birth: ', most_recent_birth)

        most_common_birth = int(df['Birth Year'].mode()[0])  # make sure year of birth is type integer
        print('most common year of birth: ', most_common_birth)

    else:
        print('Sorry, dataset does not contain data concerning Birth Year of Customers.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



# Asking for more data
def show_data(df):
    show_lines = 0
    while True:
        answer = input("Do you want to see 5 (more) lines of raw data? Print Yes or No. ").lower()
        if answer not in ['yes', 'no']:
            answer = input("please type in Yes or No. ").lower()
        elif answer == 'yes':
            more = 'yes'
            while more == 'yes':
                print(df.iloc[show_lines: show_lines + 5])
                more = input("Do you want to see more? Yes or No").lower()
                show_lines += 5
            return

        elif answer == 'no':
            return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

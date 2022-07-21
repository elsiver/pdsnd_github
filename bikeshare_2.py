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
    while True:
        try:
            city=str(input("what city are you interested in? type either chicago, new york city or washington: ")).lower()
            if city in CITY_DATA:
                break
            else:
                print('that\'s not a valid city')
        except:
            print('there seems to be a problem, try again?:')
       

    # get user input for month (all, january, february, ... , june)
    month_list=['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month=str(input("what month are you interested in? type either all or january, february, march, april, may, june: ")).lower()
            if month in month_list:
                break
            else:
                print('that\'s not a valid input')
        except:
            print('there seems to be a problem, try again?:')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list=['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while True:
        try:
            day=str(input("what day are you interested in? type either: all or: monday, tuesday, wednesday, thuirsday, friday, saturday, sunday: ")).lower()
            if day in day_list:
                break
            else:
                print('that\'s not a valid input')
        except:
            print('there seems to be a problem, try again?:')

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month_number = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_name = months[popular_month_number-1]

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
   
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    
    print('Most Common Month:', month_name)
    print('Most Common Day of the Week:', popular_day)
    print('Most Common Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station:', popular_start)


    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:', popular_end)

    # display most frequent combination of start station and end station trip
   # df['start_end']= df['Start Station']+ df['End Station']
   # start_end = df['start_end'].value_counts().idxmax()
    start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print('most popular trip:', start_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def time_display(sec):
        seconds_in_week = 60 * 60 * 24 * 7
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60
    
        weeks = sec // seconds_in_week
        days = (sec - (weeks * seconds_in_week)) // seconds_in_day
        hours = (sec - (weeks * seconds_in_week) - (days * seconds_in_day)) // seconds_in_hour
        minutes = (sec - (weeks * seconds_in_week) - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
        print(' {} weeks, {} days, {} hours and {} minutes'.format(weeks, days, hours, minutes))

    # display total travel time
    total_sec = df['Trip Duration'].sum()
    print('Total travel time:')
    time_display(total_sec)
    # display mean travel time
    mean_sec = df['Trip Duration'].mean()
    print('Mean travel time:')
    time_display(mean_sec)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_count=df['User Type'].value_counts()

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
    except:
        gender_count = 'no information'
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_common = df['Birth Year'].mode()[0]
        most_recent = df['Birth Year'].max()
    else:
        earliest = 'no information'
        most_common = 'no information'
        most_recent = 'no information'

    print('Gender Count: {}\n User Type Count: {} \n'.format(gender_count, type_count))
    print('Most earliest Birth Year:{}\n Most common Birth Year:{} \n Most recent Birth Year:{}'.format(earliest, most_common, most_recent))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_view(df):
    row=0
    while True:
        try:
            raw_data = input('want to see the raw data? Type yes or no :').lower()
            if raw_data == 'yes':
                print(df.iloc[row:row+5])
                row += 5
            elif raw_data == 'no':
                break
            else:
                print('thats not a valid input')
        except:
            print('something went wrong, please try again')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

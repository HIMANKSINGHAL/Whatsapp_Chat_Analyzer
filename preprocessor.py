import re
import pandas as pd

def preprocess(data):

    # Regex for WhatsApp exported chats (MM/DD/YY, HH:MM - )
    split_pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    date_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s'

    # Extract messages and dates
    messages = re.split(split_pattern, data)[1:]
    dates = re.findall(date_pattern, data)

    # Create DataFrame
    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # Convert to datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %H:%M'
    )

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    # Remove original column
    df.drop(columns=['user_message'], inplace=True)

    # Date features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Timeline
    df['only_date'] = df['date'].dt.date

    # Week number
    df['week'] = df['date'].dt.isocalendar().week

    # Time period
    period = []

    for hour in df['hour']:
        if hour == 23:
            period.append('23-00')
        elif hour == 0:
            period.append('00-01')
        else:
            period.append(f'{hour:02d}-{hour+1:02d}')

    df['period'] = period

    return df
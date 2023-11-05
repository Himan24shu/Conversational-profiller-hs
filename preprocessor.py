import pandas as pd
import re


def preprocess(data):
    format_data = detect_time_format(data)

    if format_data == '24hr':
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})

        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

        df.rename(columns={'message_date': 'date'}, inplace=True)
        users = []
        messages = []

        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['month_num'] = df['date'].dt.month
        df['only_date'] = df['date'].dt.date
        df['day_name'] = df['date'].dt.day_name()

        period = []

        for hour in df[['day_name', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))

        df['period'] = period

        return df
    elif format_data == '12hr':
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[APap][Mm])?\s-\s'

        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})

        def convert_to_24_hour_time(time_str):
            # Extract hour and minute from the time string
            match = re.search(r'(\d{1,2}):(\d{2})', time_str)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))

                # Check if the time is in 12-hour format and adjust if necessary
                if re.search(r'[AaPp][Mm]', time_str):
                    if 'PM' in time_str.upper() and hour < 12:
                        hour += 12
                    elif 'AM' in time_str.upper() and hour == 12:
                        hour = 0

                return f"{hour:02}:{minute:02}"

            return None

        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
        df['message_date'] = df['message_date'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

        users = []
        messages = []

        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = pd.to_datetime(df['message_date']).dt.year
        df['month'] = pd.to_datetime(df['message_date']).dt.strftime('%B')
        df['day'] = pd.to_datetime(df['message_date']).dt.day
        df['hour'] = pd.to_datetime(df['message_date']).dt.hour
        df['minute'] = pd.to_datetime(df['message_date']).dt.minute
        df['month_num'] = pd.to_datetime(df['message_date']).dt.month
        df['only_date'] = pd.to_datetime(df['message_date']).dt.date
        df['day_name'] = pd.to_datetime(df['message_date']).dt.strftime('%A')

        period = []

        for time_str in df['message_date']:
            period.append(convert_to_24_hour_time(time_str))

        df['period'] = period

        return df


def detect_time_format(text):
    # Check if the text contains timestamps
    if re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', text):
        return "24hr"
    elif re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[APap][Mm])?\s-\s', text):
        return "12hr"
    else:
        return "Unknown format"

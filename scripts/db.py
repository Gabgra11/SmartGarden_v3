import datetime as dt
import pandas as pd
from scripts import user
import json

def get_current_date_window():
    # Get the timestamps of the beginning and end of the current day.
    midnight = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()).timestamp()
    end_of_day = dt.datetime.combine(dt.date.today(), dt.datetime.max.time()).timestamp()
    return midnight, end_of_day

def add_data_reading(conn, moisture, humidity, temperature):
    command = 'INSERT INTO data (timestamp, moisture, humidity, temperature) VALUES (?, ?, ?, ?)'
    conn.execute(command, (dt.datetime.now().timestamp(), moisture, humidity, temperature))
    conn.commit()

def get_data_week_df(conn, date):
    date_plus_7 = date + dt.timedelta(days=7)

    start_time = date.timestamp()
    end_time = date_plus_7.timestamp()
    command = 'SELECT timestamp, moisture, humidity, temperature FROM data WHERE timestamp BETWEEN {} AND {}'
    df = pd.read_sql_query(command.format(start_time, end_time), conn)
    return df

def add_user_vote(conn, user_id, vote):
    # Clear previous vote from user, if exists:
    command = 'DELETE FROM votes WHERE user == ?'
    conn.execute(command, (user_id,))

    # Add new vote from user:
    command = 'INSERT INTO votes (timestamp, vote, user) VALUES (?, ?, ?)'
    conn.execute(command, (dt.datetime.now().timestamp(), vote, user_id))
    conn.commit()

def get_user_vote(conn, user_id):
    if user_id == None:
        return None
    
    midnight, end_of_day = get_current_date_window()

    command = 'SELECT vote FROM votes WHERE user == ? AND timestamp BETWEEN ? AND ?'
    query = conn.execute(command, (user_id, midnight, end_of_day)).fetchone()

    if query:
        return query[0] # User vote exists
    else: 
        return None

def get_page_data(conn):
    midnight, end_of_day = get_current_date_window()

    # Get votes:
    command = 'SELECT vote, COUNT(*) as count FROM votes WHERE timestamp BETWEEN ? AND ? GROUP BY vote'
    votes_query = conn.execute(command, (midnight, end_of_day)).fetchall()
    
    yes_votes = 0
    no_votes = 0

    # Populate vote counts, if they exist:
    if votes_query:
        for row in votes_query:
            if row['vote'] == 1:
                yes_votes = row['count']
            if row['vote'] == -1:
                no_votes = row['count']

    # Get stats:
    command = 'SELECT moisture, humidity, temperature FROM data WHERE timestamp BETWEEN ? AND ?'
    stats_query = conn.execute(command, (midnight, end_of_day)).fetchone()

    if stats_query:
        moisture = stats_query[0]
        humidity = stats_query[1]
        temperature = stats_query[2]
    else:   # No results returned
        moisture = None
        humidity = None
        temperature = None
        
    data = {
        'yes_votes': yes_votes, 
        'no_votes': no_votes,
        'moisture': moisture,
        'humidity': humidity,
        'temperature': temperature
    }
    return data

def add_or_update_user(conn, user_info):
    command = 'INSERT INTO users (id, name) SELECT ?, ? WHERE NOT EXISTS (SELECT id FROM users WHERE id = ?)'
    conn.execute(command, (user_info['sub'], user_info['name'], user_info['sub']))
    conn.commit()

def get_user_by_id(conn, user_id):
    result = None

    if user_id == None:
        return result
    
    command = 'SELECT id, name FROM users WHERE id == ?'
    query = conn.execute(command, (user_id,)).fetchone()

    if query:
        user_info = {'sub': query[0], 'name': query[1]}
        result = user.User(user_info)
    
    return result

def get_user_json_by_id(conn, user_id):
    user_result = get_user_by_id(conn, user_id)
    if user_result:
        return user_result.json()
    else:
        return None
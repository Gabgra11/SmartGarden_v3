import datetime as dt
import pandas as pd
from scripts import user
import psycopg
from psycopg import sql
import config

def get_db_connection():
    conn = psycopg.connect(config.db_uri)
    return conn

def get_current_date_window():
    # Get the timestamps of the beginning and end of the current day.
    midnight = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()).timestamp()
    end_of_day = dt.datetime.combine(dt.date.today(), dt.datetime.max.time()).timestamp()
    return midnight, end_of_day

def add_data_reading(moisture, humidity, temperature):
    conn = get_db_connection()
    command = 'INSERT INTO data (timestamp, moisture, humidity, temperature) VALUES ({}, {}, {}, {})'

    with conn.cursor() as cur:
        cur.execute(sql.SQL(command.format(dt.datetime.now().timestamp(), moisture, humidity, temperature)))
    conn.commit()
    conn.close()

def get_data_week_df(date):
    conn = get_db_connection()
    date_plus_7 = date + dt.timedelta(days=7)

    start_time = date.timestamp()
    end_time = date_plus_7.timestamp()
    command = 'SELECT timestamp, moisture, humidity, temperature FROM data WHERE timestamp BETWEEN {} AND {}'
    df = pd.read_sql_query(command.format(start_time, end_time), conn)
    conn.close()
    return df

def add_user_vote(user_id, vote):
    # Clear previous vote from user, if exists:
    conn = get_db_connection()
    command1 = 'DELETE FROM votes WHERE userid = \'{}\''

    # Add new vote from user:
    command2 = 'INSERT INTO votes (timestamp, vote, userid) VALUES ({}, {}, \'{}\')'
    with conn.cursor() as cur:
        cur.execute(sql.SQL(command1.format(user_id,)))
        cur.execute(sql.SQL(command2.format(dt.datetime.now().timestamp(), vote, user_id)))
    conn.commit()
    conn.close()

def get_user_vote(user_id):
    if user_id == None:
        return None
    
    conn = get_db_connection()
    midnight, end_of_day = get_current_date_window()

    command = 'SELECT vote FROM votes WHERE userid = \'{}\' AND timestamp BETWEEN {} AND {}'
    with conn.cursor() as cur:
        query = cur.execute(sql.SQL(command.format(user_id, midnight, end_of_day))).fetchone()
    conn.close()
    
    if query:
        return query[0] # User vote exists
    else: 
        return None

def get_page_data():
    conn = get_db_connection()
    midnight, end_of_day = get_current_date_window()

    # Get votes:
    command = 'SELECT vote, COUNT(*) as count FROM votes WHERE timestamp BETWEEN {} AND {} GROUP BY vote'
    with conn.cursor() as cur:
        votes_query = cur.execute(sql.SQL(command.format(midnight, end_of_day))).fetchall()
    
    yes_votes = 0
    no_votes = 0

    # Populate vote counts, if they exist:
    if votes_query:
        for row in votes_query:
            # row = (vote number, count)
            # vote numbers: 1 = yes, -1 = no
            if row[0] == 1:
                yes_votes = row[1]
            if row[0] == -1:
                no_votes = row[1]

    # Get stats:
    command = 'SELECT moisture, humidity, temperature FROM data WHERE timestamp BETWEEN {} AND {} ORDER BY timestamp DESC'
    with conn.cursor() as cur:
        stats_query = cur.execute(sql.SQL(command.format(midnight, end_of_day))).fetchone()

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
    conn.close()
    return data

def add_or_update_user(user_info):
    # Add user to users table if not in table:
    conn = get_db_connection()
    command =   'DO $$\
                BEGIN\
                IF NOT EXISTS (SELECT * from users WHERE id = \'{}\') THEN\
                INSERT INTO users (id, name) VALUES (\'{}\', \'{}\');\
                END IF;\
                END $$;'
    with conn.cursor() as cur:
        cur.execute(sql.SQL(command.format(user_info['sub'], user_info['sub'], user_info['name'])))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    # Get user from users table, if exists:
    conn = get_db_connection()
    result = None

    if user_id == None:
        return result
    
    command = 'SELECT id, name FROM users WHERE id = \'{}\''
    with conn.cursor() as cur:
        query = cur.execute(sql.SQL(command.format(user_id,))).fetchone()

    if query:
        user_info = {'sub': query[0], 'name': query[1]}
        result = user.User(user_info)
    
    conn.close()
    return result

def get_user_json_by_id(user_id):
    user_result = get_user_by_id(user_id)
    if user_result:
        return user_result.json()
    else:
        return None
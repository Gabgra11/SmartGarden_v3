import datetime as dt
import pandas as pd

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
    command = 'DELETE from votes WHERE user == ?'
    conn.execute(command, (user_id,))

    # Add new vote from user:
    command = 'INSERT INTO votes (timestamp, vote, user) VALUES (?, ?, ?)'
    conn.execute(command, (dt.datetime.now().strftime("%S"), vote, user_id))
    conn.commit()

def get_user_vote(conn, user_id):
    if user_id == None:
        return None
    command = 'SELECT vote FROM votes WHERE user == ?'
    query = conn.execute(command, (user_id,)).fetchone()
    vote = query[0]
    return vote
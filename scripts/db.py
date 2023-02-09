import datetime as dt
import pandas as pd

def add_data_reading(conn, moisture, humidity, temperature):
    command = 'INSERT INTO data (timestamp, moisture, humidity, temperature) VALUES (?, ?, ?, ?)'
    conn.execute(command, (dt.datetime.now().strftime("%s"), moisture, humidity, temperature))
    conn.commit()

def get_data_week_df(conn, date):
    date_plus_7 = date + dt.timedelta(days=7)

    start_time = date.timestamp()
    end_time = date_plus_7.timestamp()
    command = 'SELECT timestamp, moisture, humidity, temperature FROM data WHERE timestamp BETWEEN {} AND {}'
    df = pd.read_sql_query(command.format(start_time, end_time), conn)
    return df
    
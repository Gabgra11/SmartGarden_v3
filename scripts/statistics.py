from scripts import db
import scripts.barchart as bc
import datetime as dt

def get_week_stats_json(conn):
    df = db.get_data_week_df(conn, dt.datetime.now() - dt.timedelta(days=7))
    x = [dt.datetime.fromtimestamp(date).strftime("%a, %b %d") for date in df['timestamp']]
    moist_y = df['moisture'].values.tolist()
    humid_y = df['humidity'].values.tolist()
    temp_y = df['temperature'].values.tolist()

    moistJSON = bc.make_bar_chart(x, 'Day', moist_y, 'Moisture (%)', '7-Day Moisture History')
    humidJSON = bc.make_bar_chart(x, 'Day', humid_y, 'Humidity (%)', '7-Day Humidity History')
    tempJSON = bc.make_bar_chart(x, 'Day', temp_y, 'Temperature (°F)', '7-Day Temperature History')
    return moistJSON, humidJSON, tempJSON
import plotly
import plotly.express as px
import pandas as pd
import json
import datetime as dt
from scripts import db

def make_bar_chart(x, x_label, y, y_label, title):
    df = pd.DataFrame({x_label:x, y_label:y})
     
    # Create Bar chart
    fig = px.line(df, x=x_label, y=y_label, title=title)
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

def get_week_stats_json(conn):
    df = db.get_data_week_df(conn, dt.datetime.now() - dt.timedelta(days=7))
    x = [dt.datetime.fromtimestamp(date).strftime("%a, %b %d") for date in df['timestamp']]
    moist_y = df['moisture'].values.tolist()
    humid_y = df['humidity'].values.tolist()
    temp_y = df['temperature'].values.tolist()

    moistJSON = make_bar_chart(x, 'Day', moist_y, 'Moisture (%)', '7-Day Moisture History')
    humidJSON = make_bar_chart(x, 'Day', humid_y, 'Humidity (%)', '7-Day Humidity History')
    tempJSON = make_bar_chart(x, 'Day', temp_y, 'Temperature (°F)', '7-Day Temperature History')
    return moistJSON, humidJSON, tempJSON
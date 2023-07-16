import plotly
import plotly.express as px
import pandas as pd
import json
import datetime as dt
from scripts import db

def make_bar_chart(x, x_label, y, y_label, title, waterings_x=None):
    df = pd.DataFrame({x_label:x, y_label:y})
     
    # Create Bar chart
    fig = px.line(df, x=x_label, y=y_label, title=title)
    for i in waterings_x:
        fig.add_vline(x=i, line_width=3, line_dash="dash", line_color="blue")

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

def get_week_stats_json():
    df = db.get_data_week_df(dt.datetime.now() - dt.timedelta(days=7))

    x = [dt.datetime.fromtimestamp(date).strftime("%a, %b %d") for date in df['timestamp']]
    moist_y = df['moisture'].values.tolist()
    humid_y = df['humidity'].values.tolist()
    temp_y = df['temperature'].values.tolist()

    water_query = db.get_waterings_week(dt.datetime.now() - dt.timedelta(days=7))
    waterings = []
    for i in water_query:
        waterings.append(i[0])

    waterings_x = [dt.datetime.fromtimestamp(date).strftime("%a, %b %d") for date in waterings]

    moistJSON = make_bar_chart(x, 'Day', moist_y, 'Moisture (%)', '7-Day Moisture History', waterings_x)
    humidJSON = make_bar_chart(x, 'Day', humid_y, 'Humidity (%)', '7-Day Humidity History', waterings_x)
    tempJSON = make_bar_chart(x, 'Day', temp_y, 'Temperature (°F)', '7-Day Temperature History', waterings_x)

    return moistJSON, humidJSON, tempJSON
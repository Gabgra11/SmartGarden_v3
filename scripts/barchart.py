import plotly
import plotly.express as px
import pandas as pd
import json

def make_bar_chart(x, x_label, y, y_label, title):
    df = pd.DataFrame({x_label:x, y_label:y})
     
    # Create Bar chart
    fig = px.line(df, x=x_label, y=y_label, title=title)
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON
from flask import Flask, render_template, request
from urllib.request import urlopen
import certifi
import json
import plotly.graph_objects as go
import plotly
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta



app = Flask(__name__)
app.secret_key = 'secret_key'


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def get_graph(name, startDate):
    """
    Takes company name and returns bar chart of stock prices
    """
    url = (f"https://financialmodelingprep.com/api/v3/historical-chart/1min/{name}?apikey=9382e1e33d20839887f20192d86e6309")
    data = get_jsonparsed_data(url)
    companyName = name
    df = pd.DataFrame(data)
    print(df)
    df = df[df["date"] > startDate]
    dates_series = pd.Series(df["date"])
    prices_series = pd.Series(df["high"])

    dates = dates_series.tolist()
    prices = prices_series.tolist()


    fig = go.Figure(data=go.Bar(x=dates, y=prices))

    fig.update_traces(
        marker_color='white'
    )

    fig.update_layout(
        plot_bgcolor='#222222',
        paper_bgcolor='#222222',
        xaxis=dict(
        linecolor='red',  # Set x-axis line color
        gridcolor='gray'  # Set x-axis grid color
        ),
        yaxis=dict(
            linecolor='blue',  # Set y-axis line color
            gridcolor='lightgray'  # Set y-axis grid color
        ),
        font=dict(
            color='white'
        )
    )
    graph_JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    returnData = {
        'name' : companyName,
        'graph' : graph_JSON,
        'dates' : dates,
        'prices' : prices
    }
    return returnData

def get_next_minute():
    now = datetime.now()
    formatted = now.strftime('%Y-%m-%d %H:%M')
    return formatted


def get_data(name):
    print("get data")
    url = (f"https://financialmodelingprep.com/api/v3/quote-short/{name}?apikey=9382e1e33d20839887f20192d86e6309")
    data = get_jsonparsed_data(url)

    returnData = {
        'price' : data[0]["price"],
        'date' : get_next_minute()
    }
    
    return returnData

    



#getting company names
#nasdaq
url = ("https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey=9382e1e33d20839887f20192d86e6309")        
nasData = get_jsonparsed_data(url)
nasDF = pd.DataFrame(nasData)
nasDF = nasDF.assign(index="nasdaq")
nasSymbols = nasDF['symbol'].tolist()
        
#dow
url = ("https://financialmodelingprep.com/api/v3/dowjones_constituent?apikey=9382e1e33d20839887f20192d86e6309")
dowData = get_jsonparsed_data(url)
dowDF = pd.DataFrame(dowData)
dowSymbols = dowDF['symbol'].tolist()

#combined
combinedDF = pd.concat([dowDF, nasDF], axis=0)
combinedSymbols = combinedDF['symbol'].tolist()




#route for checking running server
@app.route('/serverStatus')
def serverStatus():
    return "server running"

#if submit button is hit, data recieved, otherwise load home.html
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form['company']
        date = datetime.now()
        desired_time = timedelta(hours=9, minutes=30)
        result_datetime = date.replace(hour=0, minute=0, second=0, microsecond=0) + desired_time
        dateString = result_datetime.strftime('%Y-%m-%d %H:%M:%S')
        graph_JSON = get_graph(name, dateString)
        return render_template('home.html', graph_JSON=graph_JSON, combinedSymbols=combinedSymbols, dowSymbols=dowSymbols, nasSymbols=nasSymbols)
    else:
        date = datetime.now()
        desired_time = timedelta(hours=9, minutes=30)
        result_datetime = date.replace(hour=0, minute=0, second=0, microsecond=0) + desired_time
        dateString = result_datetime.strftime('%Y-%m-%d %H:%M:%S')
        graph_JSON = get_graph("AAPL", dateString)
        return render_template('home.html', graph_JSON=graph_JSON, combinedSymbols=combinedSymbols, dowSymbols=dowSymbols, nasSymbols=nasSymbols)


@app.route('/update_data', methods=['POST', 'GET'])
def update_data():
    name = request.args.get("name")
    data = get_data(name)
    print(data)
    return data



if __name__ == '__main__':
    app.run()
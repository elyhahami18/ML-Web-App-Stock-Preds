#!/usr/bin/env python
# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta
import dash_table
from dash.dependencies import Input, Output

# Function to retrieve stock prices
def stock_prices(stock):
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=365)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2

    df = yf.download(stock, start=start_date, end=end_date, progress=False)
    df["Date"] = df.index
    df = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    df.reset_index(drop=True, inplace=True)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(
        title=f'{stock} Candlestick Chart: Interact with the Plot by Dragging the Range Slider at the Bottom.',
        yaxis_title=f'{stock} Stock',
        shapes=[dict(
            x0='2023-5-23', x1='2023-5-23', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2023-5-23', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='AI Bubble Arguably Starts Here')]
    )

    return fig

# Create the app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    id='parent',
    style={'text-align': 'left'},
    children=[
        html.H1(
            id='H1',
            children='Stock Price Analysis: Historic Returns & Predictions/Forecasts using ML Time Series Analysis',
            style={'textAlign': 'center', 'marginTop': 20, 'marginBottom': 20}
        ),
        html.P(
            children=(
                "This web application was created by Ely Hahami on June 19th, 2023 using Python Dash -- an open-source "
                "framework for building data visualization interfaces. This web app can be opened throughout the trading "
                "week of 6/19-6/23 to check the ML model accuracy via analyzing discrepancies in predicted/forecasted "
                "price versus actual market price."
            ),
        ),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[
                {'label': 'NVDA', 'value': 'NVDA'},
                {'label': 'AAPL', 'value': 'AAPL'},
                {'label': 'GOOG', 'value': 'GOOG'}
            ],
            value='NVDA'  # Set the default value
        ),
        html.Div(id='candlestick-chart'),
        html.Div(id='forecast-table-container'),
        html.P(
            children=(
                "The automatic time series (autots) model had the following hyperparameters: forecast_length = 5, "
                "frequency = 'infer', prediction_interval = 0.95, num_validations = 3, model_list = 'univariate', "
                "no_negatives = True, max_generations = 10, ensemble = 'simple')"
            ),
        )
    ]
)


@app.callback(
    Output('candlestick-chart', 'children'),
    Input('stock-dropdown', 'value')
)
def update_candlestick_chart(selected_stock):
    figure = stock_prices(selected_stock)
    graph = dcc.Graph(figure=figure)
    return graph


def generate_forecast_table(dataframe):
    table = dash_table.DataTable(
        id='forecast-table',
        columns=[{"name": col, "id": col} for col in dataframe.columns],
        data=dataframe.to_dict('records'),
        style_table={'overflowX': 'scroll'}
    )
    return table


@app.callback(
    Output('forecast-table-container', 'children'),
    Input('stock-dropdown', 'value')
)
def update_forecast_table(selected_stock):
    date_list = ['2023-06-19', '2023-06-20', '2023-06-21', '2023-06-22', '2023-06-23']
    if selected_stock == 'NVDA':
        forecast = pd.DataFrame({
            'Date': date_list,
            'Forecast': [423.688850, 422.148223, 427.096333, 427.405782, 429.621224]
        })
    elif selected_stock == 'AAPL':
        forecast = pd.DataFrame({
            'Date': date_list,
            'Forecast': [185.948168, 186.170348, 186.755310, 187.459407, 188.451410]
        })
    elif selected_stock == 'GOOG':
        forecast = pd.DataFrame({
            'Date': date_list,
            'Forecast': [124.664999, 124.710461, 124.594352, 124.801391, 124.730978]
        })
    forecast_table = generate_forecast_table(forecast)
    return forecast_table


if __name__ == '__main__':
    app.run_server(debug=True)


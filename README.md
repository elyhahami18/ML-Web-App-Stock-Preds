# ML-Web-App-Stock-Preds
This project began with an autots ML model to predict stock prices that retrieved real-time data via the Yahoo Finance (yfinance) API. After I created the model for various stocks (NVDA, AAPL, GOOG), I used Python's Dash framework to create a web app that displays 1) a candlestick chart (used in technical analysis by investors) to relay the historic returns of said company and 2) a dataframe with my ML model's prediction for that trading week. The simple, heroku web app is interactive: you can slide the bar below the candlestick chart to zoom in on a certain time period and see the closing value of the stock's price and you may choose a stock via the dropdown, and both the candlestick chart and forecast df will update.  


Web App: https://ml-stocks-0521cf177686.herokuapp.com/

import os
from functions import *
from flask import Flask, render_template, request, redirect
from bokeh.charts import output_file, save
from bokeh.embed import components
from bokeh.resources import CDN
app_tickerTape = Flask(__name__)
app_tickerTape.vars={}

@app_tickerTape.route('/')
def main():
    return redirect('/home')

@app_tickerTape.route('/home', methods = ['GET','POST'])
def tickerTape_home():
    if request.method=='GET':
        return render_template('tickerTape_home.html')
    else:
        app_tickerTape.vars['tickerSymbol'] = request.form['symbol']
        return redirect('/results')

@app_tickerTape.route('/results', methods = ['GET','POST'])
def tickerTape_results():
    if request.method=='GET':
        ticker_str = app_tickerTape.vars['tickerSymbol']
        return render_template('tickerTape_results.html',
                                symbol = ticker_str)
    else:
        app_tickerTape.vars['tickerSymbol'] = request.form['symbol']
        return redirect('/results')

@app_tickerTape.route('/bokehPlot', methods = ['GET'])
def tickerTape_bokehPlot():
    ticker_str = app_tickerTape.vars['tickerSymbol']
    quandl.ApiConfig.api_key = 'rJS8aE3GNr2x5RBnFtr5'
    quandlData_df = getQuandlData(ticker_str)
    quandlPlot = plotQuandlData(ticker_str, quandlData_df)
    script, div = components(quandlPlot)
    return """
    <!doctype html>
    <head>
        {bokeh_css}
    </head>
    <body>
        {div}

        {bokeh_js}
        {script}
    </body>
    """.format(script=script, div=div, bokeh_css=CDN.render_css(),
    bokeh_js=CDN.render_js())

@app_tickerTape.errorhandler(500)
def tickerTape_serverError(e):
    return render_template('tickerTape_500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app_tickerTape.run(port=port)




import sys
import numpy as np
import pandas as pd
import quandl
import datetime
from datetime import timedelta
from bokeh.plotting import figure, show, output_file

def getQuandlData(ticker_str):
    today_dt = datetime.datetime.now().date()
    delta_dt = timedelta(days=30)
    end_date_str = today_dt.isoformat()
    start_date_str = (today_dt-delta_dt).isoformat()

    data = quandl.get('WIKI/'+ticker_str,
                     start_date=start_date_str,
                     end_date=end_date_str,
                     returns='numpy')
    
    data_df = pd.DataFrame(data)

    return data_df

def plotQuandlData(ticker_str, quandlData_df):
    p1 = figure(x_axis_type='datetime', title=ticker_str+' closing price')
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(quandlData_df.ix[:,'Date'], quandlData_df.ix[:,'Close'],
                        color='#A6CEE3', legend='closing price')

    return p1



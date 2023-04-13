import json
import time
import requests
import yfinance as yf
from datetime import date, timedelta 

# 參考 twstock 取得需要的 URL
SESSION_URL = 'http://mis.twse.com.tw/stock/index.jsp'
STOCKINFO_URL = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_id}&_={time}'


def get_realtime_quote(stockNo, ex='tse'):
    req = requests.Session()
    req.get(SESSION_URL)
    
    stock_id = '{}_{}.tw'.format(ex, stockNo)

    r = req.get(STOCKINFO_URL.format(stock_id=stock_id, time=int(time.time()) * 1000))
    try:
        return str(round(float(r.json()['msgArray'][0]['pz']),2))
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    


def ten_years_price(stock_num): 
    assign_date = date.today() - timedelta(days = 3650) 
    stock = yf.Ticker(stock_num + '.TW')
    stock_data = stock.history(start=assign_date)
    stock_data2 = stock_data.reset_index( )[['Date', 'Close']] 
    stock_data2['Date_part'] = stock_data2['Date'].dt.date
    # now_price = stock_data.last('1D').iloc[0,0]
    stock_data2.drop(labels=['Date'],axis=1, inplace=True)
    return str(round(stock_data2['Close'].mean(),2)) 
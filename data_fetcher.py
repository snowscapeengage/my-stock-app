# data_fetcher.py
import yfinance as yf
from database import Session, StockData
import datetime

def fetch_and_store_stock_data(ticker_symbol="7203.T"):
    """
    yfinance を使って指定の銘柄の現在株価を取得し、データベースに保存する
    """
    # yfinance を利用して株価情報を取得
    stock = yf.Ticker(ticker_symbol)
    stock_info = stock.info
    current_price = stock_info.get("currentPrice")
    
    if current_price is None:
        print("株価情報が取得できませんでした。")
        return
    
    # データベースに保存
    session = Session()
    new_data = StockData(
        ticker=ticker_symbol,
        current_price=current_price,
        fetched_at=datetime.datetime.utcnow()
    )
    session.add(new_data)
    session.commit()
    session.close()
    print(f"{ticker_symbol} の株価 {current_price} 円を保存しました。")

if __name__ == '__main__':
    fetch_and_store_stock_data()

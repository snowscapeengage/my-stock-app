# model_trainer.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import datetime

# データベースからデータを取得するためのエンジン（database.py と同じものを利用）
engine = create_engine('sqlite:///data.db')

def load_stock_data(ticker_symbol="7203.T"):
    # データベースから指定の銘柄のデータを読み込む
    query = f"SELECT * FROM stock_data WHERE ticker='{ticker_symbol}' ORDER BY fetched_at"
    df = pd.read_sql(query, engine)
    return df

def train_model(df):
    # 例として、fetched_at を日時から数値（タイムスタンプ）に変換し、
    # current_price を目的変数とする線形回帰モデルを学習します。
    # ※ 本来はもっと複雑な特徴量が必要ですが、簡単な例とします。
    df['timestamp'] = df['fetched_at'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f").timestamp())
    X = df[['timestamp']].values
    y = df['current_price'].values
    model = LinearRegression()
    model.fit(X, y)
    return model

if __name__ == '__main__':
    df = load_stock_data()
    if df.empty:
        print("データが見つかりません。まずは data_fetcher.py でデータを取得してください。")
    else:
        model = train_model(df)
        # モデルをファイルに保存する
        joblib.dump(model, 'stock_price_model.pkl')
        print("モデルを学習し、 'stock_price_model.pkl' に保存しました。")

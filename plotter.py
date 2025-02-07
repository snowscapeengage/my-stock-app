# plotter.py
import matplotlib
matplotlib.use('Agg')  # GUIなしモードに変更
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = fm.FontProperties(fname='C:/Windows/Fonts/meiryo.ttc').get_name()
from sqlalchemy import create_engine
import pandas as pd

def plot_stock_history(ticker_symbol="7203.T"):
    engine = create_engine('sqlite:///data.db')
    query = f"SELECT fetched_at, current_price FROM stock_data WHERE ticker='{ticker_symbol}' ORDER BY fetched_at"
    df = pd.read_sql(query, engine)
    if df.empty:
        print("データがありません")
        return None
    # 日付型に変換
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['fetched_at'], df['current_price'], marker='o')
    plt.title(f"{ticker_symbol} の株価推移")
    plt.xlabel("日付")
    plt.ylabel("株価（円）")
    image_path = f"static/images/{ticker_symbol}_history.png"
    plt.savefig(image_path)
    plt.close()
    return image_path

if __name__ == '__main__':
    path = plot_stock_history()
    if path:
        print("グラフ画像を保存しました：", path)

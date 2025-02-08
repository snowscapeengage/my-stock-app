from dotenv import load_dotenv
import os

# プロジェクトルートにある .env ファイルを読み込みます
load_dotenv()


from flask import Flask, render_template, request
import os
import yfinance as yf
import joblib
import time
import numpy as np
import subprocess
import logging

# logsディレクトリがなければ作成
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("アプリが起動しました。")
def scheduled_data_fetch():
    try:
        subprocess.run(['python', 'data_fetcher.py'], check=True)
        logging.info("データ自動取得ジョブが正常に実行されました。")
    except Exception as e:
        logging.error("データ自動取得ジョブでエラーが発生しました: %s", e)


from valuation import (
    calculate_intrinsic_value_dcf,
    calculate_intrinsic_value_ddm,
    calculate_intrinsic_value_relative
)
from database import Session, StockData  # database.py の読み込み
from plotter import plot_stock_history
from apscheduler.schedulers.background import BackgroundScheduler
from notifier import send_notification

# Flask アプリケーションのインスタンスを作成
app = Flask(__name__, template_folder='templates')

# トップページ
@app.route('/')
def index():
    return render_template('index.html')

# 銘柄リストページ
@app.route('/stocks')
def stocks():
    session = Session()
    data = session.query(StockData).filter(StockData.ticker == "7203.T").order_by(StockData.fetched_at.desc()).first()
    session.close()
    
    current_price = data.current_price if data else "データなし"
    image_path = plot_stock_history("7203.T")
    
    return render_template('stocks.html', ticker="7203.T", price=current_price, image_path=image_path)

# 保有銘柄ページ
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    result = None
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        try:
            acquisition_price = float(request.form.get('acquisition_price'))
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            current_price = stock_info.get("currentPrice", None)
            if current_price is not None:
                profit_loss = ((current_price - acquisition_price) / acquisition_price) * 100
                result = {
                    'ticker': ticker,
                    'acquisition_price': acquisition_price,
                    'current_price': current_price,
                    'profit_loss': profit_loss
                }
        except (TypeError, ValueError):
            pass
    return render_template('portfolio.html', result=result)

# 企業分析ページ
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# 理論株価計算ページ
@app.route('/valuation', methods=['GET', 'POST'])
def valuation():
    results = {}

    # 機械学習モデルの予測
    try:
        model = joblib.load('stock_price_model.pkl')
        current_timestamp = np.array([[time.time()]])
        predicted_price = model.predict(current_timestamp)[0]
        results['model_prediction'] = predicted_price
    except Exception as e:
        results['model_prediction'] = "モデル予測エラー：" + str(e)

    # ユーザー入力による計算
    if request.method == 'POST':
        try:
            cash_flow = float(request.form.get('cash_flow'))
            discount_rate = float(request.form.get('discount_rate'))
            growth_rate = float(request.form.get('growth_rate'))
            years = int(request.form.get('years', 10))
            per = float(request.form.get('per')) if request.form.get('per') else None
            eps = float(request.form.get('eps')) if request.form.get('eps') else None

            # 入力値が None でないことをチェック
            if (cash_flow is not None and discount_rate is not None and growth_rate is not None):
                results['dcf'] = calculate_intrinsic_value_dcf(cash_flow, discount_rate, growth_rate, years)
                dividend = cash_flow * 0.4  # 仮の配当
                results['ddm'] = calculate_intrinsic_value_ddm(dividend, discount_rate, growth_rate, years)

            if per is not None and eps is not None:
                results['relative'] = calculate_intrinsic_value_relative(per, eps)

            numeric_results = [v for k, v in results.items() if k != 'model_prediction' and isinstance(v, (int, float))]
            if numeric_results:
                results['weighted_average'] = sum(numeric_results) / len(numeric_results)
        except ValueError:
            pass

    return render_template('valuation.html', results=results)

def scheduled_data_fetch():
    try:
        subprocess.run(['python', 'data_fetcher.py'], check=True)
        logging.info("データ自動取得ジョブが正常に実行されました。")
    except Exception as e:
        error_msg = f"データ自動取得ジョブでエラーが発生しました: {e}"
        logging.error(error_msg)
        send_notification("データ取得エラー", error_msg)

# モデル再学習のスケジュール実行
def scheduled_model_training():
    try:
        subprocess.run(['python', 'model_trainer.py'], check=True)
        logging.info("モデル再学習ジョブが正常に実行されました。")
    except Exception as e:
        error_msg = f"モデル再学習ジョブでエラーが発生しました: {e}"
        logging.error(error_msg)
        send_notification("モデル再学習エラー", error_msg)

@app.route('/job_logs')
def job_logs():
    try:
        with open("logs/app.log", "r", encoding="cp932") as f:
            lines = f.readlines()
        log_content = "".join(lines[-20:])  # 最後の20行を表示
    except Exception as e:
        log_content = f"ログの読み込みエラー: {e}"
    return render_template("job_logs.html", log_content=log_content)

# スケジューラーのセットアップ
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_data_fetch, 'interval', minutes=10)
scheduler.add_job(scheduled_model_training, 'interval', hours=24)
scheduler.start()

@app.route('/dashboard')
def dashboard():
    # 銘柄情報の取得（例：7203.T の最新データを取得）
    session = Session()
    data = session.query(StockData).filter(StockData.ticker == "7203.T").order_by(StockData.fetched_at.desc()).first()
    session.close()
    if data:
        stock_info = {
            'ticker': "7203.T",
            'current_price': data.current_price,
            'image_path': plot_stock_history("7203.T")
        }
    else:
        stock_info = None

    # 機械学習モデルの予測値の取得
    try:
        model = joblib.load('stock_price_model.pkl')
        current_timestamp = np.array([[time.time()]])
        model_prediction = model.predict(current_timestamp)[0]
    except Exception as e:
        model_prediction = "モデル予測エラー：" + str(e)

    # ジョブログの読み込み（logs/app.log の最後の20行を表示）
    try:
        with open("logs/app.log", "r", encoding="cp932") as f:
            lines = f.readlines()
        job_logs = "".join(lines[-20:])  # 最後の20行を結合
    except Exception as e:
        job_logs = f"ジョブログの読み込みエラー: {e}"

    return render_template('dashboard.html', stock_info=stock_info, model_prediction=model_prediction, job_logs=job_logs)


# Flaskアプリの起動
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

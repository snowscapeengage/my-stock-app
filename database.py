# database.py
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# SQLite を使う場合のエンジン作成（ファイル名は "data.db" とします）
engine = create_engine('sqlite:///data.db', echo=False)
Base = declarative_base()

# 取得した株価データを保存するテーブルの定義（例：シンプルな株価データ）
class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

# テーブルを作成する
Base.metadata.create_all(engine)

# セッションを作成するための準備
Session = sessionmaker(bind=engine)

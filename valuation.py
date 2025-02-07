# valuation.py

def calculate_intrinsic_value_dcf(cash_flow, discount_rate, growth_rate, years=10):
    """
    DCF法による理論株価の計算
    :param cash_flow: 初年度のフリーキャッシュフロー（FCF）
    :param discount_rate: 割引率（例: 0.10）
    :param growth_rate: キャッシュフローの成長率（例: 0.05）
    :param years: 予測する年数（デフォルトは10年）
    :return: DCF法による現在価値
    """
    intrinsic_value = 0
    for t in range(1, years + 1):
        intrinsic_value += cash_flow * ((1 + growth_rate) ** t) / ((1 + discount_rate) ** t)
    return intrinsic_value

def calculate_intrinsic_value_ddm(dividend, discount_rate, growth_rate, years=10):
    """
    DDM（配当割引モデル）による理論株価の計算
    :param dividend: 初年度の配当金
    :param discount_rate: 割引率
    :param growth_rate: 配当の成長率
    :param years: 予測する年数（デフォルトは10年）
    :return: DDMによる現在価値
    """
    intrinsic_value = 0
    for t in range(1, years + 1):
        intrinsic_value += dividend * ((1 + growth_rate) ** t) / ((1 + discount_rate) ** t)
    return intrinsic_value

def calculate_intrinsic_value_relative(per, eps):
    """
    相対評価（PER × EPS）による理論株価の計算
    :param per: 株価収益率
    :param eps: 1株あたり利益
    :return: 理論株価
    """
    return per * eps

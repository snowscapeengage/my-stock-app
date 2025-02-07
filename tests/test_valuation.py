import unittest
from valuation import calculate_intrinsic_value_dcf

class TestValuationMethods(unittest.TestCase):
    def test_calculate_intrinsic_value_dcf(self):
        """
        初年度キャッシュフロー=1000, 割引率=0.1, 成長率=0.05, 期間=10年の場合、
        DCF法で計算される理論株価は正の値であることを確認します。
        """
        value = calculate_intrinsic_value_dcf(1000, 0.1, 0.05, 10)
        self.assertGreater(value, 0, "計算結果が0以下です。DCF計算のロジックを確認してください。")

if __name__ == '__main__':
    unittest.main()

# __main__.py
"""
このファイルはプロジェクト全体のエントリーポイントです。
以下のコードにより、Flask アプリケーション（app.py）および将来的に追加するモジュールの処理を一括で実行します。
"""

import app

if __name__ == '__main__':
    # app.py 内の Flask アプリケーションのインスタンス（app）を起動します。
    app.app.run(debug=True)

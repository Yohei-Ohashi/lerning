"""
課題: プログラミング授業情報のスクレイピングとデータベース保存ツール

【課題の概要】
Schooのプログラミング授業一覧ページから各授業の情報を取得し、
SQLite3データベースに保存するPythonツールを作成してください。

【実装する機能】
1. Webスクレイピング機能
    - 指定されたURLから授業情報を取得する

2. データベース保存機能
    - 取得した情報をSQLite3データベースに保存する

【ターゲットURL】
https://schoo.jp/class/category/programming/?sort=featured
※このURLには、Schooのプログラミング授業が一覧表示されています

【取得する情報】
各授業について、以下の4つの情報を取得してください：
1. 授業URL (Class URL)
    - 各授業の詳細ページへのリンクURL

2. 授業タイトル (Class Title)
    - 授業のタイトル名

3. 日付 (Date)
    - 授業の日付情報

4. ハート数 (Number of Likes/Hearts)
    - 授業に付けられた「いいね」や「ハート」の数

【使用する技術】
- sqlite3: Pythonの標準ライブラリで、SQLiteデータベースを操作するためのモジュール※SQLiteは、ファイルベースの軽量なデータベースです

【実装の流れ（参考）】
1. 必要なライブラリをインポートする（requests, BeautifulSoup, sqlite3など）
2. データベースの接続とテーブル作成
3. 指定URLからHTMLを取得
4. HTMLを解析して授業情報を抽出
5. 抽出した情報をデータベースに保存
6. データベース接続を閉じる

【注意事項】
- Webスクレイピングを行う際は、サーバーに負荷をかけないよう適切な間隔を設ける
- サイトの利用規約を確認し、遵守すること
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 定数定義
TARGET_URL = "https://schoo.jp/class/category/programming/?sort=featured"

# User-Agent情報は調べて記述する
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"


def get_page_html(url=TARGET_URL) -> str:
    """
    Seleniumを使って指定されたURLからHTMLを取得する関数

    引数:
        url (str): 取得するページのURL（デフォルトはTARGET_URL）

    戻り値:
        str: ページのHTMLソース（文字列）
    """
    options = Options()
    options.add_argument("--headless")
    # User-Agentを設定（schooのボット判定を回避するため）
    options.add_argument(f"--user-agent={USER_AGENT}")

    # Chromeドライバーを起動
    driver = webdriver.Chrome(options=options)

    try:
        # 情報を取得するためにURLにアクセス
        driver.get(url)
        html = driver.page_source.encode("utf-8")
        return html
    finally:
        # 必ずブラウザを閉じる（エラーが起きても閉じる）
        driver.quit()


def main():
    # STEP1. スクレイピング
    # HTMLを取得する
    html = get_page_html()
    print(html)

    # HTMLを解析

    # 情報を抽出

    # STEP2. データベース保存


if __name__ == "__main__":
    main()

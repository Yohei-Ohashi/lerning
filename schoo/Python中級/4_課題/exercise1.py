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

import re
import sqlite3
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 定数定義
TARGET_URL = "https://schoo.jp/class/category/programming/?sort=featured"

# User-Agent情報は調べて記述する
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"

# 　ディレクトリ関連
BASE_DIR = Path(__file__).parent
# DB
DB_DIR_NAME = "DB"
MAKE_DB_FILE_NAME = "scraping.db"


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


def make_df_get_info(soup: BeautifulSoup) -> pd.DataFrame:
    """
    BeautifulSoupオブジェクトから授業情報を抽出してDataFrameを作成する関数

    指定されたBeautifulSoupオブジェクトから授業の詳細情報（URL、タイトル、日付など）を
    抽出し、pandas DataFrameとして返す。

    Args:
        soup (BeautifulSoup): 解析対象のHTMLを含むBeautifulSoupオブジェクト

    Returns:
        pd.DataFrame: 抽出された授業情報を含むDataFrame
        カラム: 授業URL、授業タイトル、日付など
    """
    # 要素を取得
    elems = soup.find_all(
        "a",
        class_=r"group pc:mx-0 mx-auto flex w-full max-w-[400px] min-w-[260px] shrink grow flex-col gap-[12px] duration-300 active:opacity-70",
    )

    get_info_list = []

    for elem in elems:
        # 1. 授業URL (Class URL)
        # - 各授業の詳細ページへのリンクURL
        cls_url = elem.attrs["href"]

        # 2. 授業タイトル (Class Title)
        # - 授業のタイトル名
        cls_title = elem.find("h3").text

        # 3. 日付 (Date)
        # - 授業の日付情報
        date_text = (
            elem.find(
                "div",
                class_=r"text-neutral-deepgray flex h-[18px] items-center gap-[8px] text-[12px]",
            )
            .contents[2]
            .text
        )
        # 「公開」を削除
        date_text_clean = date_text.replace("公開", "").strip()

        # 日本語の日付形式 例:「2025年9月8日」を「2025-09-08」形式に変換
        # 正規表現で年、月、日を抽出
        match = re.search(r"(\d+)年(\d+)月(\d+)日", date_text_clean)
        if match:
            year = match.group(1)  # 年を取得（例: "2025"）
            month = match.group(2).zfill(2)  # 月を取得し、2桁にゼロ埋め（例: "09"）
            day = match.group(3).zfill(2)  # 日を取得し、2桁にゼロ埋め（例: "08"）
            date = f"{year}-{month}-{day}"  # ISO形式に変換（例: "2025-09-08"）
        else:
            date = ""

        # 4. ハート数 (Number of Likes/Hearts)
        # - 授業に付けられた「いいね」や「ハート」の数
        like = elem.find("span", class_=r"text-neutral-darkgray text-[11px]").text

        get_info_list.append(
            {"cls_url": cls_url, "cls_title": cls_title, "date": date, "like": like}
        )
    df = pd.DataFrame(get_info_list)

    return df


def save_sql(df: pd.DataFrame) -> None:
    """スクレイピングで取得したデータをSQLiteデータベースに保存する

    Args:
        df (pd.DataFrame): スクレイピングで取得した授業情報のデータフレーム
                        (cls_url, cls_title, date, like列を含む)
    """
    # STEP2. データベース保存
    # データベースを作成
    db_file = BASE_DIR / DB_DIR_NAME / MAKE_DB_FILE_NAME
    db_file.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # テーブルを作成する
    table_name = "ScrapingData"
    df.to_sql(table_name, con, if_exists="replace", index=False)

    con.close()


def main():
    # STEP1. スクレイピング
    # HTMLを取得する
    html = get_page_html()

    # HTMLを解析
    soup = BeautifulSoup(html, "html.parser")

    # 情報を抽出してDataFrame化
    df = make_df_get_info(soup)

    # STEP2. データベース保存
    save_sql(df)

    # 処理が長くて終わるタイミングがわからないので記述
    print("処理が終わりました!!")


if __name__ == "__main__":
    main()

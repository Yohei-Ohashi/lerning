import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


"""
https://schoo.jp/class/category/programming/?sort=featured
schoo のカテゴリーごとの授業人気順のデータを取得する
"""


def get_content_df(url):
    # selenium で chrome driverを使うための設定
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)  # urlを取得

    html = driver.page_source.encode('utf-8')  # ウェブページのhtmlを取得
    html_text = BeautifulSoup(html, "html.parser")
    content_list = html_text.find_all('div', class_='scrollContent')  # クラスに「scrollContent」を持つdivタグを抽出
    print(len(content_list))

    result = []
    for content in content_list:
        # クラスに「scrollContent」を持つdivタグのそれぞれに対し、以下処理を実行
        content_url = content.find('a').get('href')  # aタグのURLを取得
        content_title = content.find('div', class_='info').find('h3', class_='title').text  # クラスに「title」を持つh3タグのテキストを抽出
        content_date = content.find('div', class_='info').find('p', class_='date').text.split()[0]  # クラスに「date」を持つpタグのテキストを抽出
        fav_count = content.find('div', class_='info').find('div', class_='m_count').text  # クラスに「m_count」を持つdivタグのテキストを抽出

        content_info = {'url': content_url, 'title': content_title, 'date': content_date, 'fav': fav_count}  # 取得した情報を dictにまとめる
        result.append(content_info)  # resultリストに追加

    return pd.DataFrame(result)  # resultをpandasのデータフレームに変更


def save_sqlite(df, db_name, table_name):
    conn = sqlite3.connect(db_name)  # sqliteに接続
    df.to_sql(table_name, conn, if_exists='append', index=None)  # pandas の to_sql  で sqlite にデータを保存する
    conn.close()  # 接続を終了

    return


target_category = 'programming'
target_url = 'https://schoo.jp/class/category/' + target_category + '/?sort=featured'  # 取得するURLを指定
content_df = get_content_df(target_url)  # URLに対してスクレイピングを実施する
print(content_df.shape)
print(content_df.head())
print(content_df.tail())

sqlite_file = "./schoo.db"  # sqliteファイルの指定
table = 'contents'  # テーブル名を指定
save_sqlite(content_df, sqlite_file, table)
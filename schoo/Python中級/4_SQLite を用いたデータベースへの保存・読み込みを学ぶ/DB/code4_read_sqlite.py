import pandas as pd
import sqlite3

"""
https://schoo.jp/class/category/programming/?sort=featured
schoo のカテゴリーごとの授業人気順のデータを取得する
"""


def read_sqlite(db_name, sql):
    conn = sqlite3.connect(db_name)  # sqliteに接続
    df_ = pd.read_sql_query(sql, conn)  # pandas の read_sql で sqlite からデータフレームを取得する
    conn.close()  # 接続を終了

    return df_


pd.set_option('display.max_columns', 10)  # print() した際に10列まで表示するように設定
sqlite_file = "./schoo.db"  # sqliteファイルの指定
table = 'contents'  # テーブル名を指定
sql = f'SELECT * FROM {table}'  # sql文を指定
df = read_sqlite(sqlite_file, sql)

print(df.shape)
print(df.head())
print(df.tail())

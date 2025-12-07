import sqlite3
from pathlib import Path

# 定数定義
BASE_DIR = Path(__file__).parent
DB_DIR_NAME = "DB"
DB_FILE_NAME = "sample.db"
MAKE_DB_FILE_NAME = "sample_2.db"

con = sqlite3.connect(BASE_DIR / DB_DIR_NAME / MAKE_DB_FILE_NAME)
cur = con.cursor()

# テーブルの作成
sql = """
CREATE TABLE sales2(
    month TEXT,
    this_year INTEGER,
    previous INTEGER
)
"""
cur.execute(sql)

# レコードの追加
sales_list = [("202201", 100, 80), ("202202", 80, 120)]
sql = """
INSERT INTO sales2
VALUES(
    ?, ?, ?
)
"""
cur.executemany(sql, sales_list)

con.commit()
con.close()
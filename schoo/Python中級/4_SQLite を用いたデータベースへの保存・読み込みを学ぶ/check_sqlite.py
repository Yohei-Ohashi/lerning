import sqlite3
from pathlib import Path

# 定数定義
BASE_DIR = Path(__file__).parent
DB_DIR_NAME = "DB"
DB_FILE_NAME = "sample.db"
MAKE_DB_FILE_NAME = "sample_2.db"

con = sqlite3.connect(BASE_DIR / DB_DIR_NAME / MAKE_DB_FILE_NAME)
cur = con.cursor()

# データの確認
sql = """
SELECT *
FROM sales2
"""
cur.execute(sql)
sales_list = cur.fetchall()
print(sales_list)

con.close()
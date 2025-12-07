import sqlite3
from pathlib import Path

# 定数定義
BASE_DIR = Path(__file__).parent
DB_DIR_NAME = "DB"
DB_FILE_NAME = "sample.db"

con = sqlite3.connect(BASE_DIR / DB_DIR_NAME / DB_FILE_NAME)
cur = con.cursor()

sql = """SELECT *
FROM sales
WHERE previous_sales < 100
ORDER BY previous_sales
"""

cur.execute(sql)
sales_list = cur.fetchall()

print(sales_list)

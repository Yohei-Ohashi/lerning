import sqlite3
from pathlib import Path

import pandas as pd

# 定数定義
BASE_DIR = Path(__file__).parent

# DB
DB_DIR_NAME = "DB"
DB_FILE_NAME = "sample.db"
MAKE_DB_FILE_NAME = "sample_2.db"

# インプットファイル
INPUT_DIR_NAME = "input"
INPUT_FILE_NAME = "sales.csv"


con = sqlite3.connect(BASE_DIR / DB_DIR_NAME / MAKE_DB_FILE_NAME)

table_name = "test"
sql = f"""
SELECT *
FROM {table_name}
"""

# sql文で取得したデータをデータフレームに格納する
df = pd.read_sql_query(sql, con)
print(df)

con.close()

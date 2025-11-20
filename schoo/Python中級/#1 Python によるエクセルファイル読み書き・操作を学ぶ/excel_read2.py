# 外部ライブラリ
import pandas as pd
from pathlib import Path  # mac,windows両方で動くように

# 読み込みファイルのパス設定
input_path = Path(
    "schoo/Python中級/#1 Python によるエクセルファイル読み書き・操作を学ぶ/input/excels"
)
input_file_name = "sato.xlsx"
input_file_path = input_path / input_file_name

# df = pd.read_excel(input_file_path, sheet_name="202201")
# print(df)

# 労働時間が8時間を超えるもののみ抽出
# df_overwork = df.query("労働時間 > 8")
# print(df_overwork)

# 全てのデータフレームに条件を適応して抽出
all_df = pd.read_excel(input_file_path, sheet_name=None)
overwork_list = []
for sheet in all_df.keys():
    df_overwork = all_df[sheet].query("労働時間 > 8")
    overwork_list.append(df_overwork)

df = pd.concat(overwork_list)
print(df)

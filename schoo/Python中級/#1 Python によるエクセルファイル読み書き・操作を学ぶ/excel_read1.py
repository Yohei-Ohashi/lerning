# 外部ライブラリ
import pandas as pd
from pathlib import Path  # mac,windows両方で動くように

# 読み込みファイルのパス設定
input_path = Path(
    "schoo/Python中級/#1 Python によるエクセルファイル読み書き・操作を学ぶ/input/excels"
)
input_file_name = "sato.xlsx"
input_file_path = input_path / input_file_name

# データフレームとして出力
# 最初のシートをデータフレームに
# df = pd.read_excel(input_file_path)
# 202202シートをデータフレームに
# df = pd.read_excel(input_file_path, sheet_name="202202")
# 全てのシートを読み込む
# df = pd.read_excel(input_file_path, sheet_name=None)
# print(df)
# 複数のデータフレームは辞書で管理されている
# print(df.keys())

# print(df["202204"])

# スキップ
# df = pd.read_excel(input_file_path, sheet_name="202202", skiprows=[2])
# print(df)

df = pd.read_excel(input_file_path, sheet_name="202202", header=None)
print(df)

# 外部ライブラリ
import pandas as pd
from pathlib import Path  # mac,windows両方で動くように


# 読み込みファイルのパス設定
input_path = Path(
    "schoo/Python中級/1_Python によるエクセルファイル読み書き・操作を学ぶ/input/excels"
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

# 出力先の設定
output_path = Path(
    "schoo/Python中級/1_Python によるエクセルファイル読み書き・操作を学ぶ/output"
)
output_file_name = "sato_overwork2.xlsx"
output_file_path = output_path / output_file_name
# parents=True: 親ディレクトリも必要に応じて作成
# exist_ok=True: 既に存在していてもエラーにしない
output_file_path.parent.mkdir(parents=True, exist_ok=True)

# df.to_excel(output_file_path)
# シート名をつけて保存する
df.to_excel(output_file_path, sheet_name="sato_total")

# 外部ライブラリ
import pandas as pd
from pathlib import Path  # mac,windows両方で動くように


def concat_overwork(file_name):
    # 全てのデータフレームに条件を適応して抽出
    all_df = pd.read_excel(file_name, sheet_name=None)
    overwork_list = []
    for sheet in all_df.keys():
        df_overwork = all_df[sheet].query("労働時間 > 8")
        overwork_list.append(df_overwork)

    df = pd.concat(overwork_list)
    return df

input_path = Path(
    "schoo/Python中級/#1 Python によるエクセルファイル読み書き・操作を学ぶ/input/excels"
)

df_sato = concat_overwork(input_path / "sato.xlsx")
df_suzuki = concat_overwork(input_path / "suzuki.xlsx")

output_path = Path(
    "schoo/Python中級/#1 Python によるエクセルファイル読み書き・操作を学ぶ/output"
)

with pd.ExcelWriter(output_path / "sato_and_suzuki.xlsx") as writer:
    df_sato.to_excel(writer, sheet_name="sato")
    df_suzuki.to_excel(writer, sheet_name="suzuki")

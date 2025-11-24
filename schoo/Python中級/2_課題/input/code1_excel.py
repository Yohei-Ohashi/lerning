import pandas as pd
from pathlib import Path

# 「excels」フォルダ内にある、拡張子が'xlsx'ファイルを取得
temp_dir = Path('excels')
file_list = list(temp_dir.glob('*.xlsx'))

print(file_list)  # 取得されたファイル一覧を表示

target_sheet = '202202'  # 取得したいシート名を指定
all_df = []  # 取得したExcelシートを格納するためのリスト
for excel_file in file_list:
    df = pd.read_excel(excel_file, sheet_name=target_sheet)  # 対象のExcelファイルの対象シートを取得
    print(df)
    all_df.append(df)  # all_df リストに追加する

with pd.ExcelWriter(target_sheet + '.xlsx') as writer:
    for i in range(len(file_list)):
        all_df[i].to_excel(writer, sheet_name=file_list[i].stem)  # シート名を指定してExcelファイルに追加


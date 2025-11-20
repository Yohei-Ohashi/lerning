"""作成するツール
想定イメージ: あなたは経理担当です。毎月社員から送られてくるタイムカード Excelファイルを、
必要なシートだけまとめて1つのExcelファイルにしたいと考えています。

以下を一連で行うツールを作成してください：
- あるフォルダの中にあるExcelファイル一覧を取得
- 各Excelファイル内の特定シートのみ取得
- 取得したシートを一つのExcelファイルにして保存
"""

# あるフォルダの中にあるExcelファイル一覧を取得
# 標準ライブラリ
import os

# 外部ライブラリ
import pandas as pd
from pathlib import Path

# 定数定義
SHEET_NAME = "202203"
INPUT_DIR_PATH = "schoo/Python中級/1_課題/input"
OUTPUT_DIR_PATH = "schoo/Python中級/1_課題/output"
OUTPUT_FILE_NAME = "output_file.xlsx"
OUTPUT_FILE_PATH = Path(OUTPUT_DIR_PATH) / OUTPUT_FILE_NAME


def get_file_list(dir_path) -> list[str]:
    """フォルダの中にあるExcelファイル一覧を取得"""

    input_path = Path(dir_path)
    # ファイル名を取得する
    file_list = [
        f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))
    ]
    # 一応拡張子がxlsxだけに絞る
    xlsx_file_list = [xf for xf in file_list if xf.endswith(".xlsx") == True]

    return xlsx_file_list


def make_dfs(dir_path, xlsx_file_list):
    """各Excelファイル内の特定シートのみ取得"""

    df_list = []

    for file in xlsx_file_list:
        file_path = Path(dir_path) / file
        df = pd.read_excel(file_path, sheet_name=SHEET_NAME)
        df_list.append(df)

    return df_list


def output_excel(df_list, xlsx_file_list, output_file_path):
    """取得したシートを一つのExcelファイルにして保存"""

    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_file_path) as writer:
        for i, df in enumerate(df_list):
            sheet_name = xlsx_file_list[i].replace(".xlsx", "")
            df.to_excel(writer, sheet_name=sheet_name)


# メイン処理
def main():
    # フォルダの中にあるExcelファイル一覧を取得
    xlsx_file_list = get_file_list(INPUT_DIR_PATH)
    print(xlsx_file_list)

    # 各Excelファイル内の特定シートのみ取得
    df_list = make_dfs(INPUT_DIR_PATH, xlsx_file_list)
    print(len(df_list))

    # 取得したシートを一つのExcelファイルにして保存
    output_excel(df_list, xlsx_file_list, OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()

"""
課題：作成するツール

要件：
- 2019年~2021年における、東京都にどの程度人が滞在していたのかを記録したデータがあります
- なお、以下ごとにデータが記録されています：
  * 各地域(千代田区・中央区、など)
  * 休日 or 平日 or 全日
  * 昼 or 深夜 or 終日
- このデータを読み込み、横軸に年月、縦軸に滞在人口をプロットしてください

データソース：
使用するデータは、「全国の人流オープンデータ」(国土交通省)
(https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto)を加工して作成しています
"""

""" TODO
- ダウンロードしたデータを加工してプロット用のデータフレームを作成する
- プロットする
"""
from pathlib import Path

import pandas as pd

# 定数定義
BASE_DIR = Path(__file__).parent

# monthly_mdp_mesh1km_13をダウンロードし、解凍した中身をinputに展開することが前提
INPUT_TARGET_DIR_NAME = "input/13"
YEAR_LIST = [str(year) for year in range(2019, 2021 + 1)]
MONTH_LIST = [f"{month:02d}" for month in range(1, 12 + 1)]
TARGET_FILE_NAME = "monthly_mdp_mesh1km.csv.zip"

# prefcode_citycode_masterをダウンロードし、解凍した中身をinputに展開することが前提
INPUT_PREFCODE_MST_DIR_NAME = "input/prefcode_citycode_master"


def make_pref_mst_df(year: str) -> pd.DataFrame:
    """都道府県・市区町村マスターデータを読み込み、指定年に対応するデータフレームを作成する関数

    指定された年以前で利用可能な最新の都道府県・市区町村マスターファイルを
    読み込み、データフレームとして返す。マスターファイルが見つからない場合は
    FileNotFoundErrorを発生させる。

    Args:
        year (str): 対象年（文字列形式、例: "2019"）

    Raises:
        FileNotFoundError: 指定年以前のマスターデータが見つからない場合

    Returns:
        pd.DataFrame: 都道府県・市区町村マスターデータのデータフレーム
    """
    target_year_int = int(year)
    prefcode_mst_dir = BASE_DIR / INPUT_PREFCODE_MST_DIR_NAME

    # ディレクトリ内のファイルから、利用可能な年を抽出
    candidate_years = []
    for file_path in prefcode_mst_dir.glob("prefcode_citycode_master_utf8_*.csv.zip"):
        # ファイル名から年を抽出（例: "prefcode_citycode_master_utf8_2020.csv.zip" → "2020"）
        year_str = file_path.name.replace("prefcode_citycode_master_utf8_", "").replace(
            ".csv.zip", ""
        )
        if year_str.isdigit() and int(year_str) <= target_year_int:
            candidate_years.append(
                int(year_str)
            )  # 整数として保存（max()で比較しやすくするため）

    # 候補年の中から最大の年（最新の年）を見つける
    if candidate_years:
        # 最大の年を取得することで指定の年のマスタファイルが見つからない時は最新のものが反映される
        check_year = max(candidate_years)
        file_name = f"prefcode_citycode_master_utf8_{check_year}.csv.zip"
        prefcode_mst_file = prefcode_mst_dir / file_name

        # マスタデータを読み込む
        df_pref_mst = pd.read_csv(prefcode_mst_file)

        # cityname列から「東京都２３区」という接頭辞を削除する
        df_pref_mst["cityname"] = df_pref_mst["cityname"].str.replace(
            "東京２３区", "", regex=False
        )

        return df_pref_mst
    else:
        # どの都市も見つからない場合
        raise FileNotFoundError(
            f"マスターデータが見つかりません。 {year}年以前のデータを確認してください。"
        )


def make_target_df() -> pd.DataFrame:
    """指定された年月のデータファイルを読み込み、統合したデータフレームを作成する関数

    YEAR_LISTとMONTH_LISTで定義された各年月について、
    対応するデータファイル（monthly_mdp_mesh1km.csv.zip）が
    存在するかどうかを確認し、存在する場合はCSVファイルを読み込んで
    リストに追加する。最終的に全てのデータフレームを結合して返す。

    Returns:
        pd.DataFrame: 全ての年月のデータを統合したデータフレーム
    """
    df_list = []
    for year in YEAR_LIST:
        for month in MONTH_LIST:
            target_file = (
                BASE_DIR / INPUT_TARGET_DIR_NAME / year / month / TARGET_FILE_NAME
            )
            if target_file.exists():
                print(f"{year}年{month}月のデータを追加します👌")
                df = pd.read_csv(target_file)

                # 市区町村名を反映させる
                df_pref_mst = make_pref_mst_df(year)
                df = pd.merge(
                    df, df_pref_mst[["citycode", "cityname"]], on="citycode", how="left"
                )

                df_list.append(df)
            else:
                print(f"{year}年{month}月のデータは無いです❌")
    df_combined = pd.concat(df_list, ignore_index=True)
    return df_combined


def main():
    # データを一つのデータフレームにまとめる
    df = make_target_df()

    print(df)


if __name__ == "__main__":
    main()

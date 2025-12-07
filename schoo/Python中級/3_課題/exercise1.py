"""
課題：作成するツール

要件：
- 2019年~2021年における、東京都にどの程度人が滞在していたのかを記録したデータがあります
- なお、以下ごとにデータが記録されています：
    - 各地域(千代田区・中央区、など)
    - 休日 or 平日 or 全日
    - 昼 or 深夜 or 終日
- このデータを読み込み、横軸に年月、縦軸に滞在人口をプロットしてください

データソース：
使用するデータは、「全国の人流オープンデータ」(国土交通省)
(https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto)を加工して作成しています
"""

""" TODO
- [x] ダウンロードしたデータを加工してプロット用のデータフレームを作成する
- [ ] プロットしたい対象を抽出したデータフレームを作成する
- [ ] プロットする
"""
from pathlib import Path

import matplotlib.pyplot as plt
import openpyxl
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

# 日付タイプ用
DAYFLAG_HOLIDAY = 0  # 休日
DAYFLAG_WEEKDAY = 1  # 平日
DAYFLAG_ALL = 2  # 全日

# 時間帯用
TIMEZONE_DAY = 0  # 昼
TIMEZONE_NIGHT = 1  # 深夜
TIMEZONE_ALL = 2  # 終日


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

                # データフレームの加工
                # 市区町村名を反映させる
                df_pref_mst = make_pref_mst_df(year)
                df = pd.merge(
                    df, df_pref_mst[["citycode", "cityname"]], on="citycode", how="left"
                )
                # 年月フィールドを作成する
                df["yearmonth"] = f"{year}-{month}"

                df_list.append(df)
            else:
                print(f"{year}年{month}月のデータは無いです❌")
    df_combined = pd.concat(df_list, ignore_index=True)
    return df_combined


def plot_df_filter(
    df: pd.DataFrame, ax: plt.Axes, cityname: str, dayflag: int, timezone: int
) -> None:
    """指定された条件でデータフレームをフィルタリングし、グラフにプロットする関数

    市区町村名、日付タイプ、時間帯の条件でデータフレームを絞り込み、
    年月ごとの人口データを集計してグラフにプロットする。

    Args:
        df (pd.DataFrame): フィルタリング対象のデータフレーム
        ax (plt.Axes): プロット先のAxesオブジェクト
        cityname (str): 市区町村名（部分一致で検索）
        dayflag (int): 日付タイプ (0: 休日, 1: 平日, 2: 全日)
        timezone (int): 時間帯 (0: 昼, 1: 深夜, 2: 終日)

    Returns:
        pd.Series: フィルタリング後の年月別人口集計データ
    """
    # 1. 市区町村の部分一致で絞る条件を作成
    cityname_filtered = df["cityname"].str.contains(cityname)
    # 2. 日付タイプで絞る条件を作成 (0: 休日, 1: 平日, 2: 全日)
    dayflag_filtered = df["dayflag"] == dayflag
    # 3. 時間帯で絞る条件を作成 (0: 昼, 1: 深夜, 2: 終日)
    timezone_filtered = df["timezone"] == timezone
    # 　条件を組み合わせてデータフレームを作成する
    df_filtered = df[cityname_filtered & dayflag_filtered & timezone_filtered]
    df_filtered = (
        df_filtered[["yearmonth", "population"]]
        .groupby("yearmonth")
        .sum()["population"]
    )

    # プロットするAxesオブジェクトを作成する
    # pandas の Series を plot() に渡すと、Series のインデックスが自動的に x 軸として使われる
    ax.plot(df_filtered["population"], label=cityname)

    return df_filtered


def main():
    # データを一つのデータフレームにまとめる
    df = make_target_df()

    # プロットする
    # matplotlibで日本語を表示するための設定
    # 複数のフォントをリストで指定すると、利用可能な最初のフォントが自動的に使われます
    plt.rcParams["font.family"] = ["Hiragino Sans", "Yu Gothic", "MS Gothic"]
    # Figureオブジェクトの生成
    fig = plt.figure()
    fig.suptitle("People flow population per month")

    # Axesオブジェクトの生成
    ax = fig.add_subplot()
    ax.set_xlabel("month")
    ax.set_ylabel("population")
    plt.xticks(rotation=50)

    # 指定した条件でデータをフィルタリングし、グラフにプロットする
    plot_df_filter(df, ax, "千代田区", dayflag=DAYFLAG_WEEKDAY, timezone=TIMEZONE_DAY)
    plot_df_filter(df, ax, "新宿区", dayflag=DAYFLAG_WEEKDAY, timezone=TIMEZONE_DAY)
    plot_df_filter(df, ax, "町田市", dayflag=DAYFLAG_WEEKDAY, timezone=TIMEZONE_DAY)

    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()

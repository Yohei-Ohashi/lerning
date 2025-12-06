import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


"""
人流オープンデータを元に、月ごとの可視化を実施する
扱うデータは、「全国の人流オープンデータ」（国土交通省）（https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto）を加工して作成
"""


def plot_population(df, ax_, target_city, target_city_en, day_flag, timezone):
    target_df = df.query('cityname == @target_city & dayflag == @day_flag & timezone == @timezone')  # 指定されたcityname, day_flag, timezoneで抽出
    sum_population_df = target_df[['year_mm', 'population']].groupby('year_mm').sum()  # 年月ごとに合計値を計算

    ax_.plot(sum_population_df['population'], label=target_city_en)  # 横軸にyear_mm, 縦軸に人口データで折れ線グラフを表示
    plt.legend()


df_mesh = pd.read_csv('mesh1kmid_tokyo.csv')
print(df_mesh.head())

"""
target_city: [
    '千代田区', '中央区', '港区', '新宿区', '文京区', '台東区', '墨田区', '江東区', '品川区',
    '目黒区', '大田区', '世田谷区', '渋谷区', '中野区', '杉並区', '豊島区', '北区', '荒川区',
    '板橋区', '練馬区', '足立区', '葛飾区', '江戸川区', '八王子市', '立川市', '武蔵野市', '三鷹市',
    '青梅市', '府中市', '昭島市', '調布市', '町田市', '小金井市', '小平市', '日野市', '東村山市',
    '国分寺市', '国立市', '福生市', '狛江市', '東大和市', '清瀬市', '東久留米市', '武蔵村山市',
    '多摩市', '稲城市', '羽村市', 'あきる野市', '西東京市', '西多摩郡瑞穂町', '西多摩郡日の出町',
    '西多摩郡檜原村', '西多摩郡奥多摩町', '大島町', '利島村', '新島村', '神津島村', '三宅島三宅村',
    '八丈島八丈町', '青ヶ島村', '小笠原村', '御蔵島村'
]

day_flag 0: 休日, 1: 平日, 2: 全日
timezone 0: 昼, 1: 深夜: 2: 終日
"""


fig = plt.figure()
fig.suptitle('People flow population per month')  # グラフにタイトルを設定

ax = fig.add_subplot()
ax.set_xlabel('month')  # x軸のラベルを設定
ax.set_ylabel('population')  # y軸のラベルを設定
plt.xticks(rotation=50)  # x軸の項目を斜めで表示する

plot_population(df_mesh, ax, target_city='千代田区', target_city_en='chiyoda', day_flag=1, timezone=0)  # 千代田区の平日、昼の人流データを可視化
plot_population(df_mesh, ax, target_city='新宿区', target_city_en='shinjuku', day_flag=1, timezone=0)  # 新宿区の平日、昼の人流データを可視化
plot_population(df_mesh, ax, target_city='町田市', target_city_en='machida', day_flag=1, timezone=0)  # 町田市の平日、昼の人流データを可視化

plt.show()

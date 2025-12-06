import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto
# からダウンロードした、attribute, prefcode_citycode_master, monthly_mdp_mesh1km_13（東京都）を使用
# 「全国の人流オープンデータ」（国土交通省）（https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto）を加工して作成

attribute_mesh1km = pd.DataFrame() # 1kmメッシュ属性
prefcode_citycode_master = pd.DataFrame() # 都道府県・市区町村マスタ-
for year in [2019, 2020, 2021]:
    tmp_df01 = pd.read_csv(f'data/attribute/attribute_mesh1km_{year}.csv.zip')
    tmp_df02 = pd.read_csv(f'data/prefcode_citycode_master/prefcode_citycode_master_utf8_{year}.csv.zip')
    tmp_df01['year'] = year
    tmp_df02['year'] = year
    attribute_mesh1km = pd.concat([attribute_mesh1km, tmp_df01])
    prefcode_citycode_master = pd.concat([prefcode_citycode_master, tmp_df02])

# 滞在人口1kmメッシュデータ
dfs = []
pref_code = 13
for mm in range(12):
    mm = str(mm+1).zfill(2)
    dfs.append(pd.read_csv(f'data/{pref_code}_mesh1km/2019/{mm}/monthly_mdp_mesh1km.csv.zip'))
    dfs.append(pd.read_csv(f'data/{pref_code}_mesh1km/2020/{mm}/monthly_mdp_mesh1km.csv.zip'))
    dfs.append(pd.read_csv(f'data/{pref_code}_mesh1km/2021/{mm}/monthly_mdp_mesh1km.csv.zip'))

df = pd.concat(dfs).reset_index(drop=True)
df = pd.merge(df, attribute_mesh1km, on=['mesh1kmid', 'prefcode', 'citycode', 'year'])
df = pd.merge(df, prefcode_citycode_master[['citycode', 'cityname', 'year']], on=['citycode', 'year'])

df['cityname'] = df['cityname'].apply(lambda x : x[5:] if '東京２３区' in x else x)
df['year_mm'] = df['year'].astype(str) + '/' + df['month'].astype(str).str.zfill(2)
df = df.drop(['prefcode', 'citycode', 'lon_center', 'lat_center', 'lon_max', 'lat_max', 'lon_min', 'lat_min'], axis=1)
df = df.set_index('mesh1kmid')
df.to_csv('mesh1kmid_tokyo.csv')
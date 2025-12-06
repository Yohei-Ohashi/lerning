from pathlib import Path

import pandas as pd
import plotly
import plotly.graph_objects as go

# 定数定義
BASE_DIR = Path(__file__).parent
INPUT_DIR_PATH = BASE_DIR / "input"
INPUT_FILE_NAME = "sales.csv"
INPUT_FILE_PATH = INPUT_DIR_PATH / INPUT_FILE_NAME

df = pd.read_csv(INPUT_FILE_PATH)

plot_data = go.Scatter(x=df["month"], y=df["sales"], mode="markers")

fig = go.Figure(plot_data)
fig.show()
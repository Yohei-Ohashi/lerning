from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 定数定義
BASE_DIR = Path(__file__).parent
INPUT_DIR_PATH = BASE_DIR / "input"
INPUT_FILE_NAME = "sales.csv"
INPUT_FILE_PATH = INPUT_DIR_PATH / INPUT_FILE_NAME

df = pd.read_csv(INPUT_FILE_PATH)

sns.pairplot(df)

plt.show()
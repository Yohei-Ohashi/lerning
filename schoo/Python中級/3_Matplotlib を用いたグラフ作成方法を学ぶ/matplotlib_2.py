from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# 定数定義
BASE_DIR = Path(__file__).parent
INPUT_DIR_PATH = BASE_DIR / "input"
INPUT_FILE_NAME = "sales.csv"
INPUT_FILE_PATH = INPUT_DIR_PATH / INPUT_FILE_NAME

df = pd.read_csv(INPUT_FILE_PATH)
print(df)

fig = plt.figure()
ax = fig.add_subplot()
fig.suptitle("sales result")

ax.plot(df["month"], df["sales"])
ax.plot(df["month"], df["previous_sales"])
ax.set_xlabel("month")
ax.set_ylabel("sales")

plt.show()

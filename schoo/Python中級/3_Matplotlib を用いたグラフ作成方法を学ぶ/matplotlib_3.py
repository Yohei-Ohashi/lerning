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
fig.suptitle("sales result")

ax1 = fig.add_subplot(2, 2, 1)
ax1.pie(df["sales"], labels=df["month"])

ax2 = fig.add_subplot(2, 2, 2)
ax2.hist(df["sales"])

ax3 = fig.add_subplot(2, 2, 3)
ax3.scatter(df["month"], df["sales"])

ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(df["month"], df["sales"])


# ax.set_xlabel("month")
# ax.set_ylabel("sales")

plt.show()

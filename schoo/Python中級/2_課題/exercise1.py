"""
タイムカードExcelファイル統合ツール（GUI版）

【想定シナリオ】
あなたは経理担当です。毎月社員から送られてくるタイムカードExcelファイルを、
必要なシートだけまとめて1つのExcelファイルにしたいと考えています。

【ツールの要件】
以下の機能を一連で行うGUIツールを作成してください。

1. フォルダ選択機能
    - ユーザーがタイムカードExcelファイルが入っているフォルダを選択できる
    - tkinterのフォルダ選択ダイアログを使用

2. Excelファイル一覧の取得
    - 選択したフォルダ内にあるすべてのExcelファイル（.xlsx, .xls）を取得
    - ファイル一覧を表示（リストボックスなど）

3. 特定シートの選択・取得
    - ユーザーが取得したいシート名を指定できる（入力欄または選択肢）
    - 各Excelファイルから指定されたシートのみを読み込む
    - シートが存在しない場合はエラーハンドリング（スキップまたは警告表示）

4. 統合Excelファイルの保存
    - 取得したすべてのシートを1つの新しいExcelファイルにまとめる
    - 保存先とファイル名をユーザーが指定できる
    - 保存先のフォルダ選択ダイアログを使用

【GUIの構成要素（推奨）】
- フォルダ選択ボタン
- 選択したフォルダのパス表示
- Excelファイル一覧表示（リストボックス）
- シート名入力欄（または選択肢）
- 保存先選択ボタン
- 実行ボタン
- 進捗状況や結果の表示エリア（ラベルやテキストエリア）

【技術的な要件】
- tkinterを使用してGUIを作成
- openpyxlまたはpandasを使用してExcelファイルを操作
- エラーハンドリングを適切に実装（ファイルが開けない、シートが存在しないなど）
- ユーザーフレンドリーなメッセージ表示（成功、エラー、警告など）

【実装のヒント】
- フォルダ選択: tkinter.filedialog.askdirectory()
- ファイル保存: tkinter.filedialog.asksaveasfilename()
- Excel操作: openpyxlやpandasを使用
- ファイル一覧取得: os.listdir()やglobモジュールを使用
"""

import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def btn_select_dir() -> None:

    base_dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=base_dir)

    if dir_path:  # ユーザーがキャンセルしなかった場合
        text_input1.set(dir_path)

        # ファイル一覧を取得
        file_list = get_file_list(dir_path)

        # text2にファイル一覧を表示
        text2.delete(1.0, tk.END)  # 既存の内容をクリア
        if file_list:
            # 各ファイル名を改行区切りで表示
            file_list_text = "\n".join(file_list)
            text2.insert(1.0, file_list_text)
        else:
            text2.insert(1.0, "Excelファイルが見つかりませんでした。")


def get_file_list(dir_path: str | Path) -> list[str]:
    """フォルダの中にあるExcelファイル一覧を取得"""

    input_path = Path(dir_path)
    # ファイル名を取得する
    file_list = [
        f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))
    ]
    # 一応拡張子がxlsxだけに絞る
    xlsx_file_list = [xf for xf in file_list if xf.endswith(".xlsx") == True]

    return xlsx_file_list


root = tk.Tk()
root.title("Excelファイル統合ツール")
root.geometry("600x400")
root.lift()
root.focus_force()

# フォルダ選択
frame1 = ttk.Frame(root)
frame1.grid(row=0, column=0, sticky="nw")

text1_label = ttk.Label(frame1, text="フォルダ選択: ")
text1_label.grid(row=0, column=0)

text_input1 = tk.StringVar()
entry1 = ttk.Entry(frame1, textvariable=text_input1, width=40)
entry1.grid(row=0, column=1)

button1 = ttk.Button(frame1, text="参照", command=btn_select_dir)
button1.grid(row=0, column=2)

# フォントを揃えるために、ウィジェットを更新してからフォントを取得
root.update()
entry_font = entry1.cget("font")

# 一覧表示
frame2 = ttk.Frame(root)
frame2.grid(row=1, column=0, sticky="nw")

text2_label = ttk.Label(frame2, text="ファイル一覧: ")
text2_label.grid(row=0, column=0, sticky="nw")

text2 = tk.Text(frame2, width=40, height=10, wrap=tk.WORD, font=entry_font)
text2.grid(row=0, column=1)

# 取得シートの設定

# 保存

root.mainloop()

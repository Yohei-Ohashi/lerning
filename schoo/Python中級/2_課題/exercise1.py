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

# TODO
# - [] 入力値の検証
#     - フォルダが選択されていない場合
#     - シート名が入力されていない場合
#     - 出力ファイル名が入力されていない場合
# - [] ファイル操作のエラーハンドリング
#     - ファイルが開けない場合（権限エラー、ファイル破損など）
#     - シートが存在しない場合（要件で要求されている）
#     - ディレクトリが作成できない場合


import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pandas as pd

# 定数定義
OUTPUT_DIR_PATH = "schoo/Python中級/2_課題/output"


def btn_select_dir() -> None:
    """ディレクトリの選択
    
    フォルダを選択するためのボタンがクリックされた時に呼び出されます。
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=base_dir)

    if dir_path:  # ユーザーがキャンセルしなかった場合
        text_input1.set(dir_path)

        try:
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
        
        except Exception as e:
            # エラーをユーザーに表示
            messagebox.showerror("エラー", f"ファイル一覧の取得に失敗しました:\n{str(e)}")
            text2.delete(1.0, tk.END)
            text2.insert(1.0, "エラーが発生しました。")


def get_file_list(dir_path: str | Path) -> list[str]:
    """フォルダの中にあるExcelファイル一覧を取得"""
    try:
        input_path = Path(dir_path)
        # ディレクトリが存在するか確認
        if not input_path.exists():
            raise FileNotFoundError(f"指定されたフォルダが存在しません: {dir_path}")
        if not input_path.is_dir():
            raise NotADirectoryError(f"指定されたパスはフォルダではありません: {dir_path}")
        
        # ファイル名を取得する
        file_list = [
            f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))
        ]
        # 一応拡張子がxlsxだけに絞る
        xlsx_file_list = [xf for xf in file_list if xf.endswith(".xlsx")]

        return xlsx_file_list
    
    except PermissionError as e:
        # アクセス権限がない場合
        raise PermissionError(f"フォルダへのアクセス権限がありません: {dir_path}") from e
    except Exception as e:
        # その他の予期しないエラー
        raise Exception(f"ファイル一覧の取得中にエラーが発生しました: {str(e)}") from e


def make_dfs(dir_path: str | Path, xlsx_file_list: list[str], sheet_name: str) -> list[pd.DataFrame]:
    """各Excelファイル内の特定シートのみ取得"""

    df_list = []
    skipped_files = []  # スキップしたファイルを記録

    for file in xlsx_file_list:
        file_path = Path(dir_path) / file
        try:
            # Excelファイルを読み込む
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df_list.append(df)
        
        except FileNotFoundError:
            # ファイルが見つからない場合
            skipped_files.append(f"{file} (ファイルが見つかりません)")
            continue
        
        except PermissionError:
            # ファイルが開けない場合 (権限エラー)
            skipped_files.append(f"{file} (アクセス権限がありません)")
            continue
        
        except ValueError as e:
            # シートが存在しない場合 (pandasはvalueErrorを発生させる)
            if "Worksheet named" in str(e) or "Sheet named" in str(e):
                skipped_files.append(f"{file} (シート '{sheet_name}' が存在しません)")
            else:
                skipped_files.append(f"{file} (読み込みエラー: {str(e)})")
            continue
        
        except Exception as e:
            # その他の予期しないエラー(ファイルは損など)
            skipped_files.append(f"{file} (エラー: {str(e)})")
            continue
        
    # スキップしたファイルがある場合は警告を返す情報として保持
    # (後でGUIに表示するために、戻り値に含めるか、別の方法で通知)
    if skipped_files:
        # ここでは警告メッセージを返す(後でGUIに表示)
        pass  # 後で実装

    return df_list, skipped_files  # スキップ情報も返す


def output_excel(
    df_list: list[pd.DataFrame], xlsx_file_list: list[str], output_file_path: Path
) -> None:
    """取得したシートを一つのExcelファイルにして保存"""

    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_file_path) as writer:
        for i, df in enumerate(df_list):
            sheet_name = xlsx_file_list[i].replace(".xlsx", "")
            df.to_excel(writer, sheet_name=sheet_name)


def validate_inputs() -> tuple[bool, str]:
    """入力値の検証を行う

    Returns:
        tuple[bool, str]: (検証成功かどうか、 エラーメッセージ)
    """
    # フォルダが選択されているか確認
    if not text_input1.get().strip():
        return False, "フォルダを選択してください。"
    
    # シート名が入力されているか確認
    if not sheet_name_input.get().strip():
        return False, "取得するシート名を入力してください。"
    
    # 出力ファイル名が入力されているか確認
    if not output_file_name_input.get().strip():
        return False, "出力ファイル名を入力してください。"
    
    return True, ""


def run():
    # 入力値の検証
    is_valid, error_message = validate_inputs()
    if not is_valid:
        messagebox.showwarning("入力エラー", error_message)
        return

    try:
        # フォルダの中にあるExcelファイル一覧を取得
        xlsx_file_list = get_file_list(text_input1.get())

        if not xlsx_file_list:
            messagebox.showwarning("警告", "Excelファイルが見つかりませんでした。")
            return

        # 各Excelファイル内の特定シートのみ取得
        df_list, skipped_files = make_dfs(text_input1.get(), xlsx_file_list, sheet_name_input.get())

        if not df_list:
            messagebox.showwarning("エラー", "読み込めるシートが1つもありませんでした。")
            return

        # 取得したシートを一つのExcelファイルにして保存
        output_file_path = Path(OUTPUT_DIR_PATH) / output_file_name_input.get()

        try:
            output_excel(df_list, xlsx_file_list, output_file_path)
        except PermissionError:
            messagebox.showwarning("エラー", f"ファイルを保存できませんでした。\n権限を確認してください。\n{output_file_path}")
            return
        except Exception as e:
            messagebox.showwarning("エラー", f"ファイルの保存中にエラーが発生しました:\n{str(e)}")
            return

        # 完了通知(スキップ情報も表示させる)
        message = f"処理完了！\n保存先: \n{output_file_path}\n\n読み込んだファイル数: {len(df_list)}"
        if skipped_files:
            message += f"\n\nスキップされたファイル ({len(skipped_files)}件):\n" + "\n".join(skipped_files)
        messagebox.showinfo("完了", message)

    except FileNotFoundError as e:
        messagebox.showerror("エラー", f"ファイルが見つかりませんでした:\n{str(e)}")
    except PermissionError as e:
        messagebox.showerror("エラー", f"アクセス権限がありません:\n{str(e)}")
    except Exception as e:
        # エラーをユーザーに表示
        messagebox.showerror("エラー", f"予期しないエラーが発生しました:\n{str(e)}")

def close_window():
    """ウィンドウを閉じる関数"""
    root.destroy()


root = tk.Tk()
root.title("Excelファイル統合ツール")
root.geometry("700x400")
root.lift()
root.focus_force()

# フォルダ選択
frame1 = ttk.Frame(root)
frame1.grid(row=0, column=0, sticky="nw")

text1_label = ttk.Label(frame1, text="フォルダ選択: ")
text1_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

text_input1 = tk.StringVar()
entry1 = ttk.Entry(frame1, textvariable=text_input1, width=40)
entry1.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

select_button = ttk.Button(frame1, text="選択", command=btn_select_dir)
select_button.grid(row=0, column=2, padx=10, pady=10, sticky="nw")

# フォントを揃えるために、ウィジェットを更新してからフォントを取得
root.update()
entry_font = entry1.cget("font")

# 一覧表示
text2_label = ttk.Label(frame1, text="ファイル一覧: ")
text2_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

text2 = tk.Text(frame1, width=40, height=10, wrap=tk.WORD, font=entry_font)
text2.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

# 取得シートの設定
text2_label = ttk.Label(frame1, text="取得シート設定: ")
text2_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

sheet_name_input = tk.StringVar()
entry2 = ttk.Entry(frame1, textvariable=sheet_name_input, width=40)
entry2.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

# 出力ファイル名の設定
output_file_name_label = ttk.Label(frame1, text="出力ファイル名: ")
output_file_name_label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

output_file_name_input = tk.StringVar()
entry3 = ttk.Entry(frame1, textvariable=output_file_name_input, width=40)
entry3.grid(row=3, column=1, padx=10, pady=10, sticky="nw")

# 保存
run_button = ttk.Button(frame1, text="実行", command=run)
run_button.grid(row=4, column=1, padx=10, pady=10, sticky="ne")

close_button = ttk.Button(frame1, text="閉じる", command=close_window)
close_button.grid(row=4, column=2, padx=10, pady=10, sticky="nw")


root.mainloop()

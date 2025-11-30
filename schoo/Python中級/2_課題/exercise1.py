import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pandas as pd

# 定数定義
OUTPUT_DIR_PATH = "schoo/Python中級/2_課題/output"


class ExcelMergerApp:
    """Excelファイル統合アプリケーションのメインクラス"""

    def __init__(self, root):
        self.root = root
        self.root.title("Excelファイル統合ツール")
        self.root.geometry("700x400")
        root.lift()
        root.focus_force()

        # 変数をインスタンス変数として管理
        self.folder_path = tk.StringVar()
        self.sheet_name = tk.StringVar()
        self.output_file_name = tk.StringVar()

        # UIの構築を実行
        self.setup_ui()

    def setup_ui(self):
        """UIの構築：すべてのウィジェット（ボタン、入力欄など）を作成"""

        # メインフレーム(コンテナ)を作成
        frame1 = ttk.Frame(self.root)
        frame1.grid(row=0, column=0, sticky="nw")

        # フォルダ選択のラベルと入力欄
        text1_label = ttk.Label(frame1, text="フォルダ選択: ")
        text1_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # 入力欄を作成(self.folder_path に接続)
        entry1 = ttk.Entry(frame1, textvariable=self.folder_path, width=40)
        entry1.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        # 選択ボタン(command=self.btn_select_dir でクラスメソッドを呼び出し)
        select_button = ttk.Button(frame1, text="選択", command=self.btn_select_dir)
        select_button.grid(row=0, column=2, padx=10, pady=10, sticky="nw")

        # フォントを揃えるために、ウィジェットを更新してからフォントを取得
        self.root.update()
        entry_font = entry1.cget("font")

        # ファイル一覧表示のラベルとテキストエリア
        text2_label = ttk.Label(frame1, text="ファイル一覧: ")
        text2_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        self.file_list_text = tk.Text(
            frame1, width=40, height=10, wrap=tk.WORD, font=entry_font
        )
        self.file_list_text.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

        # 取得シートの設定
        sheet_label = ttk.Label(frame1, text="取得シート設定: ")
        sheet_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        entry2 = ttk.Entry(frame1, textvariable=self.sheet_name, width=40)
        entry2.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

        # 出力ファイル名の設定
        output_file_name_label = ttk.Label(frame1, text="出力ファイル名: ")
        output_file_name_label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

        entry3 = ttk.Entry(frame1, textvariable=self.output_file_name, width=40)
        entry3.grid(row=3, column=1, padx=10, pady=10, sticky="nw")

        # 実行ボタンと閉じるボタン
        run_button = ttk.Button(frame1, text="実行", command=self.run)
        run_button.grid(row=4, column=1, padx=10, pady=10, sticky="ne")

        close_button = ttk.Button(frame1, text="閉じる", command=self.close_window)
        close_button.grid(row=4, column=2, padx=10, pady=10, sticky="nw")

    def btn_select_dir(self) -> None:
        """ディレクトリの選択

        フォルダを選択するためのボタンがクリックされた時に呼び出されます。
        """
        base_dir = os.path.abspath(os.path.dirname(__file__))
        dir_path = filedialog.askdirectory(initialdir=base_dir)

        if dir_path:  # ユーザーがキャンセルしなかった場合
            self.folder_path.set(dir_path)

            try:
                # ファイル一覧を取得
                file_list = self.get_file_list(dir_path)

                # text2にファイル一覧を表示
                self.file_list_text.delete(1.0, tk.END)  # 既存の内容をクリア
                if file_list:
                    # 各ファイル名を改行区切りで表示
                    file_list_text = "\n".join(file_list)
                    self.file_list_text.insert(1.0, file_list_text)
                else:
                    self.file_list_text.insert(
                        1.0, "Excelファイルが見つかりませんでした。"
                    )

            except Exception as e:
                # エラーをユーザーに表示
                messagebox.showerror(
                    "エラー", f"ファイル一覧の取得に失敗しました:\n{str(e)}"
                )
                self.file_list_text.delete(1.0, tk.END)
                self.file_list_text.insert(1.0, "エラーが発生しました。")

    def get_file_list(self, dir_path: str | Path) -> list[str]:
        """フォルダの中にあるExcelファイル一覧を取得

        このメソッドは他のメソッドから呼び出されるだけなので、
        グローバル関数のままでも動くが、クラス内にまとめた方が整理できるのでクラスメソッド化
        """
        try:
            input_path = Path(dir_path)
            # ディレクトリが存在するか確認
            if not input_path.exists():
                raise FileNotFoundError(f"指定されたフォルダが存在しません: {dir_path}")
            if not input_path.is_dir():
                raise NotADirectoryError(
                    f"指定されたパスはフォルダではありません: {dir_path}"
                )

            # ファイル名を取得する
            file_list = [
                f
                for f in os.listdir(input_path)
                if os.path.isfile(os.path.join(input_path, f))
            ]
            # 一応拡張子がxlsxだけに絞る
            xlsx_file_list = [xf for xf in file_list if xf.endswith(".xlsx")]

            return xlsx_file_list

        except PermissionError as e:
            # アクセス権限がない場合
            raise PermissionError(
                f"フォルダへのアクセス権限がありません: {dir_path}"
            ) from e
        except Exception as e:
            # その他の予期しないエラー
            raise Exception(
                f"ファイル一覧の取得中にエラーが発生しました: {str(e)}"
            ) from e

    def make_dfs(
        self, dir_path: str | Path, xlsx_file_list: list[str], sheet_name: str
    ) -> tuple[list[pd.DataFrame], list[str]]:
        """各Excelファイル内の特定シートのみ取得

        Returns:
            tuple[list[pd.DataFrame], list[str]]
        """
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
                    skipped_files.append(
                        f"{file} (シート '{sheet_name}' が存在しません)"
                    )
                else:
                    skipped_files.append(f"{file} (読み込みエラー: {str(e)})")
                continue

            except Exception as e:
                # その他の予期しないエラー(ファイルは損など)
                skipped_files.append(f"{file} (エラー: {str(e)})")
                continue

        return df_list, skipped_files  # スキップ情報も返す

    def output_excel(
        self,
        df_list: list[pd.DataFrame],
        xlsx_file_list: list[str],
        output_file_path: Path,
    ) -> None:
        """取得したシートを一つのExcelファイルにして保存"""

        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_file_path) as writer:
            for i, df in enumerate(df_list):
                sheet_name = xlsx_file_list[i].replace(".xlsx", "")
                df.to_excel(writer, sheet_name=sheet_name)

    def validate_inputs(self) -> tuple[bool, str]:
        """入力値の検証を行う

        Returns:
            tuple[bool, str]: (検証成功かどうか、 エラーメッセージ)
        """
        # フォルダが選択されているか確認
        if not self.folder_path.get().strip():
            return False, "フォルダを選択してください。"

        # シート名が入力されているか確認
        if not self.sheet_name.get().strip():
            return False, "取得するシート名を入力してください。"

        # 出力ファイル名が入力されているか確認
        if not self.output_file_name.get().strip():
            return False, "出力ファイル名を入力してください。"

        return True, ""

    def run(self):
        """実行処理"""
        # 入力値の検証
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            messagebox.showwarning("入力エラー", error_message)
            return

        try:
            # フォルダの中にあるExcelファイル一覧を取得
            xlsx_file_list = self.get_file_list(self.folder_path.get())

            if not xlsx_file_list:
                messagebox.showwarning("警告", "Excelファイルが見つかりませんでした。")
                return

            # 各Excelファイル内の特定シートのみ取得
            df_list, skipped_files = self.make_dfs(
                self.folder_path.get(), xlsx_file_list, self.sheet_name.get()
            )

            if not df_list:
                messagebox.showwarning(
                    "エラー", "読み込めるシートが1つもありませんでした。"
                )
                return

            # 取得したシートを一つのExcelファイルにして保存
            output_file_path = Path(OUTPUT_DIR_PATH) / self.output_file_name.get()

            try:
                self.output_excel(df_list, xlsx_file_list, output_file_path)
            except PermissionError:
                messagebox.showwarning(
                    "エラー",
                    f"ファイルを保存できませんでした。\n権限を確認してください。\n{output_file_path}",
                )
                return
            except Exception as e:
                messagebox.showwarning(
                    "エラー", f"ファイルの保存中にエラーが発生しました:\n{str(e)}"
                )
                return

            # 完了通知(スキップ情報も表示させる)
            message = f"処理完了！\n保存先: \n{output_file_path}\n\n読み込んだファイル数: {len(df_list)}"
            if skipped_files:
                message += (
                    f"\n\nスキップされたファイル ({len(skipped_files)}件):\n"
                    + "\n".join(skipped_files)
                )
            messagebox.showinfo("完了", message)

        except FileNotFoundError as e:
            messagebox.showerror("エラー", f"ファイルが見つかりませんでした:\n{str(e)}")
        except PermissionError as e:
            messagebox.showerror("エラー", f"アクセス権限がありません:\n{str(e)}")
        except Exception as e:
            # エラーをユーザーに表示
            messagebox.showerror("エラー", f"予期しないエラーが発生しました:\n{str(e)}")

    def close_window(self):
        """ウィンドウを閉じる関数"""
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ExcelMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

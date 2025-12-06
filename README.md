# Learning Repository

三重県主催の「みえDXスキルアップアカデミー」における学習記録用リポジトリです。動画教材で学習した内容を記録・管理するために作成されました。

## 📋 概要

このリポジトリは、みえDXスキルアップアカデミーの動画教材で学習した内容を記録するためのものです。主にスクー（Schoo）の学習コンテンツを中心に、その他の学習コンテンツも含めて管理しています。

学習コンテンツは日々追加されていくため、このリポジトリも継続的に更新されます。

## 🛠️ 環境セットアップ

このプロジェクトは **uv** を使用して依存関係を管理しています。uvは、Pythonのパッケージ管理を高速かつ効率的に行うツールです。

### 必要な環境

- Python 3.12以上
- [uv](https://github.com/astral-sh/uv)（パッケージマネージャー）

### セットアップ手順

1. **uvのインストール**（まだインストールしていない場合）

   ```bash
   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **プロジェクトの依存関係をインストール**

   ```bash
   # プロジェクトのルートディレクトリで実行
   uv sync
   ```

   これにより、`pyproject.toml`に記載されているすべての依存関係がインストールされます。

3. **仮想環境の有効化**

   ```bash
   # uvが自動的に仮想環境を管理します
   # スクリプトを実行する際は、以下のように実行します
   uv run python <スクリプト名>.py
   ```

## 📁 プロジェクト構造

```text
learning/
├── schoo/                    # スクー（Schoo）の学習教材
│   ├── Python初級/          # 初級レベルの学習内容
│   └── Python中級/          # 中級レベルの学習内容
├── youtube/                  # YouTube関連の学習コンテンツ
├── free-app/                 # フリーアプリ関連のプロジェクト
├── pyproject.toml           # プロジェクト設定と依存関係
└── README.md                # このファイル
```

### ディレクトリ構造について

- 各学習コンテンツは、その内容に応じたディレクトリに整理されています
- 各ディレクトリには、学習で使用したスクリプト、ノート、入力データ（`input/`）、出力結果（`output/`）が含まれる場合があります
- 学習コンテンツは日々追加されていくため、ディレクトリ構成は継続的に更新されます

## 📦 主な依存関係

このプロジェクトで使用している主なライブラリは以下の通りです：

- **pandas**: データ分析・操作
- **openpyxl**: Excelファイルの操作
- **matplotlib**: グラフ作成
- **seaborn**: 統計データの可視化
- **plotly**: インタラクティブなグラフ作成
- **jupyterlab**: Jupyter Notebookの実行環境
- **japanize-matplotlib**: Matplotlibの日本語表示対応
- **scikit-learn**: 機械学習ライブラリ

詳細は `pyproject.toml` を参照してください。

## 🚀 使用方法

### Pythonスクリプトの実行

```bash
# uv環境でスクリプトを実行
uv run python <スクリプトのパス>
```

### Jupyter Notebookの起動

```bash
# JupyterLabを起動
uv run jupyter lab
```

### 依存関係の追加

新しいパッケージを追加する場合：

```bash
# パッケージを追加（例：numpy）
uv add numpy

# 開発用の依存関係を追加する場合
uv add --dev pytest
```

## 📝 注意事項

- 各ディレクトリには `input/` と `output/` フォルダが含まれている場合があります
- 実行前に必要な入力ファイルが `input/` フォルダに配置されているか確認してください
- 実行結果は `output/` フォルダに保存されます
- 学習コンテンツは継続的に追加されるため、ディレクトリ構成は随時更新されます

## 🔗 参考リンク

- [uv公式ドキュメント](https://github.com/astral-sh/uv)
- [Python公式ドキュメント](https://docs.python.org/ja/)
- [pandas公式ドキュメント](https://pandas.pydata.org/docs/)
- [Matplotlib公式ドキュメント](https://matplotlib.org/)

## 📄 ライセンス

このリポジトリは学習目的で作成されています。

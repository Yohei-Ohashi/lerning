from flask import Flask, render_template

# Flaskアプリの作成
app = Flask(__name__)

# トップページへのアクセス設定 (ルートURLの定義)
@app.route("/")
def index():
    return render_template("index.html")

# アプリの起動
def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
from flask import Flask, render_template, request

# Flaskアプリの作成
app = Flask(__name__)


# トップページへのアクセス設定 (ルートURLの定義)
@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = ""

    # POSTを受けたら
    if request.method == "POST":
        # htmlのuser_inputで受けた値を取得する
        user_input = request.form["user_input"]
        bot_response = f"あなた: {user_input}"
        # 取得した値をresponseへ返す
        return render_template("index.html", response=bot_response)
    return render_template("index.html")


# アプリの起動
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()

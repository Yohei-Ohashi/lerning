import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template, request
from openai import OpenAI

# OpenAI API keyをこの.envに設定しておくこと!
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  # 読み込む.envファイルパスを指定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flaskアプリの作成
app = Flask(__name__)


# トップページへのアクセス設定 (ルートURLの定義)
@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = ""

    if request.method == "POST":
        # ユーザー入力
        user_input = request.form["user_input"]
        # OpenAIに質問を投げる
        response = client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": user_input}]
        )

        # AIの回答
        bot_response = response.choices[0].message.content

        # 取得した値をresponseへ返す
        return render_template(
            "index.html", user_input=user_input, response=bot_response
        )
    return render_template("index.html")


# アプリの起動
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()

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
chat_history = []


# トップページへのアクセス設定 (ルートURLの定義)
@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = ""

    if request.method == "POST":
        # ユーザー入力
        user_input = request.form["user_input"]
        # ユーザーの発言を履歴に追加
        chat_history.append({"role": "user", "content": user_input})
        
        # 履歴ごとOpenAIに質問を投げる
        response = client.chat.completions.create(
            model="gpt-4o", messages=chat_history
        )

        # AIの回答
        bot_response = response.choices[0].message.content
        # AIの回答も履歴に追加
        chat_history.append({"role": "assistant", "content": bot_response})

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

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 定数定義
TARGET_URL = "https://schoo.jp/"

# オプション設定（schooがヘッドレスモード検出してブロックしているっぽいのでヘッドレスモードはコメントアウト）
options = Options()
# options.add_argument("--headless")  # この行をコメントアウト
driver = webdriver.Chrome(options=options)
driver.get(TARGET_URL)

html = driver.page_source.encode("utf-8")
html_text = BeautifulSoup(html, "html.parser")

content_list = html_text.find_all("div", class_="classlistItem")
class_title1 = content_list[0].find("h3", class_="class_title").text
class_url1 = content_list[0].find("a").get("href")

# print(content_list)
print(class_title1)
print(class_url1)

driver.quit()  # ブラウザを閉じる

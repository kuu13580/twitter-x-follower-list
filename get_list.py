from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle, os
from time import sleep
from datetime import datetime
import sys

args = sys.argv
if len(args) != 2 and args[1] not in ["follow", "follower"]:
    print("Usage: python get_list.py <follow or follower>")
    exit(1)
target = args[1]

# 開始
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
input_wait = WebDriverWait(driver, 1000)
url_home = "https://twitter.com/home"

# クッキーがない場合はログイン
if not os.path.exists("cookies"):
    # ログイン
    url_login = "https://twitter.com/i/flow/login"
    driver.get(url_login)
    input_wait.until(EC.title_contains("ホーム"))
    # クッキーを保存
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("cookies", "wb"))
else:
    cookies = pickle.load(open("cookies", "rb"))
    driver.get(url_home)
    for cookie in cookies:
        driver.add_cookie(cookie)

driver.get(url_home)
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'プロフィール')))
element.click()
element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'フォロー中' if target == "follow" else "フォロワー")))
element.click()
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'フォロー中' if target == "follow" else "フォロワー")))
element.click()

account_dict = {}
if target == "follow":
    print("フォロー中のユーザーを取得中...")
if target == "follower":
    print("フォロワーを取得中...")
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    accounts = driver.find_element(By.XPATH, '//div[@aria-label="タイムライン: フォロー中"]' if target == "follow" else '//div[@aria-label="タイムライン: フォロワー"]')
    # 解析
    soup = BeautifulSoup(accounts.get_attribute("outerHTML"), "html.parser")
    accounts_containers = list(soup.select_one("div > div").children)
    end_flag = False
    if accounts_containers is None or len(accounts_containers) == 0:
        break
    for account_container in accounts_containers:
        try:
            inner_div = account_container.select_one('div[data-testid="UserCell"] > div > div:nth-of-type(2) > div > div > div')
            name = inner_div.select_one('div > div').get_text()
            id = inner_div.select_one('div > div:nth-of-type(2) > div').get_text()
            account_dict[id] = name
        except:
            end_flag = True
            break
    if end_flag:
        break
print("完了")

# ファイル出力
accounts = [f'{key} {value}' for key, value in account_dict.items()]
now_str = datetime.now().strftime("%Y%m%d_%H%M")
file_name = f"follow_list_{now_str}.txt" if target == "follow" else f"follower_list_{now_str}.txt"
with open(file_name, mode="w", encoding="utf-8") as f:
    f.write(f"フォロー数: {len(accounts)}\n" if target == "follow" else f"フォロワー数: {len(accounts)}\n")
    f.write("\n".join(accounts))
print(f"{file_name}に保存しました。")
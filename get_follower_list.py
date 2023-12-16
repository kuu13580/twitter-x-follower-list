from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle, os
from time import sleep
from datetime import datetime

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
element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'フォロワー')))
element.click()
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'フォロワー')))
element.click()

followers_dict = {}
print("フォロワーを取得中...")
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    follower_list = driver.find_element(By.XPATH, '//div[@aria-label="タイムライン: フォロワー"]')
    # 解析
    soup = BeautifulSoup(follower_list.get_attribute("outerHTML"), "html.parser")
    followers = list(soup.select_one("div > div").children)
    flag = False
    if followers is None or len(followers) == 0:
        break
    for follower in followers:
        try:
            inner_div = follower.select_one('div[data-testid="UserCell"] > div > div:nth-of-type(2) > div > div > div')
            name = inner_div.select_one('div > div').get_text()
            id = inner_div.select_one('div > div:nth-of-type(2) > div').get_text()
            followers_dict[id] = name
        except:
            flag = True
            break
    if flag:
        break
print("完了")

# フォロワー数
follower_list = [f'{key} {value}' for key, value in followers_dict.items()]
now_str = datetime.now().strftime("%Y%m%d_%H%M")
file_name = f"follower_list_{now_str}.txt"
with open(f"follower_list_{now_str}.txt", mode="w", encoding="utf-8") as f:
    f.write(f"フォロワー数: {len(follower_list)}\n")
    f.write("\n".join(follower_list))
print(f"{file_name}に保存しました。")
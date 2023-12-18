from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pickle, os
from datetime import datetime
import sys
from time import sleep

def get_list(target):
    # 現在のディレクトリを取得
    current_dir = current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # クッキーがない場合はログイン
    if not os.path.exists(f"{current_dir}/cookies"):
        # ログイン
        driver = webdriver.Chrome()
        input_wait = WebDriverWait(driver, 1000)
        url_login = "https://twitter.com/i/flow/login"
        driver.get(url_login)
        input_wait.until(EC.title_contains("ホーム"))
        # クッキーを保存
        cookies = driver.get_cookies()
        pickle.dump(cookies, open(f"{current_dir}/cookies", "wb"))
        driver.quit()

    # 開始
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument('window-size=1000,2000')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {'password_manager_enabled': False}
    })
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    url_home = "https://twitter.com/home"
    cookies = pickle.load(open(f"{current_dir}/cookies", "rb"))
    driver.get(url_home)
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get(url_home)
    # ログインページに遷移されたらキャッシュクリア
    if "ログイン" in driver.title:
        os.remove(f"{current_dir}/cookies")
        print("クッキーが無効です。再ログインしてください。")
        driver.quit()
        exit(1)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="プロフィール"]')))
    element.click()
    element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'フォロー中' if target == "follow" else "フォロワー")))
    shown_count = int(element.text.split(None, 1)[0])
    element.click()
    element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'フォロー中' if target == "follow" else "フォロワー")))
    element.click()

    account_dict = {}
    if target == "follow":
        print("フォロー中のユーザーを取得中...")
    if target == "follower":
        print("フォロワーを取得中...")
    buffer_count = 0
    prev_account = ""
    tmp_account = ""
    while True:
        col, _ = os.get_terminal_size()
        factor = 2 if col < 108 else 1
        progress = round(min(len(account_dict) / shown_count * 100 / factor, 100 / factor))
        print("\r", "0%|", "|" * progress, " " * int(100 / factor - progress), "|100%", end="", sep="")
        wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="progressbar"]')))
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
                tmp_account = id
            except:
                # 例外を5秒まで許容
                if buffer_count < 5:
                    sleep(1)
                    buffer_count += 1
                    continue
                inner_HTML = account_container.select_one('div[data-testid="cellInnerDiv"] > div > div')
                if not len(inner_HTML.contents):
                    end_flag = True
                    break
        # 末尾のアカウントが変更されたらリセット
        if prev_account != tmp_account:
            buffer_count = 0
        # 末尾のアカウントを記録
        prev_account = tmp_account
        if end_flag:
            break
        driver.execute_script('window.scrollBy(0, document.body.clientHeight);')
    print("\r", "0%|", "|" * int(100 / factor), "|100%", " 完了", sep="")

    # ファイル出力
    accounts = [f'{key} {value}' for key, value in account_dict.items()]
    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"{current_dir}/follow_list_{now_str}.txt" if target == "follow" else f"{current_dir}/follower_list_{now_str}.txt"
    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write(f"フォロー数: {len(accounts)}\n" if target == "follow" else f"フォロワー数: {len(accounts)}\n")
        f.write("\n".join(accounts))
    print(f"{file_name}に保存しました。")
    return file_name

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 and args[1] not in ["follow", "follower"]:
        print("Usage: python get_list.py <follow or follower>")
        exit(1)
    get_list(args[1])

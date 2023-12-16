from get_list import get_list
from diff_report import diff_report

def main():
    print("実行内容を選択")
    print("0. 終了")
    print("1. フォロワー一覧を取得")
    print("2. フォロー一覧を取得")
    print("3. 差分を表示")
    mode = int(input(">> "))
    if not mode in range(4):
        print("不正な入力です。")
        return
    if mode == 0:
        print("終了します。")
        exit(0)
    elif mode == 1:
        get_list("follower")
    elif mode == 2:
        get_list("follow")

if __name__ == "__main__":
    while True:
        main()
        print()
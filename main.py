from get_list import get_list
from diff_report import diff_report
from tkinter import filedialog
import argparse

def main():
    parser = argparse.ArgumentParser(description="Twitterのフォロー・フォロワー一覧を取得するスクリプト")
    parser.add_argument("--mode", "-m", type=int, help="実行内容を選択 1:フォロワー取得 2:フォロー取得 3:差分表示 0:終了")
    parser.add_argument("--files", "-f", type=str, help="比較するファイルのパスを指定", nargs=2, metavar=("previous_list_file", "new_list_file"))
    # 引数を解析
    args = parser.parse_args()

    if args.mode == 3 and args.files is None:
        print("ファイルを指定してください。")
        return

    if args.mode is not None:
        print("実行内容を選択")
        print("0. 終了")
        print("1. フォロワー一覧を取得")
        print("2. フォロー一覧を取得")
        print("3. 差分を表示")
        mode = int(input(">> "))
    else:
        mode = args.mode
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
    elif mode == 3:
        if args.files is not None:
            previous_list_file = args.files[0]
            new_list_file = args.files[1]
        else:
            typ = [('テキストファイル', '*.txt')]
            dir = './'
            print("比較元データを選択してください。")
            previous_list_file = filedialog.askopenfilename(title="比較元データを選択", filetypes = typ, initialdir = dir)
            print("比較先データを選択してください。")
            new_list_file = filedialog.askopenfilename(title="比較先データを選択", filetypes = typ, initialdir = dir)
        diff_report(previous_list_file, new_list_file)

if __name__ == "__main__":

    while True:
        main()
        print()
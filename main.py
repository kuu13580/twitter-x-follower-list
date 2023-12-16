from get_list import get_list
from diff_report import diff_report
from tkinter import filedialog
import argparse
import os
import sys

def mainGUI():
    
    print("実行内容を選択")
    print("0. 終了")
    print("1. フォロワー一覧を取得")
    print("2. フォロー一覧を取得")
    print("3. 差分を表示")
    print("4. 最新版を直近の結果と比較")
    mode = int(input(">> "))
    if not mode in range(5):
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
        typ = [('テキストファイル', '*.txt')]
        dir = './'
        print("比較元データを選択してください。")
        previous_list_file = filedialog.askopenfilename(title="比較元データを選択", filetypes = typ, initialdir = dir)
        print("比較先データを選択してください。")
        new_list_file = filedialog.askopenfilename(title="比較先データを選択", filetypes = typ, initialdir = dir)
        diff_report(previous_list_file, new_list_file)
    elif mode == 4:
        print("比較対象を選択してください。(follow or follower)")
        target = input(">> ")
        if target not in ["follow", "follower"]:
            print("不正な入力です。")
            return
        files = os.listdir()
        files = [file for file in files if file.startswith(target + "_") and file.endswith(".txt")]
        if len(files) == 0:
            print("ファイルが見つかりませんでした。")
            return
        files.sort()
        recent_file = files[-1]
        new_file = get_list(target)
        diff_report(recent_file, new_file)

def mainCLI(args):

    # 引数チェック
    if args.mode is None:
        print("実行内容を選択してください。")
        return
    mode = args.mode
    
    if mode == 0:
        print("終了します。")
        exit(0)
    elif mode == 1:
        get_list("follower")
    elif mode == 2:
        get_list("follow")
    elif mode == 3:
        if args.files is None:
            print("ファイルを指定してください。")
            return
        previous_list_file = args.files[0]
        new_list_file = args.files[1]
        diff_report(previous_list_file, new_list_file)
    elif mode == 4:
        if args.target is None:
            print("比較対象を指定してください。")
            return
        target = args.target
        files = os.listdir()
        files = [file for file in files if file.startswith(target + "_") and file.endswith(".txt")]
        if len(files) == 0:
            print("ファイルが見つかりませんでした。")
            return
        files.sort()
        recent_file = files[-1]
        new_file = get_list(target)
        diff_report(recent_file, new_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitterのフォロー・フォロワー一覧を取得するスクリプト")
    parser.add_argument("--mode", "-m", type=int, help="実行内容を選択 1:フォロワー取得 2:フォロー取得 3:差分表示 4:最新版比較 0:終了", choices=range(5))
    parser.add_argument("--files", "-f", type=str, help="比較するファイルのパスを指定", nargs=2, metavar=("previous_list_file", "new_list_file"))
    parser.add_argument("--target", "-t", type=str, help="最新版比較の対象指定", metavar=("follow or follower"), choices=["follow", "follower"])
    # 引数を解析
    args = parser.parse_args()
    print(len(sys.argv))
    # 引数がない場合はGUIで実行
    if len(sys.argv) == 1:
        while True:
            mainGUI()
            print()
    else:
        mainCLI(args)
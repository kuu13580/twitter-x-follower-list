import sys
import os

def diff_report(prev_list_path, new_list_path):
    # 現在のディレクトリを取得
    current_dir = current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # ファイルが存在しない場合は終了
    if os.path.exists(f"{current_dir}/{prev_list_path}"):
        prev_list_path = f"{current_dir}/{prev_list_path}"
    if os.path.exists(f"{current_dir}/{new_list_path}"):
        new_list_path = f"{current_dir}/{new_list_path}"
    if not os.path.exists(prev_list_path) or not os.path.exists(new_list_path):
        print("ファイルが見つかりませんでした。")
        exit(1)
    prev_count = 0
    new_count = 0

    prev_list = set()
    prev_map = {}
    new_list = set()
    new_map = {}

    with open(prev_list_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        prev_count = int(lines[0].split(None, 1)[1])
        for line in lines[1:]:
            prev_list.add(line.split(None, 1)[0])
            if len(line.split(None, 1)) == 1:
                prev_map[line.split(None, 1)[0]] = ""
            else:
                prev_map[line.split(None, 1)[0]] = line.split(None, 1)[1].strip()
                

    with open(new_list_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        new_count = int(lines[0].split(None, 1)[1])
        for line in lines[1:]:
            new_list.add(line.split(None, 1)[0])
            if len(line.split(None, 1)) == 1:
                new_map[line.split(None, 1)[0]] = ""
            else:
                new_map[line.split(None, 1)[0]] = line.split(None, 1)[1].strip()

    # 増減表示
    print()
    count_diff = new_count - prev_count
    if count_diff > 0:
        print(f"増減： \033[32m{count_diff}\033[0m")
    elif count_diff < 0:
        print(f"増減： \033[31m{count_diff}\033[0m")
    else:
        print(f"増減： {count_diff}")

    # 
    for id in new_list - prev_list:
        print(f"\033[32m+ {id} {new_map[id]}\033[0m")
    for id in prev_list - new_list:
        print(f"\033[31m- {id} {prev_map[id]}\033[0m")

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: python diff_report.py <prev_list_path> <new_list_path>")
        exit(1)
    if not os.path.exists(args[1]) or not os.path.exists(args[2]):
        print("File not found.")
        exit(1)

    prev_list_path = args[1]
    new_list_path = args[2]
    diff_report(prev_list_path, new_list_path)

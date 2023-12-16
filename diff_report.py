import sys
import os

args = sys.argv
if len(args) != 3:
    print("Usage: python diff_report.py <prev_list_path> <new_list_path>")
    exit(1)
if not os.path.exists(args[1]) or not os.path.exists(args[2]):
    print("File not found.")
    exit(1)

prev_list_path = args[1]
new_list_path = args[2]

prev_count = 0
new_count = 0

prev_list = set()
new_list = set()

with open(prev_list_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    prev_count = int(lines[0].split(None, 1)[1])
    for line in lines[1:]:
        prev_list.add(line.split(None, 1)[0])

with open(new_list_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    new_count = int(lines[0].split(None, 1)[1])
    for line in lines[1:]:
        new_list.add(line.split(None, 1)[0])

# 増減表示
count_diff = new_count - prev_count
if count_diff > 0:
    print(f"増減： \033[32m{count_diff}\033[0m")
elif count_diff < 0:
    print(f"増減： \033[31m{count_diff}\033[0m")
else:
    print(f"増減： {count_diff}")

# 
for id in new_list - prev_list:
    print(f"\033[32m+ {id}\033[0m")
for id in prev_list - new_list:
    print(f"\033[31m- {id}\033[0m")
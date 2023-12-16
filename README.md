# twitter-x-follower-list

![スクリーンショット 2023-12-16 230214](https://github.com/kuu13580/twitter-x-follower-list/assets/46004336/30ed71ef-7eda-4b83-8249-41e0cccecbfa)

X(旧Twitter)のAPIが有料化してフォロー管理ツールが軒並み有料化してしまったので、  
ローカルで見れるならそれを保存しちゃおうというツール。  

## 使い方
ダウンロードしたexeファイルを起動して処理内容を入力すると取得できます。  
(初回のみログインが必要です)  
cookieのファイルや出力ファイルが同ディレクトリに生成されるのでフォルダを作ってその中で起動を推奨。
![スクリーンショット 2023-12-16 230649](https://github.com/kuu13580/twitter-x-follower-list/assets/46004336/6d24c831-252a-4465-9fe0-2f76503a8c94)
  
差分表示はデータ選択が開くので、比較したい過去のデータと直近のデータを選択すると表示されます。

## コマンドラインから使用する
オプションは以下のとおりです
```
usage: follower_list_getter.exe [-h] [--mode {0,1,2,3,4}] [--files previous_list_file new_list_file] [--target follow or follower]

options:
  -h, --help            show this help message and exit
  --mode {0,1,2,3,4}, -m {0,1,2,3,4}
                        実行内容を選択 1:フォロワー取得 2:フォロー取得 3:差分表示 4:最新版比較 0:終了
  --files previous_list_file new_list_file, -f previous_list_file new_list_file
                        比較するファイルのパスを指定
  --target follow or follower, -t follow or follower
                        最新版比較の対象指定
```
### 例
差分を表示する
```
follower_list_getter.exe --mode 3 --files previous.txt new.txt
```
最新版と直近のフォロワーを比較する
```
follower_list_getter.exe --mode 4 --target follower
```

### ビルドメモ
```
pyinstaller pyinstaller.spec --clean -y
```

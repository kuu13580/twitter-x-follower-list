# twitter-x-follower-list

![スクリーンショット 2023-12-16 230214](https://github.com/kuu13580/twitter-x-follower-list/assets/46004336/30ed71ef-7eda-4b83-8249-41e0cccecbfa)

X(旧Twitter)のAPIが有料化してフォロー管理ツールが軒並み有料化してしまったので、  
ローカルで見れるならそれを保存しちゃおうというツール。  

# 使い方
ダウンロードしたexeファイルを起動して処理内容を入力すると取得できます。  
(初回のみログインが必要です)  
cookieのファイルや出力ファイルが同ディレクトリに生成されるのでフォルダを作ってその中で起動を推奨。
![スクリーンショット 2023-12-16 230649](https://github.com/kuu13580/twitter-x-follower-list/assets/46004336/6d24c831-252a-4465-9fe0-2f76503a8c94)
  
差分表示はデータ選択が開くので、比較したい過去のデータと直近のデータを選択すると表示されます。

### ビルドメモ
```
pyinstaller pyinstaller.spec --clean -y
```

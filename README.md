# ディレクトリ構成

## akochan-only  
うまくいかなかったやつ   
過去のREADMEやソースコードはこちらにあります

## mjai-reviewer   
akochanサーバ用ディレクトリ

## backend 
Webサーバのバックエンド処理用ディレクトリ

# mjai-reviewer  
## 前提事項 
Dockerインストール済み 
gitインストール済み 

## mjai-reviewer-flaskのコンテナをDockerで建てる手順
1. リポジトリ直下に移動する 
cd akochan-docker

2. mjai-reviewer ディレクトリに移動する 
cd mjai-reviewer

3. Docker イメージをビルドする 
docker build -f Dockerfile.flask -t mjai-reviewer-flask:latest . 

4. コンテナを実行する 
docker run --rm -d -p 8000:8000 --name mjai-reviewer-flask-test mjai-reviewer-flask:latest 

## 使い方 
### 直接curlする場合
- ローカルファイルを実行するとき(-i)
curl.exe -X POST "http://localhost:8000/report?seat=0&source_type=file" -F "file=@backend/source/test.json"  

- 天鳳IDを指定して実行するとき(-t)
使わなそうなので記載しません

- 天鳳URLを指定して実行するとき(-u)
curl.exe -X POST "http://localhost:8000/report?seat=0&source_type=url&url=https://tenhou.net/0/?log=2026071211gm-0009-0000-4888ed75&tw=1" -o report-a.html


### python版
backend 配下の callreport.pyに引数を設定して実行すると、プログラム内部でcurlコマンドを実行し、結果を取得します。
- `--file <path>`: ローカルJSONを multipart 形式で送信
- `--json <path>`: JSON ボディとして送信
- `--url <url>`: 天鳳のログ URL を送信
- `--seat <0-3>`: 自家の番号。デフォルトは `0`
- `--endpoint <url>`: API の URL。デフォルトは `http://localhost:8000/report`


- 天鳳のログ URL を指定する 
python callreport.py --url "https://tenhou.net/0/?log=2026070520gm-0009-0000-44bf82d0&tw=2" --seat 2

- JSON ファイルをボディとして送る 
python callreport.py --json ../mjai-reviewer/test.json --seat 0 

出力は `backend/result` 配下に `url-YYYYMMDD-HHMMSS.html` などの自動生成名で保存されます。




# 過去のDocker実行例 (解析処理をローカルで実行するとき：現在は不可能)
- どっかの天鳳から持ってくるやつ 
docker run --rm mjai-reviewer:latest -e akochan --no-open -t 2019050417gm-0029-0000-4f2a8622 -a 3 -o - > report.html

- MortalのJSONからとってきたやつ 
docker run --rm mjai-reviewer:latest -e akochan --no-open -i test.json -a 0 -o - > report.html

- 天鵬のログURLからとってくるやつ 
docker run --rm mjai-reviewer:latest -e akochan --no-open -u "https://tenhou.net/0/?log=2026070520gm-0009-0000-44bf82d0&tw=2" -a 2 -o - > report.html
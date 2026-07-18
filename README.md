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

## mjai-reviewer-flask Docker を建てる手順
1. リポジトリ直下に移動する
cd akochan-docker

2. mjai-reviewer ディレクトリに移動する
cd mjai-reviewer

3. Docker イメージをビルドする
docker build -f Dockerfile.flask -t mjai-reviewer-flask:latest . 

4. コンテナを実行する
docker run --rm -d -p 8000:8000 --name mjai-reviewer-flask-test mjai-reviewer-flask:latest 


## HTTP API版
### 使い方
Flask サーバを起動したうえで、backend 配下の callreport.py から呼び出せます。

- `--file <path>`: ローカルJSONを multipart 形式で送信
- `--json <path>`: JSON ボディとして送信
- `--url <url>`: 天鳳のログ URL を送信
- `--seat <0-3>`: 自家の番号。デフォルトは `0`
- `--endpoint <url>`: API の URL。デフォルトは `http://localhost:8000/report`



### 実行例(REST APIで呼び出すとき：推奨)
- 天鳳のログ URL を指定する
python callreport.py --url "https://tenhou.net/0/?log=2026070520gm-0009-0000-44bf82d0&tw=2" --seat 2

- ローカル JSON を送る
python callreport.py --file ../mjai-reviewer/test.json --seat 0

- JSON ファイルをボディとして送る
python callreport.py --json ../mjai-reviewer/test.json --seat 0

出力は `backend/result` 配下に `url-YYYYMMDD-HHMMSS.html` などの自動生成名で保存されます。

### 実行例 (解析処理をローカルで実行するとき：非推奨)
- どっかの天鳳から持ってくるやつ
docker run --rm mjai-reviewer-flask:latest -e akochan --no-open -t 2019050417gm-0029-0000-4f2a8622 -a 3 -o - > report.html

- MortalのJSONからとってきたやつ
docker run --rm mjai-reviewer-flask:latest -e akochan --no-open -i test.json -a 0 -o - > report.html

- 天鵬のログURLからとってくるやつ
docker run --rm mjai-reviewer-flask:latest -e akochan --no-open -u "https://tenhou.net/0/?log=2026070520gm-0009-0000-44bf82d0&tw=2" -a 2 -o - > report1.html
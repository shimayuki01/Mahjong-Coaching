

## 前提事項
Dockerインストール済み
gitインストール済み

## 手順

1. Dockerfileがあるディレクトリに移動

//コンテナ立ち上げ
2. docker compose up --build --force-recreate -d

//コンテナ内のbashに入る
3. docker exec -it akochan /bin/bash

//実行
4. .system 〇〇 

### 例（stats取れる）
./system.exe stats ./match_result

### 備考
*雀魂のURLはこのままじゃまだ無理っぽい
*天鳳の牌譜もまだ取れなそう。mjai形式ってやつにしないといけない？（AIに聞いた）
*変換出来たら.system <ファイル名>でいけそう？

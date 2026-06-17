

## 前提事項
Dockerインストール済み
gitインストール済み

## 手順

1. Dockerfileがあるディレクトリに移動

2. コンテナ立ち上げ  
docker compose up --build --force-recreate -d

3. コンテナ内のbashに入る  
docker exec -it akochan /bin/bash


4. 実行  
.system 〇〇 

### 実行例（stats取れる）  

./system.exe stats ./match_result

## 備考  
- 雀魂のURLはこのままじゃまだ無理っぽい  
- 天鳳の牌譜もまだ取れなそう。mjai形式ってやつにしないといけない？（AIに聞いた）
- 変換出来たら.system <ファイル名>でいけそう？



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

### 実行例

- Statsとるやつ  
./system.exe stats ./match_result

- 多分実行したいコマンド
system.exe full_analyze <ファイル名> <自家の番号>  

<ファイル名>：mjai JSON  
<自家の番号>： （東家=0、南家=1、西家=2、北家=3）  


## 備考  
- 雀魂のURLはこのままじゃまだ無理っぽい  
- 天鳳の牌譜もまだ取れなそう。mjai形式ってやつにしないといけない？（AIに聞いた）
- 変換出来たら.system <ファイル名>でいけそう？

##  トラブルシューティング備忘録(石原)

### ① ~/.docker/config.json から "credsStore": "desktop" を削除
* **効果：** M1/M2/M3などのMac環境において、Docker Desktop固有の認証管理ツール（docker-credential-desktop）のパスが見つからずにビルドが異常終了するエラーを回避します。

### ② docker logout の実行
* **効果：** ローカルにキャッシュされた古い認証情報や、不整合を起こしているログイン状態を強制的にクリアします。これにより、パブリックイメージ（ubuntuなど）の取得時に不要な認証エラーが発生するのを防ぎます。

### ③ DockerにIntel環境（linux/amd64）をエミュレートさせる
* **具体的な設定方法：** プロジェクトのルートにある **`docker-compose.yaml`** を開き、対象となるサービス（例: `app`）の中に `platform: linux/amd64` の行を追加します。
* **効果：** Apple Silicon（ARM64）環境ではサポートされていないコンパイルオプション（-mcmodel=medium など）を含むLinux向けソースコードを、コードを変更することなくそのままビルド・実行可能にします。

### ④ Dockerfile の COPY コマンドを `COPY . /app` に統一
* **効果：** サブモジュール（akochanなど）のロード状況によって、コンテナビルド時に「ファイルが見つからない」というエラーが発生するのを防ぎます。Mac側のフォルダ構造をそのまま100%コンテナ内に再現することで、環境によるパスのズレやビルド失敗を確実に回避します。

##  トラブルシューティング備忘録(大脇)
### ② コンフリクト発生時
* **効果：** リモートリポジトリとローカルリポジトリの競合を解消して正常にgit更新できます
git stash -u  
git fetch origin  
git log --oneline HEAD..origin/master  
git pull --rebase origin master  
git add .  
git rebase --continue  
git push -u origin master  
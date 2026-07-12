## フォルダ構成

### akochan-only  
うまくいかなかったやつ  
過去のREADMEやソースコードはこちらにあります

### mjai-reviewer  
うまくいったやつ  
mjai-reviewerからakochan呼び出す必要あった

## 前提事項
Dockerインストール済み
gitインストール済み

## 手順(mjai-reviewer)  
1. mjai-reviewerへディレクトリ移動  
cd mjai-reviewer

2. ビルドする  
docker build -t mjai-reviewer:latest .

3. 実行する  
docker run -rm mjai-reviewer:latest -e akochan --no-open -<牌譜のオプション> <牌譜> -a <自家の引数> -o - > report.html  

- <牌譜のオプション>
  - i:ローカルのJSONファイル
  - t:天鳳のログファイル
  - u:天鳳のログURL

- <牌譜> 
  - オプションに応じて選択
- <自家の引数>
  - 東家=0、南家=1、西家=2、北家=3

### 実行例  
- どっかの天鳳から持ってくるやつ  
docker run --rm mjai-reviewer:latest -e akochan --no-open -t 2019050417gm-0029-0000-4f2a8622 -a 3 -o - > report.html  

- MortalのJSONからとってきたやつ  
docker run --rm mjai-reviewer:latest -e akochan --no-open -i test.json -a 0 -o - > report.html

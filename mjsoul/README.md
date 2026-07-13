# Mahjong Soul 牌譜 JSON 取得ツール

このスクリプトは、雀魂の牌譜 URL から牌譜 JSON を取得します。

## 必要要件

- Python 3.8+
- Playwright

## インストール

```bash
pip install playwright
python -m playwright install
```

> PowerShell で `playwright` コマンドが見つからない場合は、`python -m playwright install` を使ってください。

## 使い方

```bash
python mjsoul.py "<replay_url>" -o replay.json
```

### オプション

- `<replay_url>`: 雀魂の牌譜 URL
- `-o, --output`: 出力 JSON ファイルパス（デフォルト: `mjsoul.json`）
- `--browser`: Playwright のブラウザ種類 (`chromium`, `firefox`, `webkit`)
- `--headless`: ヘッドレスモードで実行
- `--wait`: ページ読み込みと JSON 取得の待機時間上限（秒、デフォルト: `30`）
- `--manual-login`: ブラウザを開いて手動ログイン後に取得

## 例

```bash
python mjsoul.py "https://example.com/replay/12345" -o mjsoul.json
```

ログインが必要な場合や、ページ上にすぐ JSON が見えない場合は次のように実行します。

```bash
python mjsoul.py "https://example.com/replay/12345" --manual-login -o mjsoul.json
```

## 注意事項

- 雀魂では認証が必要な場合があり、URL だけでは直接 JSON が取得できないことがあります。
- 自動取得に失敗した場合は、`--manual-login` で手動ログインしてから再度実行してください。

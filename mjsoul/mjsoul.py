#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    # コマンドライン引数を解析する
    parser = argparse.ArgumentParser(
        description="Download Mahjong Soul replay JSON from a Mahjong Soul replay URL."
    )
    parser.add_argument("url", help="Mahjong Soul replay URL")
    parser.add_argument(
        "-o",
        "--output",
        default="mjsoul.json",
        help="Output path for the saved JSON file (default: mjsoul.json)",
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Playwright browser type to use.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode.",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=30,
        help="Maximum seconds to wait for the replay page to load and JSON to be captured.",
    )
    parser.add_argument(
        "--manual-login",
        action="store_true",
        help="Open browser and allow manual login before downloading JSON.",
    )
    return parser.parse_args()


def save_json(output_path: Path, data: str) -> None:
    # JSON データを指定されたファイルに保存する
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(data, encoding="utf-8")
    print(f"Saved JSON to: {output_path}")


def score_json_text(text: str) -> int:
    # 再生データに見える JSON かどうかをスコアリングする
    lower = text.lower()
    if "privacy_agreement" in lower or "隐私政策" in lower or "privacy policy" in lower:
        return -1000

    score = 0
    for token in [
        "replay",
        "hand",
        "discard",
        "draw",
        "player",
        "game",
        "round",
        "seat",
        "dora",
        "wind",
        "action",
        "tiles",
        "score",
    ]:
        if token in lower:
            score += 1

    # JSON の長さにも少しだけ重みを与える
    score += min(len(text) // 2000, 5)
    return score


def choose_json_candidate(candidates: list[tuple[str, str]]) -> str | None:
    # 候補 JSON から最も再生データらしいものを選択する
    if not candidates:
        return None
    scored = []
    for url, text in candidates:
        score = score_json_text(text)
        scored.append((score, len(text), url, text))

    scored = [item for item in scored if item[0] >= 0]
    if not scored:
        return None

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best_score, best_len, best_url, best_text = scored[0]
    print(f"Selected JSON candidate from {best_url} with score={best_score} length={best_len}")
    return best_text


def find_json_in_html(html: str) -> str | None:
    # HTML 内に埋め込まれた JSON を探す
    patterns = [
        r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});",
        r"window\.__DATA__\s*=\s*(\{.*?\});",
        r"window\.REPLAY_DATA\s*=\s*(\{.*?\});",
        r"var\s+replayData\s*=\s*(\{.*?\});",
        r"window\[\"__INITIAL_STATE__\"\]\s*=\s*(\{.*?\});",
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.S)
        if match:
            text = match.group(1)
            try:
                json.loads(text)
                return text
            except json.JSONDecodeError:
                pass
    return None


def extract_global_json(page) -> str | None:
    # ページの global window から JSON データを取り出す
    names = [
        "__INITIAL_STATE__",
        "__DATA__",
        "REPLAY_DATA",
        "replayData",
        "__PLAYBACK__",
        "__REPLAYER__",
    ]
    for name in names:
        try:
            text = page.evaluate(f"() => {{ const v = window['{name}']; return v ? JSON.stringify(v) : null; }}")
        except Exception:
            continue
        if not text:
            continue
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            continue
    return None


def download_mjsoul_json(
    url: str,
    output_path: Path,
    browser: str,
    headless: bool,
    wait: int,
    manual_login: bool,
) -> int:
    # Playwright を使ってページを開き、JSON を取得する
    try:
        from playwright.sync_api import Error, TimeoutError, sync_playwright
    except ImportError:
        print(
            "Error: playwright is not installed. Install it with `pip install playwright` and run `playwright install`.",
            file=sys.stderr,
        )
        return 1

    with sync_playwright() as pw:
        browser_impl = getattr(pw, browser)
        browser_obj = browser_impl.launch(headless=headless)
        context = browser_obj.new_context()
        page = context.new_page()

        json_candidates: list[tuple[str, str]] = []

        def handle_response(response) -> None:
            # レスポンスのうち、JSON と見なせるものを候補に追加する
            try:
                content_type = response.headers.get("content-type", "")
                if "application/json" not in content_type:
                    return
                if response.status != 200:
                    return
                text = response.text()
                if not text:
                    return
                try:
                    json.loads(text)
                except json.JSONDecodeError:
                    return
                json_candidates.append((response.url, text))
            except Exception:
                return

        page.on("response", handle_response)

        try:
            page.goto(url, wait_until="networkidle", timeout=wait * 1000)
        except TimeoutError:
            print("Warning: page navigation timed out, continuing with partial content.")

        if manual_login:
            # 手動ログインモード: ユーザーがブラウザでログインするのを待つ
            print(
                "Manual login mode: please complete login in the opened browser window, then press Enter to continue..."
            )
            input()

        page.wait_for_timeout(2000)

        try:
            # ページのショートカットキー S で JSON をダウンロードできる場合に対応
            with page.expect_download(timeout=wait * 1000) as download_info:
                page.keyboard.press("S")
            download = download_info.value
            download_path = output_path
            download.save_as(str(download_path))
            print(f"Downloaded replay JSON via page shortcut S: {download_path}")
            browser_obj.close()
            return 0
        except TimeoutError:
            pass
        except Error as exc:
            print(f"Download shortcut failed: {exc}")

        page.wait_for_timeout(2000)
        html = page.content()
        json_text = find_json_in_html(html)
        if json_text:
            # HTML に埋め込まれた JSON を見つけた場合は保存する
            save_json(output_path, json_text)
            browser_obj.close()
            return 0

        json_text = extract_global_json(page)
        if json_text:
            save_json(output_path, json_text)
            browser_obj.close()
            return 0

        json_text = choose_json_candidate(json_candidates)
        if json_text:
            # ネットワークレスポンスから適切な JSON を選んで保存する
            save_json(output_path, json_text)
            browser_obj.close()
            return 0

        print(
            "Failed to capture JSON automatically. "
            "If the page requires login, rerun with --manual-login. "
            "If the shorthand download does not work, open the URL in your browser and inspect network traffic for JSON responses."
        )
        browser_obj.close()
        return 2


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    return download_mjsoul_json(
        args.url,
        output_path,
        browser=args.browser,
        headless=args.headless,
        wait=args.wait,
        manual_login=args.manual_login,
    )


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import json
import re
import sys
import time
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

AI_BOTS = [
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "Google-Extended",
    "ClaudeBot",
    "PerplexityBot",
    "anthropic-ai",
    "cohere-ai",
    "meta-externalagent",
    "Bytespider",
    "Applebot-Extended",
]


def fetch(url: str, timeout: int = 20):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    start = time.time()
    with urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="ignore")
        code = r.getcode()
        headers = dict(r.getheaders())
    return code, headers, body, time.time() - start


def text_content(html: str) -> str:
    no_script = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    no_style = re.sub(r"<style[\s\S]*?</style>", " ", no_script, flags=re.I)
    stripped = re.sub(r"<[^>]+>", " ", no_style)
    stripped = re.sub(r"\s+", " ", stripped)
    return stripped.strip()


def check_robots(base_url: str):
    robots_url = urljoin(base_url, "/robots.txt")
    result = {"url": robots_url, "found": False, "bot_status": {}}
    try:
        code, _, body, _ = fetch(robots_url)
        if code == 200:
            result["found"] = True
            for bot in AI_BOTS:
                # naive parse: blocked if explicit disallow under matching user-agent line
                blocked = False
                pattern = rf"User-agent:\s*{re.escape(bot)}[\s\S]*?(?=User-agent:|$)"
                m = re.search(pattern, body, flags=re.I)
                if m and re.search(r"Disallow:\s*/", m.group(0), flags=re.I):
                    blocked = True
                result["bot_status"][bot] = "Blocked" if blocked else "Allowed"
    except Exception as e:
        result["error"] = str(e)
    return result


def extract_schema_types(html: str):
    types = []
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>', html, flags=re.I):
        content = m.group(1)
        found = re.findall(r'"@type"\s*:\s*"([^"]+)"', content)
        types.extend(found)
    return sorted(set(types))


def run(base_url: str):
    out = {"base_url": base_url}
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    code, headers, html, load_s = fetch(base_url)
    txt = text_content(html)

    out["homepage"] = {
        "status": code,
        "https": base_url.startswith("https://"),
        "load_seconds": round(load_s, 3),
        "meta_description_length": len(re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, flags=re.I).group(1)) if re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, flags=re.I) else 0,
        "has_h1": bool(re.search(r"<h1[^>]*>.*?</h1>", html, flags=re.I | re.S)),
        "word_count": len(re.findall(r"\b\w+\b", txt)),
        "question_h2_count": len(re.findall(r"<h2[^>]*>[^<]*\?[^<]*</h2>", html, flags=re.I)),
        "has_list": bool(re.search(r"<(ul|ol)[^>]*>", html, flags=re.I)),
        "has_table": bool(re.search(r"<table[^>]*>", html, flags=re.I)),
        "has_noscript": "<noscript" in html.lower(),
        "has_video": bool(re.search(r"<(video|iframe)[^>]*>", html, flags=re.I)),
        "has_images": bool(re.search(r"<img[^>]*>", html, flags=re.I)),
        "schema_types": extract_schema_types(html),
    }

    out["robots"] = check_robots(base_url)

    for p in ["/sitemap.xml", "/llms.txt"]:
        url = urljoin(base_url, p)
        try:
            c, _, b, _ = fetch(url)
            out[p.strip("/")] = {"found": c == 200, "size": len(b)}
        except Exception as e:
            out[p.strip("/")] = {"found": False, "error": str(e)}

    must_have_schema = ["Organization", "FAQPage", "Person", "BreadcrumbList"]
    have = set(out["homepage"]["schema_types"])
    out["gaps"] = {
        "missing_schema": [s for s in must_have_schema if s not in have],
        "content_js_risk": out["homepage"]["word_count"] < 250,
        "missing_h1": not out["homepage"]["has_h1"],
        "thin_content": out["homepage"]["word_count"] < 1200,
        "missing_question_h2": out["homepage"]["question_h2_count"] == 0,
    }

    return out


def main():
    ap = argparse.ArgumentParser(description="AI visibility quick auditor")
    ap.add_argument("url", help="Base URL, e.g. https://daisy.sg")
    ap.add_argument("--markdown", action="store_true", help="Print markdown summary")
    args = ap.parse_args()

    result = run(args.url)
    if not args.markdown:
        print(json.dumps(result, indent=2))
        return

    h = result["homepage"]
    print(f"# AI Visibility Audit — {result['base_url']}")
    print(f"\n- Load time: {h['load_seconds']}s")
    print(f"- HTTPS: {'Yes' if h['https'] else 'No'}")
    print(f"- Word count (raw HTML): {h['word_count']}")
    print(f"- H1 present: {'Yes' if h['has_h1'] else 'No'}")
    print(f"- llms.txt: {'Found' if result['llms.txt'].get('found') else 'Missing'}")
    print(f"- sitemap.xml: {'Found' if result['sitemap.xml'].get('found') else 'Missing'}")
    print("\n## Schema types found")
    for t in h["schema_types"]:
        print(f"- {t}")
    print("\n## Missing high-impact schema")
    for s in result["gaps"]["missing_schema"]:
        print(f"- {s}")
    print("\n## Bot access snapshot")
    for k, v in result["robots"].get("bot_status", {}).items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

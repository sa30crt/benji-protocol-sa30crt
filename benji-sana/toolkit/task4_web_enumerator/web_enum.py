import argparse
import sys

import requests
from bs4 import BeautifulSoup, Comment

SENSITIVE_PATHS = [
    "/robots.txt",
    "/admin",
    "/phpmyadmin",
    "/login",
    "/.git",
]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Web enumerator")
    parser.add_argument("url", help="Target URL")
    return parser.parse_args()


def analyse_headers(url: str):
    response = requests.get(url, timeout=5)

    headers = {
        "Server": response.headers.get("Server", "Not disclosed"),
        "X-Powered-By": response.headers.get("X-Powered-By", "Not disclosed"),
    }

    return headers, response.text


def extract_comments(html: str):
    soup = BeautifulSoup(html, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    return [c.strip() for c in comments]


def check_sensitive_paths(base_url: str):
    results = []

    for path in SENSITIVE_PATHS:
        url = base_url.rstrip("/") + path

        try:
            resp = requests.get(url, timeout=5, allow_redirects=False)
            code = resp.status_code

            if code == 200:
                status = "FOUND"
            elif code == 404:
                status = "NOT FOUND"
            elif code == 403:
                status = "FORBIDDEN"
            elif code in (301, 302):
                status = "REDIRECT"
            else:
                status = f"HTTP {code}"

            results.append((path, status, code))

        except requests.exceptions.RequestException:
            results.append((path, "ERROR", None))

    return results


def main():
    args = parse_arguments()

    try:
        headers, html = analyse_headers(args.url)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not connect: {e}", file=sys.stderr)
        sys.exit(1)

    comments = extract_comments(html)
    paths = check_sensitive_paths(args.url)

    # ---------------- OUTPUT (STRICT FORMAT) ----------------

    print("[HEADERS]")
    print(f"Server: {headers['Server']}")
    print(f"X-Powered-By: {headers['X-Powered-By']}")

    print("\n[COMMENTS]")
    if comments:
        for c in comments:
            print(c)
    else:
        print("No comments found.")

    print("\n[SENSITIVE PATHS]")
    for path, status, code in paths:
        print(f"{path} — {status} ({code})")


if __name__ == "__main__":
    main()

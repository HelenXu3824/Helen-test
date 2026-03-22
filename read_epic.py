#!/usr/bin/env python3
"""
Read the PO Work Order md file and the Epic feature description from Jira.
If the Epic is not accessible, exit and explain the reason.

Optional environment variable:
  JIRA_TOKEN – Personal Access Token (PAT) for the Jira instance.
               When provided, it is sent as a Bearer token so that
               authenticated Epics can be fetched without a browser session.
"""

import base64
import os
import sys
import urllib.error
import urllib.request

PO_MD_FILE = "Engineering AI Work Order-PO.md"
EPIC_URL = "https://eaton-corp.atlassian.net/browse/BDCSPM-8379"

# Maximum number of characters to display from the raw Jira page.
# Jira returns a full HTML document; we show only a leading preview so that
# the output stays readable in a terminal.
HTML_PREVIEW_LENGTH = 2000


def read_po_md(path: str) -> str:
    """Read and return the content of the PO Work Order md file."""
    if not os.path.isfile(path):
        print(f"[ERROR] PO md file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def fetch_epic_page(url: str) -> str:
    """
    Attempt to fetch the Epic page from Jira and return a preview of the HTML.
    Exits with a human-readable explanation if the page is not accessible.

    If the JIRA_TOKEN environment variable is set, the token is included as a
    Bearer authorization header to allow access to authenticated Jira instances.
    """
    headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}

    jira_token = os.environ.get("JIRA_TOKEN", "").strip()
    if jira_token:
        headers["Authorization"] = f"Bearer {jira_token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")
        return html[:HTML_PREVIEW_LENGTH]
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            reason = (
                f"HTTP 401 Unauthorized – The Jira instance at {url} requires "
                "authentication. Set the JIRA_TOKEN environment variable to a "
                "valid Personal Access Token and retry."
            )
        elif exc.code == 403:
            reason = (
                f"HTTP 403 Forbidden – Access to {url} is denied. "
                "Your account may not have permission to view this Epic."
            )
        elif exc.code == 404:
            reason = (
                f"HTTP 404 Not Found – The Epic at {url} does not exist or "
                "has been deleted."
            )
        else:
            reason = f"HTTP {exc.code} error while fetching {url}: {exc.reason}"
        print(
            f"[ERROR] Unable to read Epic feature description.\nReason: {reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except TimeoutError:
        reason = (
            f"Connection to {url} timed out. "
            "The Jira instance may be slow or unreachable from this environment."
        )
        print(
            f"[ERROR] Unable to read Epic feature description.\nReason: {reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as exc:
        reason = (
            f"Network error while connecting to {url}: {exc.reason}. "
            "The Jira instance may not be reachable from this environment "
            "(e.g., it is behind a corporate VPN or firewall), or the URL "
            "is incorrect."
        )
        print(
            f"[ERROR] Unable to read Epic feature description.\nReason: {reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as exc:
        reason = f"OS-level error while fetching {url}: {exc}"
        print(
            f"[ERROR] Unable to read Epic feature description.\nReason: {reason}",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    # Resolve paths relative to the script's own directory so the script
    # works from any working directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    po_md_path = os.path.join(script_dir, PO_MD_FILE)

    # Step 1: Read the PO Work Order md file
    print("=" * 60)
    print(f"Reading PO Work Order: {po_md_path}")
    print("=" * 60)
    po_content = read_po_md(po_md_path)
    print(po_content)

    # Step 2: Fetch the Epic feature description
    print()
    print("=" * 60)
    print(f"Fetching Epic feature description from: {EPIC_URL}")
    print("=" * 60)
    epic_content = fetch_epic_page(EPIC_URL)
    print(epic_content)


if __name__ == "__main__":
    main()

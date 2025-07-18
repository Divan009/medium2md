#!/usr/bin/env python3
"""

Download a public Medium article and save it as Markdown.

Usage:
    python medium2md.py <medium-url>  [--out out_dir]

Notes:
* Respects Medium TOS.  Works only for fully public, paywall-free posts.
* Uses `markdownify` for HTML → Markdown conversion.
"""

from __future__ import annotations

import re
import argparse
import pathlib
from dataclasses import dataclass
from typing import Tuple

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


ARTICLE_NOT_FOUND_MSG = "Unable to locate <article> section on the page."


@dataclass
class MediumToMarkdownConverter:
    """
    A tiny utility to convert public Medium articles to Markdown.
    """

    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0 Safari/537.36"
    )
    session: requests.Session = requests.Session()

    def __post_init__(self) -> None:
        self.session.headers.update({"User-Agent": self.user_agent})

    # ---------- public API -------------------------------------------------

    def convert_from_url(self, url: str) -> Tuple[str, str]:
        """
        Fetch a Medium post and return (title, markdown_body).
        Raises `RuntimeError` if the <article> tag cannot be found.
        """
        html = self._download(url)
        soup = BeautifulSoup(html, "html.parser")

        article_tag = soup.find("article")
        if article_tag is None:
            raise RuntimeError(ARTICLE_NOT_FOUND_MSG)

        # Convert to Markdown and post-process.
        markdown = self._to_markdown(article_tag, base=url)
        title = self._extract_title(markdown)
        markdown = self._clean_markdown(markdown)

        return title, markdown

    # ---------- internal helpers -------------------------------------------

    def _download(self, url: str) -> str:
        """Download raw HTML, raising for HTTP errors."""
        resp = self.session.get(url, timeout=20)
        resp.raise_for_status()
        return resp.text

    def _to_markdown(self, tag, *, base: str) -> str:
        """HTML → Markdown via markdownify; make image/video URLs absolute."""
        # First convert any <img src> / <a href> that are relative.
        for el in tag.find_all(["img", "a"]):
            attr = "src" if el.name == "img" else "href"
            if el.has_attr(attr):
                el[attr] = urljoin(base, el[attr])

        return md(str(tag), heading_style="ATX")

    @staticmethod
    def _extract_title(markdown: str) -> str:
        """Assume the very first ATX heading is the title."""
        first_line = markdown.lstrip().splitlines()[0]
        return re.sub(r"^#+\s*", "", first_line).strip()

    @staticmethod
    def _clean_markdown(markdown: str) -> str:
        """
        Strip Medium-specific cruft:

        * 'Published in …' lines
        * 'Listen', 'Share', 'Sign in' prompts
        * Empty reference-style link leftovers
        """
        cleaned_lines: list[str] = []
        for line in markdown.splitlines():
            # Skip embedded sign-in / image proxies.
            if any(u in line for u in ("miro.medium.com", "medium.com/m/signin")):
                continue
            # Skip common Medium template phrases.
            if re.search(r"Published in|Listen|Share", line):
                continue
            # Skip blank reference links like "[ ]"
            if re.fullmatch(r"\[\s*]", line):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip() + "\n"


def slugify(text: str, maxlen: int = 60) -> str:
    """
    Turn 'Back-end Web Framework: Flask (Part-2: Routing & URL Binding)'
    into 'back-end-web-framework-flask-part-2-routing-url-binding'.
    """
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    slug = re.sub(r"[-\s]+", "-", text)
    return slug[:maxlen] or "medium-post"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a Medium article and save as Markdown."
    )
    parser.add_argument("url", help="Medium article URL")
    parser.add_argument(
        "-o", "--out", default="md_files",
        help="Output directory (default: md_files)"
    )
    args = parser.parse_args()

    converter = MediumToMarkdownConverter()
    title, markdown_text = converter.convert_from_url(args.url)

    out_dir = pathlib.Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)  # ensure folder

    safe_name = slugify(title) + ".md"  # safe filename
    outfile = out_dir / safe_name
    outfile.write_text(markdown_text, encoding="utf-8")  # write file

    print(f"✓ Saved '{title}' → {outfile}")

if __name__ == "__main__":
    main()

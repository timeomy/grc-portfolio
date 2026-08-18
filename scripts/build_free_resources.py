#!/usr/bin/env python3
"""Build downloadable versions of the free resources.

Converts free/*.md into:
  - styled standalone HTML (print-friendly)
  - .docx via macOS textutil (resume template + policy pack)

Run from the repo root:  python3 scripts/build_free_resources.py
"""

import pathlib
import subprocess
import sys

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
FREE = ROOT / "free"

DOC_CSS = """
  body { font-family: -apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
         max-width: 760px; margin: 0 auto; padding: 48px 28px; color: #1a1a1a;
         line-height: 1.6; font-size: 15px; }
  h1 { font-size: 26px; line-height: 1.25; margin: 0 0 6px; }
  h2 { font-size: 19px; margin: 30px 0 10px; border-bottom: 2px solid #b8860b;
       padding-bottom: 4px; }
  h3 { font-size: 16px; margin: 22px 0 8px; }
  hr { border: none; border-top: 1px solid #ddd; margin: 26px 0; }
  li { margin-bottom: 5px; }
  table { border-collapse: collapse; width: 100%; margin: 14px 0; }
  th, td { border: 1px solid #ccc; padding: 7px 10px; text-align: left;
           font-size: 14px; }
  th { background: #faf6ec; }
  code { background: #f4f4f4; padding: 1px 5px; border-radius: 3px;
         font-size: 13px; }
  blockquote { border-left: 3px solid #b8860b; margin: 14px 0; padding: 4px 16px;
               color: #555; }
  .doc-footer { margin-top: 44px; padding-top: 14px; border-top: 1px solid #ddd;
                font-size: 12.5px; color: #888; }
  .doc-footer a { color: #b8860b; }
  @media print { body { padding: 0; } .doc-footer { display: none; } }
"""

FOOTER = (
    '<p class="doc-footer">Free resource from '
    '<a href="https://zabez.com/">ZABEZ.com</a> — independent GRC analyses '
    'of the world’s largest enterprises. Share freely; please keep this line.</p>'
)

RESOURCES = [
    # (source md, docx output wanted, page title)
    ("grc-resume-template.md", True, "GRC Resume Template — ZABEZ.com"),
    ("starter-policy-pack.md", True, "Starter Policy Pack — ZABEZ.com"),
    ("what-is-grc.md", False, "What Is GRC? A Plain-Language Guide — ZABEZ.com"),
]


def build_html(md_path: pathlib.Path, title: str) -> pathlib.Path:
    body = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "sane_lists"],
    )
    html = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        f"<title>{title}</title>\n"
        "<meta name=\"robots\" content=\"noindex\">\n"
        f"<style>{DOC_CSS}</style>\n</head>\n<body>\n"
        f"{body}\n{FOOTER}\n</body>\n</html>\n"
    )
    out = md_path.with_suffix(".html")
    out.write_text(html, encoding="utf-8")
    return out


def build_docx(html_path: pathlib.Path) -> None:
    result = subprocess.run(
        ["textutil", "-convert", "docx", str(html_path), "-output",
         str(html_path.with_suffix(".docx"))],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"textutil failed for {html_path.name}: {result.stderr}")


def main() -> None:
    for name, wants_docx, title in RESOURCES:
        md_path = FREE / name
        if not md_path.exists():
            sys.exit(f"Missing source file: {md_path}")
        html_path = build_html(md_path, title)
        if wants_docx:
            build_docx(html_path)
        print(f"built {html_path.name}" + (" + .docx" if wants_docx else ""))


if __name__ == "__main__":
    main()

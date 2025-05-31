#!/usr/bin/env python3
"""
find_unused_javascript_files.py
--------------------------------
Scan a directory tree and list JavaScript files that are referenced
NOWHERE – not in any HTML <script> tag and not in any JS import/require.

Date: 2025-05-31
"""

# ==== Standard-library imports ====
import os                      # Path handling & directory walking
import sys                     # Command-line argument reading
import re                       # Simple pattern matching inside JS
import logging                 # Clean terminal output

# ==== Third-party import (HTML parsing) ====
# Install once with:  pip install beautifulsoup4
from bs4 import BeautifulSoup  # type: ignore

# ------------------------------------------------------------------
# ------------------------ GLOBAL CONSTANTS ------------------------
# ------------------------------------------------------------------

HTML_EXT   = ".html"   # Extension marking HTML files
JS_EXT     = ".js"     # Extension marking JavaScript files

LOG_LEVEL  = logging.INFO         # Default verbosity
LOG_FMT    = "%(levelname)s: %(message)s"  # Log line style

HTML_TAG   = "script"  # Tag we look for in HTML
HTML_ATTR  = "src"     # Attribute on <script> tag that holds the path

# Regexes to catch most common import syntaxes inside JS -----------------
IMPORT_PATTERNS = [
    # ES-module static imports: import abc from './utils.js'
    re.compile(r"""import\s+(?:[\w*\s{},]*\s+from\s+)?["']([^"']+)["']"""),
    # Dynamic import(): const mod = await import('./chunk')
    re.compile(r"""import\(\s*["']([^"']+)["']\s*\)"""),
    # CommonJS require(): const lib = require('../lib/core.js')
    re.compile(r"""require\(\s*["']([^"']+)["']\s*\)"""),
]

# ------------------------------------------------------------------
# --------------------------- HELPERS ------------------------------
# ------------------------------------------------------------------

def collect_files(root: str, extension: str) -> list[str]:
    """
    Recursively gather **absolute paths** of every file whose name ends with *extension*.
    """
    files: list[str] = []
    for current_dir, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(extension):
                files.append(os.path.abspath(os.path.join(current_dir, fname)))
    return files


# ------------- HTML → JS -----------------------------------------

def js_names_in_html(html_path: str) -> set[str]:
    """
    Return basenames of every .js file referenced by <script src="…"> tags
    in a single HTML file.
    """
    names: set[str] = set()

    with open(html_path, "r", encoding="utf-8", errors="ignore") as fp:
        soup = BeautifulSoup(fp.read(), "html.parser")

    for tag in soup.find_all(HTML_TAG, src=True):
        basename = os.path.basename(tag.get(HTML_ATTR, ""))
        if basename.lower().endswith(JS_EXT):
            names.add(basename)
    return names


def all_js_names_from_html(html_files: list[str]) -> set[str]:
    """
    Union of every JS basename referenced by all HTML files.
    """
    union: set[str] = set()
    for html in html_files:
        union.update(js_names_in_html(html))
    return union


# ------------- JS → JS -------------------------------------------

def js_names_in_js(js_path: str) -> set[str]:
    """
    Scan one JS file, returning basenames of any imported / required JS.
    """
    names: set[str] = set()

    with open(js_path, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()

    for pattern in IMPORT_PATTERNS:
        for match in pattern.findall(content):
            base = os.path.basename(match)

            # If no extension supplied (e.g. `import './helper'`), assume .js
            if not os.path.splitext(base)[1]:
                base += JS_EXT

            if base.lower().endswith(JS_EXT):
                names.add(base)
    return names


def all_js_names_from_js(js_files: list[str]) -> set[str]:
    """
    Union of every JS basename imported or required by all JS files.
    """
    union: set[str] = set()
    for js in js_files:
        union.update(js_names_in_js(js))
    return union


# ------------- MAIN WORK -----------------------------------------

def main() -> None:
    """
    * Get the folder to scan (default '.') from CLI.
    * Collect all HTML and JS files.
    * Figure out every JS basename referenced from HTML and JS.
    * Log only those JS paths that are referenced **nowhere**.
    """
    target_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FMT)
    logging.info("Scanning directory: %s", target_dir)

    html_files = collect_files(target_dir, HTML_EXT)
    js_files   = collect_files(target_dir, JS_EXT)
    logging.info("Found %d HTML files and %d JS files.", len(html_files), len(js_files))

    # ----- Gather all referenced JS basenames -----
    referenced_from_html = all_js_names_from_html(html_files)
    referenced_from_js   = all_js_names_from_js(js_files)

    referenced_anywhere  = referenced_from_html | referenced_from_js  # Union

    # ----- Determine unused JS paths -----
    unused_js_paths: list[str] = [
        path for path in js_files
        if os.path.basename(path) not in referenced_anywhere
    ]

    # ----- Log result -----
    if unused_js_paths:
        logging.info("")
        logging.info("===== UNUSED JavaScript files =====")
        for p in unused_js_paths:
            logging.info("UNUSED  %s", p)
    else:
        logging.info("Great! Every JavaScript file is referenced somewhere.")

# ------------- ENTRY POINT ---------------------------------------

if __name__ == "__main__":
    main()

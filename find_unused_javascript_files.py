#!/usr/bin/env python3
"""
find_unused_javascript_files.py
--------------------------------
Walks through a directory tree, finds every *.html* and *.js* file,
identifies which JavaScript files are referenced by the HTML files,
and logs which JavaScript files are **used** and which are **unused**.

Date: 2025-05-31
"""

# ==== Standard-library imports ====
import os                     # For directory walking and file-path handling
import sys                    # For reading the folder name from command-line arguments
import logging                # For nicely formatted console output

# ==== Third-party import ====
# BeautifulSoup is the safest, most popular way to parse HTML.
from bs4 import BeautifulSoup # type: ignore

# ------------------------------------------------------------------------
# ------------------------ GLOBAL CONSTANTS ------------------------------
# ------------------------------------------------------------------------

HTML_EXTENSION = ".html"   # File extension that marks HTML files
JS_EXTENSION   = ".js"     # File extension that marks JavaScript files

LOG_FORMAT     = "%(levelname)s: %(message)s" # How log lines appear
LOG_LEVEL      = logging.INFO                 # Default verbosity level

SCRIPT_TAG     = "script" # The tag we search for in HTML
SRC_ATTR       = "src"    # The attribute inside <script> that carries the path

# ------------------------------------------------------------------------
# ---------------------  HELPER FUNCTIONS  -------------------------------
# ------------------------------------------------------------------------

def collect_files_by_extension(root_folder: str, extension: str) -> list[str]:
    """
    Recursively gather **absolute paths** of every file in *root_folder*
    that ends with *extension*.
    """
    files: list[str] = []                         # Accumulator list
    for current_dir, _, filenames in os.walk(root_folder):
        for name in filenames:
            if name.lower().endswith(extension):  # Match desired extension
                full_path = os.path.join(current_dir, name) # Create full path
                files.append(os.path.abspath(full_path))    # Store absolute path
    return files                                   # Return the complete list


def extract_js_filenames_from_html(html_path: str) -> set[str]:
    """
    Parse one HTML file and return a **set** of all JavaScript file *names*
    (just the basenames, not the directories) referenced in <script src="..."> tags.
    """
    used_names: set[str] = set()       # Container for JS basenames we discover

    # Read the whole HTML file safely
    with open(html_path, "r", encoding="utf-8", errors="ignore") as fp:
        html_content = fp.read()       # Load file contents as a string

    soup = BeautifulSoup(html_content, "html.parser")   # Parse HTML

    # Loop through every <script> tag that has a 'src' attribute
    for script in soup.find_all(SCRIPT_TAG, src=True):
        src_value = script.get(SRC_ATTR, "")            # Fetch src attribute
        js_name   = os.path.basename(src_value)         # Keep only the file name
        if js_name.lower().endswith(JS_EXTENSION):      # Ensure it's a .js file
            used_names.add(js_name)                     # Store unique name
    return used_names                                   # Return the discovered set


def gather_all_used_js_names(html_files: list[str]) -> set[str]:
    """
    Aggregate the union of all JavaScript file names referenced
    by **every** HTML file in the project.
    """
    all_used: set[str] = set()             # Start with an empty union
    for html_path in html_files:           # Iterate over each HTML file
        used_in_file = extract_js_filenames_from_html(html_path)
        all_used.update(used_in_file)      # Merge sets together
    return all_used                        # Return the global set of uses


def partition_js_files(js_files: list[str],
                       used_names: set[str]) -> tuple[list[str], list[str]]:
    """
    Split the list of JavaScript file **paths** into two buckets:
    (1) paths whose *basename* appears in *used_names*  -> used_js
    (2) all other paths                                -> unused_js
    """
    used_js:   list[str] = []  # Container for used JS file paths
    unused_js: list[str] = []  # Container for unused JS file paths

    for js_path in js_files:
        js_name = os.path.basename(js_path)  # Extract the file name
        # Compare names case-insensitively for robustness
        if js_name in used_names:
            used_js.append(js_path)          # Mark as used
        else:
            unused_js.append(js_path)        # Mark as unused
    return used_js, unused_js                # Return the two buckets


def log_results(used_js: list[str], unused_js: list[str]) -> None:
    """
    Print clear, friendly messages to the terminal listing
    which JavaScript files are used or unused.
    """
    logging.info("----- SUMMARY -----")                    # Section header

    # --- Used files ---
    if used_js:
        logging.info("JavaScript files referenced by HTML:")
        for path in used_js:
            logging.info("  USED   %s", path)               # List each used file
    else:
        logging.info("No JavaScript files are referenced.") # Edge case

    # --- Unused files ---
    if unused_js:
        logging.info("JavaScript files NOT referenced by any HTML:")
        for path in unused_js:
            logging.info("  UNUSED %s", path)               # List each unused file
    else:
        logging.info("All JavaScript files are referenced!")# Edge case


# ------------------------------------------------------------------------
# --------------------------  MAIN LOGIC  --------------------------------
# ------------------------------------------------------------------------

def main() -> None:
    """
    Orchestrates the whole scan:
    1. Reads the target folder from CLI (defaults to ".").
    2. Collects all HTML and JS files.
    3. Builds a set of JS names used in the HTML.
    4. Separates JS files into used vs unused.
    5. Logs the outcome.
    """
    # -------- Argument handling --------
    if len(sys.argv) > 1:                   # User provided a folder path
        target_folder = sys.argv[1]         # Use it
    else:
        target_folder = "."                 # Default: current directory

    # Normalize the folder path to absolute path
    target_folder = os.path.abspath(target_folder)

    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT) # Configure logging
    logging.info("Scanning project folder: %s", target_folder)

    # -------- Collect all HTML & JS files --------
    html_files = collect_files_by_extension(target_folder, HTML_EXTENSION)
    js_files   = collect_files_by_extension(target_folder, JS_EXTENSION)

    logging.info("Found %d HTML files and %d JS files.",
                 len(html_files), len(js_files))

    # -------- Determine which JS files are referenced --------
    used_js_names = gather_all_used_js_names(html_files)

    # -------- Partition JS paths into used / unused --------
    used_js_paths, unused_js_paths = partition_js_files(js_files, used_js_names)

    # -------- Present results to the user --------
    log_results(used_js_paths, unused_js_paths)


# ------------------------------------------------------------------------
# ----------------------------  ENTRY  -----------------------------------
# ------------------------------------------------------------------------

if __name__ == "__main__":
    main()  # Run the main workflow when script is executed directly

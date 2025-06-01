# 🕵️‍♂️ find-unused-javascript-files

`find_unused_javascript_files.py` is a small Python utility that scans a project folder (recursively) and tells you which JavaScript files are never referenced:

Not in any HTML `<script src="…">` tag

Not in any JavaScript `import`, dynamic `import()` or CommonJS `require()` call

By listing only the truly dead `.js` files, it helps you delete forgotten code and keep your repo lean

## Features

| Feature                       | Description                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| **Deep scan**              | Walks every sub-directory automatically.                                           |
| **HTML → JS parsing**     | Finds filenames in `<script src="…">` tags via *BeautifulSoup*.                    |
| **JS → JS parsing**        | Detects static `import`, dynamic `import()` and `require()` statements with regex. |
| **Path-agnostic**          | Compares **only the filename**, so mismatched or relative paths don’t matter.      |
| **Concise log**           | Prints *one* list – the `.js` files that appear nowhere.                           |
| **Zero non-standard deps** | Needs only `beautifulsoup4` (install once with `pip`).                             |


## Requirements

* Python ≥ 3.8  
* `beautifulsoup4`  

Install the dependency once:
`pip install beautifulsoup4`

## Installation
1. Clone or download this repo, then make the script executable:

```
git clone https://github.com/tomcadene/find_unused_javascript_files.git
cd find_unused_javascript_files
chmod +x find_unused_javascript_files.py   # optional on Unix
```

2. Install BeautifulSoup (only once)

```pip install beautifulsoup4```

## Usage

`python find_unused_javascript_files.py /path/to/project`

If you omit the path, the current directory (.) is scanned.

## Example output

```
INFO: Scanning directory: /Users/me/my-app
INFO: Found 27 HTML files and 142 JS files.

===== UNUSED JavaScript files =====
UNUSED  /Users/me/my-app/scripts/old/polyfill-ie11.js
UNUSED  /Users/me/my-app/components/legacy/modal-legacy.js
UNUSED  /Users/me/my-app/tests/helpers/mock-fetch.js
```

If everything is referenced you’ll see:

`INFO: Great! Every JavaScript file is referenced somewhere.`




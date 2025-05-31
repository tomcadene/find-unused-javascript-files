# 🕵️‍♂️ find-unused-javascript-files

**Quickly scan a project folder to discover which JavaScript files are used in your HTML and which are collecting dust.**

## ✨ Features

* **Recursive scan** – Walks every sub-folder automatically.  
* **Name-based matching** – Ignores path differences; compares only file names.  
* **Clear terminal report** – Lists `USED` and `UNUSED` files separately.  
* **Zero config** – Just run the script and point it at a directory.  
* **Pure Python** – Only dependency is the well-known `beautifulsoup4` parser.

## 📦 Requirements

* Python ≥ 3.8  
* `beautifulsoup4`  

Install the dependency once:
`pip install beautifulsoup4`

## 🚀 Installation
Clone or download this repo, then make the script executable:
```
git clone https://github.com/your-username/find_unused_javascript_files.git
cd find_unused_javascript_files
chmod +x find_unused_javascript_files.py   # optional on Unix
```

## 🛠️ Usage
`python find_unused_javascript_files.py [TARGET_FOLDER]`

TARGET_FOLDER – Path to the directory you want to scan.

If omitted, the current working directory is used.

## Example

`python find_unused_javascript_files.py ./my-web-app`

Terminal output:
```
INFO: Scanning project folder: /absolute/path/to/my-web-app
INFO: Found 14 HTML files and 27 JS files.
INFO: ----- SUMMARY -----
INFO: JavaScript files referenced by HTML:
INFO:   USED   /my-web-app/js/app.js
INFO:   USED   /my-web-app/js/vendor/jquery.min.js
INFO: JavaScript files NOT referenced by any HTML:
INFO:   UNUSED /my-web-app/js/old-carousel.js
INFO:   UNUSED /my-web-app/js/debug-tools.js
```



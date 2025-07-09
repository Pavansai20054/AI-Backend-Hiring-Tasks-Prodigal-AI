# 📰 AI-Backend Article & Scheme Scraper Suite

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) 
![Playwright](https://img.shields.io/badge/Playwright-Automation-green?logo=playwright)
![Colorama](https://img.shields.io/badge/Colorama-Terminal-orange)
![License](https://img.shields.io/badge/License-Copyright-red)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-important)

---

🚀 A powerful, professional, and interactive suite for scraping **Microsoft Research Blogs** and **Indian Government Schemes (MyScheme.gov.in)** with robust features, beautiful terminal UI, and flexible cross-platform support.  
✨ Automates the extraction of full articles, metadata, and government scheme details into organized JSON files for your research or data needs.

> **Author:** 👨‍💻 [PAVANSAI RANGDAL](https://www.github.com/Pavansai20054)  
> **Contact:** 📧 pavansai87654321@gmail.com

---

## ▶️ Demo Video

Watch the demonstration of the Article & Scheme Scraper Suite here:  
**[🟢 Demo Video (Google Drive Link)](https://drive.google.com/file/d/1_PKZuou7T0IbYX8HK-KDpXoZyOkSFTrK/view?usp=sharing)**

---

## 📑 Table of Contents

1. [🚀 Project Overview](#-project-overview)
2. [📂 Directory Structure](#-directory-structure)
3. [🛠️ Features](#️-features)
   1. [Microsoft Research Scraper](#microsoft-research-scraper)
   2. [MyScheme Government Scheme Scraper](#myscheme-government-scheme-scraper)
4. [💻 Supported Platforms](#-supported-platforms)
5. [🔗 Repository & Clone Instructions](#-repository--clone-instructions)
6. [⚙️ Installation & Setup](#️-installation--setup)
   1. [Python Virtual Environment](#python-virtual-environment)
   2. [Conda Environment](#conda-environment)
7. [📦 Dependency Management](#-dependency-management)
8. [🎮 How to Run the Scrapers](#-how-to-run-the-scrapers)
   1. [Microsoft Research Blog Scraper](#microsoft-research-blog-scraper-1)
   2. [MyScheme Scheme Scraper](#myscheme-scheme-scraper)
9. [📁 Output & File Formats](#-output--file-formats)
10. [🖥️ Screenshots & Terminal UI Samples](#️-screenshots--terminal-ui-samples)
11. [⚡ Troubleshooting & Tips](#-troubleshooting--tips)
12. [🙋‍♂️ FAQ](#️-faq)
13. [🤝 Contact](#-contact)
14. [🔒 License](#-license)

---

## 🚀 Project Overview

🎯 This comprehensive suite contains two ready-to-use, professional web scrapers designed for maximum efficiency and user experience:

- **🔬 Microsoft Research Blog Scraper:**  
  📄 Scrapes full-length articles (including all metadata, authors, and social links) from the Microsoft Research blog, saving them as organized JSON files. 🎨 Features intelligent content extraction with full article text, author designations, publication dates, categories, and social media integrations.

- **🏛️ MyScheme Government Scheme Scraper:**  
  📋 Extracts comprehensive government scheme details from [MyScheme.gov.in](https://www.myscheme.gov.in), including title, official URLs, and complete structured content descriptions, also saving to JSON format for easy analysis and research.

✨ **Key Highlights:**
- 🌈 Real-time progress bars with colorful headers and clean output visualization
- 📖 Sophisticated pagination navigation for deep multi-page scraping capabilities
- 🛡️ Robust error handling and OS-agnostic directory management system
- 🎛️ Interactive user input and comprehensive feedback mechanisms
- 🔄 Automatic duplicate detection and content validation
- 📊 Structured data output with consistent formatting

---

## 📂 Directory Structure

📁 After cloning, the relevant project structure for **Task 6** is:

```
AI-Backend-Hiring-Tasks-Prodigal-AI/
└── Task 6 - Article + Scheme Scraper & Summary Report/
    ├── article_scheme_scraper/
    │   ├── 🐍 mircosoft.py
    │   ├── 🏛️ myscheme_scraper.py
    │   ├── 📋 requirements.txt
    │   └── 📖 README.md
    ├── outputs/
    │   ├── microsoft-articles/
    │   │   └── json-files/
    │   │       └── 📄 (Generated JSON files)
    │   └── myscehme-schemes/
    │       └── json-files/
    │           └── 📄 (Generated JSON files)
    └── ... (other supportive files)
```

- **🔬 msresearch_scraper.py:** Advanced scraper for Microsoft Research Blog with full metadata extraction
- **🏛️ myscheme_scraper.py:** Comprehensive scraper for MyScheme.gov.in with pagination support
- **📋 requirements.txt:** Complete list of Python dependencies with version specifications
- **📁 outputs/**: Organized directory where all scraped results are systematically saved

---

## 🛠️ Features

### 🔬 Microsoft Research Scraper

- **📄 Scrapes:** Full article content, comprehensive titles, authors with complete designations, publication dates, detailed categories, and social media links  
- **🔄 Navigates:** All paginated results with intelligent page detection, supporting unlimited article extraction  
- **💾 Output:** Structured, pretty-printed JSON with consistent formatting and metadata organization  
- **🎨 User Interface:** Vibrant terminal headers, animated progress bars with percentage indicators, and sample output preview functionality  
- **🛡️ Error Handling:** Advanced exception catching and comprehensive logging for page load failures or article extraction issues
- **🔍 Content Extraction:** Deep parsing of article structure including full text, author information, and social media integration
- **📊 Progress Tracking:** Real-time updates with visual progress indicators and estimated completion times

### 🏛️ MyScheme Government Scheme Scraper

- **📋 Scrapes:** Complete scheme titles, official government URLs, and comprehensive content descriptions with full detail extraction  
- **📖 Pagination:** Intelligent automatic navigation across multiple pages with seamless continuation  
- **💾 Output:** Clean, structured JSON with consistent formatting and complete data preservation  
- **🎨 User Experience:** Interactive interface with beautiful ASCII art headers, real-time progress tracking, and user-friendly prompts  
- **🛡️ Resilience:** Advanced duplicate handling, unavailable content graceful management, and retry mechanisms
- **🔍 Content Validation:** Automatic verification of extracted data quality and completeness
- **📊 Analytics:** Built-in statistics tracking for scraping performance and success rates

---

## 💻 Supported Platforms

🌍 **Cross-Platform Compatibility:**
- **🪟 Windows** (PowerShell, CMD, Windows Terminal, or WSL environments)
- **🐧 Linux** (Ubuntu, Debian, Fedora, Arch Linux, CentOS, and other distributions)
- **🍎 macOS** (Intel processors & Apple Silicon M1/M2/M3 chips)

🔧 All scripts utilize OS-agnostic directory management with automatic path resolution. No manual file path modifications required across different operating systems!

---

## 🔗 Repository & Clone Instructions

**🏠 GitHub Repository:**  
[https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git](https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git)

**📥 Clone with Git:**
```sh
git clone https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git
```

**📦 Alternative Download Methods:**
- 🔗 Direct ZIP download from GitHub
- 📋 Use GitHub CLI: `gh repo clone Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI`

---

## ⚙️ Installation & Setup

### 📁 Step 1: Navigate to Project Directory

```sh
cd "AI-Backend-Hiring-Tasks-Prodigal-AI/Task 6 - Article + Scheme Scraper & Summary Report"
cd article_scheme_scraper
```

### 🔧 Step 2: Environment Setup Options

🐍 You can use either **Python's venv** or **Conda** environment management systems.

#### Python Virtual Environment

**🪟 For Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

**🐧🍎 For Linux/macOS:**
```sh
python3 -m venv venv
source venv/bin/activate
```

#### 🐍 Conda Environment (Alternative)

```sh
conda create -n scraper-env python=3.10
conda activate scraper-env
```

### 📦 Step 3: Install Dependencies

```sh
pip install -r requirements.txt
```

**🐍 For Conda users, you may also need:**
```sh
pip install playwright colorama pandas
```

### 🌐 Step 4: Playwright Browser Setup

🎭 Playwright requires downloading browser binaries for automation:

```sh
python -m playwright install
# Or if python3 is your command:
python3 -m playwright install
```

**🔧 Additional Browser Options:**
```sh
# Install specific browsers
python -m playwright install chromium
python -m playwright install firefox
python -m playwright install webkit
```

---

## 📦 Dependency Management

📋 **Main dependencies** (see `requirements.txt` for complete specifications):

- **🎭 playwright** (async web automation and browser control)
- **🌈 colorama** (beautiful terminal output with cross-platform color support)
- **🐼 pandas** (advanced data manipulation and analysis in msresearch_scraper)
- **📄 json, datetime, os, sys, re, pathlib** (standard library modules)

🎭 **Playwright is essential** for browser-based automation and JavaScript rendering.  
🐍 All scripts are fully compatible with **Python 3.8+** and tested across multiple versions.

**🔧 Optional Dependencies:**
- **📊 matplotlib** (for data visualization if needed)
- **🔍 beautifulsoup4** (backup HTML parsing support)
- **📝 lxml** (XML/HTML processing enhancement)

---

## 🎮 How to Run the Scrapers

### 🔬 Microsoft Research Blog Scraper

```sh
python microsoft.py
```

- **📝 Follow prompts**: Enter the desired number of articles to scrape with validation
- **📊 Progress tracking**: Animated progress bar with real-time color feedback and percentage
- **💾 Output location**: Automatically saved JSON file in `outputs/microsoft-articles/json-files/`
- **🎨 Visual feedback**: Beautiful terminal UI with status updates and completion notifications

### 🏛️ MyScheme Scheme Scraper

```sh
python myscheme_scraper.py
```

- **📝 Interactive prompts**: Enter the number of schemes to scrape with input validation
- **🎨 ASCII art header**: Enjoy the beautiful terminal presentation and progress visualization
- **💾 Output location**: Automatically saved JSON file in `outputs/myscehme-schemes/json-files/`
- **📊 Progress monitoring**: Real-time updates with completion statistics and success rates

---

## 📁 Output & File Formats

📄 Both scrapers generate **beautifully formatted, pretty-printed JSON files** with consistent structure:

- **📝 Naming Convention with Timestamps:**  
  🔬 `microsoft_research_articles_10items_2025-07-08_2015.json`  
  🏛️ `myscheme_gov_schemes_20items_2025-07-08_2019.json`

- **📂 Organized Storage Locations:**  
  - 🔬 Microsoft Articles: `outputs/microsoft-articles/json-files/`
  - 🏛️ Government Schemes: `outputs/myscehme-schemes/json-files/`

### 🔬 Microsoft Research Article Output Example

```json
{
  "title": "🤖 AI for Good: Improving Healthcare Through Machine Learning",
  "link": "https://www.microsoft.com/en-us/research/blog/ai-for-good-healthcare/",
  "authors": "Dr. John Doe (Principal Researcher); Dr. Jane Smith (Director of AI Research)",
  "date": "July 8, 2025",
  "categories": ["Artificial Intelligence", "Healthcare", "Machine Learning"],
  "content": "...comprehensive full article content with complete text...",
  "full_text": "...complete article preview with formatting...",
  "social_links": {
    "Twitter": "https://twitter.com/MSFTResearch/status/...",
    "LinkedIn": "https://linkedin.com/company/microsoft-research/posts/...",
    "Facebook": "https://facebook.com/MicrosoftResearch/posts/..."
  },
  "metadata": {
    "scraped_at": "2025-07-08T20:15:30Z",
    "word_count": 2847,
    "reading_time": "12 minutes"
  }
}
```

### 🏛️ MyScheme Scheme Output Example

```json
{
  "title": "🏠 Pradhan Mantri Awas Yojana - Housing for All",
  "url": "https://www.myscheme.gov.in/schemes/pmay-urban",
  "content": "This comprehensive scheme aims to provide affordable housing for all eligible urban families by 2022. The scheme includes various components such as in-situ rehabilitation, affordable housing partnerships, and beneficiary-led individual house construction...",
  "metadata": {
    "scraped_at": "2025-07-08T20:19:45Z",
    "content_length": 1456,
    "scheme_category": "Housing & Urban Development"
  }
}
```

---

## 🖥️ Screenshots & Terminal UI Samples

🎨 **Beautiful Terminal Interface Examples:**

### 🔬 Microsoft Research Scraper UI

```
🔬============================================================
 📰 Microsoft Research Blog Scraper 🚀
============================================================
 • 📄 Scrapes full article content including text and metadata
 • 🔍 Visits each article page individually for complete data
 • 💾 Saves results in organized JSON format
 • 🎨 Beautiful progress tracking with real-time updates
============================================================
🔢 How many articles would you like to scrape? (Enter positive Integer): 5
✅ Great! I'll fetch 5 high-quality articles for you!

📊 Scraping Progress:
[████████████████████░░░░░░░░░░░░] 66.67% (2/3 articles) 🔄
📄 Currently processing: "AI Advances in Natural Language Processing"
⏱️ Estimated time remaining: 2 minutes 30 seconds

✔️ Successfully completed! 🎉
📁 File saved to organized directory:
   • 💾 JSON: outputs/microsoft-articles/json-files/microsoft_research_articles_5items_2025-07-08_2019.json
   • 📊 Total articles scraped: 5
   • ⏱️ Total time taken: 4 minutes 15 seconds
```
  __  ____     _______  _____ _    _ ______ __  __ ______    _____  _____ _____            _____  ______ _____  
 |  \/  \ \   / / ____|/ ____| |  | |  ____|  \/  |  ____|  / ____|/ ____|  __ \     /\   |  __ \|  ____|  __ \ 
 | \  / |\ \_/ / (___ | |    | |__| | |__  | \  / | |__    | (___ | |    | |__) |   /  \  | |__) | |__  | |__) |
 | |\/| | \   / \___ \| |    |  __  |  __| | |\/| |  __|    \___ \| |    |  _  /   / /\ \ |  ___/|  __| |  _  / 
 | |  | |  | |  ____) | |____| |  | | |____| |  | | |____   ____) | |____| | \ \  / ____ \| |    | |____| | \ \ 
 |_|  |_|  |_| |_____/ \_____|_|  |_|______|_|  |_|______| |_____/ \_____|_|  \_\/_/    \_\_|    |______|_|  \_\ 

 MyScheme Government Scheme Scraper 
============================================================
 • 📋 Scrapes government schemes with title, URL, and content
 • 💾 Saves results in JSON format
 • 🎨 Interactive progress tracking and vibrant ASCII art
============================================================

🔢 How many schemes would you like to scrape? (Enter positive Integer): 10
✅ Great! I'll fetch 10 government schemes for you!

📊 Scraping Progress:
[███████░░░░░░░░░░░░░░░░░░░░░░] 30.0% (3/10 schemes) 🔄
📋 Currently processing: "National Digital Health Mission"
⏱️ Estimated time remaining: 1 minute 12 seconds

✔️ Successfully completed! 🎉
📁 File saved:
   • 💾 JSON: outputs/myscehme-schemes/json-files/myscheme_gov_schemes_10items_2025-07-08_2019.json
   • 📊 Total schemes scraped: 10
   • ⏱️ Total time taken: 2 minutes 17 seconds

---

## ⚡ Troubleshooting & Tips

- **Browser/Playwright Errors:**  
  If Playwright reports missing browsers, always run `python -m playwright install` in your virtual environment.  
  For headless scraping, you can set `headless=True` in the script for faster performance.

- **Permission Denied:**  
  On Linux/macOS, ensure you have write permissions for the outputs directory. Use `sudo` if required, or adjust directory ownership with `chown`.

- **Long Waits or Timeouts:**  
  - Slow internet can affect scraping; increase timeouts in the script if needed.
  - If scraping large numbers, consider running in smaller batches.

- **Unicode/Terminal Issues:**  
  - Use a Unicode-compatible terminal (Windows Terminal, macOS Terminal, or modern terminals on Linux) for best ASCII/art and color experience.
  - If you see garbled output, switch to a different terminal or set your shell to UTF-8 encoding.

- **Output Directory Not Found:**  
  - All output directories are created automatically by the script.  
  - If there's an error, manually create the expected folders as described above.

---

## 🙋‍♂️ FAQ

**Q1: Can I scrape more than 100 articles/schemes at once?**  
A: Absolutely! Enter any positive integer when prompted—the script paginates until your number is reached or data ends.

**Q2: Can I contribute, fork, or modify this project?**  
A: **No.** This repository is strictly under a copyright license (see below).  
Any unauthorized use, modification, distribution, or contribution is prohibited.

**Q3: Where do the output files go?**  
A: All outputs are placed in `outputs/microsoft-articles/json-files/` or `outputs/myscehme-schemes/json-files/` within your project directory, with clear timestamped filenames.

**Q4: Can I use a different browser engine?**  
A: Yes! Playwright supports Chromium, Firefox, and WebKit. Install additional engines using:
```sh
python -m playwright install chromium
python -m playwright install firefox
python -m playwright install webkit
```
Modify the script if you want to use a specific engine.

**Q5: Is it necessary to use a virtual environment?**  
A: Strongly recommended for isolation and dependency management. Both venv and conda are supported.

**Q6: What if the script fails on a particular article/scheme?**  
A: The script gracefully skips failed items after logging the error and continues scraping.

---

## 🤝 Contact

**Name:** PAVANSAI RANGDAL  
**Gmail:** pavansai87654321@gmail.com  
**GitHub:** [https://www.github.com/Pavansai20054](https://www.github.com/Pavansai20054)

> 📬 _For technical queries, usage support, or feedback, please feel free to reach out._

---

## 🔒 License

```
Copyright (c) 2025 PAVANSAI RANGDAL

All rights reserved. No part of this repository, its code, or output may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the copyright owner.

- Commercial use: Not permitted
- Redistribution: Not permitted
- Modification: Not permitted
- Contributions: Not permitted

Violation will result in legal action under applicable copyright law.
```

---

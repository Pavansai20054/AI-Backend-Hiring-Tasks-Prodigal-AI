# 🌐 Web3 Daily Newsletter Bot 🤖

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Ollama](https://img.shields.io/badge/Powered%20By-Ollama%20LLM-ff69b4)

A sophisticated, production-ready automated newsletter system that **aggregates, summarizes, and delivers the latest Web3 news** from top sources directly to Telegram groups using AI-powered summarization and seamless automation.

---

## 📑 Table of Contents

- [🚀 Getting Started](#-getting-started)
  - [✨ Features](#-features)
  - [📦 Prerequisites](#-prerequisites)
  - [⚙️ Installation](#️-installation)
- [🛠 Configuration](#-configuration)
  - [🔐 Environment Setup](#-environment-setup)
  - [🤖 Telegram Bot Setup](#-telegram-bot-setup)
  - [👥 Telegram Group Configuration](#-telegram-group-configuration)
  - [🦙 Ollama LLM Setup](#-ollama-llm-setup)
- [🏗 Architecture](#-architecture)
  - [📊 System Diagram](#-system-diagram)
  - [⚡ Why Not Block Websites?](#-why-not-block-websites)
- [🚦 Usage](#-usage)
  - [🏃 Running the Bot](#-running-the-bot)
  - [⏰ Scheduling](#-scheduling)
  - [🔍 Manual Testing](#-manual-testing)
- [🩺 Troubleshooting](#-troubleshooting)
  - [⚠️ Common Issues](#️-common-issues)
  - [🔧 Debugging Tips](#-debugging-tips)
- [🤝 Contributing](#-contributing)
  - [🧑‍💻 Development](#-development)
  - [📝 Code Style](#-code-style)
- [📜 License](#-license)
- [📞 Contact](#-contact)

---

## 🚀 Getting Started

This bot is intended for Web3 and crypto communities, project founders, and enthusiasts who want a **daily digest** of the latest, deduplicated, and summarized news, delivered directly to their Telegram groups with zero manual intervention.

---

### ✨ Features

- **🌐 Multi-Source Aggregation:** Automatically collects news from CoinDesk, CoinTelegraph, Decrypt, and Bankless, ensuring a broad and up-to-date coverage of the Web3 ecosystem.
- **🧠 AI Summarization:** Harnesses the power of Ollama and Llama3-8b (or lighter alternatives) for concise, human-like summaries of each news item.
- **🔍 Smart Deduplication:** Uses sentence-transformers and FAISS vector search to detect and remove duplicate or highly similar stories across multiple news sources.
- **📬 Automated Delivery:** Sends beautifully formatted, daily newsletters to Telegram groups at scheduled times.
- **📊 Simulation Mode:** Test the entire flow with historical data before live deployment, ensuring reliability.
- **🎨 Rich Formatting:** Uses Markdown to present news in an attractive, readable layout (headlines, sources, summaries, links).
- **⚡ Modular Design:** Easily add new sources, templates, or delivery channels as needed.
- **🔒 Privacy-First:** No scraping of full content, only official RSS feeds and legal sources.

---

### 📦 Prerequisites

Before installation, ensure your environment meets the following:

- **Python 3.9+**  
  Check with: `python --version`
- **pip 23.0+**  
  Check with: `pip --version`
- **Ollama** (for running Llama3 or compatible models locally)  
  See [Ollama LLM Setup](#-ollama-llm-setup)
- **Telegram Account** with permission to create bots and add them as group admins
- **Hardware:**  
  - Minimum: 2GB RAM (for basic operation and light LLMs)  
  - Recommended: 4GB+ RAM (for larger models and faster processing)

---

### ⚙️ Installation

#### 1. Clone the repository

```bash
git clone https://github.com/Pavansai20054/web3-newsletter-bot.git
cd web3-newsletter-bot
```

#### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set up Ollama

Install Ollama (if not already):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Download an appropriate model:

```bash
ollama pull llama3:8b         # For high-end PCs
# OR for low-end systems:
ollama pull llama3:instruct   # Smaller model
```

---

## 🛠 Configuration

### 🔐 Environment Setup

Create a `.env.local` file in the project root directory and fill in the following:

```ini
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here
```

- **TELEGRAM_BOT_TOKEN:**  
  Get this from [@BotFather](https://t.me/BotFather) after creating your bot.
- **TELEGRAM_GROUP_ID:**  
  See [Getting Group ID](#getting-group-id).

---

### 🤖 Telegram Bot Setup

#### 1. Create a new bot

- Open the [@BotFather](https://t.me/BotFather) chat on Telegram
- Send `/newbot` and follow the prompts to set a name and username for your bot (e.g., `Web3NewsBot`)
- Copy the provided API token for your `.env.local`

#### 2. Add the bot to your group

- Open your Telegram group
- Tap the group name > *Add Members* > search for your bot’s username > add the bot

#### 3. Make the bot an admin

- Go to group settings > *Administrators*
- Find your bot in the list and toggle all admin privileges, especially **"Post Messages"**

---

### 👥 Telegram Group Configuration

#### Getting Group ID

1. Add [@RawDataBot](https://t.me/RawDataBot) to your group.
2. Send any message within the group.
3. The bot will reply with raw JSON data.  
   Look for: `"chat":{"id":-123456789}`  
   The **negative number** is your group ID.

**Important Notes:**
- For supergroups, the ID starts with `-100`
- The bot must be admin to send messages
- Enable **"Allow anonymous admins"** in group settings if needed

---

### 🦙 Ollama LLM Setup

Choose a model based on your hardware:

#### For High-End PCs (16GB+ RAM):

```bash
ollama pull llama3:70b        # Most powerful model
ollama pull mixtral:latest    # Alternative
```

#### For Low-End PCs (4GB RAM):

```bash
ollama pull llama3:instruct   # Optimized version
ollama pull gemma:2b          # Very lightweight
```

#### Performance Tuning

Set environment variables before running for optimal performance:

```bash
export OLLAMA_NUM_GPU=1           # Use GPU if available
export OLLAMA_MAX_KEEP_ALIVE=30m  # Keep model loaded for 30 minutes
```

---

## 🏗 Architecture

### 📊 System Diagram

**How the bot delivers your daily news:**

```
sequenceDiagram
    participant S as Scheduler
    participant C as Scrapers
    participant D as Deduplicator
    participant L as LLM
    participant T as Telegram
    
    S->>C: Trigger daily scrape
    C->>D: Send raw articles
    D->>L: Forward unique articles
    L->>T: Send summarized news
    T->>Users: Deliver newsletter
```

---

### ⚡ Why Not Block Websites?

We intentionally avoid scraping full websites for the following reasons:

- **Respect for Publishers:**  
  We use only official RSS feeds, which provide legal access to headlines.
- **Sustainability:**  
  Prevents IP bans from aggressive scraping practices.
- **Focus on Value:**  
  Summarization adds more value than copying full articles.
- **Compliance:**  
  Adheres to most websites’ terms of service.
- **Performance:**  
  RSS is lightweight, fast, and reduces server load.

---

## 🚦 Usage

### 🏃 Running the Bot

#### Normal Mode (Live):

```bash
python main.py
```

#### Simulation Mode (Test):

```bash
# Tests 2 days of newsletters without sending
python main.py --simulate --days 2
```

#### Dry Run (Debug):

```bash
# Fetches but doesn't send to Telegram
python main.py --dry-run
```

---

### ⏰ Scheduling

#### Linux (systemd):

To run the bot automatically each day, create a systemd service:

```bash
sudo tee /etc/systemd/system/web3news.service > /dev/null <<EOL
[Unit]
Description=Web3 Newsletter Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/python /path/to/project/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl enable web3news
sudo systemctl start web3news
```

#### Windows (Task Scheduler):

- Open Task Scheduler
- Create Basic Task
- Set trigger to "Daily"
- Action: "Start a program"
- Program: `pythonw.exe`
- Arguments: `main.py`

---

### 🔍 Manual Testing

Test individual components before going live:

```bash
# Test CoinDesk scraper
python -m scraping.coindesk

# Test summarization
python -m summarizer --text "Your test news headline here"

# Test Telegram sending
python -m telegram_bot --test "Hello World"
```

---

## 🩺 Troubleshooting

### ⚠️ Common Issues

#### 1. Ollama Not Responding

```bash
# Check service status
ollama serve

# Reset the service
sudo systemctl restart ollama
```

#### 2. Telegram API Errors

- Ensure bot token is correct
- Verify group ID is properly set
- Check bot has admin privileges

#### 3. Scraping Failures

```bash
# Test connectivity
curl -v https://cointelegraph.com/rss

# Check if being blocked
python -m scraping.cointelegraph --debug
```

#### 4. Low Memory Errors

```ini
# In .env.local add:
OLLAMA_MAX_MEMORY=2048  # MB
```

---

### 🔧 Debugging Tips

- **Enable verbose logging:**
    ```bash
    python main.py --verbose
    ```
- **Check network connections:**
    ```bash
    lsof -i :11434  # Ollama port
    ```
- **Monitor resource usage:**
    ```bash
    htop      # Linux
    taskmgr   # Windows
    ```

---

## 🤝 Contributing

### 🧑‍💻 Development

**Code Structure:**

```
├── scraping/          # Website scrapers
├── config.py          # Configuration
├── deduplicate.py     # Article deduplication
├── models.py          # Data models
├── newsletter.py      # Newsletter templates
├── summarizer.py      # AI summarization
├── telegram_bot.py    # Telegram integration
└── main.py            # Main application
```

**Adding New Sources:**

1. Create a new scraper in the `scraping/` folder
2. Add your function to `SCRAPER_FUNCS` in `scraping/__init__.py`
3. Update the `PUBLICATIONS` dictionary in `config.py` with a label and URL

---

### 📝 Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines
- Use type hints for all function signatures
- Write docstrings for all public methods
- 120 character line limit
- 4-space indentation (no tabs)

---

## 📜 License

See full license at: [LICENSE](./LICENSE)

```
Copyright (c) 2025 RANGDAL PAVANSAI
All Rights Reserved.
```

---

## 📞 Contact

**Maintainer:**  
PAVANSAI RANGDAL  
📧 Email: [pavansai87654321@gmail.com](mailto:pavansai87654321@gmail.com)  
🐙 GitHub: [https://github.com/Pavansai20054](https://github.com/Pavansai20054)

---

> **Feedback, suggestions, and contributions are welcome!**  
> Please open an issue or pull request to propose improvements or report bugs.

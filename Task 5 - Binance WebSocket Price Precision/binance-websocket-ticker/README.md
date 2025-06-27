# 🚀 Binance Tick Data Streamer to InfluxDB ☁️💹

A professional-grade Python application for streaming real-time Binance cryptocurrency tick data into InfluxDB Cloud, supporting robust analytics, research, and time-series dashboards.

---

## 📑 Table of Contents

- [🚀 Binance Tick Data Streamer to InfluxDB ☁️💹](#-binance-tick-data-streamer-to-influxdb-️)
  - [📑 Table of Contents](#-table-of-contents)
  - [📚 Project Overview](#-project-overview)
  - [✨ Features](#-features)
  - [🛠️ Prerequisites](#️-prerequisites)
  - [🏗️ Architecture](#️-architecture)
  - [🧰 Step 1: Get the Code (Clone the Directory)](#-step-1-get-the-code-clone-the-directory)
  - [📦 Step 2: Install Required Python Packages](#-step-2-install-required-python-packages)
    - [🐍 Option A: Using Python venv (Recommended for most users)](#-option-a-using-python-venv-recommended-for-most-users)
    - [🐍 Option B: Using Conda (If you have Anaconda/Miniconda installed)](#-option-b-using-conda-if-you-have-anacondaminiconda-installed)
    - [📋 Install Required Packages](#-install-required-packages)
      - [Method A: Install from requirements.txt (Recommended)](#method-a-install-from-requirementstxt-recommended)
      - [Method B: Install packages individually](#method-b-install-packages-individually)
    - [✅ Verify Installation](#-verify-installation)
    - [🔄 Managing Your Virtual Environment](#-managing-your-virtual-environment)
    - [📝 Important Notes](#-important-notes)
    - [🚨 Troubleshooting Virtual Environments \& Package Installation](#-troubleshooting-virtual-environments--package-installation)
      - [Common Error: "ModuleNotFoundError: No module named 'websockets'"](#common-error-modulenotfounderror-no-module-named-websockets)
      - [Other Common Issues:](#other-common-issues)
  - [🥇 Step 3: Create Your InfluxDB Cloud Account](#-step-3-create-your-influxdb-cloud-account)
  - [🏷️ Step 4: Set Up InfluxDB for the Project](#️-step-4-set-up-influxdb-for-the-project)
    - [🪣 Create a Bucket (Database)](#-create-a-bucket-database)
    - [🌐 Get Your InfluxDB URL](#-get-your-influxdb-url)
    - [🔑 Create an API Token](#-create-an-api-token)
    - [✅ Verify Your Configuration](#-verify-your-configuration)
  - [🧠 Step 5: Understanding the Code](#-step-5-understanding-the-code)
    - [Key Components:](#key-components)
    - [Main Script Flow:](#main-script-flow)
  - [▶️ Step 6: Running the Streamer](#️-step-6-running-the-streamer)
    - [Start the Streamer:](#start-the-streamer)
    - [Expected Output:](#expected-output)
    - [🛑 To Stop the Streamer:](#-to-stop-the-streamer)
    - [🔧 Troubleshooting:](#-troubleshooting)
  - [📈 Visualizing and Querying Your Data](#-visualizing-and-querying-your-data)
    - [Using InfluxDB Data Explorer:](#using-influxdb-data-explorer)
    - [Integration with External Tools:](#integration-with-external-tools)
  - [📊 Data Model](#-data-model)
    - [Measurement Structure:](#measurement-structure)
    - [Example Data Point:](#example-data-point)
  - [🔒 Security Notes](#-security-notes)
    - [API Token Security:](#api-token-security)
    - [Environment Variables Best Practices:](#environment-variables-best-practices)
  - [📬 Contact](#-contact)
  - [📝 License](#-license)

---

## 📚 Project Overview

This project captures and stores high-frequency Binance trade data ("tick data") in real time, utilizing InfluxDB Cloud for scalable time-series storage. It is designed for developers, data scientists, and financial analysts who require accurate and high-resolution streaming price data for cryptocurrencies. You can use this data for algorithmic trading, research, or real-time dashboards.

---

## ✨ Features

- ⚡ **Real-Time Binance Trade Data:** Streams live trade ticks for multiple cryptocurrency pairs (e.g., BTCUSDT, ETHUSDT)
- 🧮 **High-Precision Storage:** Records price as both a float (for queries) and a string (full decimal precision) to preserve accuracy
- ⏱️ **Millisecond Resolution:** Each trade is timestamped with UTC time at millisecond precision
- 🔁 **Robust Connection Handling:** Automatically reconnects in case of WebSocket interruptions for uninterrupted data collection
- ☁️ **Cloud-Native Integration:** Designed for InfluxDB Cloud, allowing instant access to data from anywhere and integration with visualization tools

---

## 🛠️ Prerequisites

Before starting, ensure you have:

- 🐍 **Python 3.8 or newer** installed on your system
- 💻 **Command-line familiarity** (Windows, Linux, or macOS)
- 🌐 **Internet connection** for downloading packages and streaming data
- 🏦 **No Binance account required** (uses public trade stream)

> **Note:** You'll create a free InfluxDB Cloud account in Step 3 (no credit card required)

---

## 🏗️ Architecture

The architecture of this project is designed for reliability, error-handling, and real-time data streaming:

- 🔌 **Binance WebSocket API:** Provides a continuous, real-time stream of cryptocurrency trade events for selected trading pairs

- 🐍 **Python Streamer (asyncio & websockets):**
  - Connects to Binance's WebSocket API and listens for incoming tick data using asynchronous networking
  - Parses and validates each tick, extracting the trade pair, price (as string and float), and timestamp
  - Handles errors robustly:
    - 🔃 Automatically reconnects if the WebSocket connection drops
    - 📝 Logs and skips malformed or invalid messages
    - 🛡️ Ensures data integrity before writing to InfluxDB Cloud

- ☁️ **InfluxDB Cloud:** Receives and stores each tick as a time-series data point in the `price_ticks` measurement with millisecond-precision timestamps

**Data Flow:**
```
[Binance WebSocket API] → [Python Streamer] → [InfluxDB Cloud]
         ↓                        ↓
[Auto-Reconnect Logic]    [Error Handling & Validation]
```

---

## 🧰 Step 1: Get the Code (Clone the Directory)

First, let's get the project code on your machine. We'll clone only the specific directory you need to keep your setup lightweight.

```bash
# Create a project folder
mkdir binance-websocket-ticker
cd binance-websocket-ticker

# Clone only the specific directory using sparse checkout
git clone --depth 1 --filter=blob:none --sparse https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git .
git sparse-checkout init --cone
git sparse-checkout set "Task 5 - Binance WebSocket Price Precision"

# Navigate to the project files
cd "Task 5 - Binance WebSocket Price Precision/binance-websocket-ticker"
```

**Verify your setup:**

**On Windows:**
```cmd
# Check if you're in the right directory
dir

# You should see files like: binance_ws_influxdb.py, requirements.txt, README.md.
```

**On Linux/macOS:**
```bash
# Check if you're in the right directory
ls -la

# You should see files like: binance_ws_influxdb.py, requirements.txt, README.md.
```

---

## 📦 Step 2: Install Required Python Packages

Setting up a virtual environment is crucial to avoid conflicts with your system Python packages and keep your project dependencies isolated.

### 🐍 Option A: Using Python venv (Recommended for most users)

**Create and activate virtual environment:**

**On Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv binance_env

# Activate the virtual environment
.\binance_env\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation again:
.\binance_env\Scripts\Activate.ps1

# You should see (binance_env) at the beginning of your command prompt
```

**On Windows Command Prompt (CMD):**
```cmd
# Create virtual environment
python -m venv binance_env

# Activate the virtual environment
binance_env\Scripts\activate.bat

# You should see (binance_env) at the beginning of your command prompt
```

**On Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv binance_env

# Activate the virtual environment
source binance_env/bin/activate

# You should see (binance_env) at the beginning of your terminal prompt
```

### 🐍 Option B: Using Conda (If you have Anaconda/Miniconda installed)

```bash
# Create conda environment with Python 3.8+
conda create -n binance_env python=3.9

# Activate the conda environment
conda activate binance_env

# You should see (binance_env) at the beginning of your terminal prompt
```

### 📋 Install Required Packages

Once your virtual environment is activated, install the required packages:

#### Method A: Install from requirements.txt (Recommended)

```bash
# Make sure your virtual environment is activated first!
# You should see (binance_env) in your prompt
pip install -r requirements.txt
```

#### Method B: Install packages individually

```bash
# Install each package manually (virtual environment should be activated)
pip install websockets==12.0
pip install influxdb-client==1.49.0
pip install python-dotenv==1.1.0
```

### ✅ Verify Installation

```bash
# Check if packages are installed correctly in your virtual environment
python -c "import websockets, influxdb_client, dotenv; print('All packages installed successfully!')"

# Check which Python interpreter you're using (should show your virtual environment path)
which python    # On Linux/macOS
where python    # On Windows
```

### 🔄 Managing Your Virtual Environment

**To deactivate the virtual environment when you're done:**
```bash
deactivate
```

**To reactivate it later (whenever you want to run the streamer):**

**On Windows PowerShell:**
```powershell
.\binance_env\Scripts\Activate.ps1
```

**On Windows Command Prompt:**
```cmd
binance_env\Scripts\activate.bat
```

**On Linux/macOS:**
```bash
source binance_env/bin/activate
```

**For Conda users:**
```bash
conda activate binance_env
```

### 📝 Important Notes

- ⚠️ **Always activate your virtual environment** before running the streamer script
- 🔍 **Verify activation:** You should see `(binance_env)` at the beginning of your command prompt
- 📦 **Package isolation:** Packages installed in this environment won't affect your system Python
- 🗂️ **Environment location:** The `binance_env` folder will be created in your current directory

### 🚨 Troubleshooting Virtual Environments & Package Installation

#### Common Error: "ModuleNotFoundError: No module named 'websockets'"

**Problem:** You see this error even after installing packages:
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'websockets','influxdb-client'
```

**Solution Steps:**

1. **First, verify your virtual environment is actually activated:**
   ```bash
   # You should see (binance_env) at the start of your prompt
   # If not, activate it:
   
   # Windows PowerShell:
   .\binance_env\Scripts\Activate.ps1
   
   # Windows CMD:
   binance_env\Scripts\activate.bat
   
   # Linux/macOS:
   source binance_env/bin/activate
   ```

2. **Check which Python and pip you're using:**
   ```bash
   # Should point to your virtual environment
   which python    # Linux/macOS
   where python    # Windows
   
   which pip       # Linux/macOS  
   where pip       # Windows
   ```

3. **Upgrade pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **If you still face errors, upgrade your virtual environment tooling:**  
   (Sometimes, especially on older systems, venv might be out of date.)
   ```bash
   python -m venv binance_env --upgrade-deps
   ```

5. **Install packages with explicit python -m pip:**
   ```bash
   python -m pip install websockets==12.0
   python -m pip install influxdb-client==1.49.0
   python -m pip install python-dotenv==1.1.0
   ```

6. **Alternative: Force reinstall all packages:**
   ```bash
   python -m pip install --force-reinstall websockets==12.0 influxdb-client==1.49.0 python-dotenv==1.1.0
   ```

7. **Verify installation again:**
   ```bash
   python -c "import websockets; print('websockets version:', websockets.__version__)"
   python -c "import influxdb_client; print('influxdb-client imported successfully')"
   python -c "import dotenv; print('python-dotenv imported successfully')"
   ```

#### Other Common Issues:

**If you get permission errors:**
```bash
# On Linux/macOS, you might need:
python3 -m pip install --user virtualenv
python3 -m virtualenv binance_env

# On Windows, try:
py -m pip install --user virtualenv
py -m virtualenv binance_env
```

**If `python` command is not found:**
```bash
# Try python3 instead of python
python3 -m venv binance_env

# Or on Windows:
py -m venv binance_env
```

**If packages still fail to install:**
```bash
# Try installing with --user flag (not recommended for virtual environments, but can help diagnose)
pip install --user websockets==12.0

# Or try with --no-cache-dir
pip install --no-cache-dir websockets==12.0
```

**To completely remove and recreate the virtual environment:**
```bash
# Deactivate first
deactivate

# Remove the environment folder
rm -rf binance_env    # Linux/macOS
rmdir /s binance_env  # Windows

# For conda:
conda env remove -n binance_env

# Then recreate from scratch
python -m venv binance_env
```

**Virtual environment not activating properly:**
```bash
# Windows - try different activation methods:
binance_env\Scripts\activate.bat
# or
.\binance_env\Scripts\Activate.ps1

# Linux/macOS - ensure you're using source:
source binance_env/bin/activate
# not just:
binance_env/bin/activate
```

---

## 🥇 Step 3: Create Your InfluxDB Cloud Account

Now let's set up your cloud database where the streaming data will be stored.

1. **Visit InfluxDB Cloud:** Go to [cloud2.influxdata.com/signup](https://cloud2.influxdata.com/signup)

2. **Sign up using your preferred method:**
   - Click **GOOGLE** or **MICROSOFT** for instant signup with existing accounts
   - Or manually fill in: First Name, Last Name, Email, Password and click **CREATE ACCOUNT**
   - If you already have an account, click **LOG IN**

3. **Set up your workspace:**
   - **Company Name:** Enter something like "Personal" or "Prodigal AI"
   - **Project Name:** Use "Binance WebSocket Live Feed" or similar
   - **Storage Provider:** Choose your preferred region (e.g., AWS US East)
   - Agree to terms and continue

4. **Select a plan:**
   - Choose **🆓 Free** (30 days storage, no credit card required)
   - You can upgrade later if needed

5. **Access the dashboard:** You'll now see the InfluxDB Cloud dashboard

---

## 🏷️ Step 4: Set Up InfluxDB for the Project

Configure your InfluxDB instance for the streaming application.

### 🪣 Create a Bucket (Database)

1. In the InfluxDB dashboard, navigate to **Load Data → Buckets**
2. Click **+ Create Bucket**
3. Configure your bucket:
   - **Name:** `binance_ticks`
   - **Retention Period:** Choose based on your needs:
     - `1 day` for testing/demo
     - `30 days` for short-term analysis
     - `1 year` for long-term storage
4. Click **Create**

### 🌐 Get Your InfluxDB URL

1. **Copy the URL** from your InfluxDB dashboard (e.g., `https://us-east-1-1.aws.cloud2.influxdata.com`)
2. **⚠️ IMPORTANT: Create your `.env.local` file RIGHT NOW and paste this URL:**

**🚨 FIXED FILE CREATION COMMANDS:**

**For Windows PowerShell:**
```powershell
# Create .env.local file
New-Item -ItemType File -Name ".env.local" -Force

# Alternative method:
Out-File -FilePath ".env.local" -InputObject ""
```

**For Windows Command Prompt (CMD):**
```cmd
# Create .env.local file
type nul > .env.local

# Alternative method:
copy con .env.local
# Press Ctrl+Z then Enter to finish
```

**For Linux/macOS:**
```bash
# Create .env.local file
touch .env.local

# Alternative method:
echo "" > .env.local
```

**Open `.env.local` in your text editor and immediately add:**
```bash
INFLUXDB_URL=https://us-east-1-1.aws.cloud2.influxdata.com
INFLUXDB_TOKEN=placeholder-will-add-token-next
INFLUXDB_ORG=company-name
INFLUXDB_BUCKET=binance_ticks
BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade
```

**Replace the example URL with your actual copied URL and save the file.**

### 🔑 Create an API Token

1. Navigate to **Load Data → API Tokens**
2. Click **+ Generate API Token**
3. Select **All Access Token** (for initial setup)
4. Provide a description:
   ```
   Binance WebSocket Streamer - Write access to binance_ticks bucket
   ```
5. Click **Save**
6. **⚠️ CRITICAL: Copy the token and IMMEDIATELY update your `.env.local` file:**
   
   **Replace the placeholder token line in your `.env.local` file:**
   ```bash
   # Change this line:
   INFLUXDB_TOKEN=placeholder-will-add-token-next
   
   # To this (with your actual token):
   INFLUXDB_TOKEN=your-actual-api-token-here
   ```
   
   **Save the file immediately - you won't see this token again!**

### ✅ Verify Your Configuration

Your final `.env.local` file should look like this:
```bash
INFLUXDB_URL=https://us-east-1-1.aws.cloud2.influxdata.com
INFLUXDB_TOKEN=your-actual-api-token-here
INFLUXDB_ORG=company-name
INFLUXDB_BUCKET=binance_ticks
BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade
```

**🔒 Security Setup:**

**For Windows PowerShell:**
```powershell
# Add .env.local to .gitignore to prevent accidental commits
Add-Content -Path ".gitignore" -Value ".env.local"
```

**For Windows CMD:**
```cmd
# Add .env.local to .gitignore to prevent accidental commits
echo .env.local >> .gitignore
```

**For Linux/macOS:**
```bash
# Add .env.local to .gitignore to prevent accidental commits
echo ".env.local" >> .gitignore
```

**⚠️ Important Configuration Rules:**

- **Replace ALL placeholder values** with your actual values
- **No quotes around values**
- **No spaces around the `=` sign**
- **If you modify `.env.local` while the script is running, restart the Python script**
- **Add more trading pairs** by extending the `BINANCE_WS_URL` streams parameter

**🚨 Common File Creation Errors and Solutions:**

**Error in PowerShell: "The term 'echo.' is not recognized"**
```
echo. : The term 'echo.' is not recognized as the name of a cmdlet, function, script file, or operable program.
```
**Solution:** Use the PowerShell-specific commands provided above:
```powershell
New-Item -ItemType File -Name ".env.local" -Force
```

**Error in CMD: "The system cannot find the file specified"**
**Solution:** Use the CMD-specific commands:
```cmd
type nul > .env.local
```

**Error: "Access is denied" or "Permission denied"**
**Solution:** Run your terminal as administrator or use alternative methods:
```bash
# Try creating in a different location first, then move
cd %USERPROFILE%
echo. > temp.env
move temp.env path\to\your\project\.env.local
```

---

## 🧠 Step 5: Understanding the Code

Before running the streamer, let's understand what the code does:

### Key Components:

- **🔗 WebSocket Connection:** Connects to Binance's real-time trade stream for specified trading pairs
- **🎯 Data Processing:** Each trade tick contains:
  - **Symbol:** Trading pair (e.g., BTCUSDT)
  - **Price:** Stored as both string (full precision) and float (for queries)
  - **Timestamp:** Millisecond-precision UTC timestamp
- **🛡️ Error Handling:** 
  - Auto-reconnects on connection drops
  - Validates and skips malformed messages
  - Logs all activities for monitoring
- **☁️ InfluxDB Integration:** Writes validated ticks to the `price_ticks` measurement

### Main Script Flow:

```python
1. Load environment variables from .env.local
2. Connect to Binance WebSocket
3. For each received trade tick:
   a. Parse and validate the data
   b. Extract symbol, price, and timestamp
   c. Write to InfluxDB Cloud
   d. Log the activity
4. Handle errors and reconnect as needed
```

---

## ▶️ Step 6: Running the Streamer

Now you're ready to start streaming live cryptocurrency data!

### Start the Streamer:

```bash
python binance_ws_influxdb.py
```

### Expected Output:

You should see real-time output like:
```
Connected to Binance WebSocket
Processing tick: BTCUSDT @ 68341.15000000 at 2025-06-27T10:30:15.123Z
Processing tick: ETHUSDT @ 3456.78900000 at 2025-06-27T10:30:15.456Z
Data written to InfluxDB successfully
Processing tick: BTCUSDT @ 68342.00000000 at 2025-06-27T10:30:16.789Z
...
```

### 🛑 To Stop the Streamer:

Press `Ctrl+C` in your terminal.

### 🔧 Troubleshooting:

- **Connection errors:** Check your internet connection and InfluxDB credentials
- **Import errors:** Ensure all packages are installed correctly (see troubleshooting section in Step 2)
- **Environment errors:** Verify your `.env.local` file format and values
- **Permission errors:** Check your InfluxDB API token permissions

---

## 📈 Visualizing and Querying Your Data

Once data is streaming, you can analyze and visualize it:

### Using InfluxDB Data Explorer:

1. **Navigate to Data Explorer** by clicking on the bottom slider you will see the names of the sidebars in that click on Data Explorer.
2. **Select your bucket:** `binance_ticks`
3. **Choose measurement:** `price_ticks`
4. **Filter by symbol:** Select specific trading pairs
5. **Select fields:** Choose `price` for visualization
6. **Set time range:** Last 1 hour, 1 day, etc.
7. **Click on Run** to see your live price charts

### Integration with External Tools:

- **Grafana:** Create professional dashboards
- **Tableau:** Advanced analytics and visualization
- **Python/Jupyter:** Custom analysis with InfluxDB client
- **Excel/Google Sheets:** Export data for spreadsheet analysis

---

## 📊 Data Model

Understanding how your data is structured in InfluxDB:

### Measurement Structure:
- **Measurement Name:** `price_ticks`
- **Tags:** 
  - `symbol`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- **Fields:**
  - `price` (float): Optimized for queries and calculations
  - `price_str` (string): Full precision as received from Binance
- **Timestamp:** Trade execution time in UTC with millisecond precision

### Example Data Point:

| Time | Symbol | Price | Price String | 
|------|--------|-------|--------------|
| 2025-06-27T10:30:15.123Z | BTCUSDT | 68341.15 | "68341.15000000" |
| 2025-06-27T10:30:15.456Z | ETHUSDT | 3456.789 | "3456.78900000" |

---

## 🔒 Security Notes

Protect your setup and data:

### API Token Security:
- 🚫 **Never commit** `.env.local` to version control
- 🔒 **Use minimum permissions** for production tokens
- 🔄 **Rotate tokens regularly** for enhanced security
- 📋 **Store backups securely** in password managers

### Environment Variables Best Practices:
```bash
# Good: Use environment variables
INFLUXDB_TOKEN=your_token_here

# Bad: Hardcode in source code
token = "your_token_here"  # Never do this!
```

---

## 📬 Contact

For questions, suggestions, or collaboration:

- 📧 **Email:** [pavansai7654321@gmail.com](mailto:pavansai7654321@gmail.com)
- 🐛 **Issues:** Open an issue in this repository

---

## 📝 License

This project is provided for educational and research purposes. See [LICENSE](../../LICENSE) for full terms.

---

**🎉 Congratulations! You now have a professional-grade cryptocurrency data streaming system! 🚀💹**
# 🚀 Binance Tick Data Streamer to InfluxDB ☁️💹

[![Python](https://img.shields.io/badge/Python-3.8+-FFD43B?logo=python&logoColor=blue)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Latest-0DB7ED?logo=docker&logoColor=white)](https://www.docker.com/) 
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Latest-3371E3?logo=kubernetes&logoColor=white)](https://kubernetes.io/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-00C7B7?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Proprietary-E85C33)](../../LICENSE)

> A professional-grade Python application for streaming real-time Binance cryptocurrency tick data into InfluxDB Cloud, supporting robust analytics, research, and time-series dashboards.

---

## 📑 Table of Contents

- [📚 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Prerequisites](#️-prerequisites)
- [🧰 Installation Guide](#-installation-guide)
  - [🛠️ Step 1: Check and Install Git](#step-1-check-and-install-git)
    - [🔍 Check if Git is Already Installed](#check-if-git-is-already-installed)
    - [⬇️ If Git is Not Installed or Version is Too Old](#if-git-is-not-installed-or-version-is-too-old)
  - [🐍 Step 2: Check and Install Python](#step-2-check-and-install-python)
    - [🔍 Check if Python is Already Installed](#check-if-python-is-already-installed)
    - [⬇️ If Python is Not Installed or Version is Too Old](#if-python-is-not-installed-or-version-is-too-old)
  - [🐘 Step 3: Check and Install PostgreSQL](#step-3-check-and-install-postgresql)
    - [🔍 Check if PostgreSQL is Already Installed](#check-if-postgresql-is-already-installed)
    - [⬇️ If PostgreSQL is Not Installed or Version is Too Old](#if-postgresql-is-not-installed-or-version-is-too-old)
  - [📦 Step 4: Get the Code](#step-4-get-the-code)
    - [🔗 Clone the Repository](#clone-the-repository)
    - [🗂️ Verify Your Setup](#verify-your-setup)
  - [🛡️ Step 5: Create Database and User](#step-5-create-database-and-user)
    - [🔐 Access PostgreSQL](#access-postgresql)
    - [🗄️ Create Database and User](#create-database-and-user)
    - [✅ Test the Connection](#test-the-connection)
  - [🧪 Step 6: Set Up Python Virtual Environment](#step-6-set-up-python-virtual-environment)
    - [🌱 Create Virtual Environment](#create-virtual-environment)
    - [📥 Install Required Packages](#install-required-packages)
    - [🔎 Verify Activation and Installation](#verify-activation-and-installation)
  - [⚙️ Step 7: Create and Configure .env.local](#step-7-create-and-configure-envlocal)
    - [📄 Create Configuration File](#create-configuration-file)
    - [📝 Add Configuration](#add-configuration)
    - [🛠️ Configuration Options](#configuration-options)
- [🧠 Understanding the Code](#-understanding-the-code)
  - [🧩 Core Components](#core-components)
  - [🔄 Data Flow](#data-flow)
- [▶️ Running the Streamer](#️-running-the-streamer)
  - [🏁 Start the Application](#start-the-application)
  - [🖥️ Expected Output](#expected-output)
  - [🛑 Stop the Application](#stop-the-application)
  - [♻️ Managing the Virtual Environment](#managing-the-virtual-environment)
- [📊 Data Model](#-data-model)
  - [📋 Table Structure](#table-structure)
  - [🗂️ SQL Schema](#sql-schema)
  - [📈 Sample Data](#sample-data)
- [📈 Querying Your Data](#-querying-your-data)
  - [🔗 Connect to PostgreSQL](#connect-to-postgresql)
  - [🔎 Basic Queries](#basic-queries)
  - [📊 Advanced Analytics](#advanced-analytics)
- [🚨 Troubleshooting](#-troubleshooting)
  - [🧰 Common Issues and Solutions](#common-issues-and-solutions)
  - [🐞 Debug Mode](#debug-mode)
  - [🆘 Getting Help](#getting-help)
- [🔒 Security Notes](#-security-notes)
  - [🔏 Database Security](#database-security)
  - [🌐 Network Security](#network-security)
  - [🛡️ Code Security](#code-security)
- [📝 License](#-license)
- [📬 Contact](#-contact)
  - [🙋 Get Help & Support](#get-help--support)
  - [⏰ Response Times](#response-times)

---

## 📚 Project Overview

This project captures and stores high-frequency Binance trade data ("tick data") in real time, utilizing **PostgreSQL** for scalable, reliable, and millisecond-precision time-series storage. It is designed for developers, data scientists, and financial analysts who require accurate and high-resolution streaming price data for cryptocurrencies.

---

## ✨ Features

- **🔄 Real-Time Binance Trade Data:** Streams live trade ticks for multiple cryptocurrency pairs (e.g., BTCUSDT, ETHUSDT)
- **🎯 High-Precision Storage:** Records price as both a float (for queries) and a string (full decimal precision) to preserve accuracy
- **⚡ Millisecond Resolution:** Each trade is timestamped with UTC time at millisecond precision
- **🔧 Robust Connection Handling:** Automatically reconnects in case of WebSocket interruptions for uninterrupted data collection
- **🆓 Open Source Database:** Uses PostgreSQL, a battle-tested, scalable, and free open-source RDBMS
- **🚀 Production Ready:** Built with async/await for high performance and proper error handling

---

## 🏗️ Architecture

```
┌─────────────────┐    WebSocket     ┌───────────────────┐    asyncpg     ┌─────────────────┐
│   Binance API   │ ──────────────►  │  Python Streamer  │ ─────────────► │   PostgreSQL    │
│                 │  Real-time data  │                   │  Store ticks   │                 │
│ • BTCUSDT       │                  │ • Parse & Validate│                │ • price_ticks   │
│ • ETHUSDT       │                  │ • Error Handling  │                │ • Millisecond   │
│ • More pairs... │                  │ • Auto-reconnect  │                │   precision     │
└─────────────────┘                  └───────────────────┘                └─────────────────┘
```

**🔧 Components:**
- **Binance WebSocket API:** Provides continuous real-time trade events
- **Python Streamer:** Handles connection, parsing, validation, and database writes
- **PostgreSQL:** Stores tick data with high precision and performance

---

## 🛠️ Prerequisites

- **💻 Operating System:** Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **🔧 Git:** Version 2.0+ (for cloning the repository)
- **🐍 Python:** Version 3.8 or newer
- **🗄️ PostgreSQL:** Version 12+ (we'll help you install this)
- **🌐 Internet Connection:** Required for streaming data from Binance
- **⌨️ Command Line Access:** Basic familiarity with terminal/command prompt
- **❌ No Binance Account Required:** Uses public trade stream data

---

## 🧰 Installation Guide

### Step 1: Check and Install Git

Git is required to clone the repository from GitHub.

#### 🔍 Check if Git is Already Installed by command prompt or windows powershell

**🪟 Windows:**
```cmd
git --version
```

**🍎🐧 macOS/Linux:**
```bash
git --version
```

#### ✅ Version Requirements
- **Minimum Required:** Git 2.0+
- **Recommended:** Latest stable version

#### 📥 If Git is Not Installed or Version is Too Old

**🪟 Windows:**
1. Download Git from [git-scm.com](https://git-scm.com/downloads)
2. Run the installer with default settings
3. Restart Command Prompt/PowerShell
4. Verify: `git --version`

**🍎 macOS:**
```bash
# Using Homebrew (recommended)
brew install git

# Or download from git-scm.com
```

**🐧 Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

---

### Step 2: Check and Install Python

#### 🔍 Check if Python is Already Installed by command prompt or windows powershell


**🪟 Windows:**
```cmd
python --version
pip --version
```

**🍎🐧 macOS/Linux:**
```bash
python3 --version
pip3 --version
```

#### ✅ Version Requirements
- **Minimum Required:** Python 3.8+
- **Recommended:** Python 3.9+ or latest stable version

#### 📥 If Python is Not Installed or Version is Too Old

**🪟 Windows:**
1. **📥 Download Python:**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8+ (latest stable version recommended)

2. **💾 Install Python:**
   - Run the installer
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
   - Choose "Install Now"

3. **✅ Verify Installation:**
   ```cmd
   python --version
   pip --version
   ```

**🍎 macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**🐧 Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

### Step 3: Check and Install PostgreSQL 

#### 🔍 Check if PostgreSQL is Already Installed by command prompt or windows powershell

**🪟🍎🐧 All Platforms:**
```bash
psql --version
```

#### ✅ Version Requirements
- **Minimum Required:** PostgreSQL 12+
- **Recommended:** PostgreSQL 14+ or latest stable version

#### 📥 If PostgreSQL is Not Installed or Version is Too Old

**🪟 Windows:**
1. **📥 Download PostgreSQL:**
   - Go to [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Download the latest stable version

2. **💾 Install PostgreSQL:**
   - Run the installer
   - Remember the password you set for the `postgres` user
   - Default port 5432 is usually fine
   - Install pgAdmin (database management tool) when offered

3. **✅ Verify Installation:**
   ```cmd
   psql --version
   ```

**🍎 macOS:**
```bash
# Using Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Verify installation
psql --version
```

**🐧 Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

---

### Step 4: Get the Code

#### 📥 Clone the Repository

> **⚠️ Note:**  
> On Windows, you should open Command Prompt or PowerShell in a folder where you have full write permissions. This can be your user folder (like `C:\Users\YourUsername`), a subfolder (such as `C:\Users\YourUsername\Projects`), or any other folder you create on other drives (for example, `D:\Projects`, `E:\Crypto`, etc.).  
>  
> **Do not** run commands from system folders like `C:\Windows\System32`—this may cause permission errors.

**🪟 Windows:**
```cmd
# Navigate to your desired location
cd C:\Users\YourUsername\Projects

# Clone the repository
git clone https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git

# Navigate to the project files
cd "AI-Backend-Hiring-Tasks-Prodigal-AI\Task 5 - Binance WebSocket Price Precision\binance-websocket-ticker"
```

**🍎🐧 macOS/Linux:**
```bash
# Navigate to your desired location
cd ~/Projects

# Open the command prompt in that directory and clone the repository
git clone https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git

# Navigate to the project files
cd "AI-Backend-Hiring-Tasks-Prodigal-AI/Task 5 - Binance WebSocket Price Precision/binance-websocket-ticker"
```

#### 📂 Verify Your Setup

**🪟 Windows:**
```cmd
dir
```

**🍎🐧 macOS/Linux:**
```bash
ls -la
```

**✅ You should see files like:**
- `binance_ws_postgres.py` (main application)
- `requirements.txt` (Python dependencies)
- `README.md` (this file)

---

### Step 5: Create Database and User

#### 🔐 Access PostgreSQL

**🪟 Windows:**
```cmd
# Using terminal
psql -U postgres

# Or find "SQL Shell (psql)" in Start Menu
```

**🍎🐧 macOS/Linux:**
```bash
# Access PostgreSQL as postgres user
sudo -u postgres psql

# Or if you installed via Homebrew on macOS:
psql postgres
```

#### 🗄️ Create Database and User

Once in the PostgreSQL shell (you'll see `postgres=#`), run these commands:

```sql
-- Create a new database for our project
CREATE DATABASE binance_ticker_db;

-- Create a new user with a secure password
CREATE USER binance_user WITH PASSWORD 'your_secure_password_here';

-- Grant all privileges on the database to our user
GRANT ALL PRIVILEGES ON DATABASE binance_ticker_db TO binance_user;

-- Grant connection privileges
GRANT CONNECT ON DATABASE binance_ticker_db TO binance_user;

-- Exit PostgreSQL shell
\q
```

#### 🧪 Test the Connection
```bash
# Test connecting with your new user
psql -h localhost -U binance_user -d binance_ticker_db

# It will ask to enter the Password for user binance_user
```

**💡 Tips:**
- Replace `your_secure_password_here` with a strong password
- Write down your database credentials - you'll need them for configuration
- If you prefer, you can use the default `postgres` user instead

---

### Step 6: Set Up Python Virtual Environment

Virtual environments keep your project dependencies isolated and prevent conflicts with other Python projects.

#### 🐍 Create Virtual Environment

**🪟 Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv binance_env

# Activate the virtual environment
.\binance_env\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**🪟 Windows Command Prompt / terminal:**
```cmd
# Create virtual environment
python -m venv binance_env

# Activate the virtual environment
binance_env\Scripts\activate.bat
```

**🍎🐧 macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv binance_env

# Activate the virtual environment
source binance_env/bin/activate
```

#### ✅ Verify Activation
After activation, you should see `(binance_env)` at the beginning of your terminal.

#### 📋 Install Required Packages

With your virtual environment activated:

**🎯 Method A: Install from requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**🔧 Method B: Install packages individually**
```bash
pip install websockets==12.0
pip install asyncpg==0.29.0
pip install python-dotenv==1.0.0
```

#### 🔍 Verify Installation
```bash
python -c "import websockets, asyncpg, dotenv; print('All packages installed successfully!')"
```

---

### Step 7: Create and Configure .env.local

#### 📝 Create Configuration File

Create a file named `.env.local` in your project root directory (same folder as `binance_ws_postgres.py`). This file will store your database credentials and configuration.

**⚠️ Important:** The `.env.local` file is not included in the repository for security reasons. You must create it yourself.

**🪟 Windows (using Notepad):**
```cmd
notepad .env.local
```

**🍎🐧 macOS/Linux (using nano):**
```bash
nano .env.local
```

#### ⚙️ Add Configuration

Copy and paste this configuration, replacing the values with your actual database credentials:

```env
# PostgreSQL Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=binance_ticker_db
POSTGRES_USER=binance_user
POSTGRES_PASSWORD=your_secure_password_here

# Binance WebSocket URL (you can modify the trading pairs)
BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade
```

#### 🔧 Configuration Options

**📊 Trading Pairs:**
You can modify the `BINANCE_WS_URL` to include different trading pairs:

```env
# Single pair
BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade

# Multiple pairs
BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade/adausdt@trade/dotusdt@trade
```

**⚠️ Important Notes:**
- **Do not use quotes** around values
- **No spaces** around the `=` sign
- **Add `.env.local` to `.gitignore`** to keep credentials safe
- 💡 Replace `your_secure_password_here` with your actual PostgreSQL password

---

## 🧠 Understanding the Code

### 🔧 Core Components

**1. 🌐 WebSocket Connection Management**
```python
# Connects to Binance's real-time trade stream
async with websockets.connect(BINANCE_WS_URL) as ws:
    # Handles reconnection automatically on disconnects
```

**2. 📈 Tick Data Processing**
Each trade tick contains:
- **📊 Symbol:** Trading pair (e.g., "BTCUSDT")
- **💰 Price:** Trade price (stored as both string and decimal for precision)
- **🕒 Timestamp:** Millisecond-precision UTC timestamp

**3. 🗄️ Database Storage**
```python
# High-precision storage with millisecond timestamps
INSERT INTO price_ticks (symbol, price_str, price, ts)
VALUES ($1, $2, $3, $4);
```

**4. 🛡️ Error Handling**
- **🔄 Auto-reconnect:** Automatically reconnects on connection drops
- **✅ Data validation:** Skips malformed messages with logging
- **⚡ Connection pooling:** Efficient database connection management

### 🔄 Data Flow
1. **🔗 Connect** to Binance WebSocket stream
2. **📥 Receive** real-time trade messages
3. **🔍 Parse** and validate each message
4. **⚙️ Convert** timestamp and price data
5. **💾 Store** in PostgreSQL with full precision
6. **📝 Log** successful writes and handle errors

---

## ▶️ Running the Streamer

### 🏁 Start the Application

1. **✅ Ensure your virtual environment is activated:**
   You should see `(binance_env)` in your prompt.

2. **📂 Navigate to your project directory:**
   ```bash
   cd /path/to/AI-Backend-Hiring-Tasks-Prodigal-AI/Task\ 5\ -\ Binance\ WebSocket\ Price\ Precision/binance-websocket-ticker
   ```

3. **🚀 Run the streamer:**
   ```bash
   python binance_ws_postgres.py
   ```

### 📺 Expected Output

You should see output like this:

```
Connecting to Binance WebSocket...
✅ Connected! Streaming BTCUSDT & ETHUSDT ticks...
Press Ctrl+C to stop.

[BTCUSDT] 61345.32000000 at 2025-06-30 19:05:05.123456 UTC
[ETHUSDT] 3450.12000000 at 2025-06-30 19:05:03.789123 UTC
[BTCUSDT] 61346.15000000 at 2025-06-30 19:05:07.456789 UTC
[ETHUSDT] 3449.98000000 at 2025-06-30 19:05:09.123456 UTC
...
```

### 🛑 Stop the Application

Press `Ctrl+C` to stop the streamer gracefully:

```
^C
Stopped Binance WebSocket to PostgreSQL streamer.
```

### 🔄 Managing the Virtual Environment

**❌ To deactivate when done:**
```bash
deactivate
```

**✅ To reactivate later:**
```bash
# Windows PowerShell
.\binance_env\Scripts\Activate.ps1

# Windows CMD
binance_env\Scripts\activate.bat

# macOS/Linux
source binance_env/bin/activate
```

---

## 📊 Data Model

### 🗄️ Table Structure

**📋 Table Name:** `price_ticks`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PRIMARY KEY | 🔢 Auto-incrementing unique identifier |
| `symbol` | TEXT NOT NULL | 📊 Trading pair symbol (e.g., "BTCUSDT") |
| `price_str` | TEXT NOT NULL | 💰 Price as string (preserves full precision) |
| `price` | NUMERIC(30,12) NOT NULL | 📈 Price as decimal (for calculations) |
| `ts` | TIMESTAMPTZ NOT NULL | 🕒 UTC timestamp with millisecond precision |

### 🔧 SQL Schema

The table is automatically created when you first run the application:

```sql
CREATE TABLE IF NOT EXISTS price_ticks (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price_str TEXT NOT NULL,
    price NUMERIC(30, 12) NOT NULL,
    ts TIMESTAMPTZ NOT NULL
);
```

### 📋 Sample Data

| id | symbol | price_str | price | ts |
|----|--------|-----------|-------|-----|
| 1 | BTCUSDT | 61345.32000000 | 61345.320000000000 | 2025-06-30 19:05:05.123456+00 |
| 2 | ETHUSDT | 3450.12000000 | 3450.120000000000 | 2025-06-30 19:05:07.789123+00 |

---

## 📈 Querying Your Data

### 🔗 Connect to PostgreSQL

```bash
# Connect to your database
psql -h localhost -U binance_user -d binance_ticker_db
```

### 📊 Basic Queries

**👀 View recent trades:**
```sql
SELECT * FROM price_ticks 
ORDER BY ts DESC 
LIMIT 10;
```

**📊 Count total trades:**
```sql
SELECT COUNT(*) as total_trades FROM price_ticks;
```

**📈 Trades by symbol:**
```sql
SELECT symbol, COUNT(*) as trade_count 
FROM price_ticks 
GROUP BY symbol 
ORDER BY trade_count DESC;
```

**💰 Price range for a symbol:**
```sql
SELECT 
    symbol,
    MIN(price) as min_price,
    MAX(price) as max_price,
    AVG(price) as avg_price
FROM price_ticks 
WHERE symbol = 'BTCUSDT'
GROUP BY symbol;
```

**🕒 Recent trades with time formatting:**
```sql
SELECT 
    symbol,
    price,
    TO_CHAR(ts, 'YYYY-MM-DD HH24:MI:SS.MS TZ') as formatted_time
FROM price_ticks 
ORDER BY ts DESC 
LIMIT 5;
```

**⏰ Trades in the last hour:**
```sql
SELECT * FROM price_ticks 
WHERE ts >= NOW() - INTERVAL '1 hour'
ORDER BY ts DESC;
```

### 🔍 Advanced Analytics

**📊 Price movements over time:**
```sql
SELECT 
    symbol,
    DATE_TRUNC('minute', ts) as minute,
    COUNT(*) as trades,
    MIN(price) as low,
    MAX(price) as high,
    FIRST(price ORDER BY ts) as open,
    LAST(price ORDER BY ts) as close
FROM price_ticks 
WHERE ts >= NOW() - INTERVAL '1 hour'
GROUP BY symbol, minute
ORDER BY symbol, minute;
```

---

## 🚨 Troubleshooting

### 🔧 Common Issues and Solutions

#### 1. **❌ ModuleNotFoundError: No module named 'websockets'**

**🔍 Problem:** Python can't find the required modules.

**✅ Solution:**
```bash
# Ensure virtual environment is activated (you should see (binance_env) in prompt)
source binance_env/bin/activate  # Linux/macOS
# or
.\binance_env\Scripts\Activate.ps1  # Windows

# Reinstall packages
pip install -r requirements.txt

# Verify installation
python -c "import websockets, asyncpg, dotenv; print('Success!')"
```

#### 2. **🔌 Connection refused to PostgreSQL**

**🔍 Problem:** Can't connect to PostgreSQL database.

**✅ Solutions:**
- **🔍 Check PostgreSQL is running:**
  ```bash
  # Linux/macOS
  sudo systemctl status postgresql
  
  # macOS with Homebrew
  brew services list | grep postgresql
  
  # Windows - check Services app for "postgresql" service
  ```

- **🧪 Verify database credentials:**
  ```bash
  # Test connection manually
  psql -h localhost -U binance_user -d binance_ticker_db
  ```

- **📝 Check `.env.local` file:**
  - Ensure no quotes around values
  - Verify password matches what you set
  - Check for typos in database name/username

#### 3. **🌐 WebSocket connection errors**

**🔍 Problem:** Can't connect to Binance WebSocket.

**✅ Solutions:**
- **🌐 Check internet connection**
- **🔍 Verify Binance URL in `.env.local`**
- **🛡️ Check firewall/antivirus settings**
- **🔄 Try a different network (sometimes corporate firewalls block WebSocket connections)**

#### 4. **🔒 Permission denied errors**

**🔍 Problem:** Can't create virtual environment or install packages.

**✅ Solutions:**
```bash
# Linux/macOS - ensure you have permission to write in current directory
sudo chown -R $USER:$USER ~/Projects/AI-Backend-Hiring-Tasks-Prodigal-AI

# Windows - run Command Prompt as Administrator

# Alternative: use --user flag (not recommended for virtual environments)
pip install --user websockets asyncpg python-dotenv
```

#### 5. **🔄 Virtual environment not activating**

**🔍 Problem:** Virtual environment activation fails.

**✅ Solutions:**
```bash
# Windows - try different methods
.\binance_env\Scripts\activate.bat
# or
.\binance_env\Scripts\Activate.ps1

# Linux/macOS - ensure you're using 'source'
source binance_env/bin/activate

# If still failing, recreate the environment
rm -rf binance_env
python3 -m venv binance_env
```

#### 6. **🗄️ Database table creation errors**

**🔍 Problem:** Can't create the `price_ticks` table.

**✅ Solutions:**
```sql
-- Connect to PostgreSQL and manually grant permissions
\c binance_ticker_db
GRANT ALL PRIVILEGES ON SCHEMA public TO binance_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO binance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO binance_user;
```

#### 7. **📦 ModuleNotFoundError: No module named 'pip._internal'**

**🔍 Problem:**  
Your virtual environment is missing pip, or pip is corrupted.

**✅ Solutions:**
- **🔄 Delete and recreate the virtual environment using Python 3.8 or newer:**
  ```cmd
  rmdir /s /q binance_env
  python -m venv binance_env
  binance_env\Scripts\activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```
- **🐍 Make sure you are using Python 3.8 or newer,** not Python 3.7 or below.
- If you have multiple Python versions, specify the right one:
  ```cmd
  py -3.8 -m venv binance_env
  ```

**❓ Why this happens:**  
This occurs if pip isn't installed properly in the virtual environment, or if you're using an outdated Python version.

### 🔍 Debug Mode

Add this to your `.env.local` for more detailed logging:
```env
DEBUG=True
```

Then modify the script to add more verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 🆘 Getting Help

If you're still having issues:

1. **🔍 Check the error message carefully** - it usually contains the solution
2. **✅ Verify each step** - ensure you didn't skip anything
3. **🧪 Test components individually:**
   - Test PostgreSQL connection separately
   - Test internet connectivity
   - Verify Python environment setup

---

## 🔒 Security Notes

### 🗄️ Database Security
- **🔐 Use strong passwords** for your PostgreSQL user (mix of letters, numbers, symbols)
- **🔒 Restrict database access** to localhost only for development
- **❌ Never commit `.env.local`** to version control
- **🌐 Use environment variables** in production, not `.env.local` files

### 🛡️ Network Security
- **🔥 Firewall rules:** Ensure PostgreSQL port (5432) is not exposed to the internet
- **🔒 VPN usage:** Consider using a VPN if running on public networks
- **🔐 HTTPS only:** The Binance WebSocket connection uses WSS (secure WebSocket)

### 🔧 Code Security
- **🔄 Keep dependencies updated:** Regularly update Python packages
- **👀 Code review:** Review any modifications before running in production
- **💾 Backup data:** Regularly backup your PostgreSQL database

---

## ⚖️ License

This project is **not open source**. All rights reserved.

### See the [LICENSE](../../LICENSE) file for details.
---

---

## 📬 Contact

### 🆘 Get Help & Support

**🔧 For technical questions or issues:**
- 📧 **Email:** pavansai7654321@gmail.com
- 🐛 **Bug Reports:** Create an issue with detailed error logs
- 💡 **Feature Requests:** Describe your use case and requirements

**🤝 For collaboration or commercial use:**
- **Partnerships:** Contact for enterprise implementations
- **Custom Development:** Available for custom features or integrations
- **Consulting:** Data pipeline architecture and optimization

### ⏰ Response Times
- **🐛 Bug reports:** 24-48 hours
- **❓ General questions:** 2-3 business days
- **💡 Feature requests:** 1 week for initial feedback

---

**⭐ If this project helps you, please consider giving it a star!**

**🔔 Watch the repository for updates and new features.**

---
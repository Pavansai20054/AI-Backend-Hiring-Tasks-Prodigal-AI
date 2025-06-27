# 🚀 Binance Tick Data Streamer to InfluxDB ☁️💹

A professional-grade Python application for streaming real-time Binance cryptocurrency tick data into InfluxDB Cloud, supporting robust analytics, research, and time-series dashboards.

---

## 📑 Table of Contents

- [🚀 Binance Tick Data Streamer to InfluxDB ☁️💹](#-binance-tick-data-streamer-to-influxdb-️)
  - [📑 Table of Contents](#-table-of-contents)
  - [📚 Project Overview](#-project-overview)
  - [✨ Features](#-features)
  - [🛠️ Prerequisites](#️-prerequisites)
  - [🧰 How to Get the Code (Clone the Directory)](#-how-to-get-the-code-clone-the-directory)
  - [🏗️ Architecture](#️-architecture)
  - [🥇 Step 1: Create Your InfluxDB Cloud Account](#-step-1-create-your-influxdb-cloud-account)
  - [🏷️ Step 2: Set Up InfluxDB for the Project](#️-step-2-set-up-influxdb-for-the-project)
    - [🪣 Create a Bucket / Database](#-create-a-bucket--database)
    - [🌐 InfluxDB URL](#-influxdb-url)
    - [🔑 Create an API Token](#-create-an-api-token)
  - [🔧 Step 3: Create and Configure the `.env.local` File](#-step-3-create-and-configure-the-envlocal-file)
  - [📦 Step 4: Install Required Python Packages](#-step-4-install-required-python-packages)
  - [🧠 Step 5: Understanding the Code](#-step-5-understanding-the-code)
  - [▶️ Step 6: Running the Streamer](#️-step-6-running-the-streamer)
  - [📊 Data Model](#-data-model)
  - [📈 Visualize and Query Your Data](#-visualize-and-query-your-data)
  - [🔒 Security Notes](#-security-notes)
  - [📬 Contact](#-contact)
  - [📝 License](#-license)

---

## 📚 Project Overview

This project captures and stores high-frequency Binance trade data (“tick data”) in real time, utilizing InfluxDB Cloud for scalable time-series storage.  
It is designed for developers, data scientists, and financial analysts who require accurate and high-resolution streaming price data for cryptocurrencies.  
You can use this data for algorithmic trading, research, or real-time dashboards.

---

## ✨ Features

- ⚡ **Real-Time Binance Trade Data:** Streams live trade ticks for multiple cryptocurrency pairs (e.g., BTCUSDT, ETHUSDT).
- 🧮 **High-Precision Storage:** Records price as both a float (for queries) and a string (full decimal precision) to preserve accuracy.
- ⏱️ **Millisecond Resolution:** Each trade is timestamped with UTC time at millisecond precision.
- 🔁 **Robust Connection Handling:** Automatically reconnects in case of WebSocket interruptions for uninterrupted data collection.
- ☁️ **Cloud-Native Integration:** Designed for InfluxDB Cloud, allowing instant access to data from anywhere and integration with visualization tools.

---

## 🛠️ Prerequisites

- 🐍 Python 3.8 or newer
- 💻 Command-line familiarity (Windows, Linux, or macOS)
- ☁️ Free [InfluxDB Cloud](https://cloud2.influxdata.com/signup) account (no credit card required for free tier)
- 🏦 *No Binance account required* (public trade stream)

---

## 🧰 How to Get the Code (Clone the Directory)

To keep your setup lightweight, **clone only the Task 5 - Binance WebSocket Price Precision directory** from the main repository.  
Follow these steps:

1. **Create a folder for this project and navigate into it:**
    ```bash
    mkdir binance-websocket-ticker
    ```

    ```bash
    cd binance-websocket-ticker
    ```

2. **Clone only the Task 5 directory from the repository using sparse checkout:**
    ```bash
    git clone --depth 1 --filter=blob:none --sparse https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git .
    ```

    ```bash
    git sparse-checkout init --cone
    ```

    ```bash
    git sparse-checkout set "Task 5 - Binance WebSocket Price Precision"
    ```

    ```bash
    cd "Task 5 - Binance WebSocket Price Precision/binance-websocket-ticker"
    ```

This will fetch **only** the `Task 5 - Binance WebSocket Price Precision` directory and its content, making your setup fast and focused.

---
---

## 🏗️ Architecture

The architecture of this project is designed for reliability, error-handling, and real-time data streaming:

- 🔌 **Binance WebSocket API:**  
  Provides a continuous, real-time stream of cryptocurrency trade events for selected trading pairs.

- 🐍 **Python Streamer (asyncio & websockets):**
  - Connects to Binance's WebSocket API and listens for incoming tick data using asynchronous networking.
  - Parses and validates each tick, extracting the trade pair, price (as string and float), and timestamp.
  - Handles errors robustly:
    - 🔃 Automatically reconnects if the WebSocket connection drops (due to network issues or server-side events).
    - 📝 Logs and skips malformed or invalid messages, so only clean, valid data is processed.
    - 🛡️ Ensures data integrity before writing to InfluxDB Cloud.

- ☁️ **InfluxDB Cloud:**
  - Receives and stores each tick as a time-series data point in the `price_ticks` measurement.
  - Supports millisecond-precision timestamps for high-frequency analytics and visualization.

**Architecture Data Flow:**

```
[Binance WebSocket API] --(tick data)--> [Python Streamer]
       |                                  |
       |--(connection errors)--> [Auto-Reconnect Logic]
                                        |
[Python Streamer] --(validated tick)--> [InfluxDB Cloud]
         |
         |--(write errors)--> [Error Log, Retry]
```

This ensures that the system is resilient to network interruptions and that only high-quality, valid data is persisted.

---

## 🥇 Step 1: Create Your InfluxDB Cloud Account

1. Visit [InfluxDB Cloud Signup](https://cloud2.influxdata.com/signup).

2. Sign up using your preferred registration method:
   - Click **GOOGLE** or **MICROSOFT** to sign up instantly with your existing account.
   - Or, fill in your details (First Name, Last Name, Email, Password) and click **CREATE ACCOUNT**.
   - If you already have an account, click **LOG IN** and proceed.

3. Upon successful sign-up, you will be prompted to set up your workspace:
   - **Workspace Details:** Set your company/account name and your first organization/project.  
     For example, you can use "Prodigal AI" as Company and "Binance WebSocket Live Feed" as Project.
   - **Storage Provider:** Choose your preferred cloud storage region (e.g., AWS US East).
   - Agree to the terms and continue.

4. Next, you will be asked to select a plan:
   - 🆓 **Free:** Ideal for getting started. 30 days storage, no credit card required.
   - 💼 **Usage-Based or Annual:** For higher limits and enterprise features. You can upgrade at any time.
   - Proceed with the Free plan.

5. After selecting the plan, you will enter the InfluxDB Cloud dashboard.

---

## 🏷️ Step 2: Set Up InfluxDB for the Project

### 🪣 Create a Bucket / Database

1. Navigate to **Data Explorer → Buckets**.
2. Click **Create Bucket**.
3. Name your bucket, e.g., `binance_ticks`.
4. Set a retention period (e.g., 1 day if you want to store only the latest data, or longer for more historical data).

### 🌐 InfluxDB URL

- Copy the “URL” field, e.g., `https://us-east-1-1.aws.cloud2.influxdata.com`.

### 🔑 Create an API Token

1. Go to **Load Data → API Tokens**.
2. Click **Generate API Token**.
3. Select **All Access Token** (for initial setup; restrict permissions for production).
4. Provide a short description, for example:
   - `API token for writing Binance price data to binance_ticks bucket`
  
      or 
  
   - `Binance WebSocket Live Feed - Python data writer for binance_ticks bucket`
5. Copy and save your token securely— in .env.local file which is required for your Python script.

---

## 🔧 Step 3: Create and Configure the `.env.local` File

To keep your credentials and configuration secure and flexible, this project uses a `.env.local` file for environment variables.

**How to set up and use `.env.local`:**

1. **Create a file named `.env.local`** in your project root (same directory as your Python script).

2. **Add your credentials and settings** in the following format (no quotes, no spaces around `=`):

    ```bash
    INFLUXDB_URL=https://us-east-1-1.aws.cloud2.influxdata.com
    INFLUXDB_TOKEN=your-generated-api-token
    INFLUXDB_ORG=Binance WebSocket Live Feed
    INFLUXDB_BUCKET=binance_ticks
    BINANCE_WS_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade
    ```

    - ❌ Do **not** use quotes around values.
    - ❌ Do **not** add spaces before or after the `=`.

3. **If you change any values** in `.env.local` while your script is running, **stop and restart your Python script** to load the new values.

4. **For security:**  
   - 🚫 Do **not** commit `.env.local` to version control.  
   - ➕ Add `.env.local` to your `.gitignore` file.

5. **Your Python code must load** this file using:
    ```python
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=".env.local")
    ```

By following these steps and formatting rules, your Python application will reliably load all necessary secrets and configuration from `.env.local`.

---

## 📦 Step 4: Install Required Python Packages

Install the dependencies using pip:

```bash
pip install websockets==12.0 influxdb-client==1.49.0 python-dotenv==1.1.0
```

You can also install from `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 🧠 Step 5: Understanding the Code

**Key Components:**

- 🔗 **WebSocket Connection:**  
  The script connects to Binance’s WebSocket stream for one or more trading pairs (e.g., BTCUSDT, ETHUSDT). The URL can be customized to add more pairs.

- 🎯 **Tick Data Handling:**  
  Each incoming trade tick is parsed to extract:
  - **Symbol:** Trading pair (e.g., BTCUSDT)
  - **Price:** As a string and as a float for precision and speed
  - **Timestamp:** Millisecond UTC timestamp from Binance

- 🛡️ **Error Handling & Reconnection:**  
  - If the WebSocket disconnects or an error occurs, the script automatically attempts to reconnect after a short delay.
  - Invalid or malformed messages are logged and safely skipped.

- ☁️ **InfluxDB Write Operation:**  
  Each tick is written to InfluxDB as a new point in the `price_ticks` measurement, using both precise and float price fields. The timestamp is stored with millisecond resolution for high-frequency analysis.

- 📝 **Logging:**  
  Each processed tick is logged to the terminal for monitoring.

---

## ▶️ Step 6: Running the Streamer

To start streaming data:

1. Ensure your InfluxDB Cloud account, bucket, and token are ready.
2. Edit your `.env.local` as needed.
3. Run the following command in your terminal:

```bash
python stream_binance.py
```

You should see real-time output in your terminal, showing the symbols, prices, and timestamps for each trade tick as they are ingested.

---

## 📊 Data Model

- **Measurement:** `price_ticks`
- **Tags:** `symbol` (the trading pair, e.g., BTCUSDT)
- **Fields:**
  - `price` (float): Quick access for queries/visualization
  - `price_str` (string): Full-precision price as received from Binance
- **Timestamp:** Trade time in UTC, with millisecond precision

Example point in InfluxDB:

| time                       | symbol   | price          | price_str         |
|----------------------------|----------|----------------|-------------------|
| 2025-06-26T19:40:00.123Z   | BTCUSDT  | 68341.15       | "68341.15000000"  |

---

## 📈 Visualize and Query Your Data

1. In InfluxDB Cloud, navigate to **Data Explorer**.
2. Select your bucket (`binance_ticks`).
3. Choose the `price_ticks` measurement.
4. Use the filter panel to select one or more symbols (tags).
5. Plot the `price` field over time to visualize real-time crypto price movements.
6. You can also query the data with Flux (InfluxDB’s query language) for custom analysis.

---

## 🔒 Security Notes

- 🛡️ **API Token Safety:**  
  Never share your InfluxDB API token publicly or commit it to a public repository.
- 🔐 **Token Permissions:**  
  For production, generate tokens with the minimum required permissions for improved security.
- 🗃️ **Environment Variables:**  
  Store sensitive credentials in environment variables or configuration files not tracked by version control.

---

## 📬 Contact

For questions, suggestions, or collaboration, please open an issue in this repository or contact the maintainer at [pavansai7654321@gmail.com](mailto:pavansai7654321@gmail.com) ✉️

---

## 📝 License

This project is provided for educational and research purposes. See [LICENSE](../../LICENSE) for full terms.

---

**Happy Streaming! 🚦💹🚀**
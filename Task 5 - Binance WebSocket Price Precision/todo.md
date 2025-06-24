# 📈 Binance WebSocket Price Precision Capture (BTC/ETH)

---

## 🎯 **Objective**

**Stream, store, and query high-precision live price data for BTC/USDT & ETH/USDT from Binance WebSocket, with robust DB design for analytics.**

---

## 🛠️ **Setup Overview**

- 🔌 **Connect to Binance WebSocket** for BTC/USDT and ETH/USDT.
- ⚡ **Handle high-frequency, multi-millisecond updates.**
- 🗃️ **Store price ticks** with:
  - Timestamp (high precision)
  - Symbol (BTCUSDT or ETHUSDT)
  - Price (as string/decimal for precision)
- 🏦 **Database**: Design for 1-day retention per pair (PostgreSQL or InfluxDB).

---

## 📦 **Deliverables**

- [ ] **WebSocket client** (Node.js or Python)
- [ ] **DB schema** & efficient storage logic
- [ ] **Sample queries** with expected output:
  - Latest price
  - Price at a specific second
  - Highest/Lowest price in a 1-minute interval

---

## 🌈 **Main Things To Do (Highlights)**

---

### 1. **WebSocket Client**
- Connect to Binance streams for BTCUSDT and ETHUSDT prices.
- Efficiently parse and buffer high-frequency price updates.

---

### 2. **Database Schema & Storage**
- Design a table for:
  - `timestamp` (with millisecond precision)
  - `symbol`
  - `price` (as decimal/numeric)
- Insert all ticks with minimal latency.
- Implement retention policy for 1-day data.

---

### 3. **Efficient Querying**
- **Get latest price** for a symbol.
- **Get price at a specific second** (rounded/closest tick).
- **Get highest/lowest price** in a given 1-minute window.

---

### 4. **Demonstrate & Document**
- Show sample inserts and query outputs (screenshots or code output).

---

## 🚀 **Tech Stack**

| Layer           | Technology              |
|-----------------|------------------------|
| WebSocket Client| **Python** (`websockets`, `asyncio`) or **Node.js** (`ws`) |
| Data Storage    | **PostgreSQL** (precise, relational) / **InfluxDB** (time-series) |
| ORM/Driver      | **SQLAlchemy**, `psycopg2`, or InfluxDB client |
| Visualization   | (Optional) **Jupyter Notebook** or CLI |

---

## 📝 **Summary Table**

| Step                  | What to Do                                |
|-----------------------|-------------------------------------------|
| WebSocket Connect     | Stream BTC/USDT & ETH/USDT price ticks    |
| Store Price Data      | Save (timestamp, symbol, price) to DB     |
| Retention Logic       | Keep 1 day of data per pair               |
| Query: Latest Price   | Fetch most recent tick for a symbol       |
| Query: Price at Sec   | Fetch or round to tick at given second    |
| Query: 1-min Stats    | Find high/low in a given minute window    |

---

## 💡 **Tips**

- Use **decimal** types for price in DB for highest accuracy!
- Batch inserts for better write throughput under high load.
- Index by (`symbol`, `timestamp`) for rapid querying.
- Timezone: Always use UTC for timestamps.

---

> **Pro-Tip:**  
> Use markdown tables, code highlights, and diagrams in your final docs for clarity and color!
> For bonus points, add retention policy SQL or InfluxDB config, and pretty-print sample query results.

---
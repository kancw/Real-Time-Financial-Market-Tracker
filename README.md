# Advanced Asset Terminal (v3)

This iteration upgrades the financial dashboard to include **Data Visualization** and **Time-Series Analytics**, fully integrated within the Docker microservices architecture.

## Key Enhancements in v3:
1. **Time-Series Data Extraction:** The Python backend now fetches 7-day historical arrays using Pandas and packages them alongside real-time quotes.
2. **Chart.js Integration:** The Nginx frontend dynamically renders smooth, responsive sparkline charts (`<canvas>`) showing the 7-day asset trend.
3. **Dynamic UI Rendering:** The chart automatically colors itself green (bullish) or red (bearish) based on the asset's current performance.
4. **Market State Detection:** Displays whether the relevant exchange is currently Open (REGULAR) or Closed based on Yahoo Finance metadata.
5. **Popular Stock Shortcuts:** Select Apple, Microsoft, NVIDIA, Amazon, Alphabet, Meta, Tesla, or JPMorgan to load its quote and 7-day trend without typing a ticker.

## Supported Financial Markets & Asset Classes

| Market Segment | Coverage | Example Tickers Supported |
| :--- | :--- | :--- |
| **US Financial Markets** | Equities, Mega-cap Tech, Index ETFs | `AAPL`, `NVDA`, `MSFT`, `SPY`, `QQQ` |
| **China Markets** | Hong Kong Exchanges (HKEX), Shanghai (SSE), Shenzhen (SZSE) | `0700.HK` (Tencent), `9988.HK` (Alibaba), `600519.SS` (Moutai), `000001.SS` (SSE Index) |
| **Alternative Markets** | Digital Assets (Crypto), Hard Commodities, Real Estate REITs | `BTC-USD`, `ETH-USD`, `GC=F` (Gold), `CL=F` (Crude Oil), `VNQ` (Vanguard Real Estate) |

---

## Core Architecture & Docker Containerization

The application is deployed using a decoupled, production-grade microservices pattern orchestrated via `docker-compose.yml`:

1. **Nginx Edge Reverse Proxy (`frontend`)**:
   - Binds public port `80`.
   - Serves an interactive responsive dashboard and handles internal reverse-proxy routing (`/api/*` redirected to the backend container).
2. **FastAPI Intelligence Engine (`backend`)**:
   - Uses multi-stage Docker builds to reduce image attack surface and footprint.
   - Implements automatic ticker market classification, currency conversions, and rate-limiting safeguards.
3. **Redis In-Memory Key-Value Store (`redis`)**:
   - Caches incoming ticker data with a 60-second TTL (Time to Live) to prevent upstream API exhaustion and guarantee sub-2ms response latencies for cached hits.
4. **Automated CI Pipeline (`.github/workflows/ci.yml`)**:
   - Validates Docker Compose YAML configurations and builds multi-container images on every commit.

---

## Quickstart Setup

### 1. Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### 2. Launch Stack
```bash
docker compose up -d --build
```
Navigate to `http://localhost`. Try searching `NVDA` or `BTC-USD` to view the newly added charts.

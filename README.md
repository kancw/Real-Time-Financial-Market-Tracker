# Multi-Market Intelligent Asset Tracker & In-Memory Gateway

A containerized financial intelligence stack engineered with **Docker**, **Docker Compose (YAML)**, and **GitHub Actions (YAML)**. The system processes real-time quotes, multi-market classifications, and analytics across **US Equities**, **Greater China Markets (A-Shares & HKEX)**, and **Alternative Markets (Cryptocurrencies & Commodities)**, protected by an in-memory Redis caching layer.

---

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
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
docker compose up -d --build
```

### 3. Access Application
Navigate to `http://localhost` in your browser. Click on preset market buttons (US, HKEX/A-Share, Crypto, Gold) or query any custom ticker.

### 4. Stop Application
```bash
docker compose down
```

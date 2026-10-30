from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import redis
import os
import json

app = FastAPI(title="Multi-Market Global Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

MARKET_CATEGORIES = {
    "US": ["AAPL", "NVDA", "SPY", "MSFT", "QQQ"],
    "CHINA_HK": ["0700.HK", "9988.HK", "600519.SS", "000001.SS", "300750.SZ"],
    "ALTERNATIVE": ["BTC-USD", "ETH-USD", "GC=F", "CL=F", "VNQ"]
}

def detect_market(ticker: str) -> str:
    ticker = ticker.upper()
    if ticker.endswith(".HK") or ticker.endswith(".SS") or ticker.endswith(".SZ"):
        return "Greater China (HKEX / A-Shares)"
    elif "-USD" in ticker or ticker.endswith("=F") or ticker in ["BTC", "ETH", "SOL", "GLD", "SLV", "VNQ"]:
        return "Alternative Markets (Crypto & Commodities)"
    return "US Financial Markets (Equities & Indices)"

@app.get("/api/quote/{ticker}")
def get_quote(ticker: str):
    ticker = ticker.strip().upper()
    cache_key = f"quote:{ticker}"

    cached = cache.get(cache_key)
    if cached:
        res = json.loads(cached)
        res["source"] = "Redis Cache"
        return res

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if hist.empty:
            return {"error": f"No market data found for ticker '{ticker}'."}

        latest_close = float(hist['Close'].iloc[-1])
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else latest_close
        change_pct = round(((latest_close - prev_close) / prev_close) * 100, 2)

        info = stock.info or {}
        currency = info.get("currency", "USD")
        short_name = info.get("shortName") or info.get("name") or ticker

        result = {
            "ticker": ticker,
            "name": short_name,
            "price": round(latest_close, 2),
            "change_pct": change_pct,
            "currency": currency,
            "market_classification": detect_market(ticker),
            "source": "Yahoo Finance (Live)"
        }

        # Cache for 60 seconds
        cache.setex(cache_key, 60, json.dumps(result))
        return result
    except Exception as e:
        return {"error": f"Failed to retrieve quote: {str(e)}"}

@app.get("/api/featured")
def get_featured():
    featured_tickers = {
        "us": "NVDA",
        "china_hk": "0700.HK",
        "alternative": "BTC-USD"
    }
    res = {}
    for cat, sym in featured_tickers.items():
        res[cat] = get_quote(sym)
    return res

@app.get("/health")
def health():
    return {"status": "healthy"}

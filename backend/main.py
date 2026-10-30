from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import redis
import os
import json
import pandas as pd

app = FastAPI(title="Advanced Financial Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

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
    cache_key = f"quote_v3:{ticker}"

    cached = cache.get(cache_key)
    if cached:
        res = json.loads(cached)
        res["source"] = "Redis Cache"
        return res

    try:
        stock = yf.Ticker(ticker)
        # Fetch 7 days of history for the trendline chart
        hist = stock.history(period="7d")

        if hist.empty:
            return {"error": f"No market data found for ticker '{ticker}'."}

        # 24-hour calculations
        latest_close = float(hist['Close'].iloc[-1])
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else latest_close
        change_pct = round(((latest_close - prev_close) / prev_close) * 100, 2)

        # 7-day trend data for Chart.js
        trend_dates = hist.index.strftime('%Y-%m-%d').tolist()
        trend_prices = [round(float(p), 2) for p in hist['Close'].tolist()]

        info = stock.info or {}
        currency = info.get("currency", "USD")
        short_name = info.get("shortName") or info.get("name") or ticker
        market_state = info.get("marketState", "REGULAR")

        result = {
            "ticker": ticker,
            "name": short_name,
            "price": round(latest_close, 2),
            "change_pct": change_pct,
            "currency": currency,
            "market_classification": detect_market(ticker),
            "market_state": market_state,
            "trend": {
                "dates": trend_dates,
                "prices": trend_prices
            },
            "source": "Yahoo Finance (Live)"
        }

        # Cache for 60 seconds
        cache.setex(cache_key, 60, json.dumps(result))
        return result
    except Exception as e:
        return {"error": f"Failed to retrieve quote: {str(e)}"}

@app.get("/health")
def health():
    return {"status": "healthy"}

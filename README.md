# Advanced Asset Terminal (v3)

This iteration upgrades the financial dashboard to include **Data Visualization** and **Time-Series Analytics**, fully integrated within the Docker microservices architecture.

## Key Enhancements in v3:
1. **Time-Series Data Extraction:** The Python backend now fetches 7-day historical arrays using Pandas and packages them alongside real-time quotes.
2. **Chart.js Integration:** The Nginx frontend dynamically renders smooth, responsive sparkline charts (`<canvas>`) showing the 7-day asset trend.
3. **Dynamic UI Rendering:** The chart automatically colors itself green (bullish) or red (bearish) based on the asset's current performance.
4. **Market State Detection:** Displays whether the relevant exchange is currently Open (REGULAR) or Closed based on Yahoo Finance metadata.
5. **Popular Stock Shortcuts:** Select Apple, Microsoft, NVIDIA, Amazon, Alphabet, Meta, Tesla, or JPMorgan to load its quote and 7-day trend without typing a ticker.

## How to Run:
```bash
docker compose up -d --build
```
Navigate to `http://localhost`. Try searching `NVDA` or `BTC-USD` to view the newly added charts.

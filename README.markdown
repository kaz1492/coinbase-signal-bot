# Crypto Signal System

A high-win-rate cryptocurrency signal system integrated with Coinbase, Telegram, and a web dashboard.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables in `.env`:
   ```
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=your_chat_id
   ```
3. Run the system: `bash run.sh`

## Features
- Real-time data collection via Coinbase WebSocket.
- Signal generation with delta and technical analysis (RSI, MACD, ATR).
- Automated backtesting for win rate estimation.
- Telegram notifications and web dashboard.
- Deployment on Render with GitHub integration.

## Files
- `src/data_collection/coinbase_ws_listener.py`: WebSocket data collection.
- `src/analysis/`: Delta and technical analysis.
- `src/signal_generation/`: Signal generation.
- `src/backtest/`: Automated backtesting.
- `src/web/`: FastAPI web dashboard.
- `src/notification/`: Telegram notifications.
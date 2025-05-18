
# Coinbase Signal Bot

This bot is designed to generate cryptocurrency trading signals using multiple strategies across all USD-quoted pairs on Coinbase.

## Key Features

- Smart Money Concepts (SMC)
- ICT and Market Structure
- Footprint & Order Flow Analysis
- Technical Indicators (MA, RSI, MACD, etc.)
- Fibonacci and ATR-Based Target Logic
- Delta Divergence and Whale Behavior Detection
- Automated Telegram Signal Delivery
- Multi-Timeframe Support (15m, 1h, 4h, 1d)
- Backtesting and Optimization Modules

## Files

- `coinbase_signal_bot.py`: Main signal generation logic.
- `signal_runner.py`: Loop controller for running signals.
- `utils.py`: Contains technical indicator calculations.
- `lux_smc_engine.py`: Smart Money/ICT engine.
- `delta_analyzer.py`: Delta and footprint analysis.
- `telegram_sender.py`: Sends signals to Telegram bot.
- `email_alerts.py`: Optional alert system.
- `config.py`: Configuration and API settings.
- `backtest_module.py`: Historical data backtesting.
- `order_flow_analyzer.py`: Order flow signal filters.
- `target_logic_matrix.csv`: Stores target-setting strategies per pair.

# HyperIQ Market Oracle

## Overview
HyperIQ Market Oracle is a desktop application that provides real-time market data analysis and growth forecasts for commodities and stocks. It offers insights into market trends by retrieving data directly from Yahoo Finance API.

## Features
- **Real-time market data**: Connects to Yahoo Finance API to fetch current and historical market data.
- **Multiple asset classes**: Tracks cryptocurrencies (Bitcoin, Ethereum), commodities (Gold, Silver, Oil, etc.) and stocks (Nvidia, Tesla, Apple, etc.).
- **Current prices dashboard**: Displays current prices of all assets in USD with 24-hour change percentages.
- **Time horizon analysis**: Provides both short-term (1 month) and long-term (1 year) forecasts for stocks.
- **Growth predictions**: Calculates percentage growth based on historical data.
- **Analysis reasoning**: Provides basic reasoning for price movements based on trading volume analysis.
- **Error handling**: Robust error reporting for transparency in data retrieval issues.

## Installation

### Requirements
- Python 3.6 or higher
- Required Python packages:
  - tkinter (usually comes with Python installation)
  - yfinance
  - pandas
  - threading (standard library)

### Installation Steps
1. Clone this repository or download the source code.
2. Install the required packages:
   ```
   pip install yfinance pandas
   ```
3. Run the application:
   ```
   python hyperiq_app.py
   ```

## How to Use
1. Launch the application.
2. The application automatically loads current market data from Yahoo Finance.
3. Navigate between the four tabs to view different datasets:
   - **Current Prices**: Shows current prices in USD and 24-hour changes for all assets.
   - **Commodities**: Shows forecast data for commodities like Gold, Silver, Oil, etc.
   - **Stocks (Short-term)**: Displays 1-month forecasts for major tech stocks.
   - **Stocks (Long-term)**: Shows 1-year forecasts for the same stocks.
4. Use the "Refresh market data" button to fetch the latest market data.

## Data Calculation Methods

### Current Prices Tab
- **Price data source**: Yahoo Finance API using ticker symbols (e.g., "BTC-USD" for Bitcoin)
- **Current price**: The latest closing price from the most recent available data point
- **24-hour change calculation**: 
  - Retrieves price data for the last two trading days
  - Calculates percentage change: ((current_price - previous_day_price) / previous_day_price) * 100
  - Price formatting adapts based on asset value (more decimal places for lower-value assets)
- **Display order**: Assets are sorted by type (cryptocurrencies first, followed by stocks, then commodities)

### Growth Forecast Tabs
- **Data period**: 
  - Short-term: 1 month of historical data ("1mo")
  - Long-term: 1 year of historical data ("1y")
- **Growth calculation**: 
  - Retrieved from the first and last data points of the selected period
  - Formula: ((end_price - start_price) / start_price) * 100
- **Reason determination**:
  - "Trading volume increase" - shown when the latest trading volume exceeds the period average by 20% or more
  - "Market trend" - shown when the volume change is not significant
- **Error handling**: If data cannot be retrieved for a specific asset, it is reported with a detailed error message

## Evaluation

### Strengths
- **User-friendly interface**: Simple and intuitive UI with tabbed navigation.
- **Real-time data**: Direct connection to Yahoo Finance provides up-to-date information.
- **Multiple timeframes**: Offers both short and long-term perspectives.
- **Transparent data handling**: Clear error reporting when data cannot be retrieved.
- **Responsive design**: Threaded data fetching prevents UI freezing.

### Limitations
- **Basic analysis**: The current version only uses price movement and volume for analysis.
- **Limited symbols**: Currently only tracks a preset list of commodities and stocks.
- **No historical view**: Does not provide historical performance charts.
- **No data persistence**: Data is not saved between sessions.

## Future Development Roadmap

### Short-term Improvements
1. **Add data visualization**: Implement charts and graphs to visualize price movements.
2. **Expand asset coverage**: Add more commodities, stocks, and cryptocurrencies.
3. **Enhanced analysis**: Incorporate more technical indicators (Moving averages, RSI, MACD).
4. **Custom watchlists**: Allow users to create and save their own lists of tracked assets.
5. **Data export**: Add functionality to export data to CSV or Excel formats.

### Mid-term Goals
1. **Alerts system**: Implement price and volume alerts for specified thresholds.
2. **Machine learning predictions**: Integrate ML models for more sophisticated growth forecasts.
3. **Backtesting functionality**: Allow testing prediction models against historical data.
4. **News integration**: Incorporate relevant financial news for each asset.
5. **Portfolio tracking**: Add functionality to track a simulated investment portfolio.

### Long-term Vision
1. **API expansion**: Support for additional data sources beyond Yahoo Finance.
2. **Mobile application**: Develop companion mobile apps for iOS and Android.
3. **Advanced AI insights**: Implement deeper AI-driven market analysis.
4. **Social features**: Add community insights and sentiment analysis.
5. **Real trading integration**: Connect with brokerage APIs for actual trading capability.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Yahoo Finance API for providing market data
- The Python community for excellent libraries 
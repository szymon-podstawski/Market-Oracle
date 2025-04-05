import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import yfinance as yf
import pandas as pd
import threading

# Dictionary of commodities with their ticker symbols
commodities_symbols = {
    "Gold": "GC=F", 
    "Silver": "SI=F", 
    "Oil": "CL=F", 
    "Gas": "NG=F",
    "Wheat": "ZW=F",
    "Copper": "HG=F",
    "Palladium": "PA=F",
    "Platinum": "PL=F",
    "Coffee": "KC=F",
    "Sugar": "SB=F"
}

# Dictionary of stocks with their ticker symbols
stocks_symbols = {
    "Nvidia": "NVDA", 
    "Tesla": "TSLA", 
    "Apple": "AAPL", 
    "Meta": "META", 
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "TSMC": "TSM",
    "ASML": "ASML",
    "Palantir": "PLTR"
}

# Dictionary of cryptocurrencies with their ticker symbols
crypto_symbols = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD",
    "Binance Coin": "BNB-USD",
    "XRP": "XRP-USD"
}

# Function to fetch real data from Yahoo Finance
def get_stock_data(symbols_dict, period="1mo"):
    data = []
    errors = []
    
    for name, symbol in symbols_dict.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            if hist.empty:
                errors.append(f"No data for {name} ({symbol})")
                continue
                
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            growth_pct = ((end_price - start_price) / start_price) * 100
            
            # Determine reason based on volume and other indicators
            avg_volume = hist['Volume'].mean()
            last_volume = hist['Volume'].iloc[-1]
            reason = "Trading volume increase" if last_volume > avg_volume * 1.2 else "Market trend"
            
            data.append({
                "Name": name,
                "Growth Forecast": f"{round(growth_pct, 2)}%",
                "Reason": reason
            })
        except Exception as e:
            error_msg = f"Error fetching {name} ({symbol}): {str(e)}"
            errors.append(error_msg)
    
    # Return both data and errors
    return {"data": data, "errors": errors}

# Function to fetch current prices
def get_current_prices():
    data = []
    errors = []
    
    # Combine all symbols
    all_symbols = {}
    all_symbols.update({f"Crypto: {k}": v for k, v in crypto_symbols.items()})
    all_symbols.update({f"Commodity: {k}": v for k, v in commodities_symbols.items()})
    all_symbols.update({f"Stock: {k}": v for k, v in stocks_symbols.items()})
    
    for name, symbol in all_symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            # Get data for the last 2 days to properly calculate the 24h change
            history = ticker.history(period="2d")
            
            if history.empty or len(history) < 1:
                errors.append(f"No price data for {name} ({symbol})")
                continue
            
            # Get the latest available price
            current_price = history['Close'].iloc[-1]
            
            # Calculate 24h change
            change_24h = 0
            if len(history) >= 2:  # Need at least 2 data points for a change
                prev_day_price = history['Close'].iloc[-2]  # Price from previous data point
                change_24h = ((current_price - prev_day_price) / prev_day_price) * 100
            
            # Format the price based on its magnitude
            price_formatted = ""
            if current_price < 0.1:
                price_formatted = f"${current_price:.4f}"
            elif current_price < 10:
                price_formatted = f"${current_price:.2f}"
            else:
                price_formatted = f"${int(current_price):,}" if current_price.is_integer() else f"${current_price:.2f}"
            
            data.append({
                "Asset": name,
                "Current Price (USD)": price_formatted,
                "24h Change": f"{change_24h:.2f}%" if change_24h != 0 else "0.00%"
            })
        except Exception as e:
            error_msg = f"Error fetching price for {name} ({symbol}): {str(e)}"
            errors.append(error_msg)
    
    # Sort by asset type: Crypto first, then Stocks, then Commodities
    data = sorted(data, key=lambda x: (
        0 if x["Asset"].startswith("Crypto") else
        1 if x["Asset"].startswith("Stock") else 2,
        x["Asset"]
    ))
    
    return {"data": data, "errors": errors}

class HyperIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HyperIQ Market Oracle")
        self.root.geometry("800x500")

        # Add loading indicator
        self.loading_label = ttk.Label(self.root, text="Loading market data...")
        self.loading_label.pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs
        self.tabs = {}
        for tab_name in ["Current Prices", "Commodities", "Stocks (Short-term)", "Stocks (Long-term)"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_name] = frame

        # Create empty tables
        self.create_table("Current Prices", [], columns=("Asset", "Current Price (USD)", "24h Change"))
        self.create_table("Commodities", [])
        self.create_table("Stocks (Short-term)", [])
        self.create_table("Stocks (Long-term)", [])

        # Button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        refresh_button = ttk.Button(button_frame, text="Refresh market data", command=self.load_real_data)
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Load real data on startup
        self.load_real_data()

    def create_table(self, tab_name, data, columns=("Name", "Growth Forecast", "Reason")):
        frame = self.tabs[tab_name]
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(expand=True, fill='both')
        
        self.tabs[tab_name + "_tree"] = tree

        for row in data:
            values = tuple(row[col] for col in columns)
            tree.insert("", tk.END, values=values)

    def load_real_data_thread(self):
        self.loading_label.config(text="Loading data...")
        
        # Load current prices
        prices_result = get_current_prices()
        prices_data = prices_result["data"]
        prices_errors = prices_result["errors"]
        
        # Load commodities data
        commodities_result = get_stock_data(commodities_symbols)
        commodities_data = commodities_result["data"]
        commodities_errors = commodities_result["errors"]
        
        # Load short-term stocks data
        short_stocks_result = get_stock_data(stocks_symbols, period="1mo")
        short_stocks = short_stocks_result["data"]
        short_stocks_errors = short_stocks_result["errors"]
        
        # Load long-term stocks data
        long_stocks_result = get_stock_data(stocks_symbols, period="1y")
        long_stocks = long_stocks_result["data"]
        long_stocks_errors = long_stocks_result["errors"]
        
        # Update tables on the main thread
        self.root.after(0, lambda: self.update_table("Current Prices", prices_data, 
                                                  columns=("Asset", "Current Price (USD)", "24h Change")))
        self.root.after(0, lambda: self.update_table("Commodities", commodities_data))
        self.root.after(0, lambda: self.update_table("Stocks (Short-term)", short_stocks))
        self.root.after(0, lambda: self.update_table("Stocks (Long-term)", long_stocks))
        
        # Collect all errors
        all_errors = prices_errors + commodities_errors + short_stocks_errors + long_stocks_errors
        if all_errors:
            error_message = "The following errors occurred while fetching data:\n\n" + "\n".join(all_errors)
            self.root.after(0, lambda: messagebox.showerror("Data Fetch Error", error_message))
            
        self.loading_label.config(text="Data updated: " + datetime.datetime.now().strftime("%H:%M:%S"))
    
    def update_table(self, tab_name, data, columns=("Name", "Growth Forecast", "Reason")):
        tree = self.tabs[tab_name + "_tree"]
        tree.delete(*tree.get_children())
        for row in data:
            values = tuple(row[col] for col in columns)
            tree.insert("", tk.END, values=values)
    
    def load_real_data(self):
        # Run loading in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.load_real_data_thread)
        thread.daemon = True
        thread.start()

# Launch the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HyperIQApp(root)
    root.mainloop()
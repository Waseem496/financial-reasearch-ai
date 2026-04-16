import matplotlib.pyplot as plt
import yfinance as yf


def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="5y")
        return df
    except Exception:
        return None


def plot_stock_chart(ticker: str):
    df = get_stock_data(ticker)

    if df is None or df.empty:
        return None

    plt.figure()
    plt.plot(df.index, df["Close"])
    plt.title(f"{ticker} Stock Price (5 Years)")
    plt.xlabel("Date")
    plt.ylabel("Price")

    return plt
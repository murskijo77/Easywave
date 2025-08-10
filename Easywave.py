import requests
import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd

class CryptoDataFetcher:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol

    def fetch_binance_data(self, limit=50):
        url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval=1m&limit={limit}"
        resp = requests.get(url)
        data = resp.json()
        df = pd.DataFrame(data, columns=[
            "time_open", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades", "taker_buy_base",
            "taker_buy_quote", "ignore"
        ])
        df["time_open"] = pd.to_datetime(df["time_open"], unit="ms")
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df[["time_open", "close", "volume"]]

    def fetch_tweets(self, keyword="bitcoin", limit=50):
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} lang:en since:{datetime.date.today()}").get_items()):
            if i >= limit:
                break
            tweets.append(tweet.content)
        return tweets

from CexExtractor import CexExtractor
from BinanceExtractor import BinanceExtractor
from KrakenExtractor import KrakenExtractor
from CoinbaseExtractor import CoinbaseExtractor
import timeit


class CryptoTracker:
    def __init__(self):
        """ This is init function which creates instantiates objects which extract information from all exchanges."""
        self.crypto_exchange_list = []
        start = timeit.timeit()

        cex = CexExtractor()
        self.crypto_exchange_list.append(cex)
        binance = BinanceExtractor()
        self.crypto_exchange_list.append(binance)
        kraken = KrakenExtractor()
        self.crypto_exchange_list.append(kraken)
        coinbase = CoinbaseExtractor()
        self.crypto_exchange_list.append(coinbase)

        self.fetch_data()

        print(timeit.timeit() - start)

    def fetch_data(self):
        """ This function will iterate through all exchanges and fetch data from exchanges """
        for entry in self.crypto_exchange_list:
            entry.fetch_data()


if __name__ == '__main__':
    CryptoTracker()
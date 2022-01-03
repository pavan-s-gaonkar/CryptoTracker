from CryptoExchange.CexAgent import CexAgent
from FiatCurrency import FiatCurrency
from CryptoExchange.BinanceAgent import BinanceAgent
from CryptoExchange.KrakenAgent import KrakenAgent
from CryptoExchange.CoinbaseAgent import CoinbaseAgent
import timeit


class CryptoTracker:
    def __init__(self):
        """ This is init function which creates instantiates objects which extract information from all exchanges."""
        self.crypto_exchange_list = []
        start = timeit.timeit()
        self.baseCurrencyObj = FiatCurrency()
        self.crypto_exchange_list.append(BinanceAgent(self.baseCurrencyObj))
        self.crypto_exchange_list.append(CexAgent(self.baseCurrencyObj))
        self.crypto_exchange_list.append(CoinbaseAgent(self.baseCurrencyObj))
        self.crypto_exchange_list.append(KrakenAgent(self.baseCurrencyObj))

        self.fetch_data()

        end = timeit.timeit()
        print(end -start)

    def fetch_data(self):
        """ This function will iterate through all exchanges and fetch data from exchanges """
        for entry in self.crypto_exchange_list:
            entry.fetch_data()


if __name__ == '__main__':
    CryptoTracker()
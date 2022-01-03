import requests
from CryptoTrackerData.TrackerResult import TrackerResult


class KrakenAgent():
    def __init__(self, a_fiatCurrencyObj):
        """ This is an init function that uses REST API from Kraken to gather the list of
        supported crypto-currencies."""
        self.fiat_currency_list = a_fiatCurrencyObj.get_supported_fiat_currency_info()
        self.crypto_currency_list = self.get_supported_crypto_info()



    def test_fetch(self):
        """ This function uses REST API from Kraken to test a fetch function"""
        result_entry = self.get_status("ETH", "AUD")
        result_entry.print_info()

    def fetch_data(self):
        """ This function uses REST API from Kraken to get current price w.r.t base currencies and return a set."""
        result_set = []
        for crypto_currency_entry in self.crypto_currency_list:
            for fiat_currency_entry in self.fiat_currency_list:
                result_entry = self.get_status(crypto_currency_entry, fiat_currency_entry)
                result_entry.print_info()
                result_set.append(result_entry)

        return result_set

    def get_supported_crypto_info(self):
        """ This function uses REST API from Kraken to get list of ordered unique list of crypto currencies."""
        list_of_symbols = []
        resp = requests.get('https://api.kraken.com/0/public/Assets')
        #print(resp.json()["result"])

        for attribute, value in resp.json()["result"].items():
            list_of_symbols.append(attribute)

        list_of_symbols = list(set(list_of_symbols))
        list_of_symbols.sort()

        return list_of_symbols

    def get_status(self, crypto, fiat):
        """ This function uses REST API from Kraken to get current price of crypto currency w.r.t base currency."""

        result = TrackerResult(crypto, fiat)
        resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=' + crypto + fiat)
        if "result" in resp.json() and ( crypto + fiat ) in resp.json()["result"]:
            result.valid = True
            result.value = float(resp.json()["result"][crypto + fiat]["c"][0])
        return result

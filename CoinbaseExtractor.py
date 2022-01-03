import requests
from BaseCurrency import BaseCurrency
from CryptoData import CryptoData
from TradingPairData import TradingPairData


class CoinbaseExtractor(BaseCurrency):
    def __init__(self):
        """ This is an init function that uses REST API from Coinbase to gather the list of
        supported crypto-currencies."""
        BaseCurrency.__init__(self)
        self.fiat_currency_list = self.get_supported_fiat_currency_info()
        self.crypto_fiat_pair_list = self.get_supported_crypto_fiat_pairs()
        self.update_needed_crypto_fiat_pairs()

        #self.test_fetch()



    def test_fetch(self):
        """ This function uses REST API from Coinbase to test a fetch function"""
        result_entry = self.get_status("GNT", "AUD")
        result_entry.print_info()

    def get_supported_crypto_fiat_pairs(self):
        """ This function uses REST API from Cex to get list available crpyto/fait pair"""
        cryto_list = []
        trading_pair_list = []
        temp_trading_pair_list = []

        resp = requests.get('https://api.exchange.coinbase.com/products')
        # print(resp.json()["data"]["pairs"])

        for entry in resp.json():
            trading_data = TradingPairData()
            for attribute, value in entry.items():
                if attribute == "fiat_currency":
                    trading_data.crypto = value
                    cryto_list.append(value)
                if attribute == "quote_currency":
                    trading_data.fiat = value
                    temp_trading_pair_list.append(trading_data)

        """ Following peice of code will remove duplicated entries and sort the entries. """
        cryto_list = list(set(cryto_list))
        cryto_list.sort()

        """ Following peice of code will order set of TradingPairData objects based on alphabetical order  """
        for cryto_entry in cryto_list:
            for temp_trading_pair_entry in temp_trading_pair_list:
                if cryto_entry == temp_trading_pair_entry.get_crypt_name():
                    trading_pair_list.append(temp_trading_pair_entry)

        return trading_pair_list

    def update_needed_crypto_fiat_pairs(self):
        """ This function will find which of supported crpyto/fait pairs are needed"""

        for bast_currency_entry in self.fiat_currency_list:
            for crypto_fiat_pair_entry in self.crypto_fiat_pair_list:
                crypto_fiat_pair_entry.check_if_needed(bast_currency_entry)

    def fetch_data(self):
        """ This function uses REST API from Coinbase to get current price w.r.t base currencies and return a set."""
        result_set = []
        for crypto_fiat_pair_entry in self.crypto_fiat_pair_list:
            if crypto_fiat_pair_entry.is_needed:
                result_entry = self.get_status(crypto_fiat_pair_entry.crypto, crypto_fiat_pair_entry.fiat)
                result_entry.print_info()
                result_set.append(result_entry)

        return result_set

    def get_status(self, crypto, fiat):
        """ This function uses REST API from Coinbase to get current price of crypto currency w.r.t base currency."""

        result = CryptoData(crypto, fiat)
        resp = requests.get('https://api.coinbase.com/v2/prices/' + crypto +"-"+ fiat + "/buy")
        if "data" in resp.json():
            result.valid = True
            result.value = float(resp.json()["data"]["amount"])
        return result

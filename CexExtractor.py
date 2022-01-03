import requests
from BaseCurrency import BaseCurrency
from CryptoData import CryptoData
from TradingPairData import TradingPairData


class CexExtractor(BaseCurrency):
    def __init__(self):
        """ This is an init function that uses REST API from Cex to gather the list of
        supported crypto-currencies."""
        BaseCurrency.__init__(self)
        self.fiat_currency_list = self.get_supported_fiat_currency_info()
        self.crypto_fiat_pair_list = self.get_supported_crypto_fiat_pairs()
        self.update_needed_crypto_fiat_pairs()

    def test_fetch(self):
        """ This function uses REST API from Cex to test a fetch function"""
        result_entry = self.get_status("ETH", "USD")
        result_entry.print_info()

    def fetch_data(self):
        """ This function uses REST API from Cex to get current price w.r.t base currencies and return a set."""
        result_set = []
        for crypto_fiat_pair_entry in self.crypto_fiat_pair_list:
            if crypto_fiat_pair_entry.is_needed:
                result_entry = self.get_status(crypto_fiat_pair_entry.crypto, crypto_fiat_pair_entry.fiat)
                result_entry.print_info()
                result_set.append(result_entry)

        return result_set

    def get_supported_crypto_info(self):
        """ This function uses REST API from Cex to get list of ordered unique list of crypto currencies."""
        list_of_symbols = []
        resp = requests.get('https://cex.io/api/currency_limits')
        # print(resp.json()["data"]["pairs"])

        for entry in resp.json()["data"]["pairs"]:
            for attribute, value in entry.items():
                if "symbol1" == attribute:
                    list_of_symbols.append(value)
                    # print(value)
        list_of_symbols = list(set(list_of_symbols))
        list_of_symbols.sort()

        return list_of_symbols

    def get_supported_crypto_fiat_pairs(self):
        """ This function uses REST API from Cex to get list available crpyto/fait pair"""
        cryto_list = []
        trading_pair_list = []
        temp_trading_pair_list = []
        resp = requests.get('https://cex.io/api/currency_limits')
        # print(resp.json()["data"]["pairs"])

        for entry in resp.json()["data"]["pairs"]:
            trading_data = TradingPairData()
            for attribute, value in entry.items():
                if "symbol1" == attribute:
                    trading_data.crypto = value
                    cryto_list.append(value)
                if "symbol2" == attribute:
                    trading_data.fiat = value
                    temp_trading_pair_list.append(trading_data)
                    # trading_data.print_info()

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

    def is_pair_supported(self, crypto, fiat):
        """ This function provides whether a given 'crypto' and 'fiat' pair is supported by Cex """

        result = False
        for entry in self.crypto_fiat_pair_list:
            if (crypto + "::" + fiat) == entry:
                result = True
                break

        return result

    def get_status(self, crypto, fiat):
        """ This function uses REST API from Cex to get current price of crypto currency w.r.t base currency."""

        result = CryptoData(crypto, fiat)
        resp = requests.get('https://cex.io/api/ticker/' + crypto + "/" + fiat)
        # print(resp.json()["last"])
        if "last" in resp.json():
            result.valid = True
            result.value = float(resp.json()["last"])
        return result

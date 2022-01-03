

class FiatCurrency:
    def __init__(self):
        self.data = []
        self.data.append("USD")
        self.data.append("EUR")
        self.data.append("CAD")
        self.data.append("AUD")
        self.data.append("GBP")
        self.data.append("JPY")
        self.data.append("RUB")

        self.data.sort()

    def get_supported_fiat_currency_info(self):
        return self.data

    def get_supported_crypto_info(self):
        return None

    def print_data(self):
        print(self.data)
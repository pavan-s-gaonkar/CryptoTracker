class TradingPair:
    def __init__(self):
        self.crypto = ""
        self.fiat = ""
        self.is_needed = False

    def print_info(self):
        print(self.crypto + "::" + self.fiat)

    def check_if_needed(self, a_fiat):
        if self.fiat == a_fiat:
            self.is_needed = True

    def get_crypt_name(self):
        return self.crypto

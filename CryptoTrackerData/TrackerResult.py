class TrackerResult:
    def __init__(self, a_crypto, a_fiat):
        self.crypto = a_crypto
        self.fiat = a_fiat
        self.value = 0
        self.valid = False

    def print_info(self):
        if self.valid:
            print("-----------------------------")
            print(self.crypto + "/" + self.fiat + " : " + str(self.value))
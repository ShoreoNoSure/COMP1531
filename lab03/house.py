class House:
    def __init__(self, owner, address, bedrooms):
        self.owner = owner
        self.address = address
        self.bedrooms = bedrooms
        self.sold_price = None
        self.for_sale = False

    def advertise(self):
        self.for_sale = True

    def sell(self, new_owner, price):
        if self.for_sale:
            self.for_sale = False
            self.owner = new_owner
            self.sold_price = price
        else:
            raise Exception("House is not for sale")

# Rob built a mansion with 6 bedrooms
mansion = House("Rob", "123 Fake St, Kensington", 6)

# Viv built a 3 bedroom bungalow
bungalow = House("Viv", "42 Wallaby Way, Sydney", 3)

# The bungalow is advertised for sale
bungalow.advertise()

# Hayden tries to buy the mansion but can't
try:
    mansion.sell("Hayden", 3000000)
except Exception:
    print("Hayden is sad")

# He settles for buying the Bungalow instead
bungalow.sell("Hayden", 1000000)
class Card:
    def __init__(self, n, s):
        self.number = n
        self.suit = s

    def __str__(self):
        return str(self.number) + " of " + self.suit
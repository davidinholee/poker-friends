from poker.Card import Card
import random

class Deck:
    def __init__(self):
        sA = Card(14, "Spades")
        s2 = Card(2, "Spades")
        s3 = Card(3, "Spades")
        s4 = Card(4, "Spades")
        s5 = Card(5, "Spades")
        s6 = Card(6, "Spades")
        s7 = Card(7, "Spades")
        s8 = Card(8, "Spades")
        s9 = Card(9, "Spades")
        s10 = Card(10, "Spades")
        sJ = Card(11, "Spades")
        sQ = Card(12, "Spades")
        sK = Card(13, "Spades")

        hA = Card(14, "Hearts")
        h2 = Card(2, "Hearts")
        h3 = Card(3, "Hearts")
        h4 = Card(4, "Hearts")
        h5 = Card(5, "Hearts")
        h6 = Card(6, "Hearts")
        h7 = Card(7, "Hearts")
        h8 = Card(8, "Hearts")
        h9 = Card(9, "Hearts")
        h10 = Card(10, "Hearts")
        hJ = Card(11, "Hearts")
        hQ = Card(12, "Hearts")
        hK = Card(13, "Hearts")

        cA = Card(14, "Clubs")
        c2 = Card(2, "Clubs")
        c3 = Card(3, "Clubs")
        c4 = Card(4, "Clubs")
        c5 = Card(5, "Clubs")
        c6 = Card(6, "Clubs")
        c7 = Card(7, "Clubs")
        c8 = Card(8, "Clubs")
        c9 = Card(9, "Clubs")
        c10 = Card(10, "Clubs")
        cJ = Card(11, "Clubs")
        cQ = Card(12, "Clubs")
        cK = Card(13, "Clubs")

        dA = Card(14, "Diamonds")
        d2 = Card(2, "Diamonds")
        d3 = Card(3, "Diamonds")
        d4 = Card(4, "Diamonds")
        d5 = Card(5, "Diamonds")
        d6 = Card(6, "Diamonds")
        d7 = Card(7, "Diamonds")
        d8 = Card(8, "Diamonds")
        d9 = Card(9, "Diamonds")
        d10 = Card(10, "Diamonds")
        dJ = Card(11, "Diamonds")
        dQ = Card(12, "Diamonds")
        dK = Card(13, "Diamonds")
        self.deck_card = [sA, s2, s3, s4, s5, s6, s7, s8, s9, s10, sJ, sQ, sK, hA, h2, h3, h4, h5, h6, h7, h8, h9, h10,
                          hJ, hQ, hK,
                          cA, c2, c3, c4, c5, c6, c7, c8, c9, c10, cJ, cQ, cK, dA, d2, d3, d4, d5, d6, d7, d8, d9, d10,
                          dJ, dQ, dK]

    def swap(self, a):
        new_rand = random.randrange(52)
        temp = self.deck_card[a]
        self.deck_card[a] = self.deck_card[new_rand]
        self.deck_card[new_rand] = temp

    def shuffle(self):
        for x in range(52):
            self.swap(x)

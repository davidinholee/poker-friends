from poker.card import Card
from poker.deck import Deck

class Player:
    def __init__(self):
        self.ori_hand = []
        self.hand = []
        self.bet = 0
        self.is_playing = True
        self.top_hand = "None"
        self.big_blind = False
        self.small_blind = False
        self.coins = 0
        self.seat_num = 0
        self.id = 0
        self.user = ""
        self.rebet = True
        self.top_hand_val = 0
        self.cumu_bet = 0
        self.not_side = True

    def get_num(self, c):
        return c.number

    def addToHand(self, c):
        self.hand.append(c)
        self.hand.sort(key=self.get_num, reverse=True)

    def fold(self):
        self.is_playing = False
        self.bet = 0
        self.rebet = False

    def call_check_raise(self, b):
        self.is_playing = True
        self.bet = self.bet + b

    def is_high_card(self):
        self.top_hand = "High Card", self.hand[0].number
        self.top_hand_val = self.hand[0].number

    def pair(self):
        for i in range(len(self.hand) - 1):
            if self.hand[i].number == self.hand[i + 1].number:
                self.top_hand = "Pair", self.hand[i].number
                self.top_hand_val = 100 + self.hand[i].number

    def two_pair(self):
        pairs = []
        for i in range(len(self.hand) - 1):
            if not pairs:
                if self.hand[i].number == self.hand[i + 1].number:
                    pairs.append(self.hand[i].number)
            else:
                if self.hand[i].number == self.hand[i + 1].number and self.hand[i].number != pairs[0]:
                    pairs.append(self.hand[i].number)
                    self.top_hand = "Two Pair", pairs[0], pairs[1]
                    self.top_hand_val = 200 + 5*pairs[0] + 0.2*pairs[1]

    def triple(self):
        for i in range(len(self.hand) - 2):
            if self.hand[i].number == self.hand[i + 1].number == self.hand[i + 2].number:
                self.top_hand = "Triple", self.hand[i].number
                self.top_hand_val = 300 + self.hand[i].number

    def straight(self):
        'Does not return true when there are pairs inside the straight'
        for i in range(len(self.hand)):
            if i + 4 <= len(self.hand) - 1:
                if self.hand[i].number == self.hand[i + 1].number + 1 == self.hand[i + 2].number + 2 == self.hand[
                    i + 3].number + 3 == self.hand[i + 4].number + 4:
                    self.top_hand = "Straight", self.hand[i].number
                    self.top_hand_val = 400 + self.hand[i].number

    def flush(self):
        hearts = 0
        spades = 0
        clubs = 0
        diamonds = 0
        for i in range(len(self.hand)):
            if self.hand[i].suit == "Hearts":
                hearts += 1
            elif self.hand[i].suit == "Spades":
                spades += 1
            elif self.hand[i].suit == "Clubs":
                clubs += 1
            else:
                diamonds += 1
        if hearts >= 5:
            self.top_hand = "Flush", "Hearts"
            self.top_hand_val = 500
        elif spades >= 5:
            self.top_hand = "Flush", "Spades"
            self.top_hand_val = 500
        elif clubs >= 5:
            self.top_hand = "Flush", "Clubs"
            self.top_hand_val = 500
        elif diamonds >= 5:
            self.top_hand = "Flush", "Diamonds"
            self.top_hand_val = 500

    def full_house(self):
        trip = 0
        pair = 0
        for i in range(len(self.hand)):
            if trip == 0 and pair != 0:
                if i + 2 <= len(self.hand) - 1:
                    if self.hand[i].number != pair:
                        if self.hand[i].number == self.hand[i + 1].number == self.hand[i + 2].number:
                            trip = self.hand[i].number
                            self.top_hand = "Full house", trip, pair
                            self.top_hand_val = 600 + 2*trip + 0.1*pair
            elif trip != 0 and pair == 0:
                if i + 1 <= len(self.hand) - 1:
                    if self.hand[i].number != trip:
                        if self.hand[i].number == self.hand[i + 1].number:
                            pair = self.hand[i].number
                            self.top_hand = "Full house", trip, pair
                            self.top_hand_val = 600 + 2*trip + 0.1*pair
            else:
                if i + 2 <= len(self.hand) - 1:
                    if self.hand[i].number == self.hand[i + 1].number == self.hand[i + 2].number:
                        trip = self.hand[i].number
                    elif self.hand[i].number == self.hand[i + 1].number:
                        pair = self.hand[i].number
                elif i + 1 <= len(self.hand) - 1:
                    if self.hand[i].number == self.hand[i + 1].number:
                        pair = self.hand[i].number

    def quads(self):
        for i in range(len(self.hand) - 3):
            if self.hand[i].number == self.hand[i + 1].number == self.hand[i + 2].number == self.hand[i + 3].number:
                self.top_hand = "Quads", self.hand[i].number
                self.top_hand_val = 700 + self.hand[i].number

    def straight_flush(self):
        for i in range(len(self.hand)):
            if i + 4 <= len(self.hand) - 1:
                if self.hand[i].number == self.hand[i + 1].number + 1 == self.hand[i + 2].number + 2 == self.hand[
                    i + 3].number + 3 == self.hand[i + 4].number + 4:
                    if self.hand[i].suit == self.hand[i + 1].suit == self.hand[i + 2].suit == self.hand[i + 3].suit == self.hand[i + 4].suit:
                        self.top_hand = "Straight Flush", self.hand[i].suit, self.hand[i].number
                        self.top_hand_val = 800 + self.hand[i].number

    def royal_flush(self):
        for i in range(len(self.hand)):
            if i + 4 <= len(self.hand) - 1:
                if self.hand[i] == 14:
                    if self.hand[i + 1].number == 13 and self.hand[i + 2].number == 12 and self.hand[
                        i + 3].number == 11 and self.hand[i + 4].number == 10:
                        if self.hand[i].suit == self.hand[i + 1].suit == self.hand[i + 2].suit == self.hand[i + 3].suit == self.hand[i + 4].suit:
                            self.top_hand = "Royal Flush", self.hand[i].suit
                            self.top_hand_val = 900

    def bestHand(self):
        self.is_high_card()
        self.pair()
        self.two_pair()
        self.triple()
        self.straight()
        self.flush()
        self.full_house()
        self.quads()
        self.straight_flush()
        self.royal_flush()
        return self.top_hand_val
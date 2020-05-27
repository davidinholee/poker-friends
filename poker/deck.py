import random


class Card:
    def __init__(self, n, s):
        self.number = n
        self.suit = s

    def __str__(self):
        return str(self.number) + " of " + self.suit


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


class Game:
    def __init__(self, small_b, big_b):
        self.small_blind = small_b
        self.big_blind = big_b
        self.players = [None, None, None, None, None, None, None, None]
        self.fil_players = []
        self.flop = []
        self.turn = None
        self.river = None
        self.deck = None
        self.small_b_pos = None
        self.big_b_pos = None
        self.utg_pos = None
        self.small_b_pos_f = None
        self.big_b_pos_f = None
        self.side_pot = 0
        self.pot = 0
        self.current_bet = 0  # highest bet on the table
        self.round_num = 0
        self.side_pot_active = False
        self.folded_val = 0

    def add_player(self, seat_pos, username, chips, id):
        if seat_pos < 8:
            if not self.players[seat_pos]:
                self.players[seat_pos] = Player()
                self.players[seat_pos].user = username
                self.players[seat_pos].seat_num = seat_pos
                self.players[seat_pos].coins = chips
                self.players[seat_pos].id = id

    def start_round(self):
        self.flop = []
        self.turn = None
        self.river = None
        self.deck = Deck()
        self.deck.shuffle()

    def deal_cards(self):
        for i in range(8):
            if self.players[i] is not None:
                fst_card = self.deck.deck_card.pop(0)
                self.players[i].addToHand(fst_card)
                s_card = self.deck.deck_card.pop(0)
                self.players[i].addToHand(s_card)
                print(self.players[i].user, ":", fst_card, "and", s_card)

    def deal_flop(self):
        self.flop.append(self.deck.deck_card.pop(0))
        self.flop.append(self.deck.deck_card.pop(0))
        self.flop.append(self.deck.deck_card.pop(0))
        print("The flop is:")
        for i in self.flop:
            print(i.number, i.suit)
        for i in self.flop:
            for j in self.fil_players:
                j.addToHand(i)

    def deal_turn(self):
        self.turn = self.deck.deck_card.pop(0)
        for j in self.fil_players:
            j.addToHand(self.turn)
        print("The turn is: ", self.turn)

    def deal_river(self):
        self.river = self.deck.deck_card.pop(0)
        for j in self.fil_players:
            j.addToHand(self.river)
        print("The river is: ", self.river)

    def set_blinds(self):
        cnt = 0
        if self.round_num == 0:
            self.round_num += 1
            for i in range(8):
                if self.players[i] is not None:
                    self.players[i].small_blind = False
                    self.players[i].big_blind = False
            for i in range(8):
                if self.players[i] is not None and cnt == 0:
                    self.players[i].small_blind = True
                    self.small_b_pos = i
                    cnt += 1
                elif self.players[i] is not None and cnt == 1:
                    self.players[i].big_blind = True
                    self.big_b_pos = i
                    cnt += 1
        else:
            big_b_set = False
            for i in range(8):
                if self.players[i] is not None and self.players[i].small_blind and cnt == 0:
                    self.players[i].small_blind = False
                elif self.players[i] is not None and self.players[i].big_blind and cnt == 0:
                    self.players[i].small_blind = True
                    self.players[i].big_blind = False
                    self.small_b_pos = i
                    cnt += 1
                elif self.players[i] is not None and cnt == 1:
                    self.players[i].big_blind = True
                    self.big_b_pos = i
                    big_b_set = True
                    cnt += 1
                elif i == 7 and big_b_set == False:
                    for j in range(8):
                        if self.players[j] is not None and cnt == 1:
                            self.players[j].big_blind = True
                            self.big_b_pos = i
                            big_b_set = True
                            self.round_num = 0
                            cnt = 0

    def one_pl_left(self):
        cnt = 0
        for i in self.fil_players:
            if i.is_playing:
                cnt += 1
        if cnt == 1:
            return True

    def last_player_pos(self):
        for i in range(len(self.fil_players)):
            if self.fil_players[i].is_playing:
                return i

    def fst_pos_after_bb(self):
        lst = []
        for i in range(1, len(self.fil_players)):
            if self.fil_players[(self.big_b_pos_f + i) % len(self.fil_players)].is_playing:
                lst.append((self.big_b_pos_f + i) % len(self.fil_players))
        return lst[0]

    def process_turn(self, pl_id, bet_size):
        for i in self.fil_players:
            if i.id == pl_id:
                if bet_size == -1:
                    print("You have folded.")
                    i.fold()
                    self.folded_val += i.cumu_bet
                    if self.one_pl_left():
                        print(self.fil_players[self.last_player_pos()].user, " has won the pot")
                        self.fil_players[self.last_player_pos()].coins += self.pot
                        self.pot = 0
                        break
                elif bet_size + i.bet == self.current_bet:
                    i.call_check_raise(bet_size)
                    i.coins -= bet_size
                    self.pot += bet_size
                    self.current_bet = i.bet
                    i.cumu_bet += i.bet
                    i.rebet = False
                elif bet_size + i.bet > self.current_bet:
                    i.call_check_raise(bet_size)
                    i.coins -= bet_size
                    self.pot += bet_size
                    self.current_bet = i.bet
                    i.cumu_bet += i.bet
                    i.rebet = False
                    for j in self.fil_players:
                        if j.is_playing and not j.id == i.id:
                            j.rebet = True
                elif bet_size == -2: # means player is still in but has no coins to bet
                    i.rebet = False
                else:
                    print("Invalid bet. You have folded.")
                    i.fold()
                    if self.one_pl_left():
                        print(self.fil_players[self.last_player_pos()].user, " has won the pot")
                        self.fil_players[self.last_player_pos()].coins += self.pot
                        self.pot = 0
                        break

    def bet_round_pf_new(self):
        re_bet = True
        while re_bet:
            re_bet = False
            for j in range(1, len(self.fil_players) + 1):
                if self.fil_players[(self.big_b_pos_f + j) % len(self.fil_players)].is_playing:
                    x = int(input("Enter a bet(-1 if folding): "))
                    y = self.fil_players[(self.big_b_pos_f + j) % len(self.fil_players)].id
                    self.process_turn(y, x)
                    some_true = False
                    for i in self.fil_players:
                        if i.is_playing:
                            if i.rebet:
                                some_true = True
                    if not some_true:
                        break
            for i in self.fil_players:
                if i.is_playing:
                    if i.rebet:
                        re_bet = True
            if not re_bet:
                self.current_bet = 0
                for i in self.players:
                    if i is not None:
                        i.bet = 0
                        i.rebet = True
                for i in self.fil_players:
                    i.bet = 0
                    i.rebet = True

    def bet_round_af_new(self):
        re_bet = True
        while re_bet:
            re_bet = False
            for j in range(len(self.fil_players)):
                if self.fil_players[(self.small_b_pos_f + j) % len(self.fil_players)].is_playing:
                    x = int(input("Enter a bet(-1 if folding): "))
                    y = self.fil_players[(self.small_b_pos_f + j) % len(self.fil_players)].id
                    self.process_turn(y, x)
                    some_true = False
                    for i in self.fil_players:
                        if i.is_playing:
                            if i.rebet:
                                some_true = True
                    if not some_true:
                        break
            for i in self.fil_players:
                if i.is_playing:
                    if i.rebet:
                        re_bet = True
            if not re_bet:
                self.current_bet = 0
                for i in self.players:
                    if i is not None:
                        i.bet = 0
                        i.rebet = True
                for i in self.fil_players:
                    i.bet = 0
                    i.rebet = True

    def check_dup(self, list_elems):
        if len(list_elems) == len(set(list_elems)):
            return False
        else:
            return True

    def get_winner(self):
        winner = []
        win_cumu_bets = []
        players_in = 0
        for i in self.fil_players:
            if i.is_playing:
                players_in += 1
        top_val = 0
        for i in self.fil_players:
            if i.bestHand() > top_val:
                top_val = i.bestHand()
                winner = [i]
                win_cumu_bets = [i.cumu_bet]
            elif i.bestHand() == top_val:
                winner.append(i)
                win_cumu_bets.append(i.cumu_bet)
        while win_cumu_bets:
            if len(set(win_cumu_bets)) == 1:
                self.pot -= self.folded_val
                for i in winner:
                    i.coins += round((self.pot/len(winner)) + self.folded_val/len(winner))
                    print(i.user, "wins", round(self.pot/len(winner)), "coins with a", i.top_hand[0])
                    win_cumu_bets = []
            else:
                min_val = min(win_cumu_bets)
                self.pot = self.pot - len(players_in) * min_val
                for i in winner:
                    i.coins += min_val
                for i in winner:
                    if i.cumu_bet == min_val:
                        winner.remove(i)
                for i in win_cumu_bets:
                    if i == min_val:
                        winner.remove(i)
        self.pot = 0

    def play(self):
        self.start_round()
        self.deal_cards()
        self.set_blinds()
        for i in range(8):
            if self.players[i] is not None and self.players[i].small_blind:
                self.players[i].call_check_raise(self.small_blind)
                self.players[i].coins = self.players[i].coins - self.small_blind
                self.players[i].bet = self.small_blind
                self.pot += self.small_blind
                print(self.players[i].user, " puts in a small blind of ", self.small_blind)
            if self.players[i] is not None and self.players[i].big_blind:
                self.players[i].call_check_raise(self.big_blind)
                self.players[i].coins = self.players[i].coins - self.big_blind
                self.pot += self.big_blind
                self.current_bet = self.big_blind
                self.players[i].bet = self.big_blind
                print(self.players[i].user, " puts in a small blind of ", self.big_blind)
        for i in self.players:
            if i is not None:
                self.fil_players.append(i)
        for i in range(len(self.fil_players)):
            if self.fil_players[i].big_blind:
                self.small_b_pos_f = (i - 1) % len(self.fil_players)
                self.big_b_pos_f = i
        self.bet_round_pf_new()
        self.deal_flop()
        print("---------------------")


g = Game(1, 2)
g.add_player(2, "james", 200, 100)
g.add_player(3, "mason", 200, 101)
g.add_player(5, "david", 200, 102)
g.play()
g.bet_round_af_new()
g.deal_turn()
g.bet_round_af_new()
g.deal_river()
g.bet_round_af_new()
g.get_winner()
print("james has", g.players[2].coins, "coins")
print("mason has", g.players[3].coins, "coins")
print("david has", g.players[5].coins, "coins")


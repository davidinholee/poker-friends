from poker.player import Player
from poker.deck import Deck
import random

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
        self.round_over = False

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
                        self.round_over = True
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
                if self.fil_players[(self.big_b_pos_f + j) % len(self.fil_players)].is_playing and self.fil_players[(self.big_b_pos_f + j) % len(self.fil_players)].coins != 0:
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
                if self.fil_players[(self.small_b_pos_f + j) % len(self.fil_players)].is_playing and self.fil_players[(self.big_b_pos_f + j) % len(self.fil_players)].coins != 0:
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

    def get_cumu(self, c):
        return c.cumu_bet

    def get_winner(self):
        winner = []
        win_cumu_bets = []
        loser_bets = []
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
        for i in self.fil_players:
            if i not in winner:
                loser_bets.append(i)
        winner.sort(key=self.get_cumu)
        for i in winner:
            i.coins += i.cumu_bet
            print(i.user, "wins", "with a", i.top_hand[0])
        prev_win = 0
        prev_bet = 0
        while winner:
            for i in loser_bets:
                if i.cumu_bet <= winner[0].cumu_bet:
                    r_value = round(i.cumu_bet/len(winner))
                    winner[0].coins += r_value
                    i.cumu_bet -= r_value
                else:
                    prev_win = round((winner[0].cumu_bet - prev_bet)/len(winner)) + prev_win
                    winner[0].coins += prev_win
                    i.cumu_bet -= prev_win
                    prev_bet = winner[0].cumu_bet
            winner.pop(0)
        for i in loser_bets:
            i.coins += i.cumu_bet
        self.pot = 0

    def sb_bb_setup(self):
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

    def filter_players(self):
        for i in self.players:
            if i is not None:
                self.fil_players.append(i)

    def play(self):
        self.start_round()
        self.deal_cards()
        self.set_blinds()
        self.sb_bb_setup()
        self.filter_players()
        for i in range(len(self.fil_players)):
            if self.fil_players[i].big_blind:
                self.small_b_pos_f = (i - 1) % len(self.fil_players)
                self.big_b_pos_f = i
        self.bet_round_pf_new()
        if not self.round_over:
            self.deal_flop()
        print("---------------------")


g = Game(1, 2)
g.add_player(2, "james", 200, 100)
g.add_player(3, "mason", 200, 101)
g.add_player(5, "david", 200, 102)
g.play()
if not g.round_over:
    g.bet_round_af_new()
if not g.round_over:
    g.deal_turn()
    g.bet_round_af_new()
if not g.round_over:
    g.deal_river()
    g.bet_round_af_new()
if not g.round_over:
    g.get_winner()
print("james has", g.players[2].coins, "coins")
print("mason has", g.players[3].coins, "coins")
print("david has", g.players[5].coins, "coins")
# pylint: skip-file

import blackjack
from models import Player, Hand, Dealer
import pytest
from support.testing_util import player_chooses


# ---------- PRINT FUNCTIONS ----------


# ---------- ASK USER INPUT FUNCTIONS ----------


# ask_number_of_decks()


def test_ask_number_of_decks_valid(monkeypatch):
    """ask_number_of_decks(): check a valid number gets returned"""
    player_chooses(["4"], monkeypatch)
    assert blackjack.ask_number_of_decks() == 4


def test_ask_number_of_decks_too_many(monkeypatch):
    """ask_number_of_decks(): a number above the max deck asks the user again."""
    player_chooses([str(blackjack.MAX_DECK_PACKS + 1), "2"], monkeypatch)
    assert blackjack.ask_number_of_decks() == 2


def test_ask_number_of_decks_max(monkeypatch):
    """ask_number_of_decks(): a number equal to the max is valid."""
    player_chooses([str(blackjack.MAX_DECK_PACKS)], monkeypatch)
    assert blackjack.ask_number_of_decks() == blackjack.MAX_DECK_PACKS


def test_ask_number_of_decks_too_few(monkeypatch):
    """ask_number_of_decks(): a number too low will make user input again."""
    player_chooses(["0", "3"], monkeypatch)
    assert blackjack.ask_number_of_decks() == 3


def test_ask_number_of_decks_invalid(monkeypatch):
    """ask_number_of_decks(): not a number asks the user for input again"""
    player_chooses(["a", "4"], monkeypatch)
    assert blackjack.ask_number_of_decks() == 4


def test_ask_number_of_decks_multiple_attempts(monkeypatch):
    """ask_number_of_decks(): the user is prompted until a valid input"""
    player_chooses(["a", "0", "100", "10", "b", "1"], monkeypatch)
    assert blackjack.ask_number_of_decks() == 1


# ask_number_of_players()


def test_ask_number_of_players_single(monkeypatch):
    """ask_number_of_players(): a single player is allowed to play"""
    player_chooses(["1"], monkeypatch)
    assert blackjack.ask_number_of_players() == 1


def test_ask_number_of_players_valid(monkeypatch):
    """ask_number_of_players(): a valid number returns the number"""
    player_chooses(["3"], monkeypatch)
    assert blackjack.ask_number_of_players() == 3


def test_ask_number_of_players_invalid(monkeypatch):
    """ask_number_of_players(): an invalid number forces the user to try again."""
    player_chooses(["a", "2"], monkeypatch)
    assert blackjack.ask_number_of_players() == 2


def test_ask_number_of_players_too_many(monkeypatch):
    """ask_number_of_players(): too many players prompts the user to try again."""
    player_chooses([str(blackjack.MAX_PLAYERS+1), "2"], monkeypatch)
    assert blackjack.ask_number_of_players() == 2


def test_ask_number_of_players_max(monkeypatch):
    """ask_number_of_players(): max players is a valid input"""
    player_chooses([str(blackjack.MAX_PLAYERS), "2"], monkeypatch)
    assert blackjack.ask_number_of_players() == blackjack.MAX_PLAYERS


def test_ask_number_of_players_too_few(monkeypatch):
    """ask_number_of_players(): too few players prompts the user again."""
    player_chooses(["0", "2"], monkeypatch)
    assert blackjack.ask_number_of_players() == 2


def test_ask_number_of_players_multiple_attempts(monkeypatch):
    """ask_number_of_players(): function will ask until a valid input is provided"""
    player_chooses(["0", "a", "100", "10", "3"], monkeypatch)
    assert blackjack.ask_number_of_players() == 3


# ask_player_name()


def test_ask_player_name_non_empty(monkeypatch):
    """ask_player_name(): check name returns when non-empty"""
    player_chooses(["test_name"], monkeypatch)
    assert blackjack.ask_player_name(1) == "test_name"


def test_ask_player_name_empty(monkeypatch):
    """ask_player_name(): check default name returns, and indexes properly"""
    player_chooses([""], monkeypatch)
    assert blackjack.ask_player_name(0) == "Player 1"


# ask_player_purse()


def test_ask_player_purse_valid(monkeypatch):
    """ask_player_purse(): valid input returns number as float"""
    player_chooses(["100.5"], monkeypatch)
    assert blackjack.ask_player_purse() == 100.5


def test_ask_player_purse_invalid(monkeypatch):
    """ask_player_purse(): invalid input asks again"""
    player_chooses(["a", "b", "50"], monkeypatch)
    assert blackjack.ask_player_purse() == 50.0


def test_ask_player_purse_too_low(monkeypatch):
    """ask_player_purse(): purse must be greater than or equal to minimum bet"""
    player_chooses([str(blackjack.MINIMUM_BET - 1), "100"], monkeypatch)
    assert blackjack.ask_player_purse() == 100.0


# ask_player_bet


def test_ask_player_bet_valid(monkeypatch):
    """ask_player_bet(): a valid bet is returned as a float"""
    player_chooses(["10.5"], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == 10.5


def test_ask_player_bet_insufficient_funds(monkeypatch):
    """ask_player_bet(): insufficient funds (purse below minimum) raises an error"""
    player_chooses([], monkeypatch)
    player = Player("test_name", blackjack.MINIMUM_BET - 1.0)
    with pytest.raises(ValueError):
        blackjack.ask_player_bet(player)


def test_ask_player_bet_invalid(monkeypatch):
    """ask_player_bet(): invalid inputs prompts user again"""
    player_chooses(["A", "10"], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == 10


def test_ask_player_bet_less_than_minimum(monkeypatch):
    """ask_player_bet(): input must be greater than or equal to minimum bet"""
    player_chooses([str(blackjack.MINIMUM_BET - 1.0), "10"], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == 10


def test_ask_player_bet_equal_to_minimum(monkeypatch):
    """ask_player_bet(): input equal to minimum bet is valid"""
    player_chooses([str(blackjack.MINIMUM_BET)], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == blackjack.MINIMUM_BET


def test_ask_player_bet_greater_than_purse(monkeypatch):
    """ask_player_bet(): input must be less than purse amount"""
    player_chooses(["200", "10"], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == 10.0


def test_ask_player_bet_multiple_attempts(monkeypatch):
    """ask_player_bet(): multiple attempts until valid input provided"""
    player_chooses(["200", "A", "b", "0", "20"], monkeypatch)
    player = Player("test_name", 100.0)
    assert blackjack.ask_player_bet(player) == 20.0


# ask_player_action()


def test_ask_player_action_valid(monkeypatch):
    """ask_player_action(): a player inputs a valid option"""
    player_chooses(["stick"], monkeypatch)
    assert blackjack.ask_player_action(
        ["hit", "stick", "split", "double-down"]) == "stick"


def test_ask_player_action_invalid(monkeypatch):
    """ask_player_action(): a player inputs an invalid option, then valid"""
    player_chooses(["double-down", "hit"], monkeypatch)
    assert blackjack.ask_player_action(
        ["hit", "stick", "split"]) == "hit"


# ---------- DECK AND CARDS FUNCTIONS ----------


# generate_deck()


def test_generate_deck_size():
    """generate_deck(): check the correct number of cards are present."""
    assert len(blackjack.generate_deck(1)) == 52
    assert len(blackjack.generate_deck(2)) == 104
    assert len(blackjack.generate_deck(3)) == 156
    assert len(blackjack.generate_deck(4)) == 208


def test_generate_deck_cards():
    """generate_deck(): check a single deck contains some expected cards."""
    deck = blackjack.generate_deck(1)
    assert ("A", "H") in deck
    assert ("4", "D") in deck
    assert ("J", "H") in deck
    assert ("Q", "C") in deck
    assert ("K", "D") in deck
    assert ("3", "C") in deck


def test_generate_deck_duplicates():
    """generate_deck(): check decks with multiple packs have correct number of duplicates."""
    deck = blackjack.generate_deck(2)
    assert deck.count(("A", "H")) == 2
    assert deck.count(("K", "H")) == 2


# shuffle()


def test_shuffle_returns_copy():
    """shuffle(): check that a copy is returned, rather than original"""
    deck = blackjack.generate_deck(1)
    shuffled_deck = blackjack.shuffle(deck, 123456)
    assert deck is not shuffled_deck


# take_card_from_deck()


def test_take_card_from_deck_base():
    """take_card_from_deck(): test that a card is returned and deck removes card."""
    deck = [("3", "H"), ("4", "D"), ("A", "H"), ("Q", "C"), ("7", "S")]
    card = blackjack.take_card_from_deck(deck)
    assert card == ("7", "S")
    assert len(deck) == 4


def test_take_card_from_deck_empty_deck():
    """take_card_from_deck(): Error raised if deck is empty"""
    with pytest.raises(IndexError):
        blackjack.take_card_from_deck([])


# hand_to_string()


def test_hand_to_string_base():
    """hand_to_string(): simple base test"""
    hand = Hand([("3", "H"), ("K", "D"), ("A", "H")])
    assert blackjack.hand_to_string(hand) == "3H, KD, AH"


def test_hand_to_string_empty_hand():
    """hand_to_string(): test an empty hand raises an error"""
    hand = Hand()
    with pytest.raises(ValueError):
        blackjack.hand_to_string(hand)


def test_hand_to_string_single():
    """hand_to_string(): single card"""
    hand = Hand([("10", "S")])
    assert blackjack.hand_to_string(hand) == "10S"


# ---------- PLAYER AND DEALER INFORMATION FUNCTIONS ----------


# define_players()


def test_define_players_single_player(monkeypatch):
    """define_players(): single player"""
    player_chooses(["test_name", "100"], monkeypatch)
    players = blackjack.define_players(1)
    assert len(players) == 1
    assert players[0].name == "test_name"
    assert players[0].purse == 100.


def test_define_players_multiple_players(monkeypatch):
    """define_players(): multiple players"""
    player_chooses(["test_name1", "10", "test_name2",
                   "20", "test_name3", "30"], monkeypatch)
    players = blackjack.define_players(3)
    assert len(players) == 3
    assert players[0].name == "test_name1"
    assert players[0].purse == 10.
    assert players[1].name == "test_name2"
    assert players[1].purse == 20.
    assert players[2].name == "test_name3"
    assert players[2].purse == 30.


def test_define_players_default_name(monkeypatch):
    """define_players(): player is given a default name if empty string."""
    player_chooses(["", "100"], monkeypatch)
    players = blackjack.define_players(1)
    assert len(players) == 1
    assert players[0].name == "Player 1"
    assert players[0].purse == 100.


# define_dealer()


def test_define_dealer():
    """test_define_dealer(): a dealer object is returned"""
    dealer = blackjack.define_dealer()
    assert type(dealer) == Dealer


# ---------- ROUND SETUP FUNCTIONS (BETS AND DEALING) ----------


# take_bets()


def test_take_bets_base(monkeypatch):
    """take_bets(): base situation where all players have enough money"""
    player_chooses(["10", "20"], monkeypatch)
    players = [
        blackjack.Player("test_name1", 100),
        blackjack.Player("test_name2", 50),
    ]
    bets = blackjack.take_bets(players)
    assert bets["test_name1"] == 10
    assert bets["test_name2"] == 20
    assert players[0].purse == 90
    assert players[1].purse == 30


def test_take_bets_invalid_bet(monkeypatch):
    """take_bets(): player requests too large of a bet"""
    player_chooses(["10", "60", "20"], monkeypatch)
    players = [
        blackjack.Player("test_name1", 100),
        blackjack.Player("test_name2", 50),
    ]
    bets = blackjack.take_bets(players)
    assert bets["test_name1"] == 10
    assert bets["test_name2"] == 20
    assert players[0].purse == 90
    assert players[1].purse == 30


def test_take_bets_bet_too_small(monkeypatch):
    """take_bets(): player asks for a bet that is too low"""
    player_chooses(["10", "1", "10"], monkeypatch)
    players = [
        blackjack.Player("test_name1", 100),
        blackjack.Player("test_name2", 200),
    ]
    bets = blackjack.take_bets(players)
    assert bets["test_name1"] == 10
    assert bets["test_name2"] == 10
    assert players[0].purse == 90
    assert players[1].purse == 190


# deal_initial_hands()


def test_deal_initial_hands_base():
    """deal_initial_hands(): test simple case"""
    players = [
        blackjack.Player("test_name1", 100),
        blackjack.Player("test_name2", 50),
    ]
    dealer = blackjack.Dealer()
    deck = [("A", "H"), ("2", "H"), ("3", "H"),
            ("4", "H"), ("5", "H"), ("6", "H"),
            ("7", "H"), ("8", "H"), ("9", "H"),
            ("10", "H"), ("J", "H"), ("Q", "H")]
    bets = {
        "test_name1": 10.0,
        "test_name2": 20.0,
    }
    blackjack.deal_initial_hands(deck, players, dealer, bets)
    assert players[0].hands[0].cards == [("Q", "H"), ("9", "H")]
    assert players[1].hands[0].cards == [("J", "H"), ("8", "H")]
    assert dealer.hands[0].cards == [("10", "H"), ("7", "H")]
    assert players[0].hands[0].bet == 10.0
    assert players[1].hands[0].bet == 20.0
    assert len(deck) == 6


# ---------- ROUND PAYMENTS AND HAND OUTCOME FUNCTIONS ----------


# push()


def test_push():
    """push(): money returns to player as expected"""
    player = Player("test_name", 90.)
    hand = Hand([("A", "S"), ("A", "D")], bet=10.)
    blackjack.push(player, hand)
    assert player.purse == 100.


# lost()


def test_lost():
    """lost(): money does not return to player"""
    player = Player("test_name", 90.)
    hand = Hand([("A", "S"), ("A", "D")], bet=10.)
    blackjack.lost(player, hand)
    assert player.purse == 90.


# one_to_one()


def test_one_to_one():
    """one_to_one(): money returns to player as expected, with winnings"""
    player = Player("test_name", 90.)
    hand = Hand([("A", "S"), ("A", "D")], bet=10.)
    blackjack.one_to_one(player, hand)
    assert player.purse == 110.


# three_to_two():


def test_three_to_two():
    """three_to_two(): money returns to player as expected, with winnings"""
    player = Player("test_name", 90.)
    hand = Hand([("A", "S"), ("A", "D")], bet=10.)
    blackjack.three_to_two(player, hand)
    assert player.purse == 115.


# make_hand_payment()


def test_make_hand_payment__bust_bust():
    """make_hand_payment(): dealer is bust, player is bust -> lost"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("10", "H"), ("2", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("Q", "H"), ("K", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 90.


def test_make_hand_payment__bust_score():
    """make_hand_payment(): dealer is bust, player is score -> 1:1"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("5", "H"), ("2", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("10", "H"), ("10", "H"), ("2", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 110.


def test_make_hand_payment__bust_blackjack():
    """make_hand_payment(): dealer is bust, player is blackjack -> 3:2"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("A", "H"), ("K", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("10", "H"), ("10", "H"), ("5", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 115.


def test_make_hand_payment__score_bust():
    """make_hand_payment(): dealer is score, player is bust -> lost"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("K", "H"), ("5", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("10", "H"), ("5", "H"), ("2", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 90.


def test_make_hand_payment_score_blackjack():
    """make_hand_payment(): dealer is score, player is blackjack -> 3:2"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("A", "H"), ("Q", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("10", "H"), ("5", "H"), ("5", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 115.


def test_make_hand_payment_blackjack_bust():
    """make_hand_payment(): dealer is blackjack, player is bust -> lost"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("J", "H"), ("2", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("A", "H"), ("10", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 90.


def test_make_hand_payment_blackjack_score():
    """make_hand_payment(): dealer is blackjack, player is score -> lost"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("5", "H"), ("6", "H"), ("2", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("A", "H"), ("K", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 90.


def test_make_hand_payment_blackjack_blackjack():
    """make_hand_payment(): dealer is blackjack, player is blackjack -> push"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("A", "H"), ("K", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("Q", "H"), ("A", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 100.


def test_make_hand_payment__score_score_player():
    """make_hand_payment(): dealer is score, player is score -> comparison (1:1)"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("5", "H"), ("6", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("7", "H"), ("3", "H"), ("8", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 110.


def test_make_hand_payment__score_score_dealer():
    """make_hand_payment(): dealer is score, player is score -> comparison (lost)"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("10", "H"), ("4", "H"), ("2", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("Q", "H"), ("5", "H"), ("5", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 90.


def test_make_hand_payment__score_score_tie():
    """make_hand_payment(): dealer is score, player is score -> comparison (push)"""
    # Setup
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("3", "H"), ("5", "H")], bet=10)
    hand.is_active = False
    player.give_hand(hand)
    dealer_hand = Hand([("A", "H"), ("3", "H"), ("1", "H")])
    # Function call
    blackjack.make_hand_payment(player, hand, dealer_hand)
    # Assertions
    assert player.purse == 100.


# make_payments()


def test_make_payments_multiple_players_and_hands():
    """make_payments(): expected purses from multiple players with multiple hands."""
    # Setup
    player1 = Player("test_name", 90.)
    hand1 = Hand([("7", "H"), ("3", "H")], bet=10)  # 10
    hand1.is_active = False
    player1.give_hand(hand1)
    player2 = Player("test_name", 70.)
    hand2 = Hand([("7", "H"), ("3", "H"), ("7", "H")], bet=20)  # 17
    hand3 = Hand([("7", "H"), ("3", "H"), ("2", "H")], bet=10)  # 12
    hand2.is_active = False
    hand3.is_active = False
    player2.give_hand(hand2)
    player2.give_hand(hand3)
    players = [player1, player2]
    dealer = Dealer()
    dealer_hand = Hand([("A", "H"), ("3", "H"), ("1", "H")])  # 15
    dealer.give_hand(dealer_hand)
    # Function call
    blackjack.make_payments(players, dealer)
    # Assertions
    assert player1.purse == 90.
    assert player2.purse == 110.


# ---------- PLAYER AND DEALER TURN FUNCTIONS ----------


# player_turn()


def player_turn_blackjack():
    """player_turn(): player gets a blackjack immediately"""
    # Setup
    deck = [("A", "H"), ("A", "H"), ("A", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("A", "H"), ("K", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("A", "H"), ("K", "H")]
    assert len(deck) == 3


def player_turn_stick(monkeypatch):
    """player_turn(): player sticks immediately"""
    player_chooses(["stick"], monkeypatch)
    # Setup
    deck = [("A", "H"), ("A", "H"), ("A", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("1", "H"), ("K", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("1", "H"), ("K", "H")]
    assert len(deck) == 3


def player_turn_hit_bust(monkeypatch):
    """player_turn(): player hits and goes bust"""
    player_chooses(["hit"], monkeypatch)
    # Setup
    deck = [("3", "H"), ("7", "H"), ("10", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("5", "H"), ("K", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("5", "H"), ("K", "H"), ("10", "H")]
    assert len(deck) == 2


def player_turn_hit_stick(monkeypatch):
    """player_turn(): player hits and then sticks"""
    player_chooses(["hit", "stick"], monkeypatch)
    # Setup
    deck = [("3", "H"), ("7", "H"), ("2", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("5", "H"), ("K", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("5", "H"), ("K", "H"), ("2", "H")]
    assert len(deck) == 2


def test_player_turn_hit_hit_bust(monkeypatch):
    """player_turn(): player hits, hits again and goes bust"""
    player_chooses(["hit", "hit"], monkeypatch)
    # Setup
    deck = [("4", "H"), ("7", "D"), ("2", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("7", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("7", "H"), ("7", "H"), ("2", "H"), ("7", "D")]
    assert len(deck) == 1


def test_player_turn_double_down(monkeypatch):
    """player_turn(): player double-downs"""
    player_chooses(["double-down"], monkeypatch)
    # Setup
    deck = [("4", "H"), ("7", "D"), ("5", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("4", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 20.
    assert hand.cards == [("7", "H"), ("4", "H"), ("5", "H")]
    assert len(deck) == 2


def test_player_turn_invalid_double_down(monkeypatch):
    """player_turn(): player tries to double-down, but is invalid input"""
    player_chooses(["hit", "double-down", "stick"], monkeypatch)
    # Setup
    deck = [("4", "H"), ("7", "D"), ("5", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("4", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("7", "H"), ("4", "H"), ("5", "H")]
    assert len(deck) == 2


def test_player_turn_split_stick_stick(monkeypatch):
    """player_turn(): player splits, then sticks with each hand"""
    player_chooses(["split", "stick", "stick"], monkeypatch)
    # Setup
    deck = [("4", "H"), ("2", "D"), ("5", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("7", "D")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not player.hands[0].is_active
    assert not player.hands[1].is_active
    assert player.hands[0].bet == 10.
    assert player.hands[1].bet == 10.
    assert player.hands[0].cards == [("7", "H"), ("5", "H")]
    assert player.hands[1].cards == [("7", "D"), ("2", "D")]
    assert len(deck) == 1
    assert player.purse == 80.


def test_player_turn_invalid_split_stick(monkeypatch):
    """player_turn(): player tries to split, but is invalid input"""
    player_chooses(["split", "stick"], monkeypatch)
    # Setup
    deck = [("4", "H"), ("7", "D"), ("5", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("4", "H")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not hand.is_active
    assert hand.bet == 10.
    assert hand.cards == [("7", "H"), ("4", "H")]
    assert len(deck) == 3


def test_player_turn_split_split_stick_stick_stick(monkeypatch):
    """player_round(): player splits twice, then sticks to all hands"""
    player_chooses(["split", "split", "stick", "stick", "stick"], monkeypatch)
    # Setup
    deck = [("2", "S"), ("4", "H"), ("2", "D"), ("5", "H"), ("7", "C")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("7", "D")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not player.hands[0].is_active
    assert not player.hands[1].is_active
    assert not player.hands[2].is_active
    assert player.hands[0].bet == 10.
    assert player.hands[1].bet == 10.
    assert player.hands[2].bet == 10.
    assert player.hands[0].cards == [("7", "H"), ("2", "D")]
    assert player.hands[1].cards == [("7", "D"), ("5", "H")]
    assert player.hands[2].cards == [("7", "C"), ("4", "H")]
    assert len(deck) == 1
    assert player.purse == 70.


def test_player_turn_split_double_down_stick(monkeypatch):
    """player_turn(): player splits, then double-downs on one hand and sticks the other."""
    player_chooses(["split", "double-down", "stick"], monkeypatch)
    # Setup
    deck = [("3", "H"), ("4", "H"), ("2", "D"), ("5", "H")]
    player = Player("test_name", 90.)
    hand = Hand([("7", "H"), ("7", "D")], bet=10.)
    player.give_hand(hand)
    # Function call
    blackjack.player_turn(player, deck)
    # Assertions
    assert not player.hands[0].is_active
    assert not player.hands[1].is_active
    assert player.hands[0].bet == 20.
    assert player.hands[1].bet == 10.
    assert player.hands[0].cards == [("7", "H"), ("5", "H"), ("4", "H")]
    assert player.hands[1].cards == [("7", "D"), ("2", "D")]
    assert len(deck) == 1
    assert player.purse == 70.


# complete_dealer_turn()


def test_complete_dealer_turn_all_busts():
    """complete_dealer_turn(): returns False if all hands are bust"""
    # Setup
    dealer = Dealer()
    dealer.give_hand(Hand([("10", "H"), ("7", "H")]))
    player1 = Player("test_name", 80.)
    hand1 = Hand([("10", "H"), ("7", "H"), ("8", "H")], bet=10.)
    hand2 = Hand([("7", "H"), ("7", "H"), ("10", "H")], bet=10.)
    player1.give_hand(hand1)
    player1.give_hand(hand2)
    player2 = Player("test_name", 80.)
    hand3 = Hand([("10", "H"), ("7", "H"), ("8", "H")], bet=10.)
    player2.give_hand(hand3)
    players = [player1, player2]
    # Assertion
    assert blackjack.complete_dealer_turn(players, dealer) == False


def test_complete_dealer_turn_not_all_busts():
    """complete_dealer_turn(): returns True if not all hands are bust"""
    # Setup
    dealer = Dealer()
    dealer.give_hand(Hand([("10", "H"), ("7", "H")]))
    player1 = Player("test_name", 80.)
    hand1 = Hand([("10", "H"), ("7", "H"), ("8", "H")], bet=10.)
    hand2 = Hand([("7", "H"), ("7", "H")], bet=10.)
    player1.give_hand(hand1)
    player1.give_hand(hand2)
    player2 = Player("test_name", 80.)
    hand3 = Hand([("10", "H"), ("7", "H"), ("8", "H")], bet=10.)
    player2.give_hand(hand3)
    players = [player1, player2]
    # Assertion
    assert blackjack.complete_dealer_turn(players, dealer) == True


def test_complete_dealer_turn_dealer_no_blackjack():
    """complete_dealer_turn(): if dealer has no chance of blackjack, and all players have blackjacks"""
    # Setup
    dealer = Dealer()
    dealer.give_hand(Hand([("10", "H"), ("7", "H")]))
    player1 = Player("test_name", 80.)
    hand1 = Hand([("10", "H"), ("A", "H")], bet=10.)
    hand2 = Hand([("A", "H"), ("J", "H")], bet=10.)
    player1.give_hand(hand1)
    player1.give_hand(hand2)
    player2 = Player("test_name", 80.)
    hand3 = Hand([("K", "H"), ("A", "H")], bet=10.)
    player2.give_hand(hand3)
    players = [player1, player2]
    # Assertion
    assert blackjack.complete_dealer_turn(players, dealer) == False


def test_complete_dealer_turn_dealer_blackjack():
    """complete_dealer_turn(): returns False if all hands are blackjacks"""
    # Setup
    dealer = Dealer()
    dealer.give_hand(Hand([("10", "H"), ("A", "H")]))
    player1 = Player("test_name", 80.)
    hand1 = Hand([("10", "H"), ("A", "H")], bet=10.)
    hand2 = Hand([("A", "H"), ("J", "H")], bet=10.)
    player1.give_hand(hand1)
    player1.give_hand(hand2)
    player2 = Player("test_name", 80.)
    hand3 = Hand([("K", "H"), ("5", "H")], bet=10.)
    player2.give_hand(hand3)
    players = [player1, player2]
    # Assertion
    assert blackjack.complete_dealer_turn(players) == True


# dealer_turn()


def test_dealer_turn_blackjack():
    """dealer_turn(): dealer gets a blackjack"""
    # Setup
    deck = [("3", "H"), ("4", "H"), ("5", "H")]
    dealer = Dealer()
    hand = Hand([("A", "H"), ("10", "H")])
    dealer.give_hand(hand)
    # Function call
    blackjack.dealer_turn(dealer, deck)
    # Assertions
    assert not hand.is_active
    assert hand.cards == [("A", "H"), ("10", "H")]
    assert len(deck) == 3


def test_dealer_turn_double_hit_stick():
    """dealer_turn(): dealer hits twice, then sticks"""
    # Setup
    deck = [("10", "H"), ("8", "H"), ("2", "H")]
    dealer = Dealer()
    hand = Hand([("5", "H"), ("3", "H")])
    dealer.give_hand(hand)
    # Function call
    blackjack.dealer_turn(dealer, deck)
    # Assertions
    assert not hand.is_active
    assert hand.cards == [("5", "H"), ("3", "H"), ("2", "H"), ("8", "H")]
    assert len(deck) == 1


def test_dealer_turn_soft_17_stick():
    """dealer_turn(): dealer above a soft 17 and sticks"""
    # Setup
    deck = [("Q", "H"), ("10", "H"), ("3", "H")]
    dealer = Dealer()
    hand = Hand([("A", "H"), ("8", "H")])
    dealer.give_hand(hand)
    # Function call
    blackjack.dealer_turn(dealer, deck)
    # Assertions
    assert not hand.is_active
    assert hand.cards == [("A", "H"), ("8", "H")]
    assert len(deck) == 3


# ---------- MAIN GAME LOOP AND ROUND FUNCTIONS ----------


from blackjack import Player, Asker, Card
from support.testing_util import player_chooses

import pytest


# ----------- CARD -----------


# __init__()


def test_card_valid():
    """__init__(): check card created as expected"""
    card = Card("A", "H")
    assert card._Card__rank == "A"
    assert card._Card__suit == "H"


def test_card_invalid_rank():
    """__init__(): only valid ranks allowed"""
    with pytest.raises(ValueError):
        Card("11", "H")


def test_card_invalid_suit():
    """__init__(): only valid suits allowed"""
    with pytest.raises(ValueError):
        Card("A", "P")


# get_rank()


def test_card_get_rank():
    """get_rank(): rank returned"""
    card = Card("A", "H")
    assert card.get_rank() == "A"


# get_suit()


def test_card_get_suit():
    """get_suit(): suit returned"""
    card = Card("A", "H")
    assert card.get_suit() == "H"


# ----------- ASKER -----------


# ask_number_of_decks()


def test_ask_number_of_decks_valid(monkeypatch):
    """ask_number_of_decks(): check a valid number gets returned"""
    player_chooses(["4"], monkeypatch)
    assert Asker.ask_number_of_decks() == 4


def test_ask_number_of_decks_too_many(monkeypatch):
    """ask_number_of_decks(): a number above the max deck asks the user again."""
    player_chooses([str(Asker.MAX_DECK_PACKS + 1), "2"], monkeypatch)
    assert Asker.ask_number_of_decks() == 2


def test_ask_number_of_decks_max(monkeypatch):
    """ask_number_of_decks(): a number equal to the max is valid."""
    player_chooses([str(Asker.MAX_DECK_PACKS)], monkeypatch)
    assert Asker.ask_number_of_decks() == Asker.MAX_DECK_PACKS


def test_ask_number_of_decks_too_few(monkeypatch):
    """ask_number_of_decks(): a number too low will make user input again."""
    player_chooses(["0", "3"], monkeypatch)
    assert Asker.ask_number_of_decks() == 3


def test_ask_number_of_decks_invalid(monkeypatch):
    """ask_number_of_decks(): not a number asks the user for input again"""
    player_chooses(["a", "4"], monkeypatch)
    assert Asker.ask_number_of_decks() == 4


def test_ask_number_of_decks_multiple_attempts(monkeypatch):
    """ask_number_of_decks(): the user is prompted until a valid input"""
    player_chooses(["a", "0", "100", "10", "b", "1"], monkeypatch)
    assert Asker.ask_number_of_decks() == 1


# ask_number_of_players()


def test_ask_number_of_players_single(monkeypatch):
    """ask_number_of_players(): a single player is allowed to play"""
    player_chooses(["1"], monkeypatch)
    assert Asker.ask_number_of_players() == 1


def test_ask_number_of_players_valid(monkeypatch):
    """ask_number_of_players(): a valid number returns the number"""
    player_chooses(["3"], monkeypatch)
    assert Asker.ask_number_of_players() == 3


def test_ask_number_of_players_invalid(monkeypatch):
    """ask_number_of_players(): an invalid number forces the user to try again."""
    player_chooses(["a", "2"], monkeypatch)
    assert Asker.ask_number_of_players() == 2


def test_ask_number_of_players_too_many(monkeypatch):
    """ask_number_of_players(): too many players prompts the user to try again."""
    player_chooses([str(Asker.MAX_PLAYERS+1), "2"], monkeypatch)
    assert Asker.ask_number_of_players() == 2


def test_ask_number_of_players_max(monkeypatch):
    """ask_number_of_players(): max players is a valid input"""
    player_chooses([str(Asker.MAX_PLAYERS), "2"], monkeypatch)
    assert Asker.ask_number_of_players() == Asker.MAX_PLAYERS


def test_ask_number_of_players_too_few(monkeypatch):
    """ask_number_of_players(): too few players prompts the user again."""
    player_chooses(["0", "2"], monkeypatch)
    assert Asker.ask_number_of_players() == 2


def test_ask_number_of_players_multiple_attempts(monkeypatch):
    """ask_number_of_players(): function will ask until a valid input is provided"""
    player_chooses(["0", "a", "100", "10", "3"], monkeypatch)
    assert Asker.ask_number_of_players() == 3


# ask_player_name()


def test_ask_player_name_non_empty(monkeypatch):
    """ask_player_name(): check name returns when non-empty"""
    player_chooses(["test_name"], monkeypatch)
    assert Asker.ask_player_name(1) == "test_name"


def test_ask_player_name_empty(monkeypatch):
    """ask_player_name(): check default name returns, and indexes properly"""
    player_chooses([""], monkeypatch)
    assert Asker.ask_player_name(0) == "Player 1"


# ask_player_purse()


def test_ask_player_purse_valid(monkeypatch):
    """ask_player_purse(): valid input returns number as int"""
    player_chooses(["10000"], monkeypatch)
    assert Asker.ask_player_purse() == 10000


def test_ask_player_purse_invalid(monkeypatch):
    """ask_player_purse(): invalid input asks again"""
    player_chooses(["a", "b", "50000"], monkeypatch)
    assert Asker.ask_player_purse() == 50000


def test_ask_player_purse_too_low(monkeypatch):
    """ask_player_purse(): purse must be greater than or equal to minimum bet"""
    player_chooses([str(Asker.MINIMUM_BET - 1), "50000"], monkeypatch)
    assert Asker.ask_player_purse() == 50000


# ask_player_bet()


def test_ask_player_bet_valid(monkeypatch):
    """ask_player_bet(): a valid bet is returned as an int"""
    player_chooses(["1000"], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == 1000


def test_ask_player_bet_insufficient_funds(monkeypatch):
    """ask_player_bet(): insufficient funds (purse below minimum) raises an error"""
    player_chooses([], monkeypatch)
    player = Player("test_name", Asker.MINIMUM_BET - 1.0)
    with pytest.raises(ValueError):
        Asker.ask_player_bet(player)


def test_ask_player_bet_invalid(monkeypatch):
    """ask_player_bet(): invalid inputs prompts user again"""
    player_chooses(["A", "1000"], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == 1000


def test_ask_player_bet_less_than_minimum(monkeypatch):
    """ask_player_bet(): input must be greater than or equal to minimum bet"""
    player_chooses([str(Asker.MINIMUM_BET - 1.0), "1000"], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == 1000


def test_ask_player_bet_equal_to_minimum(monkeypatch):
    """ask_player_bet(): input equal to minimum bet is valid"""
    player_chooses([str(Asker.MINIMUM_BET)], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == Asker.MINIMUM_BET


def test_ask_player_bet_greater_than_purse(monkeypatch):
    """ask_player_bet(): input must be less than purse amount"""
    player_chooses(["200000", "1000"], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == 1000


def test_ask_player_bet_multiple_attempts(monkeypatch):
    """ask_player_bet(): multiple attempts until valid input provided"""
    player_chooses(["2000000", "A", "b", "0", "2000"], monkeypatch)
    player = Player("test_name", 10000)
    assert Asker.ask_player_bet(player) == 2000


# ask_player_action()


def test_ask_player_action_valid(monkeypatch):
    """ask_player_action(): a player inputs a valid option"""
    player_chooses(["stick"], monkeypatch)
    assert Asker.ask_player_action(
        ["hit", "stick", "split", "double-down"]) == "stick"


def test_ask_player_action_invalid(monkeypatch):
    """ask_player_action(): a player inputs an invalid option, then valid"""
    player_chooses(["double-down", "hit"], monkeypatch)
    assert Asker.ask_player_action(
        ["hit", "stick", "split"]) == "hit"

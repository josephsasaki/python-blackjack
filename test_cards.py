from blackjack import Asker
from cards import Deck, Card, Hand
from has_hands import Player


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


# ----------- DECK -----------


# __init__()


def test_deck_generate_cards():
    """__init__(): deck correctly generates cards"""
    assert len(Deck(number_of_decks=1)._Deck__cards) == 52
    assert len(Deck(number_of_decks=2)._Deck__cards) == 104
    assert len(Deck(number_of_decks=3)._Deck__cards) == 156
    assert len(Deck(number_of_decks=4)._Deck__cards) == 208


def test_deck_pass_cards():
    """__init__(): passed cards"""
    cards = [Card("4", "D"), Card("A", "H"),
             Card("Q", "C"), Card("7", "S")]
    deck = Deck(cards=cards)
    assert deck._Deck__cards == cards


def test_deck_both_none():
    """__init__(): error raised when nothing passed"""
    with pytest.raises(ValueError):
        Deck()


# shuffle()


def test_deck_shuffle():
    """shuffle(): check the deck is shuffled"""
    deck = Deck(number_of_decks=1)
    card1 = deck._Deck__cards[0]
    deck.shuffle(123456)
    card2 = deck._Deck__cards[0]
    assert card1 is not card2


# take_card_from_deck()


def test_deck_pick():
    """take_card_from_deck(): test that a card is returned and deck removes card."""
    top_card = Card("3", "H")
    cards = [Card("4", "D"),
             Card("A", "H"), Card("Q", "C"),
             Card("7", "S"), top_card]
    deck = Deck(cards=cards)
    card = deck.pick()
    assert card == top_card
    assert len(deck._Deck__cards) == 4


def test_take_card_from_deck_empty_deck():
    """take_card_from_deck(): Error raised if deck is empty"""
    deck = Deck(number_of_decks=1)
    deck._Deck__cards = []
    with pytest.raises(ValueError):
        deck.pick()


# ----------- HAND -----------


# __init__()

def test_hand_empty():
    assert Hand()._Hand__cards == []


def test_hand_no_bet():
    assert Hand()._Hand__bet is None


def test_hand_cards():
    cards = [Card("A", "H"), Card("3", "D")]
    assert Hand(cards).Hand__cards == cards


def test_hand_bet():
    assert Hand(bet=1000).


# is_active()


# get_bet()


# add_card()


# get_score()


# is_blackjack()


# is_bust()


# can_split()


# can_double_down()

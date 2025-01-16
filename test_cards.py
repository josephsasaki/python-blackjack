import pytest
from support.testing_util import player_chooses
from cards import Deck, Card, Hand
from settings import Settings


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
    """__init__(): by default, empty list of cards"""
    assert Hand()._Hand__cards == []


def test_hand_non_cards():
    """__init__(): cards passed must be card objects"""
    with pytest.raises(ValueError):
        Hand(cards=[("A", "H"), ("K", "D")])


def test_hand_cards():
    """__init__(): passed cards correctly"""
    cards = [Card("A", "H"), Card("3", "D")]
    assert Hand(cards)._Hand__cards == cards


def test_hand_bet():
    """__init__(): bet stored after hand created"""
    assert Hand(bet=1000)._Hand__bet == 1000


def test_hand_no_bet():
    """__init__(): by default, bet is none"""
    assert Hand()._Hand__bet is None


def test_hand_invalid_bet():
    """__init__(): bet must be an integer"""
    with pytest.raises(ValueError):
        Hand(bet="1000")


def test_hand_bet_just_big_enough():
    """__init__(): minimum bet allowed"""
    hand = Hand(bet=Settings.MINIMUM_BET)
    assert hand._Hand__bet == Settings.MINIMUM_BET


def test_hand_bet_too_small():
    """__init__(): less than minimum bet is not allowed"""
    with pytest.raises(ValueError):
        Hand(bet=Settings.MINIMUM_BET - 1)


def test_hand_is_active_default():
    """__init__(): by default, hand is active"""
    assert Hand()._Hand__is_active


# number_of_cards()

def test_hand_number_of_cards_zero():
    hand = Hand()
    assert hand.number_of_cards() == 0


def test_hand_number_of_cards_multiple():
    hand = Hand(cards=[Card("A", "H"), Card("A", "H")])
    assert hand.number_of_cards() == 2


# is_active()


def test_hand_is_active_true():
    """is_active(): method returns is active when true"""
    hand = Hand()
    hand._Hand__is_active = True
    assert hand.is_active()


def test_hand_is_active_false():
    """is_active(): method returns is active when false"""
    hand = Hand()
    hand._Hand__is_active = False
    assert not hand.is_active()


# deactivate()

def test_hand_deactivate():
    """deactivate(): hand is active becomes false"""
    hand = Hand()
    assert hand.is_active()
    hand.deactivate()
    assert not hand.is_active()


# get_bet()


def test_hand_get_bet():
    """get_bet(): bet returned as expected"""
    hand = Hand(bet=10000)
    assert hand.get_bet() == 10000


# add_card()


def test_hand_add_card():
    """add_card(): card added as expected"""
    cards = [Card("A", "H"), Card("K", "D")]
    hand = Hand(cards=cards.copy())
    new_card = Card("3", "C")
    hand.add_card(new_card)
    assert hand._Hand__cards == cards + [new_card]


def test_hand_add_card_invalid():
    """add_card(): card must be card object"""
    with pytest.raises(ValueError):
        Hand().add_card(("A", "H"))


# get_score()


def test_hand_get_score_just_numbers():
    """Hand.get_score(): just numbered cards add correctly"""
    assert Hand([Card("2", "H"), Card("5", "C"),
                Card("9", "D")]).get_score() == 16


def test_hand_get_score_ace_11():
    """Hand.get_score(): single ace is treated as 11"""
    assert Hand([Card("A", "H"), Card("5", "C")]).get_score() == 16


def test_hand_get_score_ace_1():
    """Hand.get_score(): single ace is treated as 1"""
    assert Hand([Card("A", "H"), Card("5", "C"),
                Card("9", "D")]).get_score() == 15


def test_hand_get_score_double_ace():
    """Hand.get_score(): double aces, one is 1 and another 11"""
    assert Hand([Card("A", "H"), Card("A", "C")]).get_score() == 12


def test_hand_get_score_triple_ace():
    """Hand.get_score(): triple aces, 1 ,1 and 11"""
    assert Hand([Card("A", "H"), Card("A", "C"),
                Card("A", "D")]).get_score() == 13


def test_hand_get_score_blackjack_single_ace():
    """Hand.get_score(): ace is an 11 when score could be 21"""
    assert Hand([Card("A", "H"), Card("K", "C")]).get_score() == 21


def test_hand_get_score_blackjack_double_ace():
    """Hand.get_score(): aces are 1 and 11 when score could be 21"""
    assert Hand([Card("A", "H"), Card("10", "C"),
                Card("A", "D")]).get_score() == 12


def test_hand_get_score_blackjack_test1():
    """Hand.get_score(): """
    assert Hand([Card("A", "H"), Card("7", "C"),
                Card("6", "D")]).get_score() == 14


def test_hand_get_score_blackjack_test2():
    """Hand.get_score(): """
    assert Hand([Card("A", "H"), Card("7", "C"), Card("6", "D"),
                Card("7", "D")]).get_score() == 21


def test_hand_get_score_blackjack_test3():
    """Hand.get_score(): """
    assert Hand([Card("A", "H"), Card("7", "C"), Card("6", "D"),
                Card("8", "D")]).get_score() == 22


def test_hand_get_score_empty_hand():
    """Hand.get_score(): receiving an empty hand raises an error"""
    with pytest.raises(ValueError):
        Hand([]).get_score()


# is_blackjack()


def test_hand_is_blackjack_valid():
    """is_blackjack(): valid cards produce a blackjack"""
    assert Hand([Card("A", "H"), Card("K", "D")]).is_blackjack()


def test_hand_is_blackjack_invalid():
    """is_blackjack(): invalid cards do not produce a blackjack"""
    assert not Hand([Card("A", "H"), Card("9", "D")]).is_blackjack()


# is_bust()


def test_hand_is_bust_valid():
    """is_bust(): valid cards produce a bust"""
    assert Hand([Card("10", "H"), Card("5", "D"), Card("7", "H")]).is_bust()


def test_hand_is_bust_invalid():
    """is_bust(): valid cards produce a not bust"""
    assert not Hand([Card("A", "H"), Card("5", "D")]).is_bust()


# has_pair()


def test_hand_has_pair_not_two():
    """has_pair(): if there aren't two cards, return false"""
    assert not Hand([Card("5", "H"), Card(
        "5", "D"), Card("5", "D")]).has_pair()


def test_hand_has_pair_not_same():
    """has_pair(): two cards but different rank, return false"""
    assert not Hand([Card("5", "D"), Card("4", "D")]).has_pair()


def test_hand_has_pair():
    """has_pair(): returns true"""
    assert Hand([Card("5", "H"), Card("5", "D")]).has_pair()


# pop_card()


def test_hand_pop_card():
    """pop_card(): check the correct card is returned"""
    card1 = Card("A", "H")
    card2 = Card("K", "D")
    hand = Hand([card1, card2])
    assert hand.pop_card() == card2
    assert hand.number_of_cards() == 1


# double_bet()


def test_hand_double_bet():
    """double_bet(): the bet doubles"""
    hand = Hand(bet=10000)
    hand.double_bet()
    assert hand.get_bet() == 20000


# get_card_by_index()


def test_hand_get_card_by_index():
    """get_card_by_index(): the bet doubles"""
    card1 = Card("A", "H")
    card2 = Card("K", "D")
    hand = Hand([card1, card2])
    assert hand.get_card_by_index(0) == card1
    assert hand.get_card_by_index(1) == card2

# pylint: skip-file

from models import Hand, HasHands, Player
import pytest
from support.testing_util import player_chooses


def test_hand_instantiation_cards_passed():
    """Hand.__init__(): cards are passed to the attribute"""
    hand = Hand([("2", "H"), ("3", "D")])
    assert hand.cards == [("2", "H"), ("3", "D")]


def test_hand_instantiation_no_cards_passed():
    """Hand.__init__(): no cards are passed, so empty list"""
    hand = Hand()
    assert hand.cards == []


def test_hand_instantiation_attributes():
    """Hand.__init__(): attributes are defined as expected"""
    hand = Hand()
    assert hand.is_active
    assert hand.bet is None


def test_hand_instantiation_bet():
    """Hand.__init__(): test bet attribute correctly assigned when arg passed"""
    hand = Hand(bet=10)
    assert hand.bet == 10


def test_hand_add_card():
    """Hand.add_card(): card added"""
    card = ("2", "H")
    hand = Hand()
    hand.add_card(card)
    assert hand.cards == [("2", "H")]


def test_hand_clear_hand():
    """Hand.add_card(): hand is cleared"""
    hand = Hand([("2", "H"), ("3", "C")])
    hand.clear_hand()
    assert hand.cards == []


def test_hand_get_score_just_numbers():
    """Hand.get_score(): just numbered cards add correctly"""
    assert Hand([("2", "H"), ("5", "C"), ("9", "D")]).get_score() == 16


def test_hand_get_score_ace_11():
    """Hand.get_score(): single ace is treated as 11"""
    assert Hand([("A", "H"), ("5", "C")]).get_score() == 16


def test_hand_get_score_ace_1():
    """Hand.get_score(): single ace is treated as 1"""
    assert Hand([("A", "H"), ("5", "C"), ("9", "D")]).get_score() == 15


def test_hand_get_score_double_ace():
    """Hand.get_score(): double aces, one is 1 and another 11"""
    assert Hand([("A", "H"), ("A", "C")]).get_score() == 12


def test_hand_get_score_triple_ace():
    """Hand.get_score(): triple aces, 1 ,1 and 11"""
    assert Hand([("A", "H"), ("A", "C"), ("A", "D")]).get_score() == 13


def test_hand_get_score_blackjack_single_ace():
    """Hand.get_score(): ace is an 11 when score could be 21"""
    assert Hand([("A", "H"), ("K", "C")]).get_score() == 21


def test_hand_get_score_blackjack_double_ace():
    """Hand.get_score(): aces are 1 and 11 when score could be 21"""
    assert Hand([("A", "H"), ("10", "C"), ("A", "D")]).get_score() == 12


def test_hand_get_score_blackjack_test1():
    """Hand.get_score(): """
    assert Hand([("A", "H"), ("7", "C"), ("6", "D")]).get_score() == 14


def test_hand_get_score_blackjack_test2():
    """Hand.get_score(): """
    assert Hand([("A", "H"), ("7", "C"), ("6", "D"),
                ("7", "D")]).get_score() == 21


def test_hand_get_score_blackjack_test3():
    """Hand.get_score(): """
    assert Hand([("A", "H"), ("7", "C"), ("6", "D"),
                ("8", "D")]).get_score() == 22


def test_hand_get_score_empty_hand():
    """Hand.get_score(): receiving an empty hand raises an error"""
    with pytest.raises(ValueError):
        Hand([]).get_score()


def test_hand_is_blackjack_valid():
    """Hand.is_blackjack(): valid cards produce a blackjack"""
    assert Hand([("A", "H"), ("K", "D")]).is_blackjack()


def test_hand_is_blackjack_invalid():
    """Hand.is_blackjack(): valid cards produce a blackjack"""
    assert not Hand([("A", "H"), ("9", "D")]).is_blackjack()


def test_hand_hit_active():
    """Hand.hit(): a hand is hit and remains active"""
    deck = [("Q", "H"), ("K", "D"), ("5", "C")]
    hand = Hand([("A", "H"), ("9", "D")])
    hand.hit(deck)
    assert hand.cards == [("A", "H"), ("9", "D"), ("5", "C")]
    assert hand.is_active
    assert len(deck) == 2


def test_hand_hit_inactive():
    """Hand.hit(): a hand is hit and becomes inactive"""
    deck = [("Q", "H"), ("K", "D"), ("5", "C")]
    hand = Hand([("10", "H"), ("9", "D")])
    hand.hit(deck)
    assert hand.cards == [("10", "H"), ("9", "D"), ("5", "C")]
    assert not hand.is_active
    assert len(deck) == 2


def test_hand_stick():
    """Hand.hit(): sticking to a hand causes it to become inactive"""
    hand = Hand([("10", "H"), ("9", "D")])
    hand.stick()
    assert not hand.is_active


def test_hand_can_split_valid():
    """Hand.can_split(): hand can split"""
    player = Player(name="test_name", purse=100)
    assert Hand([("A", "H"), ("A", "D")], bet=10).can_split(player)


def test_hand_can_split_invalid():
    """Hand.can_split(): hand cant split"""
    player = Player(name="test_name", purse=100)
    assert not Hand([("Q", "H"), ("K", "D")], bet=10).can_split(player)


def test_hand_can_split_insufficient_funds():
    """Hand.can_split(): hand can split but not enough money"""
    player = Player(name="test_name", purse=10)
    assert not Hand([("Q", "H"), ("Q", "D")], bet=20).can_split(player)


def test_hand_split():
    """Hand.split(): hand is split"""
    deck = [("Q", "H"), ("K", "D"), ("5", "C")]
    player = Player(name="test_name", purse=100)
    hand = Hand([("A", "H"), ("A", "D")], bet=10)
    player.give_hand(hand)
    hand.split(deck=deck, player=player)
    assert hand.cards == [("A", "H"), ("5", "C")]
    assert len(player.hands) == 2
    assert player.hands[1].cards == [("A", "D"), ("K", "D")]
    assert len(deck) == 1
    assert player.purse == 90
    assert hand.bet == 10
    assert player.hands[1].bet == 10


def test_hand_can_double_down_valid():
    """Hand.can_double_down(): a hand with only two cards can be double-downed"""
    player = Player(name="test_name", purse=100)
    assert Hand([("A", "H"), ("A", "D")], bet=10).can_double_down(player)


def test_hand_can_double_down_invalid():
    """Hand.can_double_down(): a hand with three cards cannot be double-downed"""
    player = Player(name="test_name", purse=100)
    assert not Hand([("A", "H"), ("A", "D"), ("4", "C")],
                    bet=10).can_double_down(player)


def test_hand_can_double_down_insufficient_funds():
    """Hand.can_double_down(): hand can be double-downed but not enough money"""
    player = Player(name="test_name", purse=10)
    assert not Hand([("A", "H"), ("A", "D")],
                    bet=20).can_double_down(player)


def test_hashands_instantiation():
    """HasHands.__init__(): expected object produced"""
    has_hands = HasHands()
    assert has_hands.hands == []


def test_hashands_give_hand():
    """HasHands.give_hand(): hand added"""
    hand = Hand([("A", "H"), ("K", "D")])
    has_hands = HasHands()
    has_hands.give_hand(hand)
    assert has_hands.hands == [hand]


def test_hashands_get_next_hand_returned():
    """HasHands.get_next_hand(): first active hand returned"""
    hand1 = Hand([("A", "H")])
    hand1.is_active = False
    hand2 = Hand([("A", "S")])
    hand3 = Hand([("A", "D")])
    has_hands = HasHands()
    has_hands.give_hand(hand1)
    has_hands.give_hand(hand2)
    has_hands.give_hand(hand3)
    assert has_hands.get_next_hand() == hand2


def test_hashands_get_next_hand_none():
    """HasHands.get_next_hand(): no active hands so none returned"""
    hand1 = Hand([("A", "H")])
    hand2 = Hand([("A", "S")])
    hand3 = Hand([("A", "D")])
    hand1.is_active = False
    hand2.is_active = False
    hand3.is_active = False
    has_hands = HasHands()
    has_hands.give_hand(hand1)
    has_hands.give_hand(hand2)
    has_hands.give_hand(hand3)
    assert has_hands.get_next_hand() == None

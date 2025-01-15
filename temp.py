# pylint: skip-file

from models import Hand, HasHands, Player, Dealer
import pytest
from support.testing_util import player_chooses


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


def test_dealer_upcard():
    """Dealer.upcard(): returns the second card in hand, seen"""
    dealer = Dealer()
    hand = Hand([("A", "H"), ("K", "D")])
    dealer.give_hand(hand)
    assert dealer.upcard() == ("K", "D")


def test_dealer_hole_card():
    """Dealer.hole_card(): returns the first card in hand, hidden"""
    dealer = Dealer()
    hand = Hand([("A", "H"), ("K", "D")])
    dealer.give_hand(hand)
    assert dealer.hole_card() == ("A", "H")

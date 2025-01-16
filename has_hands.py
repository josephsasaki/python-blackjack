
from cards import Hand, Deck


class HasHands():

    def __init__(self):
        self.__hands = []
        self.__split_count = 0

    def reset(self) -> None:
        self.__hands = []
        self.__split_count = 0

    def give_hand(self, hand: Hand) -> None:
        if not isinstance(hand, Hand):
            raise ValueError("Hand object not passed.")
        self.__hands.append(hand)

    def get_next_hand(self) -> Hand:
        for hand in self.__hands:
            if hand.is_active():
                return hand
        return None

    def hit(self, hand: Hand, deck: Deck) -> None:
        drawn_card = deck.pick()
        hand.add_card(drawn_card)
        if hand.is_bust() or hand.number_of_cards() == 5:
            hand.deactivate()

    def stick(self, hand: Hand) -> None:
        hand.deactivate()


class Player(HasHands):

    def __init__(self, name: str, purse: int):
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if name == "":
            raise ValueError("Name cannot be empty.")
        if not isinstance(purse, int):
            raise ValueError("Purse amount must be an integer.")
        super().__init__()
        self.__name = name
        self.__purse = purse

    def get_name(self):
        return self.__name

    def get_purse(self):
        return self.__purse

    def get_split_count(self) -> int:
        return self.__split_count

    def can_split(self, hand: Hand):
        # Check player has enough money
        if self.__purse < hand.get_bet():
            return False
        return hand.has_pair()

    def can_double_down(self, hand: Hand):
        return self.__purse >= hand.get_bet() and hand.number_of_cards() == 2

    def split(self, hand: Hand, deck: Deck):
        # Take the further bet from the player
        self.__purse -= hand.get_bet()
        # Take the second card and produce a new hand
        second_card = hand.pop_card()
        split_hand = Hand(cards=[second_card], bet=hand.get_bet())
        # Hit each hand with a new card
        self.hit(hand, deck)
        self.hit(split_hand, deck)
        # give player the new hand
        self.give_hand(split_hand)

    def double_down(self, hand: Hand, deck: Deck):
        # Take the further bet from the player
        self.__purse -= hand.get_bet()
        self.hit(hand, deck)
        hand.double_bet()
        hand.deactivate()

    def reset(self) -> None:
        self.__hands = []
        self.__split_count = 0


class Dealer(HasHands):

    def upcard(self):
        return self.__hands[0].get_card_by_index(1)

    def hole_card(self):
        return self.__hands[0].get_card_by_index(0)

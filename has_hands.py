
from cards import Hand


class HasHands():
    def __init__(self):
        self.hands = []
        self.split_count = 0

    def give_hand(self, hand: Hand):
        self.hands.append(hand)

    def get_next_hand(self) -> Hand:
        for hand in self.hands:
            if hand.is_active:
                return hand
        # If this point reached, all hands are resolved
        return None

    def reset(self) -> None:
        self.hands = []
        self.split_count = 0


class Player(HasHands):
    def __init__(self, name, purse):
        super().__init__()
        self.name = name
        self.purse = purse


class Dealer(HasHands):
    def __init__(self):
        super().__init__()

    def upcard(self):
        return self.hands[0].cards[1]

    def hole_card(self):
        return self.hands[0].cards[0]

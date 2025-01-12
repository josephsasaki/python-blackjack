
class Hand():
    """Object representing a hand, which contains a list of cards. From this object, the
    hand score is calculated, as well as whether the hand is ongoing."""

    def __init__(self, cards: list[(str)] = None, bet=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.is_active = True
        self.bet = bet

    def add_card(self, card: (str)) -> None:
        self.cards.append(card)

    def clear_hand(self) -> None:
        self.cards = []

    def get_score(self) -> int:
        hand: list[(str)] = self.cards
        # Check list is not empty
        if len(hand) == 0:
            raise ValueError("Hand cannot be empty.")
        # First, extract the ranks from the hand
        ranks = [rank for (rank, suit) in hand]
        # Replace the jacks, queens and kings with a ten
        ranks = list(map(lambda rank: "10" if rank in {
            "J", "Q", "K"} else rank, ranks))
        # Get how many aces and remove from list
        aces_quantity = ranks.count("A")
        number_ranks = [int(rank) for rank in ranks if rank != "A"]
        # Add up the number ranks
        score = sum(number_ranks)
        # Check whether there are aces
        if aces_quantity == 0:
            return score
        # Add aces such that score is maximised but <= 21
        eleven_counter = aces_quantity
        aces_score = [11]*eleven_counter
        while sum(aces_score) + score > 21 and eleven_counter > 0:
            eleven_counter -= 1
            aces_score = [11]*eleven_counter + \
                [1]*(aces_quantity-eleven_counter)
        # Return final score
        return sum(aces_score) + score

    def is_blackjack(self) -> bool:
        # First, check the score is 21
        if self.get_score() != 21:
            return False
        if len(self.cards) != 2:
            return False
        return True

    def is_bust(self) -> bool:
        return self.get_score() > 21

    def hit(self, deck):
        drawn_card = deck.pop()
        self.add_card(drawn_card)
        if self.get_score() >= 21:
            self.is_active = False

    def stick(self):
        self.is_active = False

    def can_split(self, player):
        # Check player has enough money
        if player.purse < self.bet:
            return False
        if len(self.cards) != 2:
            return False
        if self.cards[0][0] != self.cards[1][0]:
            return False
        return True

    def split(self, deck: list[(str)], player):
        # Take the further bet from the player
        player.purse -= self.bet
        # Take the second card and produce a new hand
        second_card = self.cards.pop()
        split_hand = Hand(cards=[second_card], bet=self.bet)
        # Hit each hand with a new card
        self.add_card(deck.pop())
        split_hand.add_card(deck.pop())
        # give player the new hand
        player.give_hand(split_hand)

    def can_double_down(self, player):
        return player.purse >= self.bet and len(self.cards) == 2

    def double_down(self, deck, player):
        # Take the further bet from the player
        player.purse -= self.bet
        self.hit(deck)
        self.bet *= 2
        self.is_active = False


class HasHands():
    def __init__(self):
        self.hands = []

    def give_hand(self, hand: Hand):
        self.hands.append(hand)

    def get_next_hand(self) -> Hand:
        for hand in self.hands:
            if hand.is_active:
                return hand
        # If this point reached, all hands are resolved
        return None

    def reset_hand(self) -> None:
        self.hands = []


class Player(HasHands):
    def __init__(self, name, purse):
        super().__init__()
        self.name = name
        self.purse = purse


class Dealer(HasHands):
    def __init__(self):
        super().__init__()


from has_hands import Player

from random import Random


class Card():

    SUITS = ["S", "D", "H", "C"]
    RANKS = ["A", "2", "3", "4", "5", "6",
                  "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, rank: str, suit: str):
        if rank not in Card.RANKS:
            raise ValueError("Invalid rank passed.")
        if suit not in Card.SUITS:
            raise ValueError("Invalid suit passed.")
        self.__rank = rank
        self.__suit = suit

    def get_rank(self) -> str:
        return self.__rank

    def get_suit(self) -> str:
        return self.__suit


class Deck():

    MAX_DECK_PACKS = 5

    def __init__(self, cards: list[Card] = None, number_of_decks: int = None):
        if cards is None and number_of_decks is not None:
            self.__cards = []
            self.__generate_deck(number_of_decks)
        elif cards is not None and number_of_decks is None:
            self.__cards = []
            self.__pass_cards(cards)
        else:
            raise ValueError("Missing arguments.")

    def __generate_deck(self, number_of_decks: int) -> None:
        if not isinstance(number_of_decks, int):
            raise ValueError("Invalid number of decks passed.")
        if number_of_decks < 0 or number_of_decks > Deck.MAX_DECK_PACKS:
            raise ValueError("Invalid number of decks passed.")
        for _ in range(number_of_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.__cards.append(Card(rank, suit))

    def __pass_cards(self, cards: list[Card]):
        if not all([isinstance(card, Card) for card in cards]):
            raise ValueError("All passed cards must be Card objects.")
        if len(cards) == 0:
            raise ValueError("Deck cannot be empty.")
        self.__cards = cards

    def pick(self) -> Card:
        if len(self.__cards) == 0:
            raise ValueError("Taking card from empty deck.")
        return self.__cards.pop()

    def shuffle(self, seed: int) -> None:
        """Randomizes the deck of cards"""
        Random(seed).shuffle(self.__cards)


class Hand():

    def __init__(self, cards: list[Card] = None, bet=None):
        if cards is None:
            self.__cards = []
        else:
            if not all([isinstance(card, Card) for card in cards]):
                raise ValueError("All passed cards must be Card objects.")
            self.__cards = cards
        self.__is_active = True
        self.__bet = bet

    def is_active(self) -> bool:
        return self.__is_active

    def get_bet(self) -> int:
        return self.__bet

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise ValueError("Invalid card object passed.")
        self.__cards.append(card)

    def clear_hand(self) -> None:
        self.__cards = []

    def get_score(self) -> int:
        hand = self.__cards
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
        # Add aces such that score is maximized but <= 21
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
        if len(self.__cards) != 2:
            return False
        return True

    def is_bust(self) -> bool:
        return self.get_score() > 21

    def hit(self, deck: Deck) -> None:
        drawn_card = deck.pick()
        self.add_card(drawn_card)
        if self.get_score() >= 21:
            self.__is_active = False
        if len(self.cards) == 5:
            self.__is_active = False

    def stick(self) -> None:
        self.__is_active = False

    def can_split(self, player: Player):
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

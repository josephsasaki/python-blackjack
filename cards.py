from settings import Settings
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

    def __repr__(self) -> str:
        return self.__rank + self.__suit


class Deck():

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
        if number_of_decks < 0 or number_of_decks > Settings.MAX_DECK_PACKS:
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

    def __init__(self, cards: list[Card] = None):
        # cards
        if cards is None:
            self.__cards = []
        else:
            if not all([isinstance(card, Card) for card in cards]):
                raise ValueError("All passed cards must be Card objects.")
            self.__cards = cards
        # is_active
        self.__bet = None
        self.__is_active = True

    def get_status(self):
        if self.is_blackjack():
            return "Blackjack"
        elif self.is_bust():
            return "Bust"
        elif not self.__is_active:
            return "Stuck"
        else:
            return "Active"

    def get_cards_copy(self) -> list[Card]:
        return self.__cards.copy()

    def number_of_cards(self) -> int:
        return len(self.__cards)

    def is_active(self) -> bool:
        return self.__is_active

    def deactivate(self) -> None:
        self.__is_active = False

    def get_bet(self) -> int:
        return self.__bet

    def set_bet(self, bet: int):
        if not isinstance(bet, int):
            raise ValueError("Bet must be an integer.")
        if bet < Settings.MINIMUM_BET:
            raise ValueError("Bet must be greater than minimum bet.")
        self.__bet = bet

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise ValueError("Invalid card object passed.")
        self.__cards.append(card)

    def get_score(self) -> int:
        hand = self.__cards
        # Check list is empty
        if len(hand) == 0:
            return 0
        # First, extract the ranks from the hand
        ranks = [card.get_rank() for card in hand]
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

    def has_pair(self) -> bool:
        if self.number_of_cards() != 2:
            return False
        if self.__cards[0].get_rank() != self.__cards[1].get_rank():
            return False
        return True

    def pop_card(self) -> Card:
        return self.__cards.pop()

    def double_bet(self) -> None:
        self.__bet *= 2

    def get_card_by_index(self, index: int) -> Card:
        return self.__cards[index]

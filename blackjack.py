
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
        if len(self.cards) == 5:
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


class Asker():

    MAX_DECK_PACKS = 5
    INVALID_RESPONSE = "Invalid response. Please try again."
    MAX_PLAYERS = 5
    MINIMUM_BET = 500

    def ask_number_of_decks() -> int:
        """
        Get the number of decks that game will be played with from the user.
        """
        number_of_decks = input("How many decks do you want to play with? : ")
        try:
            number_of_decks = int(number_of_decks)
            if number_of_decks not in range(1, Asker.MAX_DECK_PACKS+1):
                raise ValueError("Invalid number of decks.")
            else:
                return number_of_decks
        except ValueError:
            print(Asker.INVALID_RESPONSE)
            return Asker.ask_number_of_decks()

    def ask_number_of_players() -> int:
        """
        The user is asked for the number of players, and this is validated.
        """
        number_of_players = input("How many players are there? : ")
        try:
            number_of_players = int(number_of_players)
            if number_of_players not in range(1, Asker.MAX_PLAYERS+1):
                raise ValueError("Number of players not in valid range.")
            else:
                return number_of_players
        except ValueError:
            print(Asker.INVALID_RESPONSE)
            return Asker.ask_number_of_players()

    def ask_player_name(index: int) -> str:
        """
        Ask the player for their name, ensuring it is not empty.
        """
        name = input(f"What is the name of Player {index + 1}? : ")
        if name == "":
            return f"Player {index + 1}"
        else:
            return name

    def ask_player_purse() -> int:
        """
        Ask the player for how much they have in their purse, ensuring valid input.
        """
        amount = input("How much money is in your purse? : ")
        try:
            amount = int(amount)
            if amount < Asker.MINIMUM_BET:
                raise ValueError(
                    "Purse amount must be greater than minimum bet.")
            return amount
        except ValueError:
            print(Asker.INVALID_RESPONSE)
            return Asker.ask_player_purse()

    def ask_player_bet(player: Player) -> int:
        """
        Ask the player how much they want to bet. Ensure the bet is less than purse amount, and there
        is sufficient funds in the purse for the minimum bet.
        """
        # First, check for sufficient funds
        if player.purse < Asker.MINIMUM_BET:
            raise ValueError(
                "Player should have been removed if insufficient funds for minimum bet.")
        # Ask for player bet amount
        bet = input(f"{player.name} : ")
        try:
            bet = int(bet)
            if bet < Asker.MINIMUM_BET or bet > player.purse:
                raise ValueError
            return bet
        except ValueError:
            print(Asker.INVALID_RESPONSE)
            return Asker.ask_player_bet(player)

    def ask_player_action(choices: list[str]) -> str:
        """
        Ask the player for whether they wish to hit, stick, split or double-down.
        """
        # Get player action
        action = input("Action : ")
        # Check the action is in the choices
        if action not in choices:
            print(Asker.INVALID_RESPONSE)
            return Asker.ask_player_action(choices)
        return action

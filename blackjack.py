from cards import Deck, Hand, Card
from has_hands import Player, Dealer
from interface import Interface
from settings import Settings


class Asker():

    INVALID_RESPONSE = "Invalid response. Please try again."

    @staticmethod
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

    @staticmethod
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


class Blackjack():

    def __init__(self):
        self.__deck = None
        self.__players = []
        self.__dealer = Dealer()
        self.__interface = Interface()

    def title(self):
        # Title screen
        self.__interface.display_title_screen()

    def setup(self):
        # Deck settings screen
        number_of_decks = self.__interface.ask_number_of_decks()
        self.__deck = Deck(number_of_decks=number_of_decks)
        # Player quantity screen
        number_of_players = self.__interface.ask_number_of_players()
        # Player information
        for i in range(1, number_of_players + 1):
            name, purse = self.__interface.ask_player_name_and_purse(i)
            player = Player(name, purse)
            self.__players.append(player)

    def deal_initial_hands(self, initial_bets: dict[str, int]) -> None:
        """
        Simulates dealing cards to each player and the dealer.
        """
        # First, give each player and dealer an empty hand with bet
        for player in self.__players:
            empty_hand = Hand(bet=initial_bets[player.get_name()])
            player.give_hand(empty_hand)
        self.__dealer.give_hand(Hand())
        # Next, go through each player and give cards to hand
        for _ in range(2):
            for person in self.__players + [self.__dealer]:
                hand = person.get_next_hand()
                person.hit(hand, self.__deck)
                self.__interface.display_table_hands(
                    self.__players, self.__dealer)

    def play_round(self):
        # Take initial bets
        initial_bets = self.__interface.ask_player_initial_bets(self.__players)
        # Deal cards
        self.deal_initial_hands(initial_bets)

    def play(self):
        self.title()
        self.setup()
        self.play_round()


if __name__ == "__main__":
    blackjack = Blackjack()
    blackjack.play()

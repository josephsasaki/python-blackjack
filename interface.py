
from cards import Hand, Card
from has_hands import Player, Dealer
from settings import Settings

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.layout import Layout
from rich.columns import Columns
from time import sleep


TITLE_GRAPHIC = [
    "╭──╮╭╮╭╮.╭────╮.╭╮.....╭────╮.╭────╮.╭╮..╭╮.╭────╮.╭────╮.╭────╮.╭╮..╭╮.",
    "│╭╮││╰╯│.│╭──╮│.││.....│╭──╮│.│╭───╯.││..││.╰──╮╭╯.│╭──╮│.│╭───╯.││..││.",
    "│╰╯│╰─╮│.│╰──╯│.││.....││..││.││.....││.╭╯│....││..││..││.││.....││.╭╯│.",
    "│╭─╯╭╮││.│╭───╯.││.....│╰──╯│.││.....│╰─╯╭╯....││..│╰──╯│.││.....│╰─╯╭╯.",
    "││..│╰╯│.│╰───╮.││.....│╭──╮│.││.....│╭─╮╰╮....││..│╭──╮│.││.....│╭─╮╰╮.",
    "╰╯..╰──╯.│╭──╮│.││.....││..││.││.....││.│.│.╭╮.││..││..││.││.....││.│.│.",
    ".........│╰──╯│.│╰───╮.││..││.│╰───╮.││.│.│.│╰─╯│..││..││.│╰───╮.││.│.│.",
    ".........╰────╯.╰────╯.╰╯..╰╯.╰────╯.╰╯.╰─╯.╰───╯..╰╯..╰╯.╰────╯.╰╯.╰─╯.",
]


HAND_GRAPHIC_5 = [
    "            ╭───────╮",
    "         ╭──┤ZZ     │",
    "      ╭──┤YY│%      │",
    "   ╭──┤XX│$ │      %│",
    "╭──┤WW│£ │  │     ZZ│",
    "│VV│@ │  │  ╰────┬──╯",
    "│! │  │  ╰────┬──╯   ",
    "│  │  ╰────┬──╯      ",
    "│  ╰────┬──╯         ",
    "╰───────╯            ",
]
HAND_GRAPHIC_4 = [
    "                     ",
    "         ╭───────╮   ",
    "      ╭──┤YY     │   ",
    "   ╭──┤XX│$      │   ",
    "╭──┤WW│£ │      $│   ",
    "│VV│@ │  │     YY│   ",
    "│! │  │  ╰────┬──╯   ",
    "│  │  ╰────┬──╯      ",
    "│  ╰────┬──╯         ",
    "╰───────╯            ",
]
HAND_GRAPHIC_3 = [
    "                     ",
    "                     ",
    "      ╭───────╮      ",
    "   ╭──┤XX     │      ",
    "╭──┤WW│£      │      ",
    "│VV│@ │      £│      ",
    "│! │  │     XX│      ",
    "│  │  ╰────┬──╯      ",
    "│  ╰────┬──╯         ",
    "╰───────╯            ",
]
HAND_GRAPHIC_2 = [
    "                     ",
    "                     ",
    "                     ",
    "   ╭───────╮         ",
    "╭──┤WW     │         ",
    "│VV│@      │         ",
    "│! │      @│         ",
    "│  │     WW│         ",
    "│  ╰────┬──╯         ",
    "╰───────╯            ",
]
HAND_GRAPHIC_1 = [
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "╭───────╮            ",
    "│VV     │            ",
    "│!      │            ",
    "│      !│            ",
    "│     VV│            ",
    "╰───────╯            ",
]
HAND_GRAPHICS = [
    HAND_GRAPHIC_1,
    HAND_GRAPHIC_2,
    HAND_GRAPHIC_3,
    HAND_GRAPHIC_4,
    HAND_GRAPHIC_5
]
TOP_RANK_REPLACE = [(5, 1), (4, 4), (3, 7), (2, 10), (1, 13)]
TOP_SUIT_REPLACE = [(6, 1), (5, 4), (4, 7), (3, 10), (2, 13)]
BOTTOM_RANK_REPLACE = [(8, 6), (7, 9), (6, 12), (5, 15), (4, 18)]
BOTTOM_SUIT_REPLACE = [(7, 7), (6, 10), (5, 13), (4, 16), (3, 19)]
SCORE_REPLACE = (0, 1)
HAND_GAP = "  │  "

# "\n".join(TITLE_GRAPHIC).replace(".", " ")
"""
Padding("", (1, 0, 0, 0)),
Align.left(
    "Please ensure your console window is large enough to fit the content."),
Padding("", (1, 0, 0, 0)),
Align.left(
    "Once you are ready to proceed, please press [bold]ENTER[/bold].")
"""


class Interface():

    PANEL_WIDTH = 180
    PANEL_HEIGHT = 20

    def __init__(self):
        self.console = Console(width=self.PANEL_WIDTH)

    @staticmethod
    def pound(pennies: int) -> str:
        return f"{(pennies/100):.2f}"

    def division_width(self, n: int) -> int:
        widths = [180, 89, 59, 44, 35]
        return widths[n-1]

    def __suit_bar(self):
        return "".join(["♠♣♥♦"]*45)

    def display_title_screen(self):
        self.console.clear()
        content = Group(
            self.__suit_bar(),
            Align.center(
                "\n".join(TITLE_GRAPHIC).replace(".", " "), vertical="middle"),
            Align.center(
                "Welcome!", vertical="middle", style="bold"),
            Padding("", (1, 0, 0, 0)),
            Align.left(
                "Please ensure your console window is large enough to fit the content."),
            Padding("", (1, 0, 0, 0)),
            Align.left(
                "Once you are ready to proceed, please press [bold]ENTER[/bold].")
        )
        self.console.print(content)
        _ = input()

    def ask_number_of_decks(self) -> int:
        data = [["Deck quantity", "---"],]
        error_message = None
        return self.__ask_number_of_decks(data, error_message)

    def __ask_number_of_decks(self, data: list[list[str]], error_message: str) -> int:
        """
        Get the number of decks that game will be played with from the user.
        """
        # Variables
        title = "DECKS"
        active_question = "How many decks do you want to play with?"
        # Print screen
        self.__display_input_screen(
            title, data, active_question, error_message)
        # Get user input
        number_of_decks = input("    > ")
        # Check validity
        if number_of_decks not in [str(n) for n in range(1, Settings.MAX_DECK_PACKS+1)]:
            error_message = "[bold red]Invalid number of decks. Please try again.[/bold red]"
            return self.__ask_number_of_decks(data, error_message)
        # Valid input
        data[0][1] = number_of_decks
        self.__display_input_screen(title, data, active_question, None)
        return int(number_of_decks)

    def ask_number_of_players(self) -> int:
        data = [["Player quantity", "---"],]
        error_message = None
        return self.__ask_number_of_players(data, error_message)

    def __ask_number_of_players(self, data: list[list[str]], error_message: str) -> int:
        """
        The user is asked for the number of players, and this is validated.
        """
        # Variables
        title = "PLAYERS"
        active_question = "How many players are at this table?"
        # Print screen
        self.__display_input_screen(
            title, data, active_question, error_message)
        # Get user input
        number_of_players = input("    > ")
        # Check validity
        if number_of_players not in [str(n) for n in range(1, Settings.MAX_PLAYERS+1)]:
            error_message = "[bold red]Invalid number of players. Please try again.[/bold red]"
            return self.__ask_number_of_players(data, error_message)
        # Valid input
        data[0][1] = number_of_players
        self.__display_input_screen(title, data, active_question, None)
        return int(number_of_players)

    def ask_player_name_and_purse(self, index: int) -> tuple[str, int]:
        data = [["Name", "---"], ["Purse", "---"]]
        error_message = None
        name = self.__ask_player_name(data, error_message, index)
        error_message = None
        purse = self.__ask_player_purse(data, error_message, index)
        return name, purse

    def __ask_player_name(self, data: list[list[str]], error_message: str, index: int) -> str:
        """
        Ask the player for their name, ensuring it is not empty.
        """
        # Variables
        title = f"PLAYER {index}"
        active_question = "What is your name?"
        # Print screen
        self.__display_input_screen(
            title, data, active_question, error_message)
        # Get user input
        name = input("    > ")
        # Check validity
        if name == "":
            name = f"Player {index}"
        # Valid input
        data[0][1] = name
        self.__display_input_screen(title, data, active_question, None)
        return name

    def __ask_player_purse(self, data: list[list[str]], error_message: str, index: int) -> int:
        """
        Ask the player for how much they have in their purse, ensuring valid input.
        """
        # Variables
        title = f"PLAYER {index}"
        active_question = f"How much money is in your purse? (Minimum bet is £{
            self.pound(Settings.MINIMUM_BET)})"
        # Print screen
        self.__display_input_screen(
            title, data, active_question, error_message)
        # Get user input
        amount = input("    > ")
        # Check validity
        try:
            amount = int(amount)
            if amount < Settings.MINIMUM_BET:
                raise ValueError()
        except Exception:
            error_message = "[bold red]Invalid purse amount. Please try again.[/bold red]"
            return self.__ask_player_purse(data, error_message, index)
        else:
            # Valid input
            data[1][1] = amount
            self.__display_input_screen(title, data, active_question, None)
            return amount

    def ask_player_initial_bets(self, players: list[Player]) -> {str, int}:
        data = [[player.get_name(), "---"] for player in players]
        initial_bets = {player.get_name(): None for player in players}
        error_message = None
        for index, player in enumerate(players):
            initial_bet = self.__ask_player_initial_bet(
                data, error_message, player, index)
            initial_bets[player.get_name()] = initial_bet
        return initial_bets

    def __ask_player_initial_bet(self, data: list[list[str]], error_message: str, player: Player, index: int) -> int:
        """
        Ask the player how much they want to bet. Ensure the bet is less than purse amount, and there
        is sufficient funds in the purse for the minimum bet.
        """
        # Variables
        title = "INITIAL BETS"
        active_question = f"{player.get_name()}, how much would you like to bet? (Minimum bet is £{
            self.pound(Settings.MINIMUM_BET)})"
        # Print screen
        self.__display_input_screen(
            title, data, active_question, error_message)
        # Get user input
        bet = input("    > ")
        # Check validity
        try:
            bet = int(bet)
            if bet < Settings.MINIMUM_BET:
                raise ValueError()
        except Exception:
            error_message = "[bold red]Invalid bet amount. Please try again.[/bold red]"
            return self.__ask_player_initial_bet(data, error_message, player, index)
        else:
            # Valid input
            data[index][1] = bet
            self.__display_input_screen(title, data, active_question, None)
            return bet

    def __display_input_screen(self, title: str, data: list[list[str]], active_question: str, error_message: str):
        self.console.clear()
        data_formatted = "\n".join([f"{row[0]}: {row[1]}" for row in data])
        data_panel = Panel(data_formatted, expand=False)
        error_message = error_message if error_message is not None else " "
        content = Group(
            self.__suit_bar(),
            Align.center(title, vertical="middle", style="bold"),
            data_panel,
            active_question,
            error_message,
        )
        self.console.print(content)

    def display_table_hands(self, players: list[Player], dealer: Dealer, can_proceed: bool = False):
        self.console.clear()
        # First, make the dealer panel
        dealer_renderable = make_hand_graphic(dealer.get_next_hand())
        dealer_panel = Panel(
            renderable=Align.center(dealer_renderable, vertical="middle"),
            subtitle=f"score: {dealer.get_next_hand().get_score()}",
            title="[bold]Dealer[/bold]",
        )
        # Next, get all the player panels
        player_renderables = []
        for player in players:
            hand = player.get_next_hand()
            score = hand.get_score()
            bet = self.pound(hand.get_bet())
            renderable = make_hand_graphic(hand)
            player_renderables.append(Panel(
                renderable=Align.center(renderable, vertical="middle"),
                title=f"[bold]{player.get_name()}[/bold]",
                subtitle=f"score: {score}, bet: £{bet}",
                expand=True,
                width=self.division_width(len(players))
            ))
        # Make layout
        columns = Columns(
            player_renderables,
            expand=True,
            equal=True,
        )
        content_list = [
            self.__suit_bar(),
            dealer_panel,
            columns,
        ]
        if can_proceed:
            content_list.append(Padding("", (1, 0, 0, 0)))
            content_list.append(Align.left(
                "Once you are ready to proceed, please press [bold]ENTER[/bold]."))
        content = Group(*content_list)
        self.console.print(content)
        if not can_proceed:
            sleep(0)
        else:
            _ = input()

    def display_player_turn(self, player: Player, dealer: Dealer, action_list: list[str]) -> str:
        content_list = self.__content_player_hands(player, dealer)
        ask_list = self.__content_ask_action(action_list)
        content = Group(*content_list)
        self.console.print(content)

    def __content_player_hands(self, player: Player, dealer: Dealer):
        self.console.clear()
        # First, make the dealer panel
        dealer_renderable = make_hand_graphic(dealer.get_next_hand())
        dealer_panel = Panel(
            renderable=Align.center(dealer_renderable, vertical="middle"),
            subtitle=f"score: {dealer.get_next_hand().get_score()}",
            title="[bold]Dealer[/bold]",
        )
        # Next, get all the player panels
        player_renderables = []
        for hand in player.get_hands():
            score = hand.get_score()
            bet = self.pound(hand.get_bet())
            renderable = make_hand_graphic(hand)
            player_renderables.append(Panel(
                renderable=Align.center(renderable, vertical="middle"),
                title=f"[bold]{player.get_name()}[/bold]",
                subtitle=f"score: {score}, bet: £{bet}",
                expand=True,
                width=45,
                box=box.HEAVY
            ))
        # Make layout
        columns = Columns(
            player_renderables,
            expand=True,
            equal=True,
        )
        content_list = [
            self.__suit_bar(),
            dealer_panel,
            columns,
        ]
        return content_list

    def __content_ask_action(self, action_list):
        pass


def make_hand_graphic(hand: Hand) -> list[str]:
    """
    Produces a graphic for a hand.
    """
    number_of_cards = hand.number_of_cards()
    if number_of_cards == 0:
        return "\n".join([" "*21 for _ in range(10)])
    hand_graphic = HAND_GRAPHICS[number_of_cards-1].copy()
    # Replace the ranks and suits in the top-left corners
    for i, card in enumerate(hand.get_cards_copy()):
        # First, replace the rank
        rank_replacement = card.get_rank() + " " if card.get_rank() != "10" else "10"
        row_index, column_index = TOP_RANK_REPLACE[i]
        hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
            rank_replacement + hand_graphic[row_index][column_index+2:]
        # Next, replace the suit
        row_index, column_index = TOP_SUIT_REPLACE[i]
        hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
            card.get_suit() + hand_graphic[row_index][column_index+1:]
    # Replace the rank and suit on the bottom-right of the top card
    top_card = hand.get_card_by_index(-1)
    # Replace the rank
    rank_replacement = " " + top_card.get_rank() if top_card.get_rank() != "10" else "10"
    row_index, column_index = BOTTOM_RANK_REPLACE[number_of_cards-1]
    hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
        rank_replacement + hand_graphic[row_index][column_index+2:]
    # Replace the suit
    row_index, column_index = BOTTOM_SUIT_REPLACE[number_of_cards-1]
    hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
        top_card.get_suit() + hand_graphic[row_index][column_index+1:]

    return "\n".join(hand_graphic)


def make_all_hands_graphic(hands: list[Hand]) -> list[str]:
    """
    Concatenates all the individual hand graphics together.
    """
    all_hands_graphic = []
    for row_index in range(10):
        lines = []
        for hand in hands:
            hand_graphic = make_hand_graphic(hand)
            lines.append(hand_graphic[row_index])
        all_hands_graphic.append(HAND_GAP.join(lines))
    return all_hands_graphic


if __name__ == "__main__":
    interface = Interface()
    interface.display_title_screen()
    interface.display_deck_screen()
    interface.display_player_quantity_screen()


from cards import Hand, Card, Deck
from has_hands import Player, Dealer
from settings import Settings
from collections.abc import Callable

from rich import box
from rich.console import ConsoleRenderable
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
CONSOLE_WIDTH = 180
CONSOLE = Console(width=CONSOLE_WIDTH)


# ---------- VALIDATION FUNCTIONS ----------


def is_valid_enter(user_input: str) -> bool | None:
    return True, None


def is_valid_deck_quantity(user_input: str) -> bool | None:
    if user_input not in [str(n) for n in range(1, Settings.MAX_DECK_PACKS+1)]:
        return False, "[bold red]Invalid number of decks. Please try again.[/bold red]"
    return True, None


def is_valid_player_quantity(user_input: str) -> bool | None:
    if user_input not in [str(n) for n in range(1, Settings.MAX_PLAYERS+1)]:
        return False, "[bold red]Invalid number of players. Please try again.[/bold red]"
    return True, None


def is_valid_name(user_input: str) -> bool:
    if user_input is None:
        return False, "[bold red]Invalid name. Please try again.[/bold red]"
    return True, None


def is_valid_purse_amount(user_input: str) -> bool:
    if not user_input.isnumeric():
        return False, "[bold red]Invalid purse amount. Please try again.[/bold red]"
    amount = int(user_input)
    if amount < Settings.MINIMUM_BET/100:
        return False, "[bold red]Invalid purse amount. Please try again.[/bold red]"
    return True, None


def is_valid_bet(user_input: str) -> bool:
    if not user_input.isnumeric():
        return False, "[bold red]Invalid bet amount. Please try again.[/bold red]"
    amount = int(user_input)
    if amount < Settings.MINIMUM_BET/100:
        return False, "[bold red]Invalid bet amount. Please try again.[/bold red]"
    return True, None


def is_valid_action(user_input: str, action_choices: list[str]) -> bool:
    pass


# ---------- UTILITY & RENDERABLE FUNCTIONS ----------


def pound(pennies: int) -> str:
    return f"£{(pennies/100):.2f}"


def panel_width(n_in_row: int) -> int:
    widths = [180, 89, 59, 44, 35]
    return widths[n_in_row-1]


def make_title_renderable() -> ConsoleRenderable:
    return Align.center("\n".join(TITLE_GRAPHIC).replace(".", " "), vertical="middle")


def make_padding() -> ConsoleRenderable:
    return Padding("", (1, 0, 0, 0))


def row_replace(graphic: list[str], row_index: int, column_index: int, replace: str) -> str:
    graphic[row_index] = graphic[row_index][:column_index] + \
        replace + graphic[row_index][column_index+len(replace):]


def make_hand_graphic(hand: Hand, hide_hole: bool) -> str:
    """
    Produces a graphic for a hand.
    """
    number_of_cards = hand.number_of_cards()
    if number_of_cards == 0:
        return "\n".join([" "*21 for _ in range(10)])
    hand_graphic = HAND_GRAPHICS[number_of_cards-1].copy()
    # Replace the ranks and suits in the top-left corners
    for i, card in enumerate(hand.get_cards_copy()):
        if i == 0 and hide_hole:
            rank_replacement = "? "
            suit_replacement = "?"
        else:
            rank_replacement = card.get_rank() + " " if card.get_rank() != "10" else "10"
            suit_replacement = card.get_suit()
        # First, replace the rank
        row_index, column_index = TOP_RANK_REPLACE[i]
        row_replace(hand_graphic, row_index, column_index, rank_replacement)
        # Next, replace the suit
        row_index, column_index = TOP_SUIT_REPLACE[i]
        row_replace(hand_graphic, row_index, column_index, suit_replacement)
    # Replace the rank and suit on the bottom-right of the top card
    top_card = hand.get_card_by_index(-1)
    if hand.number_of_cards() == 1 and hide_hole:
        rank_replacement = " ?"
        suit_replacement = "?"
    else:
        rank_replacement = " " + top_card.get_rank() if top_card.get_rank() != "10" else "10"
        suit_replacement = top_card.get_suit()
    # Replace the rank
    row_index, column_index = BOTTOM_RANK_REPLACE[number_of_cards-1]
    row_replace(hand_graphic, row_index, column_index, rank_replacement)
    # Replace the suit
    row_index, column_index = BOTTOM_SUIT_REPLACE[number_of_cards-1]
    row_replace(hand_graphic, row_index, column_index, suit_replacement)
    return "\n".join(hand_graphic)


def make_data_panel(data: list[list[str]]) -> Panel:
    data_formatted = "\n".join(
        [f"{item[0]}: {item[1]}" for item in data])
    data_panel = Panel(data_formatted, expand=False)
    return data_panel


def make_dealer_panel(hand: Hand, hide_hole: bool) -> Panel:
    hand_graphic = make_hand_graphic(hand, hide_hole)
    score = hand.get_score() if hand.get_score() != 0 else "---"
    return Panel(
        renderable=Align.center(hand_graphic, vertical="middle"),
        title="[bold]Dealer[/bold]",
        subtitle=f"score: {score}",
    )


def make_player_hand_panel(hand: Hand, player: Player, hand_type: str, n_in_row: int) -> Panel:
    hand_graphic = make_hand_graphic(hand, False)
    score = hand.get_score() if hand.get_score() != 0 else "---"
    if hand_type == "initial-bets":
        bet = pound(hand.get_bet()) if hand.get_bet() is not None else "£---"
        return Panel(
            renderable=Align.center(hand_graphic, vertical="middle"),
            title=f"[bold]{player.get_name()}[/bold]",
            subtitle=f"score: {score}, bet: {bet}",
            expand=True,
            width=panel_width(n_in_row)
        )
    elif hand_type == "dealing":
        return Panel(
            renderable=Align.center(hand_graphic, vertical="middle"),
            title=f"[bold]{player.get_name()}[/bold]",
            subtitle=f"score: {score}, bet: {pound(hand.get_bet())}",
            expand=True,
            width=panel_width(n_in_row)
        )
    elif hand_type == "player-turn":
        hand_status = hand.get_status()
        if not (hand_status == "Active" and hand == player.get_next_hand()):
            hand_status = None
        box_type = box.HEAVY_EDGE if hand_status == "Active" else box.ROUNDED
        return Panel(
            renderable=Align.center(hand_graphic, vertical="middle"),
            title=f"[bold]{hand_status}[/bold]",
            subtitle=f"score: {score}, bet: {pound(hand.get_bet())}",
            expand=True,
            width=panel_width(n_in_row),
            box=box_type,
        )


def make_table_all(players: list[Player], dealer: Dealer, hand_type: str):
    # Make dealer panel
    dealer_panel = make_dealer_panel(dealer.get_next_hand(), True)
    # Make player panels
    player_hand_panels = []
    for player in players:
        hand = player.get_next_hand()
        player_hand_panels.append(
            make_player_hand_panel(hand, player, hand_type, len(players)))
    # Make player columns
    player_hand_columns = Columns(
        player_hand_panels,
        expand=True,
        equal=True,
    )
    # Make contents list
    content = [
        dealer_panel,
        player_hand_columns,
    ]
    return content


def make_table_player(player: Player, dealer: Dealer):
    # Make dealer panel
    dealer_panel = make_dealer_panel(dealer.get_next_hand(), True)
    # Make panels for each of player's hands
    player_hand_panels = []
    for hand in player.get_hands():
        player_hand_panels.append(
            make_player_hand_panel(hand, player, "player-turn", 4))
    # Make player columns
    player_hand_columns = Columns(
        player_hand_panels,
        expand=True,
        equal=True,
    )
    # Make contents list
    content = [
        dealer_panel,
        player_hand_columns,
    ]
    return content


# ---------- DISPLAY FUNCTIONS ----------


def _display_ask(content: list[ConsoleRenderable], invalid_message: str, validity_checker: Callable, is_valid: bool) -> str:
    # Clear the screen
    CONSOLE.clear()
    # Check whether error message should be added at end of content, and it isn't already there.
    if not is_valid:
        if content[-1] != invalid_message:
            content.append(invalid_message)
    # Group content and display
    grouped_content = Group(*content)
    CONSOLE.print(grouped_content)
    # Take user input
    user_input = input("> ")
    # Validate user input using validation function
    is_valid, invalid_message = validity_checker(user_input)
    if not is_valid:
        return _display_ask(content, invalid_message, validity_checker, is_valid=False)
    else:
        return user_input


def _display_timed(content: list[ConsoleRenderable], delay: int) -> None:
    # Clear the screen
    CONSOLE.clear()
    # Group content and display
    grouped_content = Group(*content)
    CONSOLE.print(grouped_content)
    # Wait
    sleep(delay)
    return None


# ---------- BRIDGES ----------


def display_title() -> str:
    title_content = [
        make_title_renderable(),
        Align.center("Welcome!", vertical="middle", style="bold"),
        make_padding(),
        "Please ensure your console window is large enough to fit the content.",
        make_padding(),
        "Once you are ready to proceed, please press [bold]ENTER[/bold].",
    ]
    _ = _display_ask(title_content, None, is_valid_enter, True)
    return None


def display_settings() -> str:
    # First, define the data which will be updated throughout
    data = [
        ["Number of decks", "---"],
        ["Number of players", "---"],
    ]
    # Complete the deck quantity display
    deck_quantity_content = [
        make_title_renderable(),
        make_padding(),
        make_data_panel(data),
        make_padding(),
        f"How many decks will you play with? (1 to {Settings.MAX_DECK_PACKS})",
    ]
    deck_quantity = _display_ask(deck_quantity_content,
                                 None, is_valid_deck_quantity, True)
    # Update the data to include the number of decks
    data[0][1] = deck_quantity
    # Complete the player quantity display
    player_quantity_content = [
        make_title_renderable(),
        make_padding(),
        make_data_panel(data),
        make_padding(),
        f"How many players are at the table? (1 to {Settings.MAX_PLAYERS})",
    ]
    player_quantity = _display_ask(player_quantity_content,
                                   None, is_valid_player_quantity, True)
    # Update the data to include the number of players
    data[1][1] = player_quantity
    # Finally, display inputs and await user input
    final_content = [
        make_title_renderable(),
        make_padding(),
        make_data_panel(data),
        make_padding(),
        f"Once you are ready to proceed, please press [bold]ENTER[/bold].",
    ]
    _ = _display_ask(final_content,
                     None, is_valid_enter, True)
    return int(deck_quantity), int(player_quantity)


def display_player_information(player_quantity: int) -> list[(str, int)]:
    # Define the list in which all the player information will be stored.
    display_data = []
    return_data = []
    for i in range(1, player_quantity + 1):
        # First, get the player name
        player_name_content = [
            make_title_renderable(),
            make_padding(),
            make_data_panel(display_data),
            make_padding(),
            f"What is the name of Player {i}?",
        ]
        player_name = _display_ask(player_name_content,
                                   None, is_valid_name, True)
        # Update the data lists
        display_data.append([player_name, "£---"])
        return_data.append([player_name, None])
        # Next, get the purse amount
        player_purse_content = [
            make_title_renderable(),
            make_padding(),
            make_data_panel(display_data),
            make_padding(),
            f"{player_name}, how much is in your purse? (Minimum bet is {
                pound(Settings.MINIMUM_BET)})",
        ]
        player_purse = _display_ask(player_purse_content,
                                    None, is_valid_purse_amount, True)
        # Update the data list
        player_purse = int(player_purse)*100
        display_data[-1][1] = pound(player_purse)
        return_data[-1][1] = player_purse

    # Finally, display inputs and await user input
    final_content = [
        make_title_renderable(),
        make_padding(),
        make_data_panel(display_data),
        make_padding(),
        f"Once you are ready to proceed, please press [bold]ENTER[/bold].",
    ]
    _ = _display_ask(final_content,
                     None, is_valid_enter, True)
    return return_data


def display_initial_bets(players: list[Player], dealer: Dealer):

    for player in players:
        # Get the initial bet
        initial_bet_content = make_table_all(
            players, dealer, "initial-bets")
        initial_bet_content.append(make_padding())
        initial_bet_content.append(f"{player.get_name(
        )}, how much is your initial bet? (Minimum bet is {pound(Settings.MINIMUM_BET)}")
        initial_bet = _display_ask(initial_bet_content,
                                   None, is_valid_bet, True)
        # Update the bet
        hand = player.get_next_hand()
        initial_bet = int(initial_bet)*100
        hand.set_bet(initial_bet)

    # Await enter press
    initial_bet_content = make_table_all(
        players, dealer, "initial-bets")
    initial_bet_content.append(make_padding())
    initial_bet_content.append(
        "Once you are ready to proceed, please press [bold]ENTER[/bold].")
    _ = _display_ask(initial_bet_content, None, is_valid_enter, True)
    return None


def display_card_dealing(players: list[Player], dealer: Dealer, can_proceed: bool = False) -> None:
    # Make contents list
    content = make_table_all(players, dealer, "dealing")
    # Display
    if not can_proceed:
        _display_timed(content, 0)
    else:
        content.append(make_padding())
        content.append(
            "Once you are ready to proceed, please press [bold]ENTER[/bold].")
        _display_ask(content, None, is_valid_enter, True)
    return None


def display_player_turn(player: Player, deck: Deck, players: list[Player], dealer: Dealer):
    # Make contents list
    content = make_table_player(player, dealer)
    content.append(make_padding())
    content.append(
        "Once you are ready to proceed, please press [bold]ENTER[/bold].")
    _display_ask(content, None, is_valid_enter, True)

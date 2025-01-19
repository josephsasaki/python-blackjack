
from cards import Hand, Card, Deck
from has_hands import Player, Dealer
from settings import Settings
from collections.abc import Callable

from rich import box
from rich.table import Table
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


def is_valid_enter(user_input: str, player: Player) -> bool | None:
    """
    Validation function which always returns true. Is used if the display requires
    the user to press enter to continue, in which case the input does not matter.
    """
    return True, None


def is_valid_deck_quantity(user_input: str, player: Player) -> bool | None:
    """
    Validation function for the number of decks. The number of decks must be
    between 1 and the maximum number of allowed decks.
    """
    if user_input not in [str(n) for n in range(1, Settings.MAX_DECK_PACKS+1)]:
        return False, "[bold red]Invalid number of decks. Please try again.[/bold red]"
    return True, None


def is_valid_player_quantity(user_input: str, player: Player) -> bool | None:
    """
    Validation function for the number of players. The number of players must be
    between 1 and the maximum number of allowed players.
    """
    if user_input not in [str(n) for n in range(1, Settings.MAX_PLAYERS+1)]:
        return False, "[bold red]Invalid number of players. Please try again.[/bold red]"
    return True, None


def is_valid_name(user_input: str, player: Player) -> bool:
    """
    Validation function for a player name. Must not be an empty string.
    """
    if user_input == "":
        return False, "[bold red]Invalid name. Please try again.[/bold red]"
    return True, None


def is_valid_purse_amount(user_input: str, player: Player) -> bool:
    """
    Validation function for a player's purse amount. This must be numeric, and greater
    than or equal to the minimum bet, to ensure the player can play at least one round.
    """
    if not user_input.isnumeric():
        return False, "[bold red]Invalid purse amount. Please try again.[/bold red]"
    amount = int(user_input)
    if amount < Settings.MINIMUM_BET/100:
        return False, "[bold red]Invalid purse amount. Please try again.[/bold red]"
    return True, None


def is_valid_bet(user_input: str, player: Player) -> bool:
    """
    Validation function for a hand bet. This must be greater than the minimum bet, but less
    than the player's purse.
    """
    if not user_input.isnumeric():
        return False, "[bold red]Invalid bet amount. Please try again.[/bold red]"
    amount = int(user_input)
    if amount < Settings.MINIMUM_BET/100:
        return False, "[bold red]Invalid bet amount. Please try again.[/bold red]"
    if amount > player.get_purse():
        return False, "[bold red]Invalid bet amount. Please try again.[/bold red]"
    return True, None


def is_valid_action(user_input: str, player: Player) -> bool:
    """
    Validation function for a player's action choice. The player must have chosen a 
    valid action given the hand.
    """
    action_choices = player.get_action_choices()
    if user_input not in action_choices:
        return False, "[bold red]Invalid action. Please try again.[/bold red]"
    return True, None


# ---------- UTILITY & RENDERABLE FUNCTIONS ----------


def pound(pennies: int) -> str:
    """
    Converts number of pennies into a formatted string of pounds and pennies.
    """
    return f"£{(pennies/100):.2f}"


def panel_width(n_in_row: int) -> int:
    """
    Returns a panel width to ensure all n_in_rows panel fit across screen.
    """
    if n_in_row not in {1, 2, 3, 4, 5}:
        raise ValueError("Invalid number of panels across screen.")
    widths = [180, 89, 59, 44, 35]
    return widths[n_in_row-1]


def make_title_renderable() -> ConsoleRenderable:
    """
    Takes the title graphic and converts to a formatted string.
    """
    return Align.center("\n".join(TITLE_GRAPHIC).replace(".", " "), vertical="middle")


def make_padding() -> ConsoleRenderable:
    """
    Returns a 1 line padding object to place between renderables.
    """
    return Padding("", (1, 0, 0, 0))


def make_data_panel(data: list[list[str]]) -> Panel:
    """
    Given a list of lists, each of length 2, produces a panel containing the
    data neatly formatted.
    """
    data_formatted = "\n".join(
        [f"{item[0]}: {item[1]}" for item in data])
    data_panel = Panel(data_formatted, expand=False)
    return data_panel


def make_dealer_panel(hand: Hand, hide_hole: bool) -> Panel:
    """
    Makes the dealer panel, and considers whether the hole card should be hidden
    or not.
    """
    hand_graphic = make_hand_graphic(hand, hide_hole)
    # Get the score (which should be hidden if the hole is hidden)
    if hand.get_score() == 0 or hide_hole:
        score = "---"
    else:
        score = hand.get_score()
    # Return the final panel.
    return Panel(
        renderable=Align.center(hand_graphic, vertical="middle"),
        title="[bold]Dealer[/bold]",
        subtitle=f"score: {score}",
    )


def row_replace(graphic: list[str], row_index: int, column_index: int, replace: str) -> None:
    """
    Takes a card graphic and replaces a rank or suit in a particular position. Function
    works in place, so does not return anything.
    """
    graphic[row_index] = graphic[row_index][:column_index] + \
        replace + graphic[row_index][column_index+len(replace):]


def make_hand_graphic(hand: Hand, hide_hole: bool) -> str:
    """
    Produces a graphic for a hand. Takes a global graphic object and places the correct
    card symbols to produce the graphic.
    """
    number_of_cards = hand.number_of_cards()
    # First, check whether the hand is empty
    if number_of_cards == 0:
        return "\n".join([" "*21 for _ in range(10)])
    # Get the relevant blank hand graphic
    hand_graphic = HAND_GRAPHICS[number_of_cards-1].copy()
    # Replace the ranks and suits in the top-left corners
    for i, card in enumerate(hand.get_cards()):
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


def make_hand_list(player: Player) -> str:
    """
    If a player has multiple hands, a list of hands and bets are used instead. Note,
    the hide_hole parameter is not needed since the dealer will never have more than one
    hand.
    """
    table = Table(box=None, show_header=False)
    table.add_column("Hand", justify="left", no_wrap=True)
    table.add_column("Bet", justify="right", no_wrap=True)
    for hand in player.get_hands():
        table.add_row(hand.get_string(), pound(hand.get_bet()))
    return table


def make_player_table_panel(player: Player, n_in_row: int) -> Panel:
    """
    Makes a hand panel for a player which contains all their hands. This panel
    is used for when initial bets are being taken, cards are being dealt, the dealer's
    turn. If the player only has one hand, the card graphic can be used. If the player
    has multiple hands, they are listed in string form.
    """
    if len(player.get_hands()) == 1:
        hand = player.get_hands()[0]
        score = hand.get_score() if hand.get_score() != 0 else "---"
        bet = pound(hand.get_bet()) if hand.get_bet() is not None else "£---"
        # Get the hand graphic
        hand_renderable = make_hand_graphic(hand=hand, hide_hole=False)
        return Panel(
            renderable=Align.center(hand_renderable, vertical="middle"),
            title=f"[bold]{player.get_name()}[/bold]",
            subtitle=f"score: {score}, bet: {bet}",
            expand=True,
            width=panel_width(n_in_row)
        )
    else:
        hand_renderable = make_hand_list(player=player)
        return Panel(
            renderable=Align.center(hand_renderable, vertical="middle"),
            title=f"[bold]{player.get_name()}[/bold]",
            expand=True,
            width=panel_width(n_in_row),
            height=12,
        )


def make_player_turn_panel(hand: Hand, player: Player) -> Panel:
    """
    Makes a hand panel for a player while it is their turn. A player can have multiple
    hand panels for each hand.
    """
    hand_graphic = make_hand_graphic(hand=hand, hide_hole=False)
    score = hand.get_score()
    # Get hand status and format to be bold
    hand_status = player.get_hand_status(hand)
    if hand_status is not None:
        hand_status = f"[bold]{hand_status}[/bold]"
    # Determine the panel border weight based on whether hand is active
    box_type = box.HEAVY_EDGE if hand_status == "Active" else box.ROUNDED
    # Return final hand
    return Panel(
        renderable=Align.center(hand_graphic, vertical="middle"),
        title=hand_status,
        subtitle=f"score: {score}, bet: {pound(hand.get_bet())}",
        width=panel_width(4),
        box=box_type,
    )


def make_all_players_table_content(players: list[Player], dealer: Dealer, game_stage: str, hide_hole: bool):
    """
    The following function produces all the content seen during a round. This will
    change depending on what stage of the game we are at.
    """
    # First, handle the dealer panel.
    dealer_panel = make_dealer_panel(
        dealer.get_hands()[0], hide_hole=hide_hole)
    # Next, handle the player's hands panel
    player_hand_panels = []
    for player in players:
        player_hand_panels.append(
            make_player_table_panel(player, len(players)))
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


def make_single_players_table_content(player: Player, dealer: Dealer, game_stage: str, hide_hole: bool):
    """
    The following function produces all the content seen during a round. This will
    change depending on what stage of the game we are at.
    """
    # First, handle the dealer panel.
    dealer_panel = make_dealer_panel(
        dealer.get_hands()[0], hide_hole=hide_hole)
    # Next, handle the player's hands panel
    player_hand_panels = []
    for hand in player.get_hands():
        player_hand_panels.append(
            make_player_turn_panel(hand, player))
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


def _display_ask(content: list[ConsoleRenderable], invalid_message: str, validity_checker: Callable, is_valid: bool, player: Player) -> str:
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
    is_valid, invalid_message = validity_checker(user_input, player=player)
    if not is_valid:
        return _display_ask(content, invalid_message, validity_checker, is_valid=False, player=player)
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
    _ = _display_ask(title_content, None, is_valid_enter, True, player=None)
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
                                 None, is_valid_deck_quantity, True, player=None)
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
                                   None, is_valid_player_quantity, True, player=None)
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
                     None, is_valid_enter, True, player=None)
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
                                   None, is_valid_name, True, player=None)
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
                                    None, is_valid_purse_amount, True, player=None)
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
                     None, is_valid_enter, True, player=None)
    return return_data


def display_initial_bets(players: list[Player], dealer: Dealer):
    for player in players:
        # Get the initial bet
        initial_bet_content = make_all_players_table_content(
            players, dealer, "pre-turn", hide_hole=True)
        initial_bet_content.append(make_padding())
        initial_bet_content.append(f"{player.get_name(
        )}, how much is your initial bet? (Minimum bet is {pound(Settings.MINIMUM_BET)})")
        initial_bet = _display_ask(initial_bet_content,
                                   None, is_valid_bet, True, player=player)
        # Update the bet
        hand = player.get_next_hand()
        initial_bet = int(initial_bet)*100
        hand.set_bet(initial_bet)

    # Await enter press
    initial_bet_content = make_all_players_table_content(
        players, dealer, "pre-turn", hide_hole=True)
    initial_bet_content.append(make_padding())
    initial_bet_content.append(
        "Once you are ready to proceed, please press [bold]ENTER[/bold].")
    _ = _display_ask(initial_bet_content, None,
                     is_valid_enter, True, player=None)
    return None


def display_card_dealing(players: list[Player], dealer: Dealer, can_proceed: bool = False) -> None:
    # Make contents list
    content = make_all_players_table_content(
        players, dealer, "pre-turn", hide_hole=True)
    # Display
    if not can_proceed:
        _display_timed(content, 0)
    else:
        content.append(make_padding())
        content.append(
            "Once you are ready to proceed, please press [bold]ENTER[/bold].")
        _display_ask(content, None, is_valid_enter, True, player=None)
    return None


def display_player_turn(player: Player, deck: Deck, dealer: Dealer, await_enter: bool):
    # Make contents list
    content = make_single_players_table_content(
        player, dealer, "player-turn", hide_hole=True)
    if not await_enter:
        content.append(make_padding())
        content.append("Choose an action: " +
                       ", ".join(player.get_action_choices()))
        action = _display_ask(
            content, None, is_valid_action, True, player=player)
        return action
    else:
        content.append(make_padding())
        content.append(
            "Once you are ready to proceed, please press [bold]ENTER[/bold].")
        _display_ask(content, None, is_valid_enter, True, player=None)
        return None


def display_dealer_turn(players: list[Player], dealer: Dealer, can_proceed: bool = False) -> None:
    # Make contents list
    content = make_all_players_table_content(
        players, dealer, "dealer-turn", hide_hole=False)
    # Display
    if not can_proceed:
        _display_timed(content, 1)
    else:
        content.append(make_padding())
        content.append(
            "Once you are ready to proceed, please press [bold]ENTER[/bold].")
        _display_ask(content, None, is_valid_enter, True, player=None)
    return None

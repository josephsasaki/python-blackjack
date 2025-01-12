from time import time
from random import Random
import argparse
from models import Hand, Player, Dealer


# GLOBAL VARIABLES

SUITS = ["S", "D", "H", "C"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
MAX_DECK_PACKS = 5
MAX_PLAYERS = 5
MINIMUM_BET = 5.0
INVALID_RESPONSE = "Invalid response. Please try again."


# PRINT FUNCTIONS


def print_game_intro() -> None:
    """
    Print the initial game introduction, which includes a title and instructions.
    """
    print("\n#################### BLACKJACK ####################")
    print("Instructions...")


def print_get_players_title() -> None:
    """
    Print the title and information about collecting player information.
    """
    print("\n---------- PLAYER INFORMATION ----------")


def print_round_title(index: int) -> None:
    """
    Print a title which announces a round has started.
    """
    print(f"\n########## ROUND {index} ##########")


def print_dealt_cards(players: list[Player], dealer: Dealer) -> None:
    """
    Print what cards have been dealt to all the players.
    """
    print("\n---------- DEALT HANDS ----------")
    # Players' hands
    print("Players have been dealt the following cards...")
    for player in players:
        message = f"{player.name} : {
            hand_to_string(player.hands[0])}"
        print(message)
    # Dealer's hand
    message = f"The dealer has been dealt {
        hand_to_string(dealer.hands[0])}"
    print(message)


def print_player_turn_title(player: Player) -> None:
    """
    Print a title for when its a particular player's turn.
    """
    print(f"\n---------- {player.name} ----------")


def print_player_hand(hand: Hand) -> None:
    """
    Print the players hand and the amount they have bet on that hand.
    """
    print(f"(£{hand.bet:.2f}) : {hand_to_string(hand)}")


def print_blackjack_message() -> None:
    """
    Print that the player has gotten a blackjack!
    """
    print("Blackjack!")


def print_21_message() -> None:
    """
    """
    print("You hit 21!")


def print_bust_message() -> None:
    """
    Print that the player has gone bust.
    """
    print("Bust!")


def print_dealer_turn_title() -> None:
    """
    Print that it is the dealer's turn
    """
    print(f"\n---------- Dealer ----------")


def print_dealer_hand(hand: Hand) -> None:
    """
    Print the dealers hand, notably without a bet amount.
    """
    print(f"(£--) : {hand_to_string(hand)}")


def print_hand_outcome(hand: Hand, amount_change: str) -> None:
    """
    Print the outcome of a hand.
    """
    print(f"({amount_change}) : {hand_to_string(hand)}")


def print_make_payments_title() -> None:
    """
    Print title showing the payments are being made.
    """
    print(f"\n---------- ROUND RESULTS ----------")


def print_player_purse(player: Player) -> None:
    """
    Print the remaining money in the player's purse.
    """
    print(f"You have £{player.purse:.2f} remaining.")


# ASK USER INPUT FUNCTIONS


def ask_number_of_decks() -> int:
    """
    Get the number of decks that game will be played with from the user.
    """
    number_of_decks = input("How many decks do you want to play with? : ")
    try:
        number_of_decks = int(number_of_decks)
        if number_of_decks not in range(1, MAX_DECK_PACKS+1):
            raise ValueError("Invalid number of decks.")
        else:
            return number_of_decks
    except ValueError:
        print(INVALID_RESPONSE)
        return ask_number_of_decks()


def ask_number_of_players() -> int:
    """
    The user is asked for the number of players, and this is validated.
    """
    number_of_players = input("How many players are there? : ")
    try:
        number_of_players = int(number_of_players)
        if number_of_players not in range(1, MAX_PLAYERS+1):
            raise ValueError("Number of players not in valid range.")
        else:
            return number_of_players
    except ValueError:
        print(INVALID_RESPONSE)
        return ask_number_of_players()


def ask_player_name(index: int) -> str:
    """
    Ask the player for their name, ensuring it is not empty.
    """
    name = input(f"What is the name of Player {index + 1}? : ")
    if name == "":
        return f"Player {index + 1}"
    else:
        return name


def ask_player_purse() -> float:
    """
    Ask the player for how much they have in their purse, ensuring valid input.
    """
    amount = input("How much money is in your purse? : ")
    try:
        amount = float(amount)
        if amount < MINIMUM_BET:
            raise ValueError("Purse amount must be greater than minimum bet.")
        return amount
    except ValueError:
        print(INVALID_RESPONSE)
        return ask_player_purse()


def ask_player_bet(player: Player) -> float:
    """
    Ask the player how much they want to bet. Ensure the bet is less than purse amount, and there
    is sufficient funds in the purse for the minimum bet.
    """
    # First, check for sufficient funds
    if player.purse < MINIMUM_BET:
        raise ValueError(
            "Player should have been removed if insufficient funds for minimum bet.")
    # Ask for player bet amount
    bet = input(f"{player.name} : ")
    try:
        bet = float(bet)
        if bet < MINIMUM_BET or bet > player.purse:
            raise ValueError
        return bet
    except ValueError:
        print(INVALID_RESPONSE)
        return ask_player_bet(player)


def ask_player_action(choices: list[str]) -> str:
    """
    Ask the player for whether they wish to hit, stick, split or double-down.
    """
    # Get player action
    action = input("Action : ")
    # Check the action is in the choices
    if action not in choices:
        print(INVALID_RESPONSE)
        return ask_player_action(choices)
    return action


# DECK AND CARDS FUNCTIONS


def generate_deck(number: int = 1) -> list[(str)]:
    """
    The decks of cards are generated and returned. Cards are tuples, where the 
    first element is the rank and the second elements is the suit.
    """
    # Generate a single deck
    single_deck = []
    for suit in SUITS:
        for rank in RANKS:
            single_deck.append((rank, suit))
    # Generate the combines deck based on the number of decks specified.
    total_deck = []
    for _ in range(number):
        total_deck += single_deck

    return total_deck


def shuffle(deck: list[(str)], seed: int) -> list[(str)]:
    """Randomises a deck of cards"""
    copy_of_deck = deck.copy()
    Random(seed).shuffle(copy_of_deck)
    return copy_of_deck


def take_card_from_deck(deck: list[(str)]) -> (str):
    """
    Removes a card from the deck and returns it.
    """
    return deck.pop()


def hand_to_string(hand: Hand) -> str:
    """
    Takes a list of cards and returns a neat list as a string.
    """
    # check hand is not empty
    if hand.cards == []:
        raise ValueError("Empty hand is invalid.")
    str_cards = [rank+suit for (rank, suit) in hand.cards]
    return ", ".join(str_cards)


# PLAYER AND DEALER INFORMATION FUNCTIONS


def define_players(player_quantity: int) -> list[Player]:
    """
    The players are instantiated based off of user inputs.
    """
    players = []
    for i in range(player_quantity):
        name = ask_player_name(i)
        purse = ask_player_purse()
        player = Player(name, purse)
        players.append(player)
    return players


def define_dealer() -> Dealer:
    """
    The dealer is instantiated.
    """
    return Dealer()


# ROUND SETUP FUNCTIONS (BETS AND DEALING)


def take_bets(players: list[Player]) -> dict[str, float]:
    """
    Go through the players and ask them how much they wish to bet for the round.
    Bets must be above a certain minimum and less than the amount the player has.
    """
    print(
        f"How much does each player want to bet this round? The minimum bet amount is £{MINIMUM_BET:.2f}.")
    bets = {}
    for player in players:
        bet = ask_player_bet(player)
        bets[player.name] = bet
        player.purse -= bet
    return bets


def deal_initial_hands(deck: list[(str)], players: list[Player], dealer: Dealer, bets: dict[str, float]) -> None:
    """
    Simulates dealing cards to each player and the dealer.
    """
    # First, give each player and dealer an empty hand with bet
    for person in players:
        person.give_hand(Hand(bet=bets[person.name]))
    dealer.give_hand(Hand())
    # Next, go through each player and give cards to hand
    for _ in range(2):
        for person in players + [dealer]:
            drawn_card = take_card_from_deck(deck)
            person.hands[0].add_card(drawn_card)


# INSURANCE FUNCTIONS


def insurance():
    pass


# ROUND PAYMENTS AND HAND OUTCOME FUNCTIONS


def push(player: Player, hand: Hand):
    """
    The dealer and player draw.
    """
    player.purse += hand.bet
    print_hand_outcome(hand, "+£0.00")


def lost(player: Player, hand: Hand):
    """
    The player lost, so no money gained
    """
    print_hand_outcome(hand, f"-£{hand.bet:.2f}")


def one_to_one(player: Player, hand: Hand):
    """
    The player has won (but not blackjack)
    """
    player.purse += hand.bet*2
    print_hand_outcome(hand, f"+£{hand.bet:.2f}")


def three_to_two(player: Player, hand: Hand):
    """
    The player had a blackjack and beat the dealer
    """
    player.purse += hand.bet + (hand.bet/2.)*3.
    print_hand_outcome(hand, f"+£{((hand.bet/2)*3.):.2f}")


def make_hand_payment(player: Player, player_hand: Hand, dealer_hand: Hand):
    """
    Make individual payment for one hand.
    """
    # Outcomes (index 0=bust, 1=by-score, 2=blackjack)
    outcomes = [
        [lost, lost, lost],
        [one_to_one, None, lost],
        [three_to_two, three_to_two, push],
    ]
    player_outcome = None
    dealer_outcome = None

    # Dealer outcome
    if dealer_hand.is_bust():
        dealer_outcome = 0
    elif dealer_hand.is_blackjack():
        dealer_outcome = 2
    else:
        dealer_outcome = 1

    # Player outcome
    if player_hand.is_bust():
        player_outcome = 0
    elif player_hand.is_blackjack():
        player_outcome = 2
    else:
        player_outcome = 1

    # Check if scores need to be compared
    if dealer_outcome == 1 and player_outcome == 1:
        if player_hand.get_score() > dealer_hand.get_score():
            one_to_one(player, player_hand)
        elif player_hand.get_score() < dealer_hand.get_score():
            lost(player, player_hand)
        else:
            push(player, player_hand)
    else:
        outcomes[player_outcome][dealer_outcome](player, player_hand)


def make_payments(players: list[Player], dealer: Dealer):
    """
    Go through a players hand and compare to dealer to determine payments
    """
    dealer_hand = dealer.hands[0]
    for player in players:
        print_player_turn_title(player)
        for hand in player.hands:
            make_hand_payment(player, hand, dealer_hand)
        print_player_purse(player)


# PLAYER AND DEALER TURN FUNCTIONS


def player_turn(player: Player, deck: list[(str)]):
    """
    Complete a round for a player, where they can make decisions about what to do.
    """
    while player.get_next_hand() is not None:
        double_downed = False
        hand = player.get_next_hand()
        print_player_hand(hand)
        # Check the hand is not a blackjack from draw
        if hand.get_score() == 21:
            hand.is_active = False
            print_blackjack_message()
            continue
        # Get the action choices
        action_choices = ["hit", "stick"]
        if hand.can_split(player):
            action_choices.append("split")
        if hand.can_double_down(player):
            action_choices.append("double-down")
        # Get player action
        action = ask_player_action(action_choices)
        if action == "hit":
            hand.hit(deck)
        elif action == "stick":
            hand.stick()
        elif action == "split":
            hand.split(deck, player)
        elif action == "double-down":
            hand.double_down(deck, player)
            double_downed = True
        # Check whether they've gone bust to print a message
        # This is relevant for if they hit, stick or double-down
        if hand.get_score() > 21:
            print_player_hand(hand)
            print_bust_message()
        elif hand.get_score() == 21:
            print_player_hand(hand)
            print_21_message()
        elif double_downed:
            print_player_hand(hand)


def complete_dealer_turn(players: list[Player], dealer) -> bool:
    """
    Check whether the dealer's turn should be completed. Dealer's turn not completed if:
    1) All hands are bust
    2) All hands are blackjacks and 
    """


def dealer_turn(dealer: Dealer, deck: list[(str)]):
    """
    Complete a round for the dealer.
    """
    print_dealer_turn_title()
    dealer_hand = dealer.get_next_hand()
    print_dealer_hand(dealer_hand)
    # Check for blackjack
    if dealer_hand.get_score() == 21:
        print_blackjack_message()
    while dealer_hand.get_score() < 17:
        dealer_hand.hit(deck)
        print_dealer_hand(dealer_hand)
        if dealer_hand.get_score() > 21:
            print_dealer_hand(dealer_hand)
            print_bust_message()
    dealer_hand.is_active = False


# MAIN GAME LOOP AND ROUND FUNCTIONS


def round(number_of_decks: int, players: list[Player], dealer: Dealer, seed: int):
    """
    A single round of blackjack.
    """
    # Generate deck
    deck = generate_deck(number_of_decks)
    # Shuffle the deck
    shuffled_deck = shuffle(deck, seed)

    # Get the players initial bets
    initial_bets = take_bets(players)

    # Deal cards
    deal_initial_hands(shuffled_deck, players, dealer, initial_bets)
    print_dealt_cards(players, dealer)

    # Check for insurance
    pass

    # Iterate through players and complete a turns
    for player in players:
        print_player_turn_title(player)
        player_turn(player, shuffled_deck)

    # Complete the dealer turn, only is allowed
    complete_dealer_turn = True
    # Dealer doesn't have their turn if all players are bust
    busts = []
    for player in players:
        pass
        # or if all players have blackjack and dealer definitely doesn't.

    dealer_turn(dealer, shuffled_deck)

    # Make payments
    print_make_payments_title()
    make_payments(players, dealer)

    # Reset the players hands
    for player in players + [dealer]:
        player.reset_hand()


def play(seed):
    """
    The main game loop, which consists of playing rounds with the same players.
    """
    print_game_intro()

    # Get the number of decks
    number_of_decks = ask_number_of_decks()

    # Get players and dealer
    number_of_players = ask_number_of_players()
    print_get_players_title()
    players = define_players(number_of_players)
    dealer = define_dealer()

    # Play rounds
    round_number = 1
    while True:
        print_round_title(round_number)
        round(number_of_decks, players, dealer, seed+round_number)
        round_number += 1


# RANDOM SEED GENERATOR


def get_seed() -> int:
    """
    You can safely ignore this function. It is used to accept a seed from the command line.
    For example

    python3 blackjack.py --seed 313131

    Would play the game with defined seed of 313131
    """
    parser = argparse.ArgumentParser("blackjack")
    parser.add_argument(
        "--seed", dest='seed', help="The seed that a game will be played with", type=int)
    args = parser.parse_args()
    seed = args.seed

    # If no seed is given, use the current time as the seed
    if seed is None:
        return time()

    return seed


if __name__ == "__main__":
    seed = get_seed()
    play(seed)

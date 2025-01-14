

class Asker():

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
            if number_of_decks not in range(1, Deck.MAX_DECK_PACKS+1):
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

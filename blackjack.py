from cards import Deck, Hand, Card
from has_hands import Player, Dealer
import interface
from settings import Settings


class Blackjack():

    def __init__(self):
        self.deck = None
        self.players = []
        self.dealer = Dealer()

    def setup(self):
        deck_quantity, player_quantity = interface.display_settings()
        self.deck = Deck(number_of_decks=deck_quantity)
        player_information = interface.display_player_information(
            player_quantity)
        for info in player_information:
            self.players.append(Player(info[0], info[1]))

    def deal_initial_hands(self) -> None:
        """
        Simulates dealing cards to each player and the dealer.
        """
        # First, give each player and dealer an empty hand with bet
        for player in self.players:
            player.give_hand(Hand())
        self.dealer.give_hand(Hand())

    def deal_cards(self):
        # Next, go through each player and give cards to hand
        interface.display_card_dealing(self.players, self.dealer)
        for _ in range(2):
            for person in self.players + [self.dealer]:
                hand = person.get_next_hand()
                person.hit(hand, self.deck)
                interface.display_card_dealing(self.players, self.dealer)
        interface.display_card_dealing(self.players, self.dealer, True)

    def player_turn(self, player: Player, deck: Deck):
        """
        Complete a round for a player, where they can make decisions about what to do.
        """
        while player.get_next_hand() is not None:
            hand: Hand = player.get_next_hand()
            # Check the hand is not a blackjack from draw
            if hand.is_blackjack():
                hand.deactivate()
                continue
            # Get the action choices
            action_choices = ["hit", "stick"]
            if player.can_split(hand) and player.get_split_count() < Settings.MAX_SPLITS:
                action_choices.append("split")
            if player.can_double_down(hand):
                action_choices.append("double-down")
            # Get player action and commit action
            action = self.__interface.display_player_turn(
                player, self.__dealer, action_choices)
            # Actions
            if action == "hit":
                player.hit(hand, deck)
            elif action == "stick":
                player.stick(hand)
            elif action == "split":
                player.split(hand, deck)
            elif action == "double-down":
                player.double_down(hand, deck)

    def play_round(self):
        # Shuffle deck
        self.deck.shuffle(1000)
        # Deal initial hands
        self.deal_initial_hands()
        # Take initial bets
        # _ = interface.display_initial_bets(self.players, self.dealer)
        for player in self.players:
            player.get_next_hand().set_bet(500)
        # Deal cards
        self.deal_cards()
        # Iterate through player turns
        for player in self.players:
            interface.display_player_turn(
                player, self.deck, self.players, self.dealer)

    def play(self):
        # title
        _ = interface.display_title()
        # self.setup()
        self.deck = Deck(number_of_decks=2)
        self.players.append(Player("Joe", 10000))
        self.players.append(Player("Will", 10000))
        self.players.append(Player("Ines", 10000))
        self.players.append(Player("Maria", 10000))
        self.players.append(Player("Yohei", 10000))

        self.play_round()


if __name__ == "__main__":
    blackjack = Blackjack()
    blackjack.play()

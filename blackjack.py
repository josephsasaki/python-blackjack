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

    def player_turn(self, player: Player):
        """
        Complete a round for a player, where they can make decisions about what to do.

        """
        while player.get_next_hand() is not None:
            hand: Hand = player.get_next_hand()
            # Check the hand is not a blackjack from draw
            if hand.is_blackjack():
                hand.deactivate()
                continue
            # Get player action and commit action
            action = interface.display_player_turn(
                player, self.deck, self.players, self.dealer, False)
            # Actions
            if action == "hit":
                player.hit(hand, self.deck)
            elif action == "stick":
                player.stick(hand)
            elif action == "split":
                player.split(hand, self.deck)
            elif action == "double-down":
                player.double_down(hand, self.deck)
        _ = interface.display_player_turn(
            player, self.deck, self.players, self.dealer, True)

    def dealer_should_play(self) -> bool:
        """
        Check whether the dealer's turn should be completed. Dealer's turn not completed if:
        1) All hands are bust
        2) All hands are blackjacks and dealer has no chance of blackjack
        """
        busts = []
        blackjacks = []
        for player in self.players:
            for hand in player.get_hands():
                busts.append(hand.is_bust())
                blackjacks.append(hand.is_blackjack())
        # Check if all busts
        if all(busts):
            return False
        # Check if all blackjacks and dealer can't have blackjack
        if all(blackjacks) and self.dealer.upcard().get_rank() != "A":
            return False
        return True

    def dealer_turn(self):
        """
        Complete a round for the dealer.
        """
        dealer_hand = self.dealer.get_next_hand()
        _ = interface.display_dealer_turn(self.players, self.dealer)
        # Check for blackjack
        if dealer_hand.is_blackjack():
            pass
        while dealer_hand.get_score() < 17:
            self.dealer.hit(dealer_hand, self.deck)
            if dealer_hand.is_bust():
                pass
            _ = interface.display_dealer_turn(self.players, self.dealer)
        dealer_hand.is_active = False
        _ = interface.display_dealer_turn(self.players, self.dealer, True)

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
            self.player_turn(player)
        # Decide whether dealer should have turn
        if self.dealer_should_play():
            self.dealer_turn()

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

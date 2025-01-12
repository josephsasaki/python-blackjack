import rich
from models import Hand


HAND_GRAPHIC_5 = [
    "[  ]        ╭───────╮",
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
    "[  ]                 ",
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
    "[  ]                 ",
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
    "[  ]                 ",
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
    "[  ]                 ",
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


def make_hand_graphic(hand: Hand) -> list[str]:
    """
    Produces a graphic for a hand.
    """
    number_of_cards = len(hand.cards)
    hand_graphic = HAND_GRAPHICS[number_of_cards-1].copy()
    # Replace the ranks and suits in the top-left corners
    for i, card in enumerate(hand.cards):
        # First, replace the rank
        rank_replacement = card[0] + " " if card[0] != "10" else "10"
        row_index, column_index = TOP_RANK_REPLACE[i]
        hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
            rank_replacement + hand_graphic[row_index][column_index+2:]
        # Next, replace the suit
        row_index, column_index = TOP_SUIT_REPLACE[i]
        hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
            card[1] + hand_graphic[row_index][column_index+1:]
    # Replace the rank and suit on the bottom-right of the top card
    top_card = hand.cards[-1]
    # Replace the rank
    rank_replacement = " " + top_card[0] if top_card[0] != "10" else "10"
    row_index, column_index = BOTTOM_RANK_REPLACE[number_of_cards-1]
    hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
        rank_replacement + hand_graphic[row_index][column_index+2:]
    # Replace the suit
    row_index, column_index = BOTTOM_SUIT_REPLACE[number_of_cards-1]
    hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
        top_card[1] + hand_graphic[row_index][column_index+1:]
    # Add the hand score
    string_score = str(hand.get_score())
    row_index, column_index = SCORE_REPLACE
    string_score = " " + \
        string_score if len(string_score) == 1 else string_score
    hand_graphic[row_index] = hand_graphic[row_index][:column_index] + \
        string_score + hand_graphic[row_index][column_index+2:]

    return hand_graphic


def display_all_hands_graphic(hands: list[Hand]) -> list[str]:
    """
    Concatenates all the individual hand graphics together.
    """
    all_hands_graphic = []
    for row_index in range(10):
        lines = []
        for hand in hands:
            hand_graphic = make_hand_graphic(hand)
            lines.append(hand_graphic[row_index])
        all_hands_graphic.append("  │  ".join(lines))
    return all_hands_graphic


if __name__ == "__main__":
    hands = [
        Hand([("10", "H"), ("10", "D"), ("10", "C"), ("10", "C"), ("10", "C")]),
        Hand([("10", "H"), ("10", "D")]),
        Hand([("10", "H"), ("10", "D"), ("10", "C")]),
        Hand([("10", "H")]),
    ]
    g = display_all_hands_graphic(hands)
    print("\n".join(g))

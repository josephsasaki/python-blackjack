# pylint: skip-file

import graphics
import pytest
from models import Hand


def test_make_hand_graphic_one():
    """make_hand_graphic(): hand with one card is displayed correctly."""
    hand = Hand([("A", "H")])
    graphic = ["                     ",
               "                     ",
               "                     ",
               "                     ",
               "╭───────╮            ",
               "│A      │            ",
               "│H      │            ",
               "│      H│            ",
               "│      A│            ",
               "╰───────╯        [11]"]
    assert graphics.make_hand_graphic(hand) == graphic


def test_make_hand_graphic_two():
    """make_hand_graphic(): hand with two cards is displayed correctly."""
    hand = Hand([("A", "H"), ("2", "D")])
    graphic = ["                     ",
               "                     ",
               "                     ",
               "   ╭───────╮         ",
               "╭──┤2      │         ",
               "│A │D      │         ",
               "│H │      D│         ",
               "│  │      2│         ",
               "│  ╰────┬──╯         ",
               "╰───────╯        [13]"]
    assert graphics.make_hand_graphic(hand) == graphic


def test_make_hand_graphic_three():
    """make_hand_graphic(): hand with three cards is displayed correctly."""
    hand = Hand([("A", "H"), ("2", "D"), ("5", "H")])
    graphic = ["                     ",
               "                     ",
               "      ╭───────╮      ",
               "   ╭──┤5      │      ",
               "╭──┤2 │H      │      ",
               "│A │D │      H│      ",
               "│H │  │      5│      ",
               "│  │  ╰────┬──╯      ",
               "│  ╰────┬──╯         ",
               "╰───────╯        [18]"]
    assert graphics.make_hand_graphic(hand) == graphic


def test_make_hand_graphic_four():
    """make_hand_graphic(): hand with four cards is displayed correctly."""
    hand = Hand([("A", "H"), ("2", "D"), ("5", "H"), ("K", "S")])
    graphic = ["                     ",
               "         ╭───────╮   ",
               "      ╭──┤K      │   ",
               "   ╭──┤5 │S      │   ",
               "╭──┤2 │H │      S│   ",
               "│A │D │  │      K│   ",
               "│H │  │  ╰────┬──╯   ",
               "│  │  ╰────┬──╯      ",
               "│  ╰────┬──╯         ",
               "╰───────╯        [18]"]
    assert graphics.make_hand_graphic(hand) == graphic


def test_make_hand_graphic_five():
    """make_hand_graphic(): hand with five cards is displayed correctly."""
    hand = Hand([("A", "H"), ("2", "D"), ("5", "H"), ("K", "S"), ("Q", "C")])
    graphic = ["            ╭───────╮",
               "         ╭──┤Q      │",
               "      ╭──┤K │C      │",
               "   ╭──┤5 │S │      C│",
               "╭──┤2 │H │  │      Q│",
               "│A │D │  │  ╰────┬──╯",
               "│H │  │  ╰────┬──╯   ",
               "│  │  ╰────┬──╯      ",
               "│  ╰────┬──╯         ",
               "╰───────╯        [28]"]
    assert graphics.make_hand_graphic(hand) == graphic


def test_make_hand_graphic_10():
    """make_hand_graphic(): a 10 is correctly places."""
    hand = Hand([("10", "H"), ("10", "D"),
                ("10", "H"), ("10", "S"), ("10", "C")])
    graphic = ["            ╭───────╮",
               "         ╭──┤10     │",
               "      ╭──┤10│C      │",
               "   ╭──┤10│S │      C│",
               "╭──┤10│H │  │     10│",
               "│10│D │  │  ╰────┬──╯",
               "│H │  │  ╰────┬──╯   ",
               "│  │  ╰────┬──╯      ",
               "│  ╰────┬──╯         ",
               "╰───────╯        [50]"]
    print("\n".join(graphics.make_hand_graphic(hand)))
    assert graphics.make_hand_graphic(hand) == graphic

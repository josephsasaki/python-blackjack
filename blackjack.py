
class Card():

    SUITS = ["S", "D", "H", "C"]
    RANKS = ["A", "2", "3", "4", "5", "6",
                  "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, rank: str, suit: str):
        if rank not in Card.RANKS:
            raise ValueError("Invalid rank passed.")
        if suit not in Card.SUITS:
            raise ValueError("Invalid suit passed.")
        self.__rank == rank
        self.__suit == suit

    def get_rank(self) -> str:
        return self.__rank

    def get_suit(self) -> str:
        return self.__suit

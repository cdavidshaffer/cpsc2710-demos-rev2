from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    CLUBS = "clubs"


class Rank(Enum):
    ACE = "ace"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"


@dataclass(frozen=True)
class PlayingCard:
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank.value} of {self.suit.value}"


@dataclass(frozen=True)
class BlackjackCard(PlayingCard):
    def values(self) -> set[int]:
        match self.rank:
            case Rank.ACE:
                return {1, 11}
            case Rank.JACK | Rank.QUEEN | Rank.KING:
                return {10}
            case _:
                return {list(Rank).index(self.rank) + 1}

    def __str__(self) -> str:
        return f"{super().__str__()} ({sorted(self.values())})"


@dataclass(frozen=True)
class WarCard(PlayingCard):
    def strength(self) -> int:
        order = [
            Rank.TWO,
            Rank.THREE,
            Rank.FOUR,
            Rank.FIVE,
            Rank.SIX,
            Rank.SEVEN,
            Rank.EIGHT,
            Rank.NINE,
            Rank.TEN,
            Rank.JACK,
            Rank.QUEEN,
            Rank.KING,
            Rank.ACE,
        ]
        return order.index(self.rank) + 2

    def beats(self, other: WarCard) -> bool:
        return self.strength() > other.strength()


def blackjack_deck() -> list[BlackjackCard]:
    return [BlackjackCard(rank, suit) for suit in Suit for rank in Rank]


def war_deck() -> list[WarCard]:
    return [WarCard(rank, suit) for suit in Suit for rank in Rank]

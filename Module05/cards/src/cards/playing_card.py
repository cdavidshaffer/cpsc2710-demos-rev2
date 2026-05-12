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


def all_cards() -> list[PlayingCard]:
    return [PlayingCard(r, s) for s in Suit for r in Rank]

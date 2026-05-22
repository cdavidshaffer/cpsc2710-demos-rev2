from cards_inheritance.cards import BlackjackCard, Rank, Suit, WarCard


def main() -> None:
    ace = BlackjackCard(Rank.ACE, Suit.SPADES)
    king = BlackjackCard(Rank.KING, Suit.HEARTS)
    print(ace)
    print(king)

    war_ace = WarCard(Rank.ACE, Suit.CLUBS)
    war_king = WarCard(Rank.KING, Suit.CLUBS)
    print(f"{war_ace} beats {war_king}: {war_ace.beats(war_king)}")


if __name__ == "__main__":
    main()

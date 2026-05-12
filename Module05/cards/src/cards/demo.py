from cards.playing_card import PlayingCard, Rank, Suit, all_cards


def main() -> None:
    pc1 = PlayingCard(Rank.ACE, Suit.DIAMONDS)
    print(pc1)
    pc2 = PlayingCard(Rank.ACE, Suit.DIAMONDS)
    print(pc2)
    print(pc1 == pc2)
    pc3 = PlayingCard(Rank.ACE, Suit.DIAMONDS)
    print(pc3)
    print(pc1 == pc3)
    pc4 = PlayingCard(Rank.KING, Suit.SPADES)
    print(pc4)

    deck = all_cards()
    print(len(deck))
    print(deck)


if __name__ == "__main__":
    main()

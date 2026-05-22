from cards_inheritance.cards import (
    BlackjackCard,
    PlayingCard,
    Rank,
    Suit,
    WarCard,
    blackjack_deck,
    war_deck,
)


def test_blackjack_card_is_a_playing_card() -> None:
    card = BlackjackCard(Rank.ACE, Suit.SPADES)

    assert isinstance(card, PlayingCard)
    assert str(card).startswith("ace of spades")


def test_blackjack_values_for_ace_face_and_number_cards() -> None:
    assert BlackjackCard(Rank.ACE, Suit.SPADES).values() == {1, 11}
    assert BlackjackCard(Rank.QUEEN, Suit.HEARTS).values() == {10}
    assert BlackjackCard(Rank.SEVEN, Suit.CLUBS).values() == {7}


def test_war_card_strength() -> None:
    ace = WarCard(Rank.ACE, Suit.SPADES)
    king = WarCard(Rank.KING, Suit.SPADES)

    assert ace.beats(king)
    assert not king.beats(ace)


def test_deck_factories_create_game_specific_card_types() -> None:
    assert len(blackjack_deck()) == 52
    assert all(isinstance(card, BlackjackCard) for card in blackjack_deck())
    assert len(war_deck()) == 52
    assert all(isinstance(card, WarCard) for card in war_deck())

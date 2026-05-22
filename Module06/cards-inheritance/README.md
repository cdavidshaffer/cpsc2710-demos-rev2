# Cards Inheritance Demo

This project extends the Module05 `PlayingCard` example into a small hierarchy:

- `PlayingCard`: common rank, suit, and display behavior.
- `BlackjackCard`: adds blackjack-specific scoring.
- `WarCard`: adds a ranking rule for the card game War.

The example is intentionally small: the subclasses do not need new state, but
they add behavior that belongs to a particular card game.

Run:

```sh
uv run cards-inheritance
uv run pytest
```

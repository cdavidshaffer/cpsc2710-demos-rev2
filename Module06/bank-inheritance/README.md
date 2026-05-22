# Bank Inheritance Demo

This project extends the Module05 `BankAccount` idea into a small inheritance
hierarchy:

- `BankAccount`: shared account state and ordinary deposit/withdraw behavior.
- `SavingsAccount`: adds interest behavior.
- `CheckingAccount`: overrides withdrawal behavior to support overdraft.

The example is designed to show:

- shared state initialized with `super().__init__`
- inherited methods
- overriding methods
- using `super()` from an override
- why subclass behavior should still respect the base class contract

Run:

```sh
uv run bank-inheritance
uv run pytest
```

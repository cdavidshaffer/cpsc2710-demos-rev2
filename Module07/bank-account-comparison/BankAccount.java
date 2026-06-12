package edu.au;

public class BankAccount {

	private Person owner;
	private int account_number;
	private double balance;
	
	public BankAccount(int account_number, String owner) {
		this.account_number = account_number;
		this.owner = owner;
		this.balance = 0;
	}
	
	
	public String getOwner() {
		return owner;
	}

	public void setOwner(String owner) {
		if (owner == null || owner.length() < 3)
			throw new IllegalArgumentException("owner must be non-null and at least 3 characters");
		this.owner = owner;
	}
		
	public double getBalance() {
		return balance;
	}
	
	public int getAccountNumber() {
		return account_number;
	}
	
	public void deposit(double amount) {
		balance += amount;
	}
	
	public void withdraw(double amount) {
		balance -= amount;
	}


	public String toString() {
		return "Account number: " + account_number +
                    "  owner: " + owner +
                    "  with balance: " + balance;
	}
}


package edu.au;

public class BankDemo {
    public static void  main(String[] argv) {
        BankAccount account = new BankAccount(123456, "Fred");
		System.out.println(account);
        System.out.println(account.getOwner());
        account.setOwner("Betty");
		System.out.println(account);
        //account.setOwner("f");
        account.setOwner(null);
    }
}
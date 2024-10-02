package controller;

import java.util.ArrayList;
import java.util.List;
import model.Expense;

public class ExpenseManager {
    private List<Expense> expenses = new ArrayList<>();

	//set expenses 
    public void addExpense(Expense expense) {
        expenses.add(expense);
    }
	
	//remove expenses 
    public void removeExpense(Expense expense) {
        expenses.remove(expense);
    }

    public List<Expense> getAllExpenses() {
        return expenses;
    }

	//calculate total expenses 
    public double getTotalExpense() {
        double total = 0;
        for (Expense expense : expenses) {
            total += expense.getAmount();
        }
        return total;
    }
}

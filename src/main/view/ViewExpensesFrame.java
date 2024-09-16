package view;

import controller.ExpenseManager;
import java.awt.*;
import java.util.List;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import model.Expense;

public class ViewExpensesFrame extends JFrame {
    private ExpenseManager expenseManager;

    public ViewExpensesFrame(ExpenseManager expenseManager) {
        this.expenseManager = expenseManager;

        setTitle("View Expenses");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        DefaultTableModel tableModel = new DefaultTableModel(new String[] { "Name", "Amount", "Category", "Date" }, 0);
        JTable expenseTable = new JTable(tableModel);

        List<Expense> expenses = expenseManager.getAllExpenses();
        for (Expense expense : expenses) {
            tableModel.addRow(new Object[] { expense.getName(), expense.getAmount(), expense.getCategory(), expense.getDate() });
        }

        JScrollPane scrollPane = new JScrollPane(expenseTable);
        add(scrollPane, BorderLayout.CENTER);
    }
}

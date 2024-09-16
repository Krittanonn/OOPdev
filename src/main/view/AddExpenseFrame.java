package view;

import controller.ExpenseManager;
import model.Expense;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class AddExpenseFrame extends JFrame {
    private JTextField nameField;
    private JTextField amountField;
    private JComboBox<String> categoryField;
    private JTextField dateField;
    private JButton addButton;
    private ExpenseManager expenseManager;

    public AddExpenseFrame(ExpenseManager expenseManager) {
        this.expenseManager = expenseManager;
        
        setTitle("Add Expense");
        setSize(300, 200);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        nameField = new JTextField(20);
        amountField = new JTextField(20);
        categoryField = new JComboBox<>(new String[] { "Food", "Travel", "Entertainment" });
        dateField = new JTextField(20);
        addButton = new JButton("Add Expense");

        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String name = nameField.getText();
                double amount;
                try {
                    amount = Double.parseDouble(amountField.getText());
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Invalid amount.", "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                String category = (String) categoryField.getSelectedItem();
                String date = dateField.getText();

                Expense expense = new Expense(name, amount, category, date);
                expenseManager.addExpense(expense);
                JOptionPane.showMessageDialog(null, "Expense added successfully.", "Success", JOptionPane.INFORMATION_MESSAGE);
                dispose();
            }
        });

        JPanel panel = new JPanel();
        panel.add(new JLabel("Name:"));
        panel.add(nameField);
        panel.add(new JLabel("Amount:"));
        panel.add(amountField);
        panel.add(new JLabel("Category:"));
        panel.add(categoryField);
        panel.add(new JLabel("Date:"));
        panel.add(dateField);
        panel.add(addButton);

        add(panel);
    }
}

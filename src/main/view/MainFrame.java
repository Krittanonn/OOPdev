package view;

import controller.ExpenseManager;
import controller.ExportToCSV;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public class MainFrame extends JFrame {
    private ExpenseManager expenseManager;

    public MainFrame(ExpenseManager expenseManager) {
        this.expenseManager = expenseManager;

        setTitle("Expense Management");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JButton addButton = new JButton("Add Expense");
        JButton viewButton = new JButton("View Expenses");
        JButton exportButton = new JButton("Export to CSV");

        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                new AddExpenseFrame(expenseManager).setVisible(true);
            }
        });

        viewButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                new ViewExpensesFrame(expenseManager).setVisible(true);
            }
        });

        exportButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    ExportToCSV.export(expenseManager.getAllExpenses(), "expenses.csv");
                    JOptionPane.showMessageDialog(null, "Data exported successfully!");
                } catch (IOException ioException) {
                    JOptionPane.showMessageDialog(null, "Error exporting data: " + ioException.getMessage(),
                            "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        JPanel panel = new JPanel();
        panel.add(addButton);
        panel.add(viewButton);
        panel.add(exportButton);

        add(panel);
    }
}

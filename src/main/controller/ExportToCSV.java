package controller;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import model.Expense;

public class ExportToCSV {
    public static void export(List<Expense> expenses, String filename) throws IOException {
        FileWriter fileWriter = new FileWriter(filename);
        PrintWriter printWriter = new PrintWriter(fileWriter);

        printWriter.println("Name,Amount,Category,Date");

        for (Expense expense : expenses) {
            printWriter.printf("%s,%.2f,%s,%s%n",
                    expense.getName(),
                    expense.getAmount(),
                    expense.getCategory(),
                    expense.getDate());
        }

        printWriter.close();
    }
}

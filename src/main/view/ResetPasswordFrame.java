package view;

import controller.UserManager;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ResetPasswordFrame extends JFrame {
    private JTextField usernameField;
    private JPasswordField newPasswordField;
    private JButton resetButton;

    public ResetPasswordFrame() {
        setTitle("Reset Password");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        usernameField = new JTextField(20);
        newPasswordField = new JPasswordField(20);
        resetButton = new JButton("Reset Password");

        resetButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String username = usernameField.getText();
                String newPassword = new String(newPasswordField.getPassword());
                if (username.isEmpty() || newPassword.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "Please fill in both fields.", "Error", JOptionPane.ERROR_MESSAGE);
                } else {
                    UserManager.resetPassword(username, newPassword);
                    JOptionPane.showMessageDialog(null, "Password has been reset successfully.", "Success", JOptionPane.INFORMATION_MESSAGE);
                    dispose();
                }
            }
        });

        JPanel panel = new JPanel();
        panel.add(new JLabel("Username:"));
        panel.add(usernameField);
        panel.add(new JLabel("New Password:"));
        panel.add(newPasswordField);
        panel.add(resetButton);

        add(panel);
    }
}

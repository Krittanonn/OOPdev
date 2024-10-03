import view.LoginFrame;

public class Main {
    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
				// rubn frist in loginframe for login user            
				new LoginFrame().setVisible(true);
            }
        });
    }
}
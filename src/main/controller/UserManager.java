package controller;

import java.util.HashMap;

public class UserManager {
    private static HashMap<String, String> users = new HashMap<>();
    private static HashMap<String, Integer> loginAttempts = new HashMap<>();
    private static final int MAX_ATTEMPTS = 5;


	//set user and passwords 
    static {
        users.put("b6621650213", "password123");
        users.put("user2", "password2");
    }

    public static boolean authenticate(String username, String password) {
        if (loginAttempts.getOrDefault(username, 0) >= MAX_ATTEMPTS) {
            return false;
        }

        if (users.containsKey(username)) {
            boolean isAuthenticated = users.get(username).equals(password);
            if (isAuthenticated) {
                loginAttempts.put(username, 0);
            } else {
                loginAttempts.put(username, loginAttempts.getOrDefault(username, 0) + 1);
            }
            return isAuthenticated;
        }
        return false;
    }

    public static void resetPassword(String username, String newPassword) {
        if (users.containsKey(username)) {
            users.put(username, newPassword);
        }
    }
}

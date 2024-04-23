package com.ctf.ezjava.tools;

import java.io.Serializable;

public class UserCredentials implements Serializable {
    public String username;
    public String password;

    public UserCredentials(String username, String password) {
        this.username = username;
        this.password = password;
    }
}

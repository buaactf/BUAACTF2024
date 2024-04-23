package com.ctf.ezjava.tools;


import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class CookieManager {
    public static String getCookie(String username, String password) throws Exception {
        byte[] key = Base64.getDecoder().decode("bGluZ2xpbmdsaW5nbGluZw==");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
        try {
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        UserCredentials userCredentials = new UserCredentials(username, password);
        String data = SecureSerializer.serialize(userCredentials);
        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public static UserCredentials parseCookie(String cookie) throws Exception {
        byte[] encrypted = Base64.getDecoder().decode(cookie);
        byte[] key = Base64.getDecoder().decode("bGluZ2xpbmdsaW5nbGluZw==");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
        try {
            cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        byte[] decrypted = cipher.doFinal(encrypted);
        return (UserCredentials) SecureSerializer.deserialize(new String(decrypted));
    }
}


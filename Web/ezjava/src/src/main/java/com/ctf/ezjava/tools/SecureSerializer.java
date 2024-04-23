package com.ctf.ezjava.tools;

import org.nibblesec.tools.SerialKiller;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.util.Base64;

public class SecureSerializer {
    public static String serialize(Object obj) throws Exception {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bos);
        oos.writeObject(obj);
        return Base64.getEncoder().encodeToString(bos.toByteArray());
    }

    public static Object deserialize(String cookie) throws Exception {
        ByteArrayInputStream bai = new ByteArrayInputStream(Base64.getDecoder().decode(cookie));
        SerialKiller sk = new SerialKiller(bai, "/home/zeroc/My_Challenge/gongan/Web/ezjava/src/ezjava/src/main/resources/serialkiller.xml");
        return sk.readObject();
    }
}

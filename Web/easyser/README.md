# 赛题设计说明

| 出题人 | 题目类型 | 题目分值 |
| :----- | :------- | :------- |
| zeroc | web      | 500      |

## 题目信息

- 题目名称: easyser
- 预估难度(1.0~5.0): 1.5
- 题目类型:
  - [] 静态附件
  - [] 动态附件
  - [] 静态容器
  - [x] 动态容器
- 题目标签:
  - [x] web
  - [] pwn
  - [] reverse
  - [] misc
  - [] crypto
  - [] blockchain

## 题目描述

What is serialization and unserialization?

## 考点

1. 简单的 PHP 序列化和反序列化
2. PHP 魔术方法的使用
3. PHP 低版本中 `__wakeup()` 的绕过
4. PHP 任意文件包含 RCE

## 提示

1. https://www.php.net/manual/zh/language.oop5.magic.php
2. https://fushuling.com/index.php/2023/03/11/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E4%B8%ADwakeup%E7%BB%95%E8%BF%87%E6%80%BB%E7%BB%93/

## Flag

动态 FLAG

## 参考

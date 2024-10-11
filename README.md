# UART库

为了解决pyserial库只能读取给定字节的数据，制作了一个针对包头包尾读取和发送的类UART

## 包含的方法

- `send_arr` 发送整形数组
- `send` 发送整形数据
- `write` 发送字符串数据
- `read` 读取字符串数据
- `ori_read` 原Serial类的读取方法
- `ori_write` 原Serial类的写入方法

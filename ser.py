from typing import Iterable
import serial
import struct


class UART(serial.Serial):
    """
    串口类
    ====
    继承了pyserial库的串口类，封装了一些常用的串口操作
    * 发送整形数组 send_arr
    * 发送整形数据 send
    * 发送字符串数据 write
    * 读取字符串数据 read
    * 原Serial类的读取方法 ori_read
    * 原Serial类的写入方法 ori_write
    """

    def __init__(self, port, baudrate, _timeout=None):
        """
        初始化串口
        ----
        :param port: 串口号
        :param baudrate: 波特率
        """
        super().__init__(port, baudrate, timeout=_timeout)

    def send_arr(
        self,
        args: list[int] | tuple[int, ...],
        head: str | None = None,
        tail: str | None = None,
    ):
        """
        发送数组,包含包头包尾数据
        ----
        对端收到的数据是用0,1表示正负，然后再接上数字的字符串，长度为3，并且包含正负标志
        例如：-123 -> 0123

        :param args: 要发送的整型数组
        :param head: 包头
        :param tail: 包尾
        """
        if head is not None:
            self.write(head)

        for index, i in enumerate(args):
            msg = str(abs(i))  # 取绝对值，因为符号会单独处理
            #  补零，使得长度为3
            while len(msg) < 3:
                msg = "0" + msg

            # 添加标识符
            if i >= 0:
                msg = "1" + msg
            else:
                msg = "0" + msg

            self.write(msg)

        if tail is not None:
            self.write(tail)

    def send(self, data: int, head: bytes | None = None, tail: bytes | None = None):
        """
        发送整型数据,包含包头包尾
        ----
        对端回直接收到数字信息

        :param data: 要发送的整型数据
        :param head: 包头,字节类型，例如b'@'，默认为None
        :param tail: 包尾,字节类型，例如b'@'，默认为None
        """
        newdata = struct.pack(">i", data)
        if head is not None:
            super().write(head)
        super().write(newdata)
        if tail is not None:
            super().write(tail)

    def write(
        self,
        data: str,
        head: str | None = None,
        tail: str | None = None,
    ):
        """
        发送字符串数据
        ----
        重写了原有的方法，将字符串数据转换为ascii码发送

        :param data: 要发送的字符串数据，str类型
        :param head: 包头,字符串类型，例如"@",默认为None
        :param tail: 包尾,字符串类型，例如"#",默认为None
        """
        if head is not None:
            super().write(head.encode("ascii"))
        super().write(data.encode("ascii"))
        if tail is not None:
            super().write(tail.encode("ascii"))

    def read(self, ifdecode=True, head=b"@", tail=b"#"):
        """读取字符串数据,包头包尾只能是一个字节
        ----

        :param ifdecode: 是否用ascii码解码数据包
        :param head: 包头
        :param tail: 包尾
        返回读取到的已解码数据"""
        PACKET_HEAD = head
        PACKET_TAIL = tail

        data = b""  # 用于存储接收到的数据

        while True:
            byte = super().read()
            if byte == PACKET_HEAD:
                data = b""
                continue
            if byte == PACKET_TAIL:
                break
            data += byte
        if ifdecode:
            res = data.decode("ascii")
        else:
            res = data
        return res if res else None

    def ori_read(self, size: int):
        """
        原有的读取方法
        """
        return super().read(size)

    def ori_write(self, data: bytes):
        """
        原有的写入方法
        """
        return super().write(data)

    def __del__(self) -> None:
        return self.close()

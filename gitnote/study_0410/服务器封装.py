# coding=utf-8
# Copyright 2018 XXX. All Right Reserved
# Author: test@XXX.com{test}
# 服务器封装.py 18-4-10 下午4:13
# SITE: https:www.jetbrains.com/pycharm/
from socket import *
from multiprocessing import Process
import re

HTML_ROOT_DIR = "./html"
class Mains(object):
    def __init__(self):
        # 创建套接字
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        # 设置端口复用
        self.tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    def bind(self,port):
        # 绑定端口
        self.tcp_socket.bind(("", port))

    #启动服务器
    def start(self):
        # 设置监听
        self.tcp_socket.listen(5)
        # 等待客户连接
        while True:
            new_socket, new_adress = self.tcp_socket.accept()
            print("新客户%s访问服务器" % str(new_adress))
            Process(target=self.handle_client, args=(new_socket,)).start()  # new_socket.close()  # tc
            new_socket.close()

    #处理客户客户数据
    def handle_client(self,new_socket):
        recv_data = new_socket.recv(1024)
        # 回复信息
        s = recv_data.decode("gb2312")
        res_name = re.match(r"\w+ (/.*) ", s).group(1)
        file_name = res_name

        if res_name == "/" or res_name == "text.html":
            file_name = "text.html"
        # else:
        #     file_name = res_name[1:]  # /text.html--->text.html

        response_line = "HTTP/1.1 200 OK\r\n"
        response_head = "server:MyGooGle\r\n"
        f = None
        try:
            if file_name.endswith("html"):

                f = open(HTML_ROOT_DIR + file_name, "rb")  # r--->str不用decode  rb-->使用decode解码成str
            elif file_name.endswith("jpg"):
                f = open(HTML_ROOT_DIR + file_name, "rb")

            response_body = f.read()
        except:
            # 404
            response_line = "HTTP/1.1 404 Not Found\r\n"
            response = response_line + "\r\n" + response_head + "\r\n" + "文件找不到"
            new_socket.send(response.encode("gb2312"))
        else:
            # 200
            response = response_line + "\r\n" + response_head + "\r\n" + response_body.decode("gb2312")
            new_socket.send(response.encode("gb2312"))
        finally:

            if f != None:
                f.close()

            new_socket.close()
def main():
    http_server = Mains()
    http_server.bind(8888)
    http_server.start()
if __name__ == "__main__":
    main()
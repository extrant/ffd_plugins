import imgui
import logging
import glfw
import socket
import threading
import netifaces
from PIL import Image
from PIL import PngImagePlugin
from imgui.integrations.glfw import GlfwRenderer
from ff_draw.plugins import FFDrawPlugin
import OpenGL.GL as gl

IP = '127.0.0.1'
SIP = '127.0.0.1'
SSIP = '0'
PORT = 9999
inputmessage = '大家好啊，我是电棍'
send_true = False
def get_local_ipv4():
    # 这里是您之前提供的获取 IPv4 地址的函数
    # 请确保已经导入了 netifaces 模块，并定义了 get_local_ipv4 函数
    interfaces = netifaces.interfaces()
    ipv4_addresses = []
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ipv4_addresses.extend(address['addr'] for address in addresses[netifaces.AF_INET])
    return ipv4_addresses

# 调用函数获取本机每个网卡的 IPv4 地址
ipv4_addresses = get_local_ipv4()

# 构建下拉框选项列表
dropdown_options = [address for address in ipv4_addresses]


selected_option = 0
class IPv4(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.fasong = False
        self.jieshou = False

        
        
    def draw_panel(self):
        global selected_option, dropdown_options, IP, SIP, SSIP, inputmessage, send_true
        _, selected_option = imgui.combo("选择一个 IPv4 地址", selected_option, dropdown_options, len(dropdown_options))
        final_option = dropdown_options[selected_option]
        imgui.text(f"你选择的是：{final_option}")

        if imgui.button("发送端"):
            self.fasong = True
            self.jieshou = False
        if imgui.button("接受端"):
            self.fasong = False
            self.jieshou = True


        if self.jieshou is True and self.fasong is False:
            imgui.text("Start Server……")
            imgui.same_line()
            imgui.text(f"地址：{final_option}，端口:9999")
            IP = final_option
            threading.Thread(target=start_server).start()
#start_server() 
        if self.jieshou is False and self.fasong is True: 

            _, SSIP = imgui.input_text("输入接收端IP地址:", SSIP, 100)
            if imgui.button("Execute"):
                SIP = SSIP
                print(SIP)
            _, inputmessage = imgui.input_text("输入发送的内容:", inputmessage, 100)
            
            if imgui.button("Send"):
                threading.Thread(target=connect_to_server).start()
            imgui.text(f"地址：{SIP}，端口:9999")
            
            
#服务端            
def handle_client(client_socket, addr, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                message = data.decode()
                print(f"接收数据： {addr}: {message}")
                broadcast(message, clients)
        except:
            remove_client(client_socket, clients)
            break

def broadcast(message, clients):
    for client in clients:
        client.send(message.encode())

def remove_client(client_socket, clients):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"主机连接： {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
        client_thread.start()

               
               
               
#客户端
def send_message(client_socket):
    while True:
        message = inputmessage#input("Enter your message: ")
        client_socket.send(message.encode())
        break

def connect_to_server():
    global send_true
    sendb_true = send_true
    #if sendb_true is True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((SIP, PORT))
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

    while True:
    #    if sendb_true is True:
        data = client_socket.recv(1024)
        print(f"发送消息: {data.decode()}")   
        break
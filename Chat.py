import socket
import random
import threading
import time


class Broadcaster(threading.Thread):

    def __init__(self):
        super().__init__()
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = 8000
        self.is_chatting = False
        self.destination = ('255.255.255.255', self.port)

    def run(self):
        data = "Hello"
        timeout = random.randint(1, 2)
        self.UDPSock.settimeout(timeout)
        try:
            self.UDPSock.sendto(str.encode(data), self.destination)
            response, address = self.UDPSock.recvfrom(1024)
            ##address[0] is ip but port number is in response message
            ip = address[0]
            port = int(response)
            client = Client(ip, port)
            self.is_chatting = True
            client.connect()
        except:
            return


class Listener(threading.Thread):

    def __init__(self):
        super().__init__()
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.portNumber = 0
        self.is_chatting = False

    def run(self):
        self.UDPSock.bind(('', 8000))
        timeout = random.randint(2, 4)
        self.UDPSock.settimeout(timeout)
        try:
            message, address = self.UDPSock.recvfrom(1024)
            self.is_chatting = True
            if message.decode() == "Hello":
                self.portNumber = random.randint(10000, 20000)
                self.UDPSock.sendto(str(self.portNumber).encode(), address)
                self.UDPSock.close()
                server = Server('', self.portNumber)
                server.connect()
        except:
            return


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## make tcp connection
    def connect(self):
        self.TCPSock.bind((self.ip, self.port))
        self.TCPSock.listen(1)
        client_socket, address = self.TCPSock.accept()
        client_socket.send(str("Connection established").encode())
        message = client_socket.recv(1024).decode()
        if message == "Let's start chat":
            self.start_chat(client_socket)

    def start_chat(self, client_socket):
        print("Ready to Chat, type your message")
        while True:
            sending_message = input("+ ")
            client_socket.send(sending_message.encode())
            if sending_message == "EXIT":
                client_socket.close()
                break

            received_message = client_socket.recv(1024).decode()
            if received_message == "EXIT":
                print("Chat finished by ...")
                client_socket.close()
                break
            else:
                print("- ", received_message)


class Client:
    def __init__(self, ip, port):
        self.destination_ip = ip
        self.destination_port = port
        self.TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## make tcp connection
    def connect(self):
        self.TCPSock.connect((self.destination_ip, self.destination_port))
        received_message = self.TCPSock.recv(1024).decode()
        if received_message == "Connection established":
            self.TCPSock.send(str("Let's start chat").encode())
            self.start_chat()

    def start_chat(self):
        print("Ready to Chat, waiting for his/her message")
        while True:
            received_message = self.TCPSock.recv(1024).decode()
            if received_message == "EXIT":
                print("Chat finished by the  other person")
                self.TCPSock.close()
                break
            else:
                print("- ", received_message)
            sending_message = input("+ ")
            self.TCPSock.send(sending_message.encode())
            if sending_message == "EXIT":
                self.TCPSock.close()
                break


flag = True

while flag:
    probablity = random.randint(0, 10)

    ## Listener mode
    if probablity < 5:
        listener_mod = Listener()
        listener_mod.start()
        time.sleep(4)
        if listener_mod.is_chatting:
            ## it's okey, get out of the loop
            flag = False

    ## Broadcaster mode
    else:
        broacaster_mod = Broadcaster()
        broacaster_mod.start()
        time.sleep(2)
        if broacaster_mod.is_chatting:
            ## it's okey, get out of the loop
            flag = False

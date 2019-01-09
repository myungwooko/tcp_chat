from  socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


class Server_config:
    def __init__(self):
        self.config_setting()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(self.ADDR)
        self.sock.listen(5)
        print("Waiting for connection...")
        accepted_thread = Thread(target=self.accepted_incoming_connections)
        self.thread_start(accepted_thread)
        self.sock.close()

    def accepted_incoming_connections(self):
        pass



    @classmethod
    def config_setting(cls):
        cls.clients = {}
        cls.addresses = {}
        HOST = ''
        PORT = 33000
        cls.BUFSIZ = 1024
        cls.ADDR = (HOST,PORT)

    @staticmethod
    def thread_start(thread):
        thread.start()
        thread.join()




class Server(Server_config):
    def __init__(self):
        super().__init__()


    def accepted_incoming_connections(self):
        while True:
            client, client_address = self.sock.accept()
            print("%s %s has connected" % client_address)
            self.bytes_and_send(client, "Greetings from the cave! Now type your name and press enter!",)
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = "Welcome %s! If you ever want to quit, type {quit} to exit." % name
        self.bytes_and_send(client, welcome)
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name


        while True:
            msg = client.recv(self.BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name + ": ")
            else:
                self.bytes_and_send(client, "{quit}")
                client.colse()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    @staticmethod
    def bytes_and_send(client, msg):
        client.send(bytes(msg, "utf8"))



class host_and_port:
    def __init__(self, host, port):
        self.host = host
        self.port = port



class Setting_Tkinter(host_and_port):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.top = tkinter.Tk()
        self.top.title("Chatter")
        messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()
        scrollbar = tkinter.Scrollbar(messages_frame)
        self.msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        messages_frame.pack()
        entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        send_button = tkinter.Button(self.top, text="Send", command=self.send)
        send_button.pack()
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)




class Client(Setting_Tkinter):

    def __init__(self, host, port):
        super().__init__(host, port)
        ADDR = (self.host, self.port)
        self.BUFSIZ = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        receive_thread = Thread(target = self.receive)
        receive_thread.start()
        tkinter.mainloop()

    def receive(self):###################################################################################### button에 연결
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tkinter.END, msg)
            except OSError:
                break

    def send(self, event=None):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.top.quit()


    def on_closing(self, event=None):#################################################################### x 눌러서 끄는 경우
        self.my_msg.set("{quit}")
        self.send()



        # ## without Tkinter
# class Client(Setting_Tkinter):
#     def __init__(self, host, port):
#         self.sock = socket(AF_INET, SOCK_STREAM)
#         self.sock.connect((host,port))
#
#
#         iThread = Thread(target=self.sendMsg)
#         iThread.daemon = True
#         iThread.start()
#
#         while True:
#             data = self.sok.recv(1024)
#             if not data:
#                 break
#             print(str(data,"utf8"))
#
#
#     def send(self):
#         while True:
#             self.sock.send(bytes(input(""), "utf8"))


host_or_not = input("Are you host? [y/n]: ")
if host_or_not == "y":
    Server()
else:
    HOST = input("Enter Host? ")
    PORT = input("Enter Port? ")
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)
    Client(HOST, PORT)




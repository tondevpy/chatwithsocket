import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55556
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True
        
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!')
        self.sala = simpledialog.askstring('Nome', 'Digite a sala que deseja entrar')
        thread = threading.Thread(target=self.conecta)
        thread.start()
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')

        self.caixaDeTexto = Text(self.root)
        self.caixaDeTexto.place(relx=0.05, rely=0.01, width=700, height=600)

        self.enviar_mensagem = Entry(self.root)
        self.enviar_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)

        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        self.root.mainloop()
    
    def fechar(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixaDeTexto.insert('end', recebido.decode())
                except:
                    pass

    def enviarMensagem(self):
        mensagem = self.enviar_mensagem.get()
        self.client.send(mensagem.encode())

        self.enviar_mensagem.delete(0, END)

Chat = Chat()

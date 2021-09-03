import os
from tkinter import *
from socket import *
import threading
import time
import clientLigacao
import serverLigacao


def receive():
    global client
    client = socket(AF_INET, SOCK_STREAM)
    ip_info = ip.get()
    HOST = ip_info
    PORT = 5001
    client.connect((HOST, PORT))
    client.send(name.get().encode())
    message = client.recv(1024).decode()
    print("passei aqui " + message)
    if message == "Ja existe um usuario com o mesmo nome":
        write(message)
    elif message in "Conectado ao servidor":
        split = message.split("/")
        write(split[0])
        registrybtn['state'] = "disabled"
        registryentry['state'] = "disabled"
        connectbtn['state'] = "active"
        connectentry['state'] = "normal"
        endbtn['state'] = "active"
        ipentry['state'] = "disabled"
        screen.protocol("WM_DELETE_WINDOW", closeConnThread)
        thread = threading.Thread(target=listen)
        thread.start()
        thread = threading.Thread(target=serverLigacao.iniciarServidorLigacao, args=split[1], )
        thread.start()


def listen():
    print("Iniciei o listen")
    while True:
        message = client.recv(1024).decode()
        if "endereco" in message:
            print("RECEBI DO SERVER ESSES DADOS: " + str(message))
            dados = message.split('/')
            clientLigacao.iniciaConexaoUDP("Ainda não sei", dados[1], dados[3])
        if 'pedido' in message:
            dados = message.split('/')
            write(dados[1] + "Deseja se conectar" + "\nDigite S para aceitar, ou N para recusar")
            resp = input()
            ligacao = socket(AF_INET, SOCK_DGRAM)
            ligacao.sendto(resp.encode(), ('127.0.0.1', 6500))
        elif "conectado" in message:
            message = client.recv(1024).decode()
            print("Conectado à" + message)
        elif "broadcast" in message:
            split = message.split("/")
            writeUsers(split[1])
        elif message == "atualiza":
            message = client.recv(1024).decode()
            write(message)
        elif message == "Nao e possivel conectar a si mesmo":
            write(message)
        elif message == "Nome nao encontrado":
            write(message)
        elif "finish" in message:
            write("Conexão encerrada")
            write("Fechando em 2 segundos...")
            time.sleep(2)
            screen.destroy()
        elif "socket" in message:
            message = client.recv(1024).decode()
            write(f"Conectado ao usuário {message}")
            connectbtn['state'] = "disabled"
            connectentry['state'] = "disabled"
        elif "repeat" in message:
            message = client.recv(1024).decode()
            write(message)

def sendName():
    dest_info = dest.get()
    client.send("consulta".encode())
    client.send(dest_info.encode())


def closeConn():
    client.send("closeConn".encode())

def closeConnThread():
    thread = threading.Thread(target=closeConn)
    thread.start()


def sendNameThread():
    thread = threading.Thread(target=sendName)
    thread.start()

def receiveThread():
    thread = threading.Thread(target=receive)
    thread.start()

def write(*message, end = "\n", sep = " "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    console.insert(INSERT, text)
    console.see(END)

def writeUsers(*message, end = "\n", sep = " "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    users.delete('1.0', END)
    users.insert(INSERT, text)
    users.see(END)

def main():
    global name
    global dest
    global ip
    global screen
    global registryentry
    global registrybtn
    global connectentry
    global connectbtn
    global endbtn
    global atualizarbtn
    global ipentry
    global console
    global users
    screen = Tk()
    screen.geometry("300x800")
    screen.title("Sala Virtual")
    name = StringVar()
    dest = StringVar()
    ip = StringVar()
    Label(text="").pack()
    connectbtn = Button(text="Procurar usuário e conectar", height="2", width="30",state="disabled", command=sendNameThread)
    connectbtn.pack()
    Label(text="").pack()
    connectentry = Entry(textvariable=dest,state="disabled")
    connectentry.pack()
    Label(text="").pack()
    registrybtn = Button(text="Registro", height="2", width="30", command=receiveThread)
    Label(text="").pack()
    registrybtn.pack()
    Label(text="").pack()
    Label(text="Nome*:").pack()
    registryentry = Entry(textvariable=name)
    registryentry.pack()
    Label(text="IP*:").pack()
    ipentry = Entry(textvariable=ip)
    ipentry.pack()
    Label(text="").pack()
    endbtn = Button(text="Encerrar Conexão", height="2", width="30", state="disabled", command=closeConnThread)
    endbtn.pack()
    Label(text="").pack()
    log = Label(text="Usuários conectados:")
    log.pack()
    users = Text(screen, height=10, width=30)
    users.pack()
    Label(text="").pack()
    log_usuarios = Label(text="Log:")
    log_usuarios.pack()
    console = Text(screen, height=10, width = 30)
    console.pack()
    screen.mainloop()

main()

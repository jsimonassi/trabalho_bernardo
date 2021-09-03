import time
from socket import *
import threading

HOST = "25.90.35.163"
PORT = 5012

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Aguardando conexão de um cliente")
clients = []
names = []
connections = []

def broadcast(message):
    time.sleep(0.5)
    for client in clients:
        client.send(("broadcast" "/" + message).encode())

def receive():
    while True:
        client, address = s.accept()
        name = client.recv(1024).decode()
        if name in names:
            client.send("Ja existe um usuario com o mesmo nome".encode())
        if name not in names:
            print("Conectado em", str(address))
            names.append(name)
            clients.append(client)
            print(f"Nome do cliente é: {name}")
            client.send(("Conectado ao servidor /" + address[0]).encode())
            showConnections()
            stringNames = ''
            for i in names:
                stringNames += i + "\n"
            broadcast(stringNames)
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

def handle(client):
    while True:
        estado = client.recv(1024).decode()
        # print(estado + "aqui")
        if "resp_conexao" in estado:
            dados = estado.split('/')
            i = int(dados[2])
            if dados[1] == 's' or dados[1] == "S":  # CONEXAO UDP
                print("entrei" + dados[2])
                clients[i].send("socket".encode())
                clients[i].send((names[clients.index(client)] + str(clients[clients.index(client)].getpeername())).encode())
                client.send("socket".encode())
                client.send((names[i] + str(clients[i].getpeername())).encode())
                connections.append((names[i], names[clients.index(client)]))
            else:
                clients[i].send("recusa".encode())
                clients[clients.index(client)].send("recusa".encode())
            # client.send((names[i] + str(clients[i].getpeername())).encode())
            # clients[i].send("socket".encode())
            # clients[i].send((names[index] + str(clients[index].getpeername())).encode())
        if estado == "atualiza":
            client.send("atualiza".encode())
            peers = ''
            for i in clients:
                peers += str(i.getpeername())
            client.send((str(names) + "/" + (peers)).encode())
        elif estado == "closeConn":
            index = clients.index(client)
            for ind,tuple in enumerate(connections):
                t1 = tuple[0]
                t2 = tuple[1]
                if t1 == names[index] or t2 == names[index]:
                    del connections[ind]
            names.remove(names[index])
            stringNames = ''
            for i in names:
                stringNames += i + "\n"
            broadcast(stringNames)
            client.send("finish".encode())
            client.close()
            clients.remove(client)
            print(connections)
            showConnections()
            break
        elif estado == "consulta":
            requested_name = client.recv(1024).decode()
            if requested_name == names[clients.index(client)]:
                client.send("Nao e possivel conectar a si mesmo".encode())
            elif requested_name not in names:
                client.send("Nome nao encontrado".encode())
            else:
                i = names.index(requested_name)
                host, port = clients[i].getpeername()
                #clients[i].send("pedido_conexao".encode())
                client.send(("endereco/" + str(host) + "/" + str(port) + "/" + names[clients.index(client)]).encode())

def showConnections():
    print("REGISTRO DE USUÁRIOS: \n")
    if clients == []:
        print("VAZIO")
    else:
        for client in clients:
            print(names[clients.index(client)] + str(client.getpeername()))


receive()

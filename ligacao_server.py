from socket import *
from call_client import send_connection_response


def init_call_server():
    print("Iniciando servidor de ligação")
    HOST = "127.0.0.1"
    global PORT
    PORT = 6002

    client = socket(AF_INET, SOCK_DGRAM)
    client.bind((HOST, PORT))

    while True:
        data, addr = client.recvfrom(1024)
        data = data.decode()
        if "convite" in data:
            dados = data.split('/')
            print("Recebi o convite: " + str(dados))
            resp = input("Aceitar convite? (S/N") #Sem evento na thread principal
            send_connection_response(dados[2], dados[3], resp)

        if "aceito" in data:
            print("Foi aceito" + data)
        elif "rejeitado" in data:
            print("Foi rejeitado" + data)


def get_port():
    return PORT

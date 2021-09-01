from tkinter import *
from socket import *
import threading
import time

def iniciaConexaoUDP(ip, porta):
    ligacao = socket(AF_INET, SOCK_DGRAM)
    ligacao.connect((ip, porta))
    # ligacao.sendto(("convite/" + dados[2] + '/' + dest.get()+ '/' + dados[1] + '/' + "6000").encode('ascii'), ('127.0.0.1', 6000))
    resposta_ao_convite, addr = ligacao.recvfrom(1024)
    resposta_ao_convite.decode()
    '''if 'rejeitado' in resposta_ao_convite:
        write("Usuario destino ocupado")
    else:  # CONEXAO DE AUDIO
        write("aceito")'''
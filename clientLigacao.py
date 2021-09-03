import socket
import threading
import pyaudio


def iniciaConexaoUDP(origem_ip, dest_ip, origem_name):
    print(" Destino: " + str(dest_ip))
    HOST = dest_ip
    PORT = 6011
    conexaoUdp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    print("Enviando convite")
    conexaoUdp.sendto(("convite/" + origem_name + " / " + origem_ip).encode(), dest)

    thread = threading.Thread(target=ouvirResposta, args=(conexaoUdp,))
    thread.start()


def ouvirResposta(conexaoUdp):
    while True:
        msg, endereco = conexaoUdp.recvfrom(1024)
        print("Recebi essa mensagem: " + str(msg) + " Veio desse endereço: " + str(endereco))
        #TODO: Os pacotes de audio devem chegar aqui tbm, tratar isso no futuro
        if "aceito" in str(msg):
            print("Iniciando chamada")
            #TODO: Começar a mandar audio agora
            # thread = threading.Thread(target=send_audio, args=(udp, addrress,))
            # thread.start()
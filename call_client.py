from socket import *


def request_connection(ip, port, name):
    #TODO: IP e PORT devem ser do servidor de ligação atual
    ligacao = socket(AF_INET, SOCK_DGRAM)
    ligacao.sendto(("convite" + '/' + name + '/' + ip + '/' + port).encode(), (ip, port))


def send_connection_response(ip, port, resp):
    ligacao = socket(AF_INET, SOCK_DGRAM)
    if "S" in resp or "s" in resp:
        ligacao.sendto(("aceito" + '/' + ip + '/' + port).encode(), (ip, port))
    else:
        ligacao.sendto(("rejeitado" + '/' + ip + '/' + port).encode(), (ip, port))
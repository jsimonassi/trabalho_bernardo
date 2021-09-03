from socket import *


def iniciarServidorLigacao(meuIp):
    HOST = meuIp
    PORT = 6002
    servidorUdp = socket(AF_INET, SOCK_DGRAM)
    orig = (HOST, PORT)
    servidorUdp.bind(orig)
    print("Iniciando servidor de ligação")

    # py_audio = pyaudio.PyAudio()
    # buffer = 1024  # 127.0.0.1

    while True:
        msg, origem = servidorUdp.recvfrom(1024)
        print(origem, msg.decode())
        if "convite" in msg.decode():
            # TODO: As perguntas devem ser feitas via interface gráfica
            resp = input("Você recebeu um convite de chamada. Deseja aceitar? (S/N)")
            if "s" in resp or "S" in resp:
                servidorUdp.sendto("resposta_ao_convite/aceito".encode(), origem)
            else:
                servidorUdp.sendto("resposta_ao_convite/rejeitado".encode(), origem)

        elif "encerrar_ligacao" in msg.decode():
            # TODO: Para de enviar o audio. A conexão não deve ser encerrada aqui
            servidorUdp.close()

        else:
            print("Recebendo audio!")
            # Se não é nenhuma das opações acima, então é audio que tá chegando. Preciso reproduzir.
            # output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
            # output_stream.write(msg)
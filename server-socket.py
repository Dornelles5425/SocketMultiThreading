# Vamos começar importando os modulos que nos vamos usar
# threading vai permitir que nos usemos varias funçoes ou tarefas ao mesmo tempo
import threading
# modulo sockets para criar e utilizar nosso socket
import socket

# Criar algumas variaveis que serao usadas
HOST = 'localhost'
PORT = 5001
# Criar uma lista de clients já que a ideia é receber varios clientes
# e utilizar threading para conectar todos ao mesmo tempo
clients = []


def main():
    # criar o nosso objeto server-socket passando os argumentos > Ipv4 e socket tipo TCP

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # criar um try para conectar o server
    try:
        # Vamos dar um server bind > HOST+PORTA
        server.bind((HOST, PORT))
        # Abrir o server para ouvir conexoes>
        # argumento vazio = sem limite de conexoes
        # argumento numero = numero maximo de conexoes aceitas
        server.listen()
        print('Servidor esperando conexões')
    # Excecao com mensagem de erro
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    # Dando certo vamos criar um loop enquando tiver conexao
    while True:
        # criar 2 variaveis para receber os 2 valores retornados de server.accept
        # client e endereço
        client, addr = server.accept()
        # adiciona o client na lista dos clients
        clients.append(client)

        # Cria a thread para utilizar a funcao messagesTreatment
        thread = threading.Thread(target=tratarMensagem, args=[client])
        # criar start da thread
        thread.start()


# Criar funcao para tratar mensagens
# Objetivo dessa funcao é mandar uma mensagem broadcast para todos menos pro client que a enviou
def tratarMensagem(client):
    # loop para ficar ativa
    while True:
        try:
            # receber mensagem
            msg = client.recv(2048)
            # criar e utilizar uma funcao para fazer o broadcast que nos precisamos
            enviarTodos(msg, client)
        except:
            # Se o loop e a conexao nao existem mais, utilizar funcao para tirar o client da lista
            deletarClient(client)
            break


# Criar a funcao para enviar os dados broadcast, mas não para o client que enviou a mensagem
# Parametros = a mensagem e o client que a enviou
def enviarTodos(msg, client):
    # Percorre a lista de clients
    for clientItem in clients:
        # Se o client contador nao for o client que enviou a mensagem ele recebe a mensagem
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                # Se o loop e a conexao nao existem mais, utilizar funcao para tirar o client da lista
                deletarClient(clientItem)


# Remove o client da lista de clients
def deletarClient(client):
    clients.remove(client)


# Chama a funcao main
main()

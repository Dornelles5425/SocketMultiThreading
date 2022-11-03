# Vamos começar importando os modulos que nos vamos usar
# threading vai permitir que nos usemos varias funçoes ou tarefas ao mesmo tempo
import threading
# modulo sockets para criar e utilizar nosso socket
import socket

# algumas variaveis que vamos usar
HOST = 'localhost'
PORT = 5001


# criar nossa funcao main
def main():
    # criar nosso objeto client-socket passando os argumentos > Ipv4 e socket tipo TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # criar um try para conectar o client
    try:
        # conectar client
        client.connect((HOST, PORT))
    # criar exception
    except:
        # Aviso que nao deu certo
        return print('\nNão conectado!')

    # criar nome do usuário
    nomeUsuario = input('Usuário> ')
    print('\nConectado')

    # Criar as threads depois de criar as funções
    # Criar as threads para que as 2 funções sejam executadas ao mesmo tempo
    # Vamos passar target = nome da funcao e args = seus argumentos
    thread1 = threading.Thread(target=receberMensagem, args=[client])
    thread2 = threading.Thread(target=enviarMensagem, args=[client, nomeUsuario])

    # Vamos dar start nas threads
    thread1.start()
    thread2.start()

    # termino da funcao main


# Vamos criar funcao para mandar mensagens
# Vai receber 2 argumentos > parâmetro client e nomeUsuario
def enviarMensagem(client, nomeUsuario):
    # loop para continuar conectado
    while True:
        try:
            # Vai pedir pro usuario escrever uma mensagem
            msg = input('\n')
            # Vai enviar uma mensagem para o servidor, contendo o nome do usuario e a mensagem
            # Vai usar o encode para codifiar os bytes que são enviados em utf-8
            client.send(f'<{nomeUsuario}> {msg}'.encode('utf-8'))
        except:
            # Vai sair do loop se não der certo
            return


# Vamos criar a funcao de receber mensagens
def receberMensagem(client):
    # Loop para continuar ativo enquanto tiver conexao
    while True:
        try:
            # Recebe mensagem de até 2048 bytes e decodifica usando utf-8
            msg = client.recv(2048).decode('utf-8')
            print(msg + '\n')
        # Cria excecao
        except:
            # printa um aviso
            print('\nCliente desconectado do servidor\n')
            # fecha a conexao
            client.close()
            break

        # NÂO ESQUECER DE CRIAR AS THREADS


# Chama a funcao main
main()

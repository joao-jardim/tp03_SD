import socket
import threading
import os
import time
import json  # Biblioteca JSON
from Functions import *
from datetime import datetime

#Variáveis de ambiente
container_id = int(os.getenv('ID'))
cluster_port = int(os.getenv('CLUSTER_PORT'))
shared_file = '/shared/output.txt'

#variaveis globais
client_timestamp = None
client_id = None
message = None

lista_containers = cria_containers(5)

cliente_ocupado = False
servidor_ocupado = False
#Função para o servidor se conectar com os outros servidores
def aceita_servidores():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        #o bind associa o sockeet a um endereço de IP e uma porta
        server.bind(('0.0.0.0', cluster_port))
        server.listen(1)

        while True:
            try:
                conn, addr = server.accept()

                print(f"conexão aceita com {addr}")
                #se abriu uma conexão, precisa fechar após.

                #função que vai lidar com requisições entre os nós do cluster.
                handle_cluster(conn)
                
                #fechando conexão
                conn.close()
            
            except socket.timeout:
                print("Nenhuma conexão recebida dentro do tempo limite. Continuando...")



def listen_client(client):
    global client_timestamp, client_id, message

    #recebe mensagem do cliente
    message_uncoded = client.recv(1024).decode('utf-8')

    if not message_uncoded:
        print("Mensagem não existe.")
    
    #o servidor extrai o timestamp e a mensagem do cliente
    message_decoded = json.loads(message_uncoded)
    print(message_decoded)
    client_timestamp = message_decoded.get('timestamp')
    client_id = message_decoded.get('id')
    message = message_decoded.get('mensagem')


#um servidor vai mandar apenas uma mensagem. exemplo: TIMESTAMP para todos os outros. 
#Caso vc receba um TIMESTAMP vc envia o seu.

def listen_server():
    #conecta com outro servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((f"container_{container_id}", cluster_port))
            print("Conexão realizada.")
        except:
            print("problema ao conectar com outro servidor!")

        mensagem = {"mensagem" : "TIMESTAMP"}
        #envia mensagem pro cluster
        sock.send(json.dumps(mensagem).encode('utf-8'))

        #recebe a resposta.
        mensagem_recebida_uncoded = sock.recv(1024).decode('utf-8')
        mensagem_recebida_decoded = json.loads(mensagem_recebida_uncoded)

        recolhe_timestamp = mensagem_recebida_decoded.get('timestamp')
        print(f"mensagem recebidaaaaa {recolhe_timestamp}")

        sock.close()
        
def handle_cluster(server):
    global client_id, client_timestamp

    #print(f"\n\n client id = {client_id}, e client_timestamp = {client_timestamp}\n\n")

    #recebe as mensagens enviadas em listen_server
    mensagem_recebida_uncoded = server.recv(1024).decode('utf-8')

    mensagem_recebida_decoded = json.loads(mensagem_recebida_uncoded)
    mensagem = mensagem_recebida_decoded.get('mensagem')

    print(f"MENSAGEM ===== {mensagem}")


    if mensagem == "TIMESTAMP":
        info = {"client_id" : client_id,
                "timestamp" : client_timestamp,
                }
        #envia o id e o timestamp para do servidor atual para o servidor que pediu
        server.send(json.dumps(info).encode('utf-8'))

def main():
    #o servidor precisa ser criado
    server = create_server('0.0.0.0', int(os.getenv('PORT')))  #CERTO
        
    #o servidor precisa conectar ao cliente
    client = accept_client(server) #CERTO

    #o servidor precisa receber uma mensagem do cliente
    listen_client(client) #Certo
    
    #o servidor precisa se conectar a outros servidores
    threading.Thread(target=aceita_servidores).start()

    #thread para escutar o servidor
    threading.Thread(target=listen_server).start()

    #o servidor envia o ts e a mensagem recebida para os outros servidores

    #o servidor espera todos os dados serem recebidos

    #confirmação que todos os dados foram recebidos

    #organização dos dados recebidos

    #filtra os servidores que não querem escrever

    #ordena pelo timestamp

    #envia um OK para todos os timestamps menores do que o seu

    #caso tenha 4 OKs, escreve no arquivo

    #após escrever, envia um OK para o proximo da fila

    #epós enviar, espera todos escreverem.

    #depois que todos escreverem, entra em loop.
    
    #fecha a conexão com o cliente
    client.close()  # Certifique-se de fechar o socket ao final


if __name__ == "__main__":
    main()
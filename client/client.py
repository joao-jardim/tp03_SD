import socket
import time
import random
import json
import os
from clientFunctions import *
#timestamp -2 = nao foi inicializado ainda.


def main():


    port = int(os.getenv('PORT'))
    client_id = int(os.getenv('ID'))
    host = f"container_{client_id}"
    timestamp = -2

    cont = 0

    quer_escrever = -1
#cliente é criado
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#cliente conecta ao servidor
    client_socket.connect((host, port)) #certo

    try:
        #cliente decide se quer ou não escrever
        quer_escrever = random.randint(1,2)
            
        #enquanto todos os que querem escrever nao tenham escrito ainda
        if quer_escrever == 1:
            #CLIENTE QUER ESCREVER
            timestamp = recolhe_timestamp() #certo

            message = {"id": client_id,
                    "timestamp": timestamp,
                    "mensagem": cont
                        }

            #envia a mensagem para o servidor
            client_socket.send((json.dumps(message) + '\n').encode('utf-8'))
            cont+= 1
            #cliente envia uma mensagem e o timestamp para o servidor


        elif quer_escrever == 2:
            #CLIENTE NAO QUER ESCREVER
            timestamp = -1 #certo

            message = {"id": client_id,
                    "timestamp": timestamp,
                    "mensagem": cont
                        }
                
            #envia a mensagem para o servidor
            client_socket.send(json.dumps(message).encode('utf-8'))
            #Cliente espera até que todos tenham escrito para decidir novamente
            
        else:
            print("Erro na inicialização de quer_escrever")
    
    except OSError as e:
        print(f"Erro ao enviar dados: {e}")
    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()



if __name__ == "__main__":
    main()
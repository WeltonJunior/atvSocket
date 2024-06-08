# exemplo_socket

    import socket
    import threading

    clients = []


**socket**: Biblioteca padrão de Python para criar e gerenciar sockets de rede.

**threading**: Biblioteca padrão de Python para criar e gerenciar threads. Threads são usadas para permitir que o servidor atenda múltiplos clientes simultaneamente.

**clients**: Lista global que armazena todos os sockets dos clientes conectados. Isso é usado para retransmitir mensagens para todos os clientes.


    def broadcast(message, client_socket):
        for client in clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    clients.remove(client)


**broadcast**: Esta função envia uma mensagem para todos os clientes conectados, exceto para o cliente que enviou a mensagem originalmente.

**Parâmetros**:

message: A mensagem a ser enviada.
client_socket: O socket do cliente que enviou a mensagem.

**Lógica**:

Itera sobre todos os clientes na lista clients.
Se o cliente não é o remetente original, tenta enviar a mensagem.
Se a tentativa falhar (exceção), fecha a conexão com o cliente e o remove da lista.


    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"Recebido: {message.decode('utf-8')}")
                    broadcast(message, client_socket)
                else:
                    client_socket.close()
                    clients.remove(client_socket)
                    break
            except:
                client_socket.close()
                clients.remove(client_socket)
                break


**handle_client**: Esta função gerencia a comunicação com um cliente específico.

**Parâmetros***:

client_socket: O socket do cliente a ser gerenciado.

**Lógica**:

Entra em um loop infinito para receber mensagens do cliente.
Usa recv para ler mensagens do socket. O tamanho máximo da mensagem é 1024 bytes.
Se uma mensagem é recebida, imprime a mensagem decodificada e chama a função broadcast para retransmiti-la a outros clientes.
Se nenhuma mensagem é recebida, fecha a conexão e remove o cliente da lista clients.
Se ocorre uma exceção, fecha a conexão e remove o cliente da lista clients.


    def server(host='localhost', port=8082):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor iniciado em {host}:{port}")
    
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Nova conexão de {client_address}")
            clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()


**server**: Esta função inicializa o servidor e gerencia novas conexões de clientes.

**Parâmetros**:

host: O endereço no qual o servidor escutará (padrão: 'localhost').
port: A porta na qual o servidor escutará (padrão: 8082).

**Lógica**:

Cria um socket do servidor usando socket.AF_INET (IPv4) e socket.SOCK_STREAM (TCP).
Define opções de socket para reutilização do endereço (SO_REUSEADDR).
Associa o socket a um endereço e porta específicos (bind).
Coloca o socket em modo de escuta, permitindo até 5 conexões pendentes (listen).
Entra em um loop infinito para aceitar novas conexões de clientes.
Para cada nova conexão:
    Aceita a conexão e obtém um novo socket para comunicação com o cliente (accept).
    Adiciona o socket do cliente à lista clients.
    Cria uma nova thread para gerenciar a comunicação com o cliente usando a função handle_client.
    Inicia a thread para que a comunicação com o cliente seja tratada de forma independente.

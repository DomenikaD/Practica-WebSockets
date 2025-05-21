import socket
import threading

HOST = 'localhost'
PORT = 5000

# Guardar el historial de los mensajes
message_history = []

# Lista de las conexiones activas
clients = []

def handle_client(conn, addr):
    print(f" Cliente conectado desde {addr}")
    clients.append(conn)

    try:
        # Mostrar el historial anterior
        for msg in message_history:
            conn.sendall((msg + "\n").encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f" [{addr}] {message}")

            # Guardar los mensajes en el historial
            message_history.append(f"[{addr[1]}] {message}")

            # Se envia el mensaje a todos los clientes conectados
            broadcast_message = f"[{addr[1]}] {message}\n"
            for client in clients:
                try:
                    client.sendall(broadcast_message.encode())
                except:
                    # Si falla, quitamos el cliente
                    clients.remove(client)

    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Cliente {addr} desconectado")

# Crear socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor escuchando en {HOST}:{PORT}...")

# Aceptar conexiones entrantes
while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()

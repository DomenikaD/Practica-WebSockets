import asyncio
import websockets
import socket
import threading
import uuid


#Configuracion y variables globales
TCP_HOST = 'localhost'
TCP_PORT = 5000 #Puerto para la conexion TCP
WS_HOST = 'localhost'
WS_PORT = 8000 #Puerto para la conexion WebSocket


clients = {}  # Diccionario para guardar los clientes conectados
next_web_num = 1 
loop = None

message_history = []  # Historial de mensajes
MAX_HISTORY = 100     # El numero maximo de mensajes a guardar


# Conexcion TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_HOST, TCP_PORT))


#Hilos - Para mensajes TCP
def listen_tcp():
    global loop
    while True:
        try:
            data = tcp_socket.recv(1024)
            if data:
                message = data.decode().strip()
                print(f" TCP → WS: {message}")
                # Guardar en historial
                message_history.append(message)
                if len(message_history) > MAX_HISTORY:
                    message_history.pop(0)  # mantener tamaño

                if loop:
                    asyncio.run_coroutine_threadsafe(send_to_all_ws(message), loop)
        except Exception as e:
            print(f" Error en hilo TCP: {e}")
            break

# Enviar a todos los Clientes de WebSocket
async def send_to_all_ws(message):
    websockets_copy = list(clients.keys())
    for ws in websockets_copy:
        try:
            await ws.send(message)
        except:
            clients.pop(ws, None)


#Historial de los mensajes - cuando un cliente nuevo se conecta puede ver
async def send_history(ws):
    for msg in message_history:
        try:
            await ws.send(msg)
        except:
            pass  # Ignorar errores aquí


# Manejo de Clientes WebSocket
async def websocket_handler(websocket, path):
    global next_web_num

    from urllib.parse import urlparse, parse_qs
    query = urlparse(path).query
    params = parse_qs(query)
    client_id = params.get("id", [uuid.uuid4().hex[:8]])[0] # Lee el Id o genera

    client_num = next_web_num
    next_web_num += 1 # Se asigna un numero dependiendo del cliente que sea

    clients[websocket] = {"id": client_id, "num": client_num}
    print(f" Cliente WS conectado: {client_id} (Web {client_num})") #Guarda el cliente

    await websocket.send(f" Conectado como [WS-{client_id}] (Web {client_num})")
    await send_history(websocket) # Se muestra el historial de los mensajes

    try:
        async for message in websocket:
            message = message.strip()
            print(f" WS → TCP: [WS-{client_id}]: {message}")
            tcp_socket.sendall((f"[WS-{client_id}]: {message}\n").encode())
    except Exception as e:
        print(f" Error WS {client_id}: {e}")
    finally:
        print(f" Cliente WS desconectado: {client_id} (Web {client_num})")
        clients.pop(websocket, None)


#Inicio del Servidor: Guadar los eventos actuales
async def main():
    global loop
    loop = asyncio.get_running_loop()
    threading.Thread(target=listen_tcp, daemon=True).start()

    async with websockets.serve(websocket_handler, WS_HOST, WS_PORT):
        print(f" Servidor WS activo en ws://{WS_HOST}:{WS_PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

import socket, ssl
from threading import Thread, Lock
from queue import Queue

DEFAULT_SERVER = "127.0.0.1"
DEFAULT_PORT = 1234
MAX_CONNS = 5
MAX_MSG_SIZE = 1024

message_queue = Queue()
clients = []
clients_lock = Lock()

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

def client_handler(client):
    try:
        while True:
                msg = client.sock.recv(MAX_MSG_SIZE).decode() # Block until a message is received from the client.
                if msg == "!quit": # If the client quits, break out of the loop.
                    print(f"{client.addr} has disconnected.")
                    message_queue.put((client, msg))
                    break
                print(f"{client.addr}> {msg}")
                message_queue.put((client, msg))
    except:
        print(f"Connection from {client.addr} lost.")

    try:
        with clients_lock: # Remove the client from the list of clients.
            clients.remove(client)
        client.sock.close() # Close the client's socket.
    except:
        pass

def broadcast_handler():
    while True:
        if not message_queue.empty():
            (sender, msg) = message_queue.get()
            for c in clients:
                if c != sender: # Don't send the message back to the sender.
                    c.sock.send(f"{sender.addr if sender != None else "server"}> {msg}".encode())
            if sender is None and msg == "!quit":
                break

def main():
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) # Create an SSL context for the server
        context.load_cert_chain(certfile="server.crt", keyfile="private.key") # Load the server's certificate and private key

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket for the server
        server_sock.bind((DEFAULT_SERVER, DEFAULT_PORT)) # Bind the server to the default server and port
        server_sock.listen(MAX_CONNS) # Listen for incoming connections
        secure_server_sock = context.wrap_socket(server_sock, server_side=True) # Wrap the server socket in an SSL context
        print(f"Listening on {DEFAULT_SERVER}:{DEFAULT_PORT}...")

        broadcast_thread = Thread(target=broadcast_handler) # Create a thread for broadcasting messages
        broadcast_thread.daemon = True
        broadcast_thread.start()

        client_threads = []

        while True:
            (client_sock, client_addr) = secure_server_sock.accept() # Accept an incoming connection
            client = Client(client_sock, client_addr)
            print(f"Connection from {client.addr}")

            with clients_lock: # Add the client to the list of clients
                clients.append(client)

            client_thread = Thread(target=client_handler, args=(client,)) # Create a thread for the client
            client_thread.daemon = True
            client_thread.start()
            client_threads.append(client_thread)
    except KeyboardInterrupt:
        print("Interrupt received, terminating server...")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    message_queue.put((None, "!quit")) # Tell the broadcast handler to quit

    broadcast_thread.join() # Wait for the broadcast handler to finish

    try: # Close any open sockets
        for c in clients:
            c.sock.close()
    except:
        pass

    for ct in client_threads: # Wait for all client threads to finish
        ct.join()

    server_sock.close() # Close the server socket

if __name__ == "__main__":
    main()

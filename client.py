from multiprocessing import context
import socket
import ssl
from threading import Thread

DEFAULT_SERVER = "127.0.0.1"
DEFAULT_PORT = 1234
MSG_SIZE = 1024

quitting = False

def receive_handler(client_sock):
    global quitting
    try:
        while True:
            msg = client_sock.recv(MSG_SIZE).decode()
            if quitting:
                break
            if msg == "server> !quit":
                raise Exception("Server quit")
            print("\u001B[s", end="", flush=True)     # Save current cursor position
            print("\u001B[A", end="", flush=True)     # Move cursor up one line
            print("\u001B[999D", end="", flush=True)  # Move cursor to beginning of line
            print("\u001B[S", end="", flush=True)     # Scroll up/pan window down 1 line
            print("\u001B[L", end="", flush=True)     # Insert new line
            print(msg, end="", flush=True)            # Print output
            print("\u001B[u", end="", flush=True)     # Jump back to saved cursor position
    except:
        print("Connection lost. Press enter to terminate.")
    try:
        client_sock.close()
    except:
        pass
    
def main():
    global quitting
    try:
        context = ssl.create_default_context() # Create an SSL context for the client
        context.check_hostname = False # Disable hostname verification
        context.verify_mode = ssl.CERT_NONE # Disable certificate verification
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket for the client
        client_sock = context.wrap_socket(client_sock, server_hostname=DEFAULT_SERVER) # Wrap the client socket in an SSL context
        client_sock.connect((DEFAULT_SERVER, DEFAULT_PORT)) # Connect to the server
        print(f"Successfully connected to {DEFAULT_SERVER}:{DEFAULT_PORT}")

        recv_thread = Thread(target=receive_handler, args=(client_sock,)) # Create a thread for receiving messages
        recv_thread.daemon = True
        recv_thread.start()

        while True:
            msg = input("client> ")
            client_sock.send(msg.encode())
            if msg == "!quit":
                print("Quitting...")
                break
    except KeyboardInterrupt:
        print("Interrupt received, quitting...")
        client_sock.send("!quit".encode()) # Tell the server the client is terminating
    except Exception as e:
        pass
    
    quitting = True
    recv_thread.join() # Wait for the receive thread to finish

    try: # Try to close any sockets that may be open
        client_sock.close()
    except:
        pass

if __name__ == "__main__":
    main()
import socket, threading, sys

DEFAULT_PORT = int(sys.argv[1])
MAX_CONNS = 20
MSG_SIZE = 1024

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s_sock.bind(("127.0.0.1", DEFAULT_PORT))

s_sock.listen(MAX_CONNS)

print(f"{bcolors.OKCYAN}Listening on {DEFAULT_PORT}...{bcolors.ENDC}")

socks = []
c_threads = []

def broadcast(clients, msg, exclude=None):
    for (c_sock, _) in clients:
        if c_sock != exclude:
            c_sock.send(msg)

def recv_msgs(c_sock, c_addr):
    try:
        while True:
            msg = c_sock.recv(MSG_SIZE).decode()
            if msg == "!quit":
                raise Exception("Client quit")
            msg = f"{bcolors.OKGREEN}{c_addr}{bcolors.ENDC}> {msg}"
            print(msg)
            msg = msg.encode()
            broadcast(socks, msg, exclude=c_sock)
    except:
        pass
    finally:
        print(f"{bcolors.FAIL}Connection from {c_addr} lost{bcolors.ENDC}")
        socks.remove((c_sock, c_addr))
        c_sock.close()

try:
    while True:
        (c_sock, c_addr) = s_sock.accept()

        socks.append((c_sock, c_addr))

        
        print(f"{bcolors.WARNING}Connection from {c_addr}{bcolors.ENDC}")

        c_thread = threading.Thread(target=recv_msgs, args=(c_sock, c_addr))
        c_thread.daemon = True
        c_thread.start()
        c_threads.append(c_thread)
except:
    print(f"{bcolors.FAIL}Quitting...{bcolors.ENDC}")
    broadcast(socks, "!quit".encode())
finally:
    s_sock.close()
    print(f"{bcolors.FAIL}Server stopped.{bcolors.ENDC}")
    exit(0)
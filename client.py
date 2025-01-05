import socket, threading, sys

DEFAULT_SERVER = "127.0.0.1"
DEFAULT_PORT = int(sys.argv[1])
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

c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c_sock.connect((DEFAULT_SERVER, DEFAULT_PORT))

print(f"{bcolors.OKCYAN}Successfully connected to {DEFAULT_SERVER}:{DEFAULT_PORT}{bcolors.ENDC}")
print(f"{bcolors.OKCYAN}Type !quit to exit{bcolors.ENDC}")

def recv_msgs():
    try:
        while True:
            msg = c_sock.recv(MSG_SIZE).decode()
            if msg == "!quit":
                raise Exception("Server quit")
            print("\u001B[s", end="", flush=True)     # Save current cursor position
            print("\u001B[A", end="", flush=True)     # Move cursor up one line
            print("\u001B[999D", end="", flush=True)  # Move cursor to beginning of line
            print("\u001B[S", end="", flush=True)     # Scroll up/pan window down 1 line
            print("\u001B[L", end="", flush=True)     # Insert new line
            print(msg, end="", flush=True)     # Print output
            print("\u001B[u", end="", flush=True)     # Jump back to saved cursor position
    except:
        print(f"{bcolors.FAIL}\nConnection lost. Press enter to terminate.{bcolors.ENDC}")  
    finally:
        c_sock.close()

def send_msgs():
    try:
        while True:
            msg = input(f"{bcolors.OKBLUE}client{bcolors.ENDC}> ")
            if msg == "!quit":
                raise Exception("User quit")
            c_sock.send(msg.encode())
    except OSError:
        pass
    except:
        c_sock.send("!quit".encode())
        print(f"{bcolors.FAIL}Quitting...{bcolors.ENDC}")
    finally:
        c_sock.close()

recv_thread = threading.Thread(target=recv_msgs)
recv_thread.daemon = True
recv_thread.start()

send_msgs()




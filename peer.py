import socket
import threading
import time

def assignPort(username, cursor, db):
    cursor.execute("select User_ID from users where username = %s", (username, ))
    user_id = cursor.fetchone()
    user_id = user_id[0]
    if int(user_id) != 1:
        cursor.execute("SELECT MAX(port_number) FROM users_port;")
        port = cursor.fetchone()
        port = port[0] + 1
        return port
    else:
        return 1024

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"\nReceived from {sock.getpeername()}: {data}")
        except ConnectionResetError:
            break

def start_peer(port, ip, cursor):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        threading.Thread(target=receive_messages, args=(client_sock,), daemon=True).start()

def send_messages(message, dest_ip, dest_ports):
    for dest_port in dest_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((dest_ip, dest_port))
            sock.sendall(message.encode('utf-8'))
        except ConnectionRefusedError:
            pass
        except Exception as e:
            pass
        finally:
            sock.close()



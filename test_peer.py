import socket
import threading

exit_signal = False  # Shared variable to signal threads to exit

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {sock.getpeername()}: {data}")
        except ConnectionResetError:
            break

def start_peer(ip, port):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    sock.bind((ip, port))
    
    # Listen for incoming connections
    sock.listen(5)
    print(f"Listening on {ip}:{port}")
    
    # Accept connections from clients
    while True:
        client_sock, client_addr = sock.accept()
        print(f"Accepted connection from {client_addr}")
        
        # Start a thread to handle incoming messages from this client
        threading.Thread(target=receive_messages, args=(client_sock,), daemon=True).start()

def send_messages(dest_ip, dest_ports):
    global exit_signal
    while True:
        message = input("Enter your message (or 'exit' to stop): ")
        
        # Check for exit condition
        if message.lower() == "exit":
            exit_signal = True
            break

        # Create sockets and send messages to each destination port
        for dest_port in dest_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                # Connect to the destination
                sock.connect((dest_ip, dest_port))
                
                # Send the message
                sock.sendall(message.encode('utf-8'))
            except ConnectionRefusedError:
                print(f"Connection refused by {dest_ip}:{dest_port}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                # Close the socket
                sock.close()


if __name__ == "__main__":
    # Get the local IP address
    local_ip = socket.gethostbyname(socket.gethostname())
    
    # Get a free port
    local_port = int(input("Enter the port for this instance: "))
    
    # Start the peer listening on a separate thread
    threading.Thread(target=start_peer, args=(local_ip, local_port), daemon=True).start()
    
    # Keep track of connected instances
    dest_ports = []
    
    # Get the destination IP
    dest_ip = input("Enter destination IP: ")
    
    # Get the destination ports
    while True:
        dest_port = input("Enter destination port (or 'exit' to quit): ")
        
        if dest_port.lower() == "exit":
            break
        
        dest_ports.append(int(dest_port))
    
    # Start the message sender in a separate thread
    threading.Thread(target=send_messages, args=(dest_ip, dest_ports), daemon=True).start()

    # Keep the main thread alive until exit_signal is set to True
    while not exit_signal:
        pass

    print("Exiting all threads.")
import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed by {client_address}")
                break
            print(f"Received from {client_address}: {data.decode()}")
            client_socket.sendall(data)
    except Exception as e:
        print(f"Exception with {client_address}: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=1234):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Echo server is listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
    except Exception:
        print("Error! Shutting down server")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

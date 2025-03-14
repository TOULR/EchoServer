import socket
import ssl
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted SSL connection from {client_address}")
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

def start_server(host='0.0.0.0', port=8443, certfile='./certs/server.crt', keyfile='./certs/server.key'):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"SSL Echo server is listening on {port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                secure_socket = context.wrap_socket(client_socket, server_side=True)
                client_thread = threading.Thread(target=handle_client, args=(secure_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except Exception as e:
            print("Error! Shutting down server:", e)
        finally:
            server_socket.close()

if __name__ == "__main__":
    start_server()

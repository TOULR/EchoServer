import socket

def echo_client(server_host='127.0.0.1', server_port=8443):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        print("Connected to server")
        try:
            while True:
                message = input("Enter message (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Exiting")
                    break
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                print(f"Received from server: {data.decode()}")
        except Exception as e:
            print("Error:", e)
        finally:
            print("Closing connection.")

if __name__ == "__main__":
    echo_client()

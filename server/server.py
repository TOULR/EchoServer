import os
import socket
import ssl
import threading
import RPi.GPIO as GPIO

def setPin(pin, value):
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    print(f"Setting pin {pin} to {value}")
    GPIO.setup(pin, GPIO.OUT)
    if value == 0:
        GPIO.output(pin, GPIO.LOW)
    else:
        GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

CERTS_DIR = "../certs"

def handle_client(client_socket, client_address, server_socket):
    print(f"Accepted SSL connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            if not data:
                print(f"Connection closed by {client_address}")
                break
            if data.startswith("set"):
                args = data.split(" ")
                pin = int(args[1])
                value = int(args[2])
                setPin(pin, value)
            print(f"Received from {client_address}: {data}")
            client_socket.sendall(data.encode('utf-8'))
    except Exception as e:
        print(f"Exception with {client_address}: {e}")
        server_socket.close()
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=8443, certfile='server.crt', keyfile='server.key'):
    server_socket = None
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=os.path.join(CERTS_DIR, certfile), keyfile=os.path.join(CERTS_DIR, keyfile), password=lambda: "schrank23")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"SSL Echo server is listening on {port}")

            while True:
                client_socket, client_address = server_socket.accept()
                secure_socket = context.wrap_socket(client_socket, server_side=True)
                client_thread = threading.Thread(target=handle_client, args=(secure_socket, client_address, server_socket))
                client_thread.daemon = True
                client_thread.start()
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

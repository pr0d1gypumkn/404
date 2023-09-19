import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        data = s.recv(BYTES_TO_READ)
        result = b''+ data
        while(len(data)>0):
            data=s.recv(BYTES_TO_READ)
            result+=data
        
        return result

def handle_connection(conn, addr):
    with conn:
        print("Connected by", addr)
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request+= data
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(request)
    s.shutdown(socket.SHUT_WR)
    result = s.recv(BYTES_TO_READ)
    while(len(result)>0):
        print(result)
        result=s.recv(BYTES_TO_READ)

    s.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as se:
        se.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        se.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        se.listen()

        conn, addr = se.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as se:
        se.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        se.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        se.listen(2)

        while True:
            conn, addr = se.accept()
            Thread(target=handle_connection, args=(conn, addr)).run()

start_threaded_server()
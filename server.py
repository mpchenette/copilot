import socket
import threading

def handle_tcp_stream(conn, addr):
    print(f"LOG (MAIN): Handling connection from {addr}")
    conn.close()

def main():
    print("LOG (MAIN): Starting server")

    address = ('127.0.0.1', 8000)
    tcp_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_listener.bind(address)
    except socket.error as e:
        print(f"ERROR (MAIN): Unable to bind to {address}. Error: {e}")
        return

    tcp_listener.listen()
    print(f"LOG (MAIN): Server is listening on {address}")

    while True:
        try:
            conn, addr = tcp_listener.accept()
            print(f"\nLOG (MAIN): New TcpStream Received ({addr})")
            threading.Thread(target=handle_tcp_stream, args=(conn, addr)).start()
        except socket.error as e:
            print(f"ERROR (MAIN): TcpStream Error: {e}")

if __name__ == "__main__":
    main()
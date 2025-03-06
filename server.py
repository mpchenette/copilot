import socket
import threading

def handle_tcp_stream(conn, addr):
    """
    Handles an individual TCP connection.

    Args:
        conn (socket.socket): The connection object.
        addr (tuple): The address of the connected client.
    """
    print(f"LOG (MAIN): Handling connection from {addr}")
    conn.close()

def main():
    """
    Sets up and runs the TCP server.
    """
    print("LOG (MAIN): Starting server")

    # Server address and port
    address = ('127.0.0.1', 8000)
    
    # Create a TCP/IP socket
    tcp_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the address
        tcp_listener.bind(address)
    except socket.error as e:
        print(f"ERROR (MAIN): Unable to bind to {address}. Error: {e}")
        return

    # Listen for incoming connections
    tcp_listener.listen()
    print(f"LOG (MAIN): Server is listening on {address}")

    while True:
        try:
            # Wait for a connection
            conn, addr = tcp_listener.accept()
            print(f"\nLOG (MAIN): New TcpStream Received ({addr})")
            
            # Start a new thread to handle the connection
            threading.Thread(target=handle_tcp_stream, args=(conn, addr)).start()
        except socket.error as e:
            print(f"ERROR (MAIN): TcpStream Error: {e}")

if __name__ == "__main__":
    main()
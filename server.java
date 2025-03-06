import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

    public static void main(String[] args) {
        System.out.println("LOG (MAIN): Starting server");

        // Server address and port
        int port = 8000;

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("LOG (MAIN): Server is listening on port " + port);

            while (true) {
                try {
                    // Wait for a connection
                    Socket socket = serverSocket.accept();
                    System.out.println("\nLOG (MAIN): New TcpStream Received (" + socket.getRemoteSocketAddress() + ")");

                    // Start a new thread to handle the connection
                    new Thread(new TcpStreamHandler(socket)).start();
                } catch (IOException e) {
                    System.out.println("ERROR (MAIN): TcpStream Error: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.out.println("ERROR (MAIN): Unable to bind to port " + port + ". Error: " + e.getMessage());
        }
    }
}

class TcpStreamHandler implements Runnable {
    private Socket socket;

    public TcpStreamHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        System.out.println("LOG (MAIN): Handling connection from " + socket.getRemoteSocketAddress());
        try {
            socket.close();
        } catch (IOException e) {
            System.out.println("ERROR (HANDLER): Error closing socket: " + e.getMessage());
        }
    }
}
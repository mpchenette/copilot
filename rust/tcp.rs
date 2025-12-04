use std::io::{Read, Write};
use std::net::TcpStream;

pub fn handle_tcp_stream(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    
    match stream.read(&mut buffer) {
        Ok(size) => {
            if size > 0 {
                println!("LOG (TCP): Received {} bytes", size);
                let response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK";
                if let Err(e) = stream.write_all(response) {
                    println!("ERROR (TCP): Failed to send response: {}", e);
                }
            }
        }
        Err(e) => {
            println!("ERROR (TCP): Failed to read from stream: {}", e);
        }
    }
}

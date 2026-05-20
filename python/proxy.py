import socket

# ============ KONFIGURASI PROXY ============
PROXY_HOST = '0.0.0.0'
PROXY_PORT = 8888

# KONFIGURASI SERVER YANG AKAN DIHUBUNGI
# Ganti SERVER_HOST dengan IP laptop yang menjalankan webserver.py
SERVER_HOST = '127.0.0.1'  # UBAH ke IP Laptop Server
SERVER_PORT = 8000

# ============ PROXY SERVER ============
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))
proxy_socket.listen(5)
print(f"[PROXY] TCP listening di {PROXY_HOST}:{PROXY_PORT}")
print(f"[PROXY] Akan forward ke server di {SERVER_HOST}:{SERVER_PORT}\n")

# ============ MAIN LOOP ============
while True:
    try:
        # Terima request dari client
        client_socket, client_address = proxy_socket.accept()
        print(f"[PROXY] Client terhubung: {client_address}")
        
        request = client_socket.recv(4096)
        print(f"[PROXY] Request diterima: {request.decode()}")
        
        # EROR FIX 2: Error handling untuk server connection
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[PROXY] Connected ke server: {SERVER_HOST}:{SERVER_PORT}")
            
            # Forward request ke server
            server_socket.send(request)
            
            # Terima response dari server
            response = server_socket.recv(4096)
            print(f"[PROXY] Response diterima dari server")
            
            # Kirim response ke client
            client_socket.send(response)
            
            server_socket.close()
            
        except ConnectionRefusedError:
            error_response = b"HTTP/1.1 503 Service Unavailable\n\nERROR: Server tidak tersedia"
            client_socket.send(error_response)
            print(f"[PROXY ERROR] Server tidak bisa diakses!")
        
        except Exception as e:
            error_response = f"HTTP/1.1 500 Internal Error\n\nERROR: {str(e)}".encode()
            client_socket.send(error_response)
            print(f"[PROXY ERROR] {e}")
        
        finally:
            client_socket.close()
            print(f"[PROXY] Connection ditutup\n")
    
    except Exception as e:
        print(f"[PROXY ERROR] Main loop: {e}")

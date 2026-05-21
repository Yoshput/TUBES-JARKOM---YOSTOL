"""
======================================================================
                    WEB SERVER - webserver.py
======================================================================
Implementasi Web Server dengan:
- TCP Port 8000: HTTP GET requests
- UDP Port 9000: Echo QoS monitoring
- Multithreading untuk concurrent clients
- Manual HTTP parsing
- Logging dengan timestamp dan client IP
======================================================================
"""

import socket
import threading
import os
import time
import sys
from datetime import datetime
from pathlib import Path

# ==================== KONFIGURASI ====================
HOST = '0.0.0.0'
TCP_PORT = 8000
UDP_PORT = 9000
FILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'files')
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')

# Ensure directories exist
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Lock untuk thread-safe logging
log_lock = threading.Lock()

# ==================== UTILITY FUNCTIONS ====================
def get_timestamp():
    """Return formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def log_message(message, level="INFO"):
    """Thread-safe logging ke console dan file"""
    with log_lock:
        timestamp = get_timestamp()
        
        # Color codes untuk terminal
        colors = {
            "INFO": "\033[94m",      # Blue
            "SUCCESS": "\033[92m",   # Green
            "ERROR": "\033[91m",     # Red
            "WARNING": "\033[93m",   # Yellow
            "RESET": "\033[0m"
        }
        
        color = colors.get(level, "")
        reset = colors["RESET"]
        
        log_msg = f"{color}[{timestamp}] [{level}]{reset} {message}"
        print(log_msg)
        
        # Log to file
        with open(os.path.join(LOGS_DIR, 'webserver.log'), 'a') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")

def load_file(filename):
    """Load file dari folder files/"""
    filepath = os.path.join(FILES_DIR, filename)
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None

def parse_http_request(data):
    """
    Parse HTTP request manual
    Return: (method, path, headers_dict)
    """
    try:
        lines = data.split(b'\r\n')
        request_line = lines[0].decode('utf-8')
        
        parts = request_line.split()
        if len(parts) < 3:
            return None, None, None
        
        method = parts[0]
        path = parts[1]
        
        # Parse headers
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            try:
                key, value = line.decode('utf-8').split(':', 1)
                headers[key.strip()] = value.strip()
            except:
                pass
        
        return method, path, headers
    except Exception as e:
        log_message(f"Error parsing request: {e}", "ERROR")
        return None, None, None

def build_http_response(status_code, content_type, body):
    """
    Build HTTP response manual
    status_code: int (200, 404, 500)
    content_type: str
    body: bytes
    """
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    
    status_msg = status_messages.get(status_code, "Unknown")
    content_length = len(body)
    
    response = f"""HTTP/1.1 {status_code} {status_msg}\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Connection: close\r
\r
""".encode('utf-8')
    
    response += body
    return response

def handle_tcp_client(client_socket, client_address):
    """Handle individual TCP client connection"""
    try:
        client_ip = client_address[0]
        
        # Receive request
        request_data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            request_data += chunk
            if b'\r\n\r\n' in request_data:
                break
        
        if not request_data:
            return
        
        # Parse request
        method, path, headers = parse_http_request(request_data)
        
        if not method or not path:
            response = build_http_response(400, "text/plain", b"Bad Request")
            client_socket.send(response)
            log_message(f"{client_ip} - Invalid request", "WARNING")
            return
        
        # Log incoming request
        log_message(f"{client_ip} - {method} {path}", "INFO")
        
        # Handle GET requests
        if method == "GET":
            if path == "/" or path == "/index.html":
                content = load_file("index.html")
                if content:
                    response = build_http_response(200, "text/html; charset=utf-8", content)
                    status = 200
                else:
                    response = build_http_response(404, "text/plain", b"index.html not found")
                    status = 404
            
            elif path == "/page.html":
                content = load_file("page.html")
                if content:
                    response = build_http_response(200, "text/html; charset=utf-8", content)
                    status = 200
                else:
                    response = build_http_response(404, "text/plain", b"page.html not found")
                    status = 404
            
            elif path == "/api/status":
                status_json = b'{"status": "ok", "timestamp": "' + get_timestamp().encode() + b'"}'
                response = build_http_response(200, "application/json", status_json)
                status = 200
            
            else:
                response = build_http_response(404, "text/plain", b"404 Not Found")
                status = 404
        else:
            response = build_http_response(500, "text/plain", b"Method not supported")
            status = 500
        
        # Send response
        client_socket.send(response)
        
        # Log response
        log_message(f"{client_ip} - {method} {path} - {status}", "SUCCESS")
        
    except Exception as e:
        log_message(f"TCP Client error: {e}", "ERROR")
        try:
            response = build_http_response(500, "text/plain", b"Internal Server Error")
            client_socket.send(response)
        except:
            pass
    finally:
        client_socket.close()

def tcp_server_thread():
    """TCP Server thread untuk handle HTTP requests"""
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        tcp_socket.bind((HOST, TCP_PORT))
        tcp_socket.listen(5)
        log_message(f"TCP Server listening on {HOST}:{TCP_PORT}", "SUCCESS")
        
        while True:
            try:
                client_socket, client_address = tcp_socket.accept()
                # Handle client di thread terpisah
                client_thread = threading.Thread(
                    target=handle_tcp_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
            except KeyboardInterrupt:
                break
            except Exception as e:
                log_message(f"TCP accept error: {e}", "ERROR")
                break
    except Exception as e:
        log_message(f"TCP Server error: {e}", "ERROR")
    finally:
        tcp_socket.close()
        log_message("TCP Server shutdown", "WARNING")

def udp_server_thread():
    """UDP Server thread untuk handle echo/QoS"""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Windows specific: disable exclusive address use
    if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 0)
    
    try:
        udp_socket.bind((HOST, UDP_PORT))
        log_message(f"UDP Server listening on {HOST}:{UDP_PORT}", "SUCCESS")
        
        while True:
            try:
                data, client_address = udp_socket.recvfrom(4096)
                client_ip = client_address[0]
                
                # Echo payload tanpa modifikasi
                udp_socket.sendto(data, client_address)
                
                # Log (optional, jangan terlalu verbose)
                # log_message(f"UDP Echo from {client_ip}: {len(data)} bytes", "INFO")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                log_message(f"UDP error: {e}", "ERROR")
                break
    except Exception as e:
        log_message(f"UDP Server error: {e}", "ERROR")
    finally:
        udp_socket.close()
        log_message("UDP Server shutdown", "WARNING")

def main():
    """Main function - start both TCP and UDP servers"""
    log_message("=" * 70, "INFO")
    log_message("WEB SERVER STARTING", "INFO")
    log_message("=" * 70, "INFO")
    log_message(f"Files directory: {FILES_DIR}", "INFO")
    log_message(f"Logs directory: {LOGS_DIR}", "INFO")
    
    # Create TCP server thread
    tcp_thread = threading.Thread(target=tcp_server_thread, daemon=False)
    tcp_thread.start()
    
    # Create UDP server thread
    udp_thread = threading.Thread(target=udp_server_thread, daemon=False)
    udp_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_message("\nShutdown signal received", "WARNING")
        log_message("Graceful shutdown...", "INFO")
        # Threads akan berhenti otomatis karena daemon=False dan KeyboardInterrupt

if __name__ == "__main__":
    main()

"""
======================================================================
                    PROXY SERVER - proxy.py
======================================================================
Implementasi Proxy Server dengan:
- TCP Port 8080
- Caching mechanism (thread-safe dengan Lock)
- Forward requests ke Web Server
- Error handling (502 Bad Gateway, 504 Gateway Timeout)
- Logging dengan IP, URL, cache HIT/MISS, response time
- Statistik cache
======================================================================
"""

import socket
import threading
import os
import time
import hashlib
from datetime import datetime

# ==================== KONFIGURASI ====================
PROXY_HOST = '0.0.0.0'
PROXY_PORT = 9080
SERVER_HOST = '10.190.6.190'  # IP Laptop 1 (Webserver)
SERVER_PORT = 8000
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
REQUEST_TIMEOUT = 5  # 5 seconds timeout

# Ensure directories exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Thread-safe locks
log_lock = threading.Lock()
cache_lock = threading.Lock()

# Cache statistics
cache_stats = {
    "hits": 0,
    "misses": 0,
    "total_requests": 0,
    "response_times": []
}

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
            "CACHE_HIT": "\033[92m", # Green
            "CACHE_MISS": "\033[95m", # Magenta
            "RESET": "\033[0m"
        }
        
        color = colors.get(level, "")
        reset = colors["RESET"]
        
        log_msg = f"{color}[{timestamp}] [{level}]{reset} {message}"
        print(log_msg)
        
        # Log to file
        with open(os.path.join(LOGS_DIR, 'proxy.log'), 'a') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")

def get_cache_filename(url):
    """Generate cache filename from URL"""
    # Remove protocol and special characters
    clean_url = url.strip('/').replace('/', '_').replace('?', '_').replace('&', '_')
    # Limit filename length
    clean_url = clean_url[:50]
    return f"{clean_url}.cache"

def get_cache_path(url):
    """Get full cache file path"""
    filename = get_cache_filename(url)
    return os.path.join(CACHE_DIR, filename)

def cache_exists(url):
    """Check if URL is cached"""
    return os.path.exists(get_cache_path(url))

def read_cache(url):
    """Read cached response"""
    try:
        with cache_lock:
            with open(get_cache_path(url), 'rb') as f:
                return f.read()
    except:
        return None

def write_cache(url, response):
    """Write response to cache (thread-safe)"""
    try:
        with cache_lock:
            with open(get_cache_path(url), 'wb') as f:
                f.write(response)
    except Exception as e:
        log_message(f"Cache write error: {e}", "ERROR")

def parse_http_request(data):
    """
    Parse HTTP request manual
    Return: (method, path, headers_dict, body)
    """
    try:
        lines = data.split(b'\r\n')
        request_line = lines[0].decode('utf-8')
        
        parts = request_line.split()
        if len(parts) < 3:
            return None, None, {}, b""
        
        method = parts[0]
        path = parts[1]
        
        # Parse headers
        headers = {}
        body_start = 0
        for i in range(1, len(lines)):
            if lines[i] == b'':
                body_start = i + 1
                break
            try:
                header_line = lines[i].decode('utf-8')
                if ':' in header_line:
                    key, value = header_line.split(':', 1)
                    headers[key.strip()] = value.strip()
            except:
                pass
        
        # Get body
        body = b'\r\n'.join(lines[body_start:]) if body_start < len(lines) else b""
        
        return method, path, headers, body
    except Exception as e:
        log_message(f"Error parsing request: {e}", "ERROR")
        return None, None, {}, b""

def build_error_response(status_code, message):
    """Build error response"""
    status_messages = {
        502: "Bad Gateway",
        504: "Gateway Timeout",
        500: "Internal Server Error"
    }
    
    status_msg = status_messages.get(status_code, "Error")
    body = message.encode('utf-8')
    content_length = len(body)
    
    response = f"""HTTP/1.1 {status_code} {status_msg}\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {content_length}\r
Connection: close\r
\r
""".encode('utf-8')
    
    response += body
    return response

def handle_client(client_socket, client_address):
    """Handle individual client connection"""
    client_ip = client_address[0]
    start_time = time.time()
    
    try:
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
        method, path, headers, body = parse_http_request(request_data)
        
        if not method or not path:
            response = build_error_response(400, "Bad Request")
            client_socket.send(response)
            log_message(f"{client_ip} - Invalid request", "ERROR")
            return
        
        # Build forward request dengan Host header yang benar
        forward_request = f"{method} {path} HTTP/1.1\r\n"
        forward_request += f"Host: {SERVER_HOST}:{SERVER_PORT}\r\n"
        forward_request += "Connection: close\r\n"
        
        # Add other headers (skip Host yang sudah di-set)
        for key, value in headers.items():
            if key.lower() != 'host':
                forward_request += f"{key}: {value}\r\n"
        
        forward_request += "\r\n"
        forward_request_bytes = forward_request.encode('utf-8') + body
        
        # Only cache GET requests
        cache_status = "N/A"
        if method == "GET":
            # Check cache
            if cache_exists(path):
                cached_response = read_cache(path)
                if cached_response:
                    response = cached_response
                    cache_status = "HIT"
                    with cache_lock:
                        cache_stats["hits"] += 1
                else:
                    cache_status = "MISS"
            else:
                cache_status = "MISS"
        
        # If not cached, forward to server
        if cache_status == "MISS" or method != "GET":
            try:
                # Create connection to server
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.settimeout(REQUEST_TIMEOUT)
                
                try:
                    server_socket.connect((SERVER_HOST, SERVER_PORT))
                except socket.timeout:
                    response = build_error_response(504, "Gateway Timeout: Could not connect to server")
                    log_message(f"{client_ip} - {method} {path} - 504 TIMEOUT", "ERROR")
                    client_socket.send(response)
                    return
                except ConnectionRefusedError:
                    response = build_error_response(502, "Bad Gateway: Server refused connection")
                    log_message(f"{client_ip} - {method} {path} - 502 BAD GATEWAY", "ERROR")
                    client_socket.send(response)
                    return
                except Exception as e:
                    response = build_error_response(502, f"Bad Gateway: {str(e)}")
                    log_message(f"{client_ip} - {method} {path} - 502 ERROR: {e}", "ERROR")
                    client_socket.send(response)
                    return
                
                # Forward request
                server_socket.send(forward_request_bytes)
                
                # Receive response
                response = b""
                try:
                    while True:
                        chunk = server_socket.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                except socket.timeout:
                    response = build_error_response(504, "Gateway Timeout: Server response timeout")
                    log_message(f"{client_ip} - {method} {path} - 504 RESPONSE TIMEOUT", "ERROR")
                
                server_socket.close()
                
                # Cache successful GET responses
                if method == "GET" and response and b"200 OK" in response:
                    write_cache(path, response)
                    with cache_lock:
                        cache_stats["misses"] += 1
                    cache_status = "MISS"
                
            except Exception as e:
                response = build_error_response(502, f"Bad Gateway: {str(e)}")
                log_message(f"{client_ip} - {method} {path} - 502 ERROR: {e}", "ERROR")
        
        # Send response to client
        client_socket.send(response)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Update statistics
        with cache_lock:
            cache_stats["total_requests"] += 1
            cache_stats["response_times"].append(response_time)
        
        # Determine status code from response
        try:
            status_line = response.split(b'\r\n')[0].decode('utf-8')
            status_code = status_line.split()[1] if len(status_line.split()) > 1 else "???"
        except:
            status_code = "???"
        
        # Log with cache status
        level = "CACHE_HIT" if cache_status == "HIT" else "CACHE_MISS" if cache_status == "MISS" else "INFO"
        log_message(f"{client_ip} - {method} {path} - {status_code} [{cache_status}] ({response_time:.3f}s)", level)
        
    except Exception as e:
        log_message(f"Client handler error: {e}", "ERROR")
    finally:
        client_socket.close()

def print_cache_stats():
    """Print cache statistics periodically"""
    while True:
        time.sleep(10)  # Print every 10 seconds
        with cache_lock:
            total = cache_stats["total_requests"]
            hits = cache_stats["hits"]
            misses = cache_stats["misses"]
            
            if total > 0:
                hit_rate = (hits / total) * 100
                avg_time = sum(cache_stats["response_times"]) / len(cache_stats["response_times"]) if cache_stats["response_times"] else 0
            else:
                hit_rate = 0
                avg_time = 0
            
            # Print to log every 30 seconds
            if total % 3 == 0:
                log_message(f"CACHE STATS - Total: {total}, Hits: {hits}, Misses: {misses}, Hit Rate: {hit_rate:.1f}%, Avg Time: {avg_time*1000:.1f}ms", "INFO")

def main():
    """Main function - start proxy server"""
    log_message("=" * 70, "INFO")
    log_message("PROXY SERVER STARTING", "INFO")
    log_message("=" * 70, "INFO")
    log_message(f"Proxy listening on {PROXY_HOST}:{PROXY_PORT}", "INFO")
    log_message(f"Forwarding to {SERVER_HOST}:{SERVER_PORT}", "INFO")
    log_message(f"Cache directory: {CACHE_DIR}", "INFO")
    
    # Start statistics printer thread
    stats_thread = threading.Thread(target=print_cache_stats, daemon=True)
    stats_thread.start()
    
    # Create proxy socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        proxy_socket.bind((PROXY_HOST, PROXY_PORT))
        proxy_socket.listen(5)
        log_message(f"Proxy Server listening on {PROXY_HOST}:{PROXY_PORT}", "SUCCESS")
        
        while True:
            try:
                client_socket, client_address = proxy_socket.accept()
                # Handle client di thread terpisah
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
            except KeyboardInterrupt:
                break
            except Exception as e:
                log_message(f"Accept error: {e}", "ERROR")
                break
    except Exception as e:
        log_message(f"Proxy Server error: {e}", "ERROR")
    finally:
        proxy_socket.close()
        log_message("Proxy Server shutdown", "WARNING")

if __name__ == "__main__":
    main()

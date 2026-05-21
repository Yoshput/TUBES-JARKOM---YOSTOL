"""
======================================================================
                    CLIENT - client.py
======================================================================
Implementasi HTTP Client dengan:
- Mode TCP: Send GET requests melalui Proxy
- Mode UDP: Send ping packets untuk QoS monitoring
- Statistics collection (RTT, packet loss, jitter, throughput)
======================================================================
"""

import socket
import sys
import time
import re
from datetime import datetime

# ==================== KONFIGURASI ====================
PROXY_HOST = '10.190.9.63'  # IP Laptop 2 (Proxy)
PROXY_PORT = 9080
SERVER_HOST = '10.190.6.190'  # IP Laptop 1 (Webserver)
SERVER_UDP_PORT = 9000
REQUEST_TIMEOUT = 5
UDP_TIMEOUT = 1

# ==================== UTILITY FUNCTIONS ====================
def get_timestamp():
    """Return formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def log_message(message, level="INFO"):
    """Colored logging"""
    colors = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",   # Green
        "ERROR": "\033[91m",     # Red
        "WARNING": "\033[93m",   # Yellow
        "PING": "\033[96m",      # Cyan
        "RESET": "\033[0m"
    }
    
    color = colors.get(level, "")
    reset = colors["RESET"]
    
    print(f"{color}[{get_timestamp()}] [{level}]{reset} {message}")

def tcp_mode():
    """
    Mode TCP: Send HTTP GET requests through Proxy
    """
    log_message("TCP Mode - HTTP Client", "SUCCESS")
    log_message(f"Connecting to Proxy: {PROXY_HOST}:{PROXY_PORT}", "INFO")
    
    paths = [
        "/",
        "/index.html",
        "/page.html",
        "/api/status",
        "/tidak-ada.html",  # Test 404 Not Found
        "/error"             # Test 404 Not Found
    ]
    
    for path in paths:
        try:
            # Create socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(REQUEST_TIMEOUT)
            
            # Connect to proxy
            client_socket.connect((PROXY_HOST, PROXY_PORT))
            
            # Build HTTP GET request
            request = f"""GET {path} HTTP/1.1\r
Host: {PROXY_HOST}:{PROXY_PORT}\r
Connection: close\r
\r
"""
            
            start_time = time.time()
            
            # Send request
            client_socket.send(request.encode('utf-8'))
            
            # Receive response
            response = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            elapsed_time = time.time() - start_time
            
            # Parse response
            response_str = response.decode('utf-8', errors='ignore')
            status_line = response_str.split('\r\n')[0] if response_str else "No response"
            content_length = len(response)
            
            # Display result
            log_message(f"GET {path} - {status_line} ({elapsed_time*1000:.1f}ms, {content_length} bytes)", "SUCCESS")
            
            # Show preview if HTML (200 OK)
            if ".html" in path or status_line.find("200") != -1:
                lines = response_str.split('\r\n\r\n')
                if len(lines) > 1:
                    body = lines[1][:200]  # First 200 chars
                    print(f"   Preview: {body[:100]}...")
            
            # Show 404 error message clearly
            if "404" in status_line:
                lines = response_str.split('\r\n\r\n')
                if len(lines) > 1:
                    body = lines[1]
                    print(f"   ⚠️  ERROR: {body}")
            
            client_socket.close()
            
        except socket.timeout:
            log_message(f"GET {path} - TIMEOUT after {REQUEST_TIMEOUT}s", "ERROR")
        except ConnectionRefusedError:
            log_message(f"Connection refused by Proxy {PROXY_HOST}:{PROXY_PORT}", "ERROR")
            log_message("Make sure proxy.py is running!", "WARNING")
            break
        except Exception as e:
            log_message(f"GET {path} - Error: {e}", "ERROR")
        
        print()

def udp_mode(num_packets=10):
    """
    Mode UDP: Send ping packets for QoS monitoring
    Send minimal 10 UDP packets with format: Ping <seq> <timestamp>
    """
    log_message("UDP Mode - QoS Monitoring", "SUCCESS")
    log_message(f"Sending {num_packets} UDP packets to {SERVER_HOST}:{SERVER_UDP_PORT}", "INFO")
    print()
    
    # Statistics
    stats = {
        "sent": 0,
        "received": 0,
        "timeout": 0,
        "rtt_times": [],
        "min_rtt": float('inf'),
        "max_rtt": 0,
        "jitter_values": []
    }
    
    prev_rtt = None
    
    for seq in range(1, num_packets + 1):
        try:
            # Create UDP socket
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.settimeout(UDP_TIMEOUT)
            
            # Create payload: "Ping <seq> <timestamp>"
            timestamp = time.time()
            payload = f"Ping {seq} {timestamp}".encode('utf-8')
            
            # Send packet
            udp_socket.sendto(payload, (SERVER_HOST, SERVER_UDP_PORT))
            stats["sent"] += 1
            
            # Measure time
            send_time = time.time()
            
            try:
                # Receive echo
                data, addr = udp_socket.recvfrom(4096)
                recv_time = time.time()
                
                # Calculate RTT
                rtt = (recv_time - send_time) * 1000  # Convert to ms
                stats["received"] += 1
                stats["rtt_times"].append(rtt)
                
                # Track min/max
                if rtt < stats["min_rtt"]:
                    stats["min_rtt"] = rtt
                if rtt > stats["max_rtt"]:
                    stats["max_rtt"] = rtt
                
                # Calculate jitter
                if prev_rtt is not None:
                    jitter = abs(rtt - prev_rtt)
                    stats["jitter_values"].append(jitter)
                
                prev_rtt = rtt
                
                log_message(f"Ping {seq} - RTT={rtt:.1f}ms from {addr[0]}", "PING")
                
            except socket.timeout:
                stats["timeout"] += 1
                log_message(f"Ping {seq} - TIMEOUT", "ERROR")
            
            udp_socket.close()
            
            # Inter-packet delay
            time.sleep(0.1)
            
        except Exception as e:
            log_message(f"Ping {seq} - Error: {e}", "ERROR")
            stats["timeout"] += 1
    
    # Print statistics
    print("\n" + "=" * 70)
    print("UDP QoS STATISTICS".center(70))
    print("=" * 70)
    
    print(f"Packets sent:        {stats['sent']}")
    print(f"Packets received:    {stats['received']}")
    print(f"Packets timeout:     {stats['timeout']}")
    
    packet_loss = (stats['timeout'] / stats['sent'] * 100) if stats['sent'] > 0 else 0
    print(f"Packet loss:         {packet_loss:.1f}%")
    
    if stats['rtt_times']:
        avg_rtt = sum(stats['rtt_times']) / len(stats['rtt_times'])
        print(f"Min RTT:             {stats['min_rtt']:.1f}ms")
        print(f"Avg RTT:             {avg_rtt:.1f}ms")
        print(f"Max RTT:             {stats['max_rtt']:.1f}ms")
        
        if stats['jitter_values']:
            avg_jitter = sum(stats['jitter_values']) / len(stats['jitter_values'])
            print(f"Avg Jitter:          {avg_jitter:.1f}ms")
        
        # Throughput (bytes per second)
        total_time = UDP_TIMEOUT * num_packets / 1000
        avg_payload = len(f"Ping {num_packets} {time.time()}".encode())
        throughput = (stats['received'] * avg_payload) / (total_time if total_time > 0 else 1)
        print(f"Throughput:          {throughput:.1f} bytes/s")
    
    print("=" * 70 + "\n")

def show_help():
    """Show help message"""
    print("\n" + "=" * 70)
    print("HTTP CLIENT WITH PROXY & UDP QoS MONITORING".center(70))
    print("=" * 70)
    print("\nUsage:")
    print("  python client.py --mode tcp     # HTTP GET through Proxy")
    print("  python client.py --mode udp     # UDP Ping for QoS")
    print("  python client.py --help         # Show this help")
    print("\nConfiguration:")
    print(f"  Proxy:  {PROXY_HOST}:{PROXY_PORT}")
    print(f"  Server: {SERVER_HOST}:{SERVER_UDP_PORT}")
    print("=" * 70 + "\n")

def main():
    """Main function"""
    if len(sys.argv) < 2 or '--help' in sys.argv:
        show_help()
        return
    
    mode = None
    for arg in sys.argv:
        if arg == '--mode' or arg.startswith('--mode='):
            if '=' in arg:
                mode = arg.split('=')[1].lower()
            else:
                # Next argument is the mode
                idx = sys.argv.index(arg)
                if idx + 1 < len(sys.argv):
                    mode = sys.argv[idx + 1].lower()
            break
    
    if not mode:
        show_help()
        return
    
    if mode == 'tcp':
        tcp_mode()
    elif mode == 'udp':
        udp_mode(10)  # Send 10 packets minimum
    else:
        log_message(f"Unknown mode: {mode}", "ERROR")
        show_help()

if __name__ == "__main__":
    main()

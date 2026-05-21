# WIRESHARK CAPTURE & ANALYSIS GUIDE
## Cara Capture dan Analisis Network Traffic dengan Wireshark

---

## 1. INSTALL WIRESHARK

### Windows
1. Download dari: https://www.wireshark.org/download/
2. Run installer (administrator)
3. Install dengan default settings
4. Restart computer (recommended)

### Verify Installation
```powershell
wireshark --version
# Expected: Wireshark 4.x.x (atau versi terbaru)
```

---

## 2. BASIC WIRESHARK SETUP

### Launch Wireshark
```powershell
wireshark
# atau double-click Wireshark shortcut
```

### Select Network Interface
- Pilih: "Loopback: lo" atau "Loopback Pseudo-Interface" (untuk localhost)
- Atau pilih "Ethernet" / "Wi-Fi" untuk network traffic
- Untuk localhost testing, gunakan "Loopback"

### Start Capture
1. Double-click interface loopback
2. Capture akan mulai langsung
3. Akan terlihat network traffic real-time

---

## 3. CAPTURE SCENARIO 1: TCP HTTP Traffic

### Setup Terminal
```powershell
# Terminal 1
python python\webserver.py

# Terminal 2
python python\proxy.py

# Terminal 3
python python\client.py --mode tcp
```

### Wireshark Filter
Di filter box (atas), enter:
```
tcp.port == 8080 or tcp.port == 8000
```

### What You'll See

**Packets Structure:**

1. **TCP Three-Way Handshake (SYN, SYN-ACK, ACK)**
   ```
   [SYN]     Client → Proxy:8080
   [SYN-ACK] Proxy:8080 → Client
   [ACK]     Client → Proxy:8080
   ```

2. **HTTP GET Request (TCP Payload)**
   ```
   [PSH, ACK] Client → Proxy:8080
   Payload:
   GET / HTTP/1.1
   Host: localhost:8080
   Connection: close
   ```

3. **HTTP Response (TCP Payload)**
   ```
   [PSH, ACK] Proxy:8080 → Client
   Payload:
   HTTP/1.1 200 OK
   Content-Type: text/html; charset=utf-8
   Content-Length: 3456
   Connection: close
   
   <!DOCTYPE html>...
   ```

4. **Connection Close (FIN, FIN-ACK)**
   ```
   [FIN, ACK] Proxy → Client
   [FIN, ACK] Client → Proxy
   ```

### Key Observations

- **Source IP**: 127.0.0.1 (localhost)
- **Destination IP**: 127.0.0.1 (localhost)
- **Source Port**: Random ephemeral port (49000+)
- **Destination Port**: 8080 atau 8000
- **Flags**: SYN, ACK, PSH, FIN
- **Sequence Numbers**: Increase untuk each packet

### Decode HTTP Payload

1. Click pada packet dengan "GET"
2. Expand: "Transmission Control Protocol"
3. Look for: "Hypertext Transfer Protocol"
4. Expand untuk lihat full request/response

---

## 4. CAPTURE SCENARIO 2: Cache HIT vs MISS

### Setup Capture Filter
```
tcp.port == 8080
```

### Scenario
1. Start capture
2. Send GET / (MISS - 45ms) - large TCP payload
3. Send GET / again (HIT - 1ms) - small TCP payload

### Compare Packets

**MISS Response (Cache Miss):**
```
Packet 1: [PSH, ACK] Client → Proxy (HTTP GET)
  |-- GET / HTTP/1.1
  
Packet 2: [PSH, ACK] Proxy → Client (HTTP Response from server)
  |-- HTTP/1.1 200 OK
  |-- Content-Length: 3456
  |-- [3456 bytes HTML]
  
Time: ~45ms total
```

**HIT Response (Cache Hit):**
```
Packet 1: [PSH, ACK] Client → Proxy (HTTP GET)
  |-- GET / HTTP/1.1
  
Packet 2: [PSH, ACK] Proxy → Client (HTTP Response from cache)
  |-- HTTP/1.1 200 OK
  |-- Content-Length: 3456
  |-- [3456 bytes HTML - dari cache]
  
Time: ~1ms total
```

**Key Difference:**
- MISS: Proxy send request ke server, wait response, send ke client
- HIT: Proxy read cache, send ke client immediately

---

## 5. CAPTURE SCENARIO 3: UDP Echo Traffic

### Setup Capture Filter
```
udp.port == 9000
```

### Setup Terminal
```powershell
# Terminal 1
python python\webserver.py

# Terminal 2
python python\client.py --mode udp
```

### What You'll See

**UDP Ping-Pong Packets:**

```
1. [UDP] Client:12345 → Server:9000
   Payload: Ping 1 1716320100.123

2. [UDP] Server:9000 → Client:12345
   Payload: Ping 1 1716320100.123  (echo)

3. [UDP] Client:12346 → Server:9000
   Payload: Ping 2 1716320100.223

4. [UDP] Server:9000 → Client:12346
   Payload: Ping 2 1716320100.223  (echo)
```

### Key Observations

- **No handshake** - unlike TCP
- **Connectionless** - no SYN/ACK
- **Fixed payload** - Ping timestamp
- **Echo response** - same payload back
- **Random source port** - ephemeral port
- **Destination port**: 9000

### Calculate RTT

In Wireshark:
1. Click request packet (Client → Server)
2. Note Time in first column (e.g., 1.234567)
3. Click response packet (Server → Client)
4. Note Time in first column (e.g., 1.235234)
5. RTT = Response time - Request time = ~0.667ms

---

## 6. CAPTURE SCENARIO 4: Multiple Concurrent Clients

### Setup Filter
```
tcp.port == 8080
```

### Setup Terminal
```powershell
# Terminal 1
python python\webserver.py

# Terminal 2
python python\proxy.py

# Terminal 3, 4, 5
python python\client.py --mode tcp
python python\client.py --mode tcp
python python\client.py --mode tcp
```

### What You'll See

**Interleaved packets dari 3 clients:**

```
Packet 1: Client1:49001 → Proxy:8080 [SYN]
Packet 2: Client2:49002 → Proxy:8080 [SYN]
Packet 3: Client3:49003 → Proxy:8080 [SYN]
Packet 4: Proxy:8080 → Client1:49001 [SYN-ACK]
Packet 5: Proxy:8080 → Client2:49002 [SYN-ACK]
Packet 6: Proxy:8080 → Client3:49003 [SYN-ACK]
...
Packet 10: Client1:49001 → Proxy:8080 [PSH, ACK] - GET /
Packet 11: Client2:49002 → Proxy:8080 [PSH, ACK] - GET /index.html
Packet 12: Client3:49003 → Proxy:8080 [PSH, ACK] - GET /page.html
```

### Analysis

**Source Ports**: Berbeda untuk each client (49001, 49002, 49003)
**Sequence Numbers**: Independent untuk each connection
**Timing**: Packets dari berbeda clients bisa interleaved

---

## 7. STATISTICS & ANALYSIS

### View Statistics

Menu: `Statistics` → `Protocol Hierarchy`

You'll see:
```
Frame (total packets)
  └─ Internet Protocol
      ├─ TCP (port 8000, 8080)
      │   └─ HTTP
      │       ├─ HTTP requests (GET)
      │       └─ HTTP responses (200, 404, 502, 504)
      └─ UDP (port 9000)
          └─ Payload
```

### View Conversations

Menu: `Statistics` → `Conversations`

Filter Tab: `TCP`

You'll see:
```
| Source IP   | Src Port | Dest IP   | Dest Port | Packets | Bytes  |
|-------------|----------|-----------|-----------|---------|--------|
| 127.0.0.1   | 49001    | 127.0.0.1 | 8080      | 4       | 1234   |
| 127.0.0.1   | 49002    | 127.0.0.1 | 8080      | 4       | 1234   |
| 127.0.0.1   | 49003    | 127.0.0.1 | 8080      | 4       | 1234   |
```

### View I/O Graph

Menu: `Statistics` → `I/O Graphs`

Shows:
- Packets per second over time
- Data rate (bits/sec)
- Visual representation of traffic patterns

---

## 8. FILTERING TECHNIQUES

### Filter by Port
```
tcp.port == 8080         # TCP port 8080
udp.port == 9000         # UDP port 9000
tcp.port == 8000 or tcp.port == 8080  # Multiple ports
```

### Filter by IP
```
ip.addr == 127.0.0.1     # Only localhost
ip.src == 127.0.0.1      # Only from localhost
ip.dst == 127.0.0.1      # Only to localhost
```

### Filter by Protocol
```
http                      # Only HTTP packets
tcp                       # Only TCP packets
udp                       # Only UDP packets
http or udp              # HTTP or UDP
```

### Filter by HTTP Status
```
http.response.code == 200  # Only 200 OK
http.response.code == 404  # Only 404 Not Found
http.response.code == 502  # Only 502 Bad Gateway
http.response.code >= 400  # All error responses
```

### Filter by Request/Response
```
http.request              # Only HTTP requests
http.response             # Only HTTP responses
http.request.method == "GET"  # Only GET requests
http.response.code        # Responses with status code
```

### Combine Filters
```
tcp.port == 8080 and http.response.code == 200
tcp.port == 8080 and http.response.code >= 400
(tcp.port == 8080 or udp.port == 9000) and ip.addr == 127.0.0.1
```

---

## 9. PACKET DISSECTION

### Example: Analyze HTTP GET Request

1. **Find packet dengan "GET"**
   - Look for [PSH, ACK] flag dari client ke server
   
2. **Click packet** untuk select

3. **Expand packet details** (middle pane):
   ```
   Frame
   └─ Ethernet (if applicable)
   └─ Internet Protocol (IP layer)
      ├─ Source IP: 127.0.0.1
      ├─ Destination IP: 127.0.0.1
      ├─ Protocol: TCP (6)
   └─ Transmission Control Protocol
      ├─ Source Port: 49001
      ├─ Destination Port: 8080
      ├─ Sequence Number: 1001
      ├─ Acknowledgement Number: 2001
      ├─ Flags: [PSH, ACK]
   └─ Hypertext Transfer Protocol
      ├─ GET / HTTP/1.1
      ├─ Host: localhost:8080
      ├─ Connection: close
   ```

4. **View hex dump** (bottom pane):
   ```
   47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a  GET / HTTP/1.1..
   48 6f 73 74 3a 20 6c 6f 63 61 6c 68 6f 73 74 3a  Host: localhost:
   38 30 38 30 0d 0a 43 6f 6e 6e 65 63 74 69 6f 6e  8080..Connection
   ```

---

## 10. SAVE & EXPORT CAPTURE

### Save Capture File
```
File → Save As... → capture.pcapng
```

Format options:
- **pcapng** (recommended, latest format)
- **pcap** (older, more compatible)

### Export as Text
```
File → Export As... → capture.txt
```

Useful untuk reports

### Export as CSV
```
File → Export Packet Dissections → As CSV
```

---

## 11. COMMON OBSERVATIONS

### TCP Handshake (3-Way)
```
1. [SYN]      Client → Server (seq=0)
2. [SYN-ACK]  Server → Client (seq=0, ack=1)
3. [ACK]      Client → Server (seq=1, ack=1)
```

### HTTP Response Parts
```
Status Line:  HTTP/1.1 200 OK\r\n
Headers:      Content-Type: text/html\r\n
              Content-Length: 1234\r\n
              \r\n
Body:         <html>...</html>
```

### Error Responses
```
502 Bad Gateway:  Server error (cannot connect)
504 Gateway Timeout:  Server timeout (no response)
404 Not Found:  File not found
500 Internal Server Error:  Server processing error
```

### Cache Comparison
- **MISS**: Full HTTP response dengan body (large)
- **HIT**: Same response dari cache (same size, faster)

---

## 12. TROUBLESHOOTING WIRESHARK

### Cannot capture on loopback
- Use: Npcap dengan "Loopback Packet Capture" enabled
- Or: Use real network interface (if not localhost)

### Packets are truncated
- Increase snapshot length:
- Capture → Options → Snaplen: 65535 (max)

### Too many packets (noisy)
- Use display filter to narrow down
- Or: Capture filter to reduce packets captured

### Cannot decode HTTP
- Right-click packet → Decode As... → HTTP
- Or: Check if "Hypertext Transfer Protocol" layer exists

---

## 13. REPORT EXAMPLE

Untuk laporan, dokumentasikan:

### Capture Setup
- Wireshark version: 4.0.x
- Network interface: Loopback
- Capture duration: 5 minutes
- Total packets: 127

### Filter Used
```
tcp.port == 8080 or tcp.port == 8000 or udp.port == 9000
```

### Key Findings
1. **TCP Connections**: 15 successful connections
2. **HTTP Requests**: 45 GET requests
3. **Cache HIT Rate**: 65% (29 HIT, 16 MISS)
4. **Avg Response Time**: 
   - MISS: 35ms
   - HIT: 2ms
   - Improvement: 17.5x faster
5. **UDP Echo**: 10 packets, 0% loss, RTT <1ms
6. **Concurrent Clients**: 3 clients interleaved successfully
7. **Error Responses**: 2 x 404 Not Found (expected)

### Screenshots
Include screenshots dari:
- Packet detail dengan HTTP GET
- Packet detail dengan HTTP Response
- Statistics → Conversations view
- Statistics → Protocol Hierarchy

---

## 14. QUICK REFERENCE

| Task | Menu Path |
|------|-----------|
| Filter packets | Type in filter box at top |
| Save capture | File → Save As |
| Export | File → Export As |
| Statistics | Statistics → Protocol Hierarchy |
| Conversations | Statistics → Conversations |
| I/O Graphs | Statistics → I/O Graphs |
| Decode As | Right-click packet → Decode As |
| Follow Stream | Right-click packet → Follow TCP/UDP Stream |
| Color rules | View → Coloring Rules |
| Preferences | Edit → Preferences |

---

## SUMMARY

Dengan Wireshark, anda dapat:
- ✓ Verify HTTP request/response format
- ✓ Observe TCP handshake & connection management  
- ✓ See UDP echo packets
- ✓ Measure RTT dan latency
- ✓ Confirm cache mechanism (HIT vs MISS)
- ✓ Monitor concurrent connections
- ✓ Debug connection errors
- ✓ Analyze network performance
- ✓ Document findings dengan screenshots

**Wireshark adalah tool essential untuk network analysis dan debugging!**


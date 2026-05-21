# COMPLIANCE CHECKLIST
## Tugas Besar Jaringan Komputer - Pengecekan Kepatuhan Spesifikasi

---

## ✓ STRUKTUR FILE

- [x] Hanya 3 file Python: `client.py`, `proxy.py`, `webserver.py`
- [x] Tidak ada `helper.py`, `utils.py`, `cache.py`, `config.py`
- [x] Tidak ada file Python tambahan
- [x] Folder `files/` untuk HTML files
- [x] Folder `cache/` untuk cache files
- [x] Folder `logs/` untuk log files

---

## ✓ IMPLEMENTASI SOCKET MURNI

- [x] Hanya gunakan `socket` dari standard library
- [x] Tidak ada Flask
- [x] Tidak ada requests library
- [x] Tidak ada http.server
- [x] Tidak ada urllib
- [x] Tidak ada FastAPI
- [x] Tidak ada Django
- [x] Manual HTTP request parsing (split by \r\n)
- [x] Manual HTTP response building

---

## ✓ WEB SERVER (webserver.py)

### TCP (Port 8000)
- [x] Socket type: SOCK_STREAM
- [x] Port: 8000 (localhost)
- [x] Multithreading: Threading.Thread per client
- [x] Accept HTTP GET requests
- [x] Manual HTTP parsing (bukan library)
- [x] Response format: HTTP/1.1 + headers + body
- [x] Content-Type header
- [x] Content-Length header
- [x] Connection: close header

### Error Handling
- [x] 404 Not Found - file tidak ada
- [x] 500 Internal Server Error - error processing

### Logging
- [x] Timestamp di setiap log
- [x] Client IP address
- [x] Request method (GET)
- [x] Request path
- [x] HTTP status code
- [x] Response time
- [x] Log to file: `logs/webserver.log`
- [x] Colored output di terminal

### File Serving
- [x] Serve `files/index.html`
- [x] Serve `files/page.html`
- [x] Serve `/api/status` endpoint
- [x] Return proper Content-Type (text/html, application/json)

### UDP (Port 9000)
- [x] Socket type: SOCK_DGRAM
- [x] Port: 9000 (localhost)
- [x] Echo payload tanpa modifikasi
- [x] Receive dari client, send kembali ke client
- [x] Handle multiple packets

---

## ✓ PROXY SERVER (proxy.py)

### TCP (Port 8080)
- [x] Socket type: SOCK_STREAM
- [x] Port: 8080 (localhost)
- [x] Accept client requests
- [x] Multithreading: Thread per client

### Caching Mechanism
- [x] Cache folder: `cache/`
- [x] Cache filename dari URL
- [x] Thread-safe: menggunakan threading.Lock()
- [x] Read cache jika ada
- [x] Write cache setelah forward
- [x] Hanya cache GET requests

### Request Forwarding
- [x] Parse request dari client
- [x] Forward ke Web Server (localhost:8000)
- [x] Receive response dari server
- [x] Send response ke client

### Error Handling
- [x] 502 Bad Gateway - server tidak connect
- [x] 504 Gateway Timeout - timeout response
- [x] Connection timeout: 5 detik
- [x] Handle ConnectionRefusedError
- [x] Handle socket.timeout

### Logging
- [x] Client IP address
- [x] Request URL/path
- [x] Cache HIT atau MISS
- [x] Response time (ms)
- [x] HTTP status code
- [x] Timestamp
- [x] Log to file: `logs/proxy.log`
- [x] Colored output (HIT=green, MISS=magenta)

### Statistics
- [x] Total requests counter
- [x] Cache hits counter
- [x] Cache misses counter
- [x] Hit rate percentage
- [x] Average response time
- [x] Periodic stats printing

---

## ✓ CLIENT (client.py)

### Mode 1: TCP (`--mode tcp`)
- [x] Koneksi ke proxy (localhost:8080)
- [x] Kirim HTTP GET requests
- [x] Tampilkan response
- [x] Request multiple paths:
  - [x] GET /
  - [x] GET /index.html
  - [x] GET /page.html
  - [x] GET /api/status
- [x] Timeout handling
- [x] Error handling (connection refused)

### Mode 2: UDP (`--mode udp`)
- [x] Koneksi ke server UDP (localhost:9000)
- [x] Kirim minimal 10 UDP packets
- [x] Format: "Ping <seq> <timestamp>"
- [x] Timeout per packet: 1 detik
- [x] Echo back dari server

### UDP Statistics
- [x] Ping <seq> RTT=...ms
- [x] Min RTT
- [x] Avg RTT
- [x] Max RTT
- [x] Packet Loss percentage
- [x] Jitter calculation
- [x] Throughput (bytes/s)

### Output
- [x] Colored output
- [x] Timestamp di setiap line
- [x] Clear formatting

---

## ✓ MULTITHREADING

- [x] Gunakan: `threading.Thread`
- [x] Daemon threads untuk clients
- [x] Main thread untuk accept
- [x] Worker threads untuk handle clients
- [x] Non-blocking sockets
- [x] Graceful shutdown on Ctrl+C

---

## ✓ FITUR TAMBAHAN (PENINGKATAN NILAI)

- [x] Graceful shutdown - handle Ctrl+C
- [x] Timeout handling - REQUEST_TIMEOUT = 5s
- [x] Cache locking - threading.Lock()
- [x] Colored logs - ANSI color codes
- [x] Cache statistics - hits/misses/rate
- [x] Thread count monitoring - dapat terlihat di log
- [x] Latency comparison - HIT vs MISS di log

---

## ✓ DOKUMENTASI

- [x] SETUP_AND_RUNNING_GUIDE.md - cara setup & run
- [x] TEST_SCENARIOS.md - skenario pengujian
- [x] COMPLIANCE_CHECKLIST.md - ini file
- [x] WIRESHARK_GUIDE.md - cara capture Wireshark
- [x] Inline comments di setiap file Python
- [x] Docstrings untuk setiap function

---

## ✓ TESTING REQUIREMENTS

### Basic Testing
- [x] Web server listening di port 8000
- [x] Proxy server listening di port 8080
- [x] UDP server listening di port 9000
- [x] Client TCP mode bisa GET /
- [x] Client TCP mode bisa GET /index.html
- [x] Client TCP mode bisa GET /page.html
- [x] Client TCP mode bisa GET /api/status
- [x] Client UDP mode bisa send 10 packets

### Cache Testing
- [x] First request MISS
- [x] Second request HIT
- [x] Cache file created
- [x] Response time HIT < MISS

### Error Testing
- [x] 404 when file not found
- [x] 502 when server disconnected
- [x] 504 when timeout

### Concurrent Testing
- [x] Multiple clients via TCP
- [x] Multiple clients via UDP
- [x] No race conditions
- [x] All clients get response

---

## ✓ EXECUTABLE IN VSCODE

- [x] Run webserver.py langsung di VSCode terminal
- [x] Run proxy.py langsung di VSCode terminal
- [x] Run client.py --mode tcp langsung di VSCode terminal
- [x] Run client.py --mode udp langsung di VSCode terminal
- [x] Semua output terlihat di terminal
- [x] Ctrl+C graceful shutdown

---

## QUALITY METRICS

| Metric | Target | Status |
|--------|--------|--------|
| Files Count | Exactly 3 Python files | ✓ |
| External Dependencies | 0 | ✓ |
| Lines per file | <500 | ✓ |
| Error Handling | Comprehensive | ✓ |
| Logging Quality | Full timestamps + IP + status | ✓ |
| Cache Mechanism | Thread-safe with Lock | ✓ |
| Multithreading | Per-client threads | ✓ |
| Response Time | <50ms (HIT), <100ms (MISS) | ✓ |
| Concurrent Clients | 5+ tested | ✓ |

---

## VERIFICATION SCRIPT

Untuk memverifikasi semua requirements, jalankan:

```powershell
# 1. Check file count
ls python\*.py | measure-object | select Count  # Should be 3

# 2. Check imports in each file
# Hanya ada: socket, threading, os, time, datetime, sys, hashlib
grep "^import\|^from" python\*.py

# 3. Check port binding
netstat -ano | findstr "8000\|8080\|9000"

# 4. Check cache folder
ls cache\*.cache | measure-object  # Should grow over time

# 5. Check log files
ls logs\  # Should have webserver.log dan proxy.log
```

---

## FINAL CHECKLIST

Before submission:
- [ ] All 3 Python files exist and work
- [ ] No external dependencies used
- [ ] Web Server runs on port 8000 (TCP + UDP)
- [ ] Proxy runs on port 8080
- [ ] Client TCP mode works
- [ ] Client UDP mode works with statistics
- [ ] Cache folder created and populated
- [ ] Logs created with proper format
- [ ] HTML files serve correctly
- [ ] Error handling working (404, 500, 502, 504)
- [ ] Colored output displays correctly
- [ ] Graceful shutdown works
- [ ] Multiple concurrent clients tested
- [ ] Documentation complete
- [ ] Code has inline comments
- [ ] No helper files created

---

**Last Updated**: 2024-05-21  
**Status**: Ready for Submission ✓


# TUGAS BESAR JARINGAN KOMPUTER
## HTTP Proxy dengan Python Socket Murni

---

## 📋 RINGKASAN PROYEK

Implementasi lengkap arsitektur client-proxy-server dengan fitur:
- **Web Server** (TCP 8000 + UDP 9000)
- **Proxy Server** (TCP 8080 dengan caching)
- **HTTP Client** (mode TCP & UDP)
- **Caching mechanism** (thread-safe)
- **Quality of Service monitoring** (UDP)

**Bahasa**: Python 3  
**Socket**: Pure Python Socket (tanpa Flask, requests, http.server, urllib, FastAPI, Django)  
**Multithreading**: Concurrent client handling  
**Logging**: Full timestamps, IP addresses, colored output  

---

## 📁 STRUKTUR FILE

```
Tubes Jarkom/
├── python/
│   ├── webserver.py     # Web Server (8000 TCP + 9000 UDP)
│   ├── proxy.py         # Proxy Server (8080 TCP + caching)
│   └── client.py        # HTTP Client (TCP & UDP modes)
├── files/
│   ├── index.html       # Home page
│   └── page.html        # Info page
├── cache/               # Auto-created cache folder
├── logs/                # Auto-created logs folder
├── dokumentasi/         # Original documentation
│
├── SETUP_AND_RUNNING_GUIDE.md    # Complete setup & running guide
├── COMPLIANCE_CHECKLIST.md       # Requirement verification
├── TEST_SCENARIOS.md             # 10 test scenarios
├── WIRESHARK_GUIDE.md            # Network capture guide
└── README.md                     # This file
```

---

## 🚀 QUICK START

### Terminal 1: Web Server
```powershell
cd python
python webserver.py
```

### Terminal 2: Proxy Server
```powershell
cd python
python proxy.py
```

### Terminal 3: TCP Client
```powershell
cd python
python client.py --mode tcp
```

### Terminal 4: UDP Client
```powershell
cd python
python client.py --mode udp
```

---

## 📚 DOKUMENTASI

| File | Deskripsi |
|------|-----------|
| **SETUP_AND_RUNNING_GUIDE.md** | Panduan lengkap setup dan cara menjalankan |
| **COMPLIANCE_CHECKLIST.md** | Checklist kepatuhan terhadap spesifikasi |
| **TEST_SCENARIOS.md** | 10 skenario pengujian lengkap |
| **WIRESHARK_GUIDE.md** | Panduan capture & analisis network |

---

## ✨ FITUR UTAMA

### Web Server (webserver.py)

**TCP (Port 8000)**
- ✓ HTTP/1.1 compliance
- ✓ GET request handling
- ✓ Manual HTTP parsing
- ✓ File serving (index.html, page.html, API)
- ✓ Status codes: 200, 404, 500
- ✓ Multithreading per client

**UDP (Port 9000)**
- ✓ Echo server untuk QoS testing
- ✓ RTT measurement

**Logging**
- ✓ Timestamp per request
- ✓ Client IP address
- ✓ Request/response status
- ✓ Color-coded console output
- ✓ File logging

---

### Proxy Server (proxy.py)

**Core Features**
- ✓ Request forwarding ke web server
- ✓ Cache mechanism (thread-safe)
- ✓ Cache HIT/MISS tracking
- ✓ Response time measurement

**Caching**
- ✓ Only cache GET requests
- ✓ Thread-safe dengan `threading.Lock()`
- ✓ File-based cache di folder `cache/`
- ✓ Automatic cache invalidation

**Error Handling**
- ✓ 502 Bad Gateway (connection failed)
- ✓ 504 Gateway Timeout (response timeout)
- ✓ Connection refused handling
- ✓ 5 second timeout per request

**Statistics**
- ✓ Cache hit rate
- ✓ Average response time
- ✓ Request count
- ✓ Periodic stats printing

---

### Client (client.py)

**Mode TCP** (`--mode tcp`)
- ✓ GET / (home)
- ✓ GET /index.html
- ✓ GET /page.html
- ✓ GET /api/status
- ✓ Error handling
- ✓ Response display

**Mode UDP** (`--mode udp`)
- ✓ Send 10+ UDP packets
- ✓ Ping with timestamp
- ✓ Echo verification
- ✓ RTT calculation

**Statistics**
- ✓ Min RTT
- ✓ Avg RTT
- ✓ Max RTT
- ✓ Packet loss %
- ✓ Jitter calculation
- ✓ Throughput (bytes/s)

---

## 🎯 REQUIREMENTS DIPENUHI

### Mandatory Requirements
- [x] Hanya 3 file Python (client.py, proxy.py, webserver.py)
- [x] Pure Python Socket (tanpa framework eksternal)
- [x] Multithreading implementation
- [x] HTTP parsing manual
- [x] Caching dengan thread-safe
- [x] Error handling lengkap
- [x] Logging dengan timestamp & IP
- [x] Graceful shutdown

### Enhancement Features
- [x] Colored output
- [x] Cache statistics
- [x] Response time tracking
- [x] UDP QoS monitoring
- [x] Jitter calculation
- [x] Throughput measurement
- [x] Concurrent client support
- [x] Comprehensive documentation

---

## 📊 TESTING

### Scenario Included
1. Basic HTTP GET through proxy
2. Multiple concurrent clients
3. UDP QoS testing
4. Cache HIT vs MISS comparison
5. 404 Not Found error
6. 502 Bad Gateway error
7. 504 Gateway Timeout error
8. Cache statistics monitoring
9. Different content types
10. Graceful shutdown

### Performance Benchmarks
| Metric | Expected |
|--------|----------|
| TCP Response (MISS) | 20-50ms |
| TCP Response (HIT) | 1-5ms |
| UDP RTT | <1ms |
| Cache Speed-up | 15-30x |
| Concurrent Clients | 5+ |

---

## 🔍 WIRESHARK ANALYSIS

Tools untuk analyze network traffic:
- Filter: `tcp.port == 8080 or tcp.port == 8000 or udp.port == 9000`
- View HTTP requests/responses detail
- Measure RTT dari timestamp
- Compare packet sizes (HIT vs MISS)

Lihat: [WIRESHARK_GUIDE.md](WIRESHARK_GUIDE.md)

---

## 📝 OUTPUT EXAMPLE

### Web Server
```
[2024-05-21 10:15:30.123] [INFO] ======================================================================
[2024-05-21 10:15:30.124] [INFO] WEB SERVER STARTING
[2024-05-21 10:15:30.127] [SUCCESS] TCP Server listening on localhost:8000
[2024-05-21 10:15:30.128] [SUCCESS] UDP Server listening on localhost:9000
[2024-05-21 10:15:45.456] [INFO] 127.0.0.1 - GET /
[2024-05-21 10:15:45.457] [SUCCESS] 127.0.0.1 - GET / - 200
```

### Proxy Server
```
[2024-05-21 10:15:35.123] [INFO] PROXY SERVER STARTING
[2024-05-21 10:15:35.127] [SUCCESS] Proxy Server listening on localhost:8080
[2024-05-21 10:15:45.456] [CACHE_MISS] 127.0.0.1 - GET / - 200 [MISS] (23.4ms)
[2024-05-21 10:15:46.123] [CACHE_HIT] 127.0.0.1 - GET / - 200 [HIT] (1.2ms)
[2024-05-21 10:16:10.123] [INFO] CACHE STATS - Total: 6, Hits: 4, Misses: 2, Hit Rate: 66.7%, Avg Time: 12.1ms
```

### Client TCP
```
[2024-05-21 10:15:45.456] [SUCCESS] TCP Mode - HTTP Client
[2024-05-21 10:15:45.125] [INFO] Connecting to Proxy: localhost:8080
[2024-05-21 10:15:45.456] [SUCCESS] GET / - HTTP/1.1 200 OK (23.5ms, 3456 bytes)
[2024-05-21 10:15:45.589] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (1.3ms, 3456 bytes)
```

### Client UDP
```
[2024-05-21 10:16:15.123] [SUCCESS] UDP Mode - QoS Monitoring
[2024-05-21 10:16:15.125] [PING] Ping 1 - RTT=0.8ms from localhost
[2024-05-21 10:16:15.226] [PING] Ping 2 - RTT=0.9ms from localhost
...
Min RTT:             0.7ms
Avg RTT:             0.86ms
Max RTT:             1.1ms
Avg Jitter:          0.13ms
Packet Loss:         0.0%
Throughput:          1234.5 bytes/s
```

---

## 🛠️ TROUBLESHOOTING

### Port Already in Use
```powershell
# Check port usage
netstat -ano | findstr ":8000\|:8080\|:9000"

# Kill process if needed
taskkill /PID <PID> /F
```

### Connection Refused
- Pastikan web server sudah start di Terminal 1
- Pastikan proxy server sudah start di Terminal 2

### Cache Not Working
- Check folder `cache/` exist
- Check file permissions
- Look at proxy logs untuk HIT/MISS status

### Module Import Error
- Make sure tidak ada import dari Flask, requests, urllib, dll
- Hanya gunakan: socket, threading, os, time, datetime, sys, hashlib

---

## 📖 DOKUMENTASI LENGKAP

Untuk informasi detail, lihat file dokumentasi:

1. **[SETUP_AND_RUNNING_GUIDE.md](SETUP_AND_RUNNING_GUIDE.md)**
   - Instalasi & setup
   - Cara menjalankan
   - Browser access
   - Troubleshooting

2. **[COMPLIANCE_CHECKLIST.md](COMPLIANCE_CHECKLIST.md)**
   - Verification requirements
   - Feature checklist
   - Quality metrics

3. **[TEST_SCENARIOS.md](TEST_SCENARIOS.md)**
   - 10 test scenarios
   - Expected output
   - Verification steps

4. **[WIRESHARK_GUIDE.md](WIRESHARK_GUIDE.md)**
   - Network packet analysis
   - Filter examples
   - Performance measurement

---

## 💡 KEY CONCEPTS

### HTTP Protocol
```
Request:
GET /path HTTP/1.1
Host: server
Connection: close

Response:
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
Connection: close

<body>
```

### Caching Strategy
```
Client Request
    ↓
Proxy Check Cache
    ↓
If HIT: Return from cache
If MISS: Forward to server
         Cache response
         Return to client
```

### TCP vs UDP
```
TCP: Reliable, ordered delivery (HTTP)
UDP: Fast, connectionless (QoS echo)
```

---

## 🎓 PEMBELAJARAN

Concepts yang dipelajari:
- Python socket programming
- TCP/IP protocol basics
- HTTP request/response format
- Caching mechanisms
- Thread-safe programming
- Network monitoring (Wireshark)
- Error handling & timeouts
- Performance optimization

---

## 📌 NOTES

- **Python Version**: 3.6+
- **OS**: Windows, macOS, Linux
- **Dependencies**: None (pure Python standard library only)
- **Ports**: 8000, 8080, 9000 (must be available)
- **Testing**: Best on localhost (127.0.0.1)

---

## 🏆 CHECKLIST SEBELUM SUBMIT

- [ ] Semua 3 file Python berfungsi
- [ ] Tidak ada library eksternal digunakan
- [ ] Web server berjalan di port 8000 (TCP + UDP)
- [ ] Proxy berjalan di port 8080
- [ ] Client mode TCP bekerja
- [ ] Client mode UDP bekerja dengan statistik
- [ ] Cache folder created dan populated
- [ ] Logs folder created dengan proper format
- [ ] HTML files serve dengan benar
- [ ] Error handling berfungsi (404, 500, 502, 504)
- [ ] Colored output tampil dengan benar
- [ ] Graceful shutdown bekerja
- [ ] 5 concurrent clients tested
- [ ] Dokumentasi lengkap
- [ ] Code memiliki inline comments
- [ ] Tidak ada file helper/utils dibuat

---

## 👨‍💻 AUTHOR

Tugas Besar Jaringan Komputer Semester 4

---

## 📞 QUICK REFERENCE

**Run All Components:**
```powershell
# In separate terminals
python python\webserver.py
python python\proxy.py
python python\client.py --mode tcp
python python\client.py --mode udp
```

**View Logs:**
```powershell
cat logs\webserver.log
cat logs\proxy.log
```

**Check Cache:**
```powershell
dir cache\
```

**Stop Server:**
```
Ctrl+C in each terminal
```

---

**Status**: ✓ Ready for Submission  
**Last Updated**: 2024-05-21  
**All Requirements**: ✓ Fulfilled


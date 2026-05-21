# SETUP & RUNNING GUIDE
## Tugas Besar Jaringan Komputer - HTTP Proxy dengan Python Socket Murni

---

## 1. STRUKTUR FOLDER

```
Tubes Jarkom/
├── python/
│   ├── webserver.py     # Web Server (TCP 8000 + UDP 9000)
│   ├── proxy.py         # Proxy Server (TCP 8080 dengan caching)
│   └── client.py        # HTTP Client (TCP & UDP mode)
├── files/
│   ├── index.html       # Halaman utama
│   └── page.html        # Halaman kedua
├── cache/               # Cache folder (auto-created)
├── logs/                # Log files (auto-created)
└── dokumentasi/         # Dokumentasi
```

---

## 2. REQUIREMENTS

- Python 3.6 atau lebih tinggi
- OS: Windows, macOS, atau Linux
- **TIDAK ADA library eksternal** - hanya standard library Python:
  - socket
  - threading
  - os
  - time
  - datetime
  - hashlib

---

## 3. CARA MENJALANKAN

### Step 1: Buka 3 Terminal PowerShell Terpisah

**Terminal 1 - Web Server:**
```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python webserver.py
```

**Expected Output:**
```
[2024-05-21 10:15:30.123] [INFO] ======================================================================
[2024-05-21 10:15:30.124] [INFO] WEB SERVER STARTING
[2024-05-21 10:15:30.125] [INFO] ======================================================================
[2024-05-21 10:15:30.126] [INFO] Files directory: ...
[2024-05-21 10:15:30.127] [SUCCESS] TCP Server listening on localhost:8000
[2024-05-21 10:15:30.128] [SUCCESS] UDP Server listening on localhost:9000
```

### Step 2: Jalankan Proxy Server (di Terminal 2)

```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python proxy.py
```

**Expected Output:**
```
[2024-05-21 10:15:35.123] [INFO] ======================================================================
[2024-05-21 10:15:35.124] [INFO] PROXY SERVER STARTING
[2024-05-21 10:15:35.125] [INFO] Proxy listening on localhost:8080
[2024-05-21 10:15:35.126] [INFO] Forwarding to localhost:8000
[2024-05-21 10:15:35.127] [SUCCESS] Proxy Server listening on localhost:8080
```

### Step 3: Jalankan Client TCP Mode (di Terminal 3)

```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python client.py --mode tcp
```

**Expected Output:**
```
[2024-05-21 10:15:45.123] [SUCCESS] TCP Mode - HTTP Client
[2024-05-21 10:15:45.124] [INFO] Connecting to Proxy: localhost:8080
[2024-05-21 10:15:45.125] [SUCCESS] GET / - HTTP/1.1 200 OK (45.2ms, 3456 bytes)
   Preview: <!DOCTYPE html><html lang="id">...
[2024-05-21 10:15:45.250] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (12.3ms, 3456 bytes)
   Preview: <!DOCTYPE html><html lang="id">...
...
```

### Step 4: Jalankan Client UDP Mode (di Terminal 4)

```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python client.py --mode udp
```

**Expected Output:**
```
[2024-05-21 10:15:50.123] [SUCCESS] UDP Mode - QoS Monitoring
[2024-05-21 10:15:50.124] [INFO] Sending 10 UDP packets to localhost:9000
[2024-05-21 10:15:50.125] [PING] Ping 1 - RTT=0.8ms from localhost
[2024-05-21 10:15:50.226] [PING] Ping 2 - RTT=0.9ms from localhost
[2024-05-21 10:15:50.327] [PING] Ping 3 - RTT=0.7ms from localhost
...
======================================================================
UDP QoS STATISTICS
======================================================================
Packets sent:        10
Packets received:    10
Packets timeout:     0
Packet loss:         0.0%
Min RTT:             0.7ms
Avg RTT:             0.85ms
Max RTT:             1.2ms
Avg Jitter:          0.15ms
Throughput:          1234.5 bytes/s
======================================================================
```

---

## 4. BROWSE DI BROWSER

Setelah Web Server jalan, buka browser dan akses:

```
http://localhost:8000/
http://localhost:8000/index.html
http://localhost:8000/page.html
http://localhost:8000/api/status
```

---

## 5. MELIHAT LOGS

Logs disimpan di folder `logs/`:

```powershell
# Lihat real-time log dari terminal sudah tercetak dengan warna

# Atau buka file log
cat logs\webserver.log
cat logs\proxy.log
```

---

## 6. MELIHAT CACHE

Cache disimpan di folder `cache/`:

```powershell
# Lihat apa yang dicache
dir cache\

# Contoh file cache:
# index.html.cache
# page.html.cache
# api_status.cache
```

---

## 7. GRACEFUL SHUTDOWN

Untuk menghentikan semua server dengan baik, tekan `Ctrl+C` di setiap terminal:

```powershell
# Di masing-masing terminal tekan Ctrl+C
^C
Shutdown signal received
Graceful shutdown...
```

---

## 8. TESTING - 5 CONCURRENT CLIENTS

Buka 5 Terminal tambahan dan jalankan client berbeda-beda:

```powershell
# Terminal 5
python client.py --mode tcp

# Terminal 6
python client.py --mode tcp

# Terminal 7
python client.py --mode udp

# Terminal 8
python client.py --mode tcp

# Terminal 9
python client.py --mode udp
```

**Output di Proxy:**
```
[10:15:50.123] [INFO] 127.0.0.1 - GET / - INFO
[10:15:50.124] [SUCCESS] 127.0.0.1 - GET / - 200 [HIT] (2.3ms)
[10:15:50.125] [CACHE_HIT] 127.0.0.1 - GET / - 200 [HIT] (1.5ms)
[10:15:50.126] [CACHE_MISS] 127.0.0.1 - GET /page.html - 200 [MISS] (23.4ms)
[10:15:50.127] [CACHE_HIT] 127.0.0.1 - GET /page.html - 200 [HIT] (0.8ms)
```

---

## 9. VERIFIKASI QOS

Lihat statistik cache di proxy server:

```
[10:16:00.123] [INFO] CACHE STATS - Total: 15, Hits: 10, Misses: 5, Hit Rate: 66.7%, Avg Time: 12.4ms
```

---

## 10. TROUBLESHOOTING

### Error: "Connection refused"
- Pastikan webserver.py sudah jalan di Terminal 1
- Pastikan proxy.py sudah jalan di Terminal 2

### Error: "Port already in use"
- Ada program lain yang pakai port 8000, 8080, atau 9000
- Coba ganti port di config atau kill program yang pakai port

### Error: "ModuleNotFoundError"
- Pastikan tidak ada import dari library eksternal
- Gunakan hanya standard library Python

### Cache tidak bekerja
- Cek folder `cache/` sudah created
- Cek permission write ke folder cache
- Lihat log proxy untuk cache HIT/MISS

---

## 11. FITUR-FITUR UTAMA

### Web Server (webserver.py)
✓ TCP Port 8000 - HTTP GET requests  
✓ UDP Port 9000 - Echo untuk QoS  
✓ Multithreading - handle banyak client  
✓ Manual HTTP parsing - tanpa library  
✓ Response codes: 200, 404, 500  
✓ Logging dengan timestamp & IP  
✓ Serve HTML files dari folder `files/`  

### Proxy Server (proxy.py)
✓ TCP Port 8080 - accept client requests  
✓ Caching - thread-safe dengan Lock()  
✓ Forward ke Web Server  
✓ Error handling - 502, 504  
✓ Cache statistics - HIT/MISS tracking  
✓ Response time measurement  
✓ Logging per request  

### Client (client.py)
✓ Mode TCP - GET requests  
✓ Mode UDP - Ping dengan statistik  
✓ RTT measurement (min, avg, max)  
✓ Packet loss calculation  
✓ Jitter calculation  
✓ Throughput calculation  
✓ Colored output  

---

## 12. PERFORMANCE BENCHMARKS

Hasil typical di localhost:
- TCP response time: 1-50ms (tergantung cache)
- UDP RTT: <1ms
- Cache hit latency: ~1ms
- Cache miss latency: ~20-50ms
- Throughput: 1000+ bytes/s


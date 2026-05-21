# PANDUAN STEP-BY-STEP: Setup 3 Laptop (Client-Proxy-Server)

**Modul 8 - Jaringan Komputer**

> Implementasi dan Analisis Kinerja Sistem Client–Proxy–Server Berbasis Socket Python

---

## 📋 Daftar Isi
1. [Persiapan](#persiapan)
2. [Identifikasi IP Setiap Laptop](#identifikasi-ip-setiap-laptop)
3. [Setup Laptop 1 (Server)](#setup-laptop-1-server)
4. [Setup Laptop 2 (Proxy)](#setup-laptop-2-proxy)
5. [Setup Laptop 3 (Client)](#setup-laptop-3-client)
6. [Testing Koneksi](#testing-koneksi)
7. [Troubleshooting](#troubleshooting)

---

## Persiapan

### ✅ Hal yang Dibutuhkan
- **3 Laptop/PC** dengan OS Windows/Linux/Mac
- **Python 3.6+** terinstall di setiap laptop
- **Same Wi-Fi Network** (semua laptop terhubung ke jaringan yang sama)
- **File Script**: `webserver.py`, `proxy.py`, `client.py`

### ✅ Verifikasi Python
Buka terminal di setiap laptop dan ketik:
```bash
python --version
```
Pastikan Python 3.6+ terinstall.

---

## Identifikasi IP Setiap Laptop

Sebelum mulai, catat IP address masing-masing laptop.

### Windows
```bash
ipconfig
```
Cari baris **"IPv4 Address"** (biasanya `192.168.x.x` atau `10.0.x.x`)

### Linux/Mac
```bash
ifconfig
```
atau
```bash
ip addr show
```

### 📝 Catat IP Setiap Laptop

Buatlah tabel seperti ini:

| Laptop | Device | IP Address | Port | Fungsi |
|--------|--------|-----------|------|--------|
| 1 | Nama PC | `192.168.?.?` | 8000 | **Server** |
| 2 | Nama PC | `192.168.?.?` | 8888 | **Proxy** |
| 3 | Nama PC | `192.168.?.?` | - | **Client** |

**Contoh:**

| Laptop | Device | IP Address | Port | Fungsi |
|--------|--------|-----------|------|--------|
| 1 | Desktop Alice | `192.168.1.10` | 8000 | Server |
| 2 | Laptop Bob | `192.168.1.20` | 8888 | Proxy |
| 3 | Laptop Charlie | `192.168.1.30` | - | Client |

---

## Setup Laptop 1: Server

### Step 1: Copy File
Copy file `webserver.py` ke Laptop 1

### Step 2: Edit webserver.py
Buka file `webserver.py` dengan text editor dan pastikan konfigurasi seperti ini:

```python
# KONFIGURASI SERVER
HOST = '0.0.0.0'
PORT = 8000
```

**Penjelasan:**
- `HOST = '0.0.0.0'` → Server listen di semua interface jaringan
- `PORT = 8000` → Server akan berjalan di port 8000

### Step 3: Jalankan Server
```bash
python webserver.py
```

Jika berhasil, Anda akan melihat:
```
[SERVER] TCP listening di 0.0.0.0:8000
[SERVER] UDP listening di 0.0.0.0:5000
```

**✅ Server siap!**

---

## Setup Laptop 2: Proxy

### Step 1: Copy File
Copy file `proxy.py` ke Laptop 2

### Step 2: Edit proxy.py
Buka file `proxy.py` dan ganti `SERVER_HOST` dengan **IP Laptop 1 (Server)**:

```python
# KONFIGURASI PROXY
PROXY_HOST = '0.0.0.0'
PROXY_PORT = 8888

# KONFIGURASI SERVER YANG AKAN DIHUBUNGI
SERVER_HOST = '192.168.1.10'  # ⬅️ GANTI DENGAN IP LAPTOP 1
SERVER_PORT = 8000
```

**Penjelasan:**
- `SERVER_HOST = '192.168.1.10'` → **Ganti dengan IP Laptop 1**

### Step 3: Jalankan Proxy
```bash
python proxy.py
```

Jika berhasil, Anda akan melihat:
```
[PROXY] TCP listening di 0.0.0.0:8888
[PROXY] Akan forward ke server di 192.168.1.10:8000
```

**✅ Proxy siap!**

---

## Setup Laptop 3: Client

### Step 1: Copy File
Copy file `client.py` ke Laptop 3

### Step 2: Edit client.py
Buka file `client.py` dan ganti konfigurasi:

```python
# KONFIGURASI CLIENT
PROXY_HOST = '192.168.1.20'  # ⬅️ GANTI DENGAN IP LAPTOP 2
PROXY_PORT = 8888

SERVER_HOST = '192.168.1.10'  # ⬅️ GANTI DENGAN IP LAPTOP 1
SERVER_UDP_PORT = 5000
```

**Penjelasan:**
- `PROXY_HOST = '192.168.1.20'` → **Ganti dengan IP Laptop 2**
- `SERVER_HOST = '192.168.1.10'` → **Ganti dengan IP Laptop 1**

### Step 3: Jalankan Client
```bash
python client.py
```

Jika berhasil, Anda akan melihat menu:
```
[CLIENT] Terhubung ke Proxy di 192.168.1.20:8888
[CLIENT] Server UDP di 192.168.1.10:5000

========================================
   SISTEM MANAJEMEN TUGAS
========================================
1. Tambah tugas
2. Lihat daftar tugas
3. Cek reminder deadline
4. Keluar
========================================

Pilih menu (1-4):
```

**✅ Client siap!**

---

## PANDUAN LENGKAP: 3 LAPTOP SETUP

## Overview Sistem 3 Laptop

```
LAPTOP 1 (WEB SERVER)          LAPTOP 2 (PROXY SERVER)          LAPTOP 3 (CLIENT)
┌─────────────────────┐        ┌─────────────────────┐         ┌──────────────┐
│ webserver.py        │        │ proxy.py            │         │ client.py    │
│ Port 8000 (TCP)     │◄───────┤ Port 8080 (TCP)     │◄────────┤ --mode tcp   │
│ Port 9000 (UDP)     │        │ Caching             │         │ --mode udp   │
│                     │        │ Forwarding          │         │              │
│ - HTTP GET          │        │ - Forward requests  │         │ - Send GET   │
│ - UDP Echo          │        │ - Cache HIT/MISS    │         │ - Send Ping  │
│ - File serving      │        │ - Error handling    │         │ - Statistics │
└─────────────────────┘        └─────────────────────┘         └──────────────┘
        ↑                               ↑                              ↑
   IP: 192.168.1.X             IP: 192.168.1.Y                 IP: 192.168.1.Z
```

---

## REQUIREMENTS SETUP

### Yang Perlu Disiapkan
- ✓ 3 Laptop (Bisa virtual machine juga)
- ✓ Network connection (LAN/WiFi yang sama)
- ✓ Python 3.6+ di setiap laptop
- ✓ File source code (3 Python files)
- ✓ HTML files (index.html, page.html)

### Cek Network
```powershell
# Di masing-masing laptop
ipconfig /all
# Catat IP address masing-masing

# Test connectivity antar laptop
ping 192.168.1.X  # IP laptop lain
# Harus reply, bukan timeout
```

---

## STEP 1: SETUP LAPTOP 1 (WEB SERVER)

### 1.1 Persiapan File

Buat folder di Laptop 1:
```
C:\Jarkom-WebServer\
├── python\
│   └── webserver.py
├── files\
│   ├── index.html
│   └── page.html
├── logs\
└── cache\
```

### 1.2 Copy Files

Copy dari source:
- webserver.py → ke folder `python/`
- index.html, page.html → ke folder `files/`

### 1.3 Konfigurasi (PENTING!)

Edit `webserver.py`, ubah HOST dari 'localhost' menjadi '0.0.0.0':

```python
# Cari baris ini
HOST = 'localhost'

# Ubah jadi
HOST = '0.0.0.0'  # Agar bisa diakses dari laptop lain
TCP_PORT = 8000
UDP_PORT = 9000
```

### 1.4 Jalankan Web Server

```powershell
cd C:\Jarkom-WebServer\python
python webserver.py
```

**Expected Output:**
```
[2024-05-21 10:15:30.123] [INFO] ======================================================================
[2024-05-21 10:15:30.124] [INFO] WEB SERVER STARTING
[2024-05-21 10:15:30.127] [SUCCESS] TCP Server listening on 0.0.0.0:8000
[2024-05-21 10:15:30.128] [SUCCESS] UDP Server listening on 0.0.0.0:9000
```

### 1.5 Catat IP Laptop 1

Jalankan di PowerShell:
```powershell
ipconfig

# Catat IPv4 Address, contoh: 192.168.1.100
```

**Laptop 1 IP**: 192.168.1.100 (contoh, ganti dengan IP asli)

---

## STEP 2: SETUP LAPTOP 2 (PROXY SERVER)

### 2.1 Persiapan File

Buat folder di Laptop 2:
```
C:\Jarkom-Proxy\
├── python\
│   └── proxy.py
├── cache\
├── logs\
```

### 2.2 Copy Files

Copy `proxy.py` ke folder `python/`

### 2.3 Konfigurasi (PENTING!)

Edit `proxy.py`, ubah HOST dan SERVER_HOST:

```python
# CARI BAGIAN INI:
PROXY_HOST = 'localhost'
PROXY_PORT = 8080
SERVER_HOST = 'localhost'
SERVER_PORT = 8000

# UBAH JADI (ganti 192.168.1.100 dengan IP Laptop 1 asli):
PROXY_HOST = '0.0.0.0'        # Listen dari semua interface
PROXY_PORT = 8080
SERVER_HOST = '192.168.1.100' # IP Laptop 1 (GANTI!)
SERVER_PORT = 8000
REQUEST_TIMEOUT = 5
```

### 2.4 Jalankan Proxy Server

```powershell
cd C:\Jarkom-Proxy\python
python proxy.py
```

**Expected Output:**
```
[2024-05-21 10:15:35.123] [INFO] PROXY SERVER STARTING
[2024-05-21 10:15:35.127] [SUCCESS] Proxy Server listening on 0.0.0.0:8080
[2024-05-21 10:15:35.128] [INFO] Forwarding to 192.168.1.100:8000
```

### 2.5 Catat IP Laptop 2

```powershell
ipconfig
# Contoh: 192.168.1.101
```

**Laptop 2 IP**: 192.168.1.101 (contoh, ganti dengan IP asli)

---

## STEP 3: SETUP LAPTOP 3 (CLIENT)

### 3.1 Persiapan File

Buat folder di Laptop 3:
```
C:\Jarkom-Client\
└── python\
    └── client.py
```

### 3.2 Copy Files

Copy `client.py` ke folder `python/`

### 3.3 Konfigurasi (PENTING!)

Edit `client.py`, ubah HOST:

```python
# CARI BAGIAN INI:
PROXY_HOST = 'localhost'
PROXY_PORT = 8080
SERVER_HOST = 'localhost'
SERVER_UDP_PORT = 9000

# UBAH JADI (ganti IP sesuai)
PROXY_HOST = '192.168.1.101'  # IP Laptop 2 (GANTI!)
PROXY_PORT = 8080
SERVER_HOST = '192.168.1.100' # IP Laptop 1 untuk UDP (GANTI!)
SERVER_UDP_PORT = 9000
REQUEST_TIMEOUT = 5
UDP_TIMEOUT = 1
```

### 3.4 Jalankan Client TCP

```powershell
cd C:\Jarkom-Client\python
python client.py --mode tcp
```

**Expected Output:**
```
[10:15:45.456] [SUCCESS] TCP Mode - HTTP Client
[10:15:45.125] [INFO] Connecting to Proxy: 192.168.1.101:8080
[10:15:45.456] [SUCCESS] GET / - HTTP/1.1 200 OK (45.2ms, 3456 bytes)
[10:15:45.589] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (23.3ms, 3456 bytes)
```

### 3.5 Jalankan Client UDP

```powershell
cd C:\Jarkom-Client\python
python client.py --mode udp
```

**Expected Output:**
```
[10:16:15.125] [PING] Ping 1 - RTT=5.2ms from 192.168.1.100
[10:16:15.226] [PING] Ping 2 - RTT=4.9ms from 192.168.1.100
...
Min RTT:             4.7ms
Avg RTT:             5.1ms
Max RTT:             5.8ms
Packet Loss:         0.0%
```

---

## NETWORK TROUBLESHOOTING

### Masalah: Client tidak bisa connect ke Proxy

**Solusi 1: Cek IP address**
```powershell
# Di Laptop 2 (Proxy)
ipconfig
# Pastikan IP cocok dengan PROXY_HOST di client.py

# Di Laptop 3 (Client)
ping 192.168.1.101
# Harus reply, bukan timeout
```

**Solusi 2: Firewall**
```powershell
# Di Laptop 2 (Proxy) - Allow port 8080
netsh advfirewall firewall add rule name="Proxy Port 8080" dir=in action=allow protocol=tcp localport=8080

# Di Laptop 1 (Web Server) - Allow port 8000 dan 9000
netsh advfirewall firewall add rule name="WebServer Port 8000" dir=in action=allow protocol=tcp localport=8000
netsh advfirewall firewall add rule name="UDP Echo Port 9000" dir=in action=allow protocol=udp localport=9000
```

**Solusi 3: Antivirus**
- Pastikan firewall/antivirus tidak block port 8000, 8080, 9000
- Atau whitelist aplikasi Python

### Masalah: Proxy tidak bisa connect ke Web Server

**Cek koneksi:**
```powershell
# Di Laptop 2 (Proxy terminal)
ping 192.168.1.100
# Harus reply

# Cek port 8000 terbuka
telnet 192.168.1.100 8000
# Connected = OK, Refused = Server belum start
```

### Masalah: UDP Echo timeout

**Cek UDP:**
```powershell
# Di Laptop 1 (Web Server)
netstat -ano | findstr ":9000"
# Harus terlihat listening

# Di Laptop 3 (Client)
telnet 192.168.1.100 9000
# UDP tidak reply ke telnet, tapi UDP ping harus jalan
```

---

## MONITORING & LOGS

### View Logs di Laptop 1

```powershell
cd C:\Jarkom-WebServer\logs
Get-Content webserver.log -Wait  # Real-time monitoring
```

Perhatikan:
- Client IP yang connect
- Request paths
- Response status (200, 404, 500)

### View Logs di Laptop 2

```powershell
cd C:\Jarkom-Proxy\logs
Get-Content proxy.log -Wait  # Real-time monitoring
```

Perhatikan:
- Client IP
- Cache HIT/MISS
- Response times
- Error responses (502, 504)

### View Cache di Laptop 2

```powershell
cd C:\Jarkom-Proxy\cache
dir  # Lihat cache files yang tercipta
Get-ChildItem -Recurse | Measure-Object -Sum Length  # Total cache size
```

---

## TESTING SCENARIOS

### Scenario 1: Basic Test

**Di Laptop 3 (Client):**
```powershell
python client.py --mode tcp
```

**Cek di Laptop 1 (Web Server) Logs:**
```
[10:15:45.456] [INFO] 192.168.1.103 - GET /
[10:15:45.457] [SUCCESS] 192.168.1.103 - GET / - 200
```

**Cek di Laptop 2 (Proxy) Logs:**
```
[10:15:45.456] [CACHE_MISS] 192.168.1.103 - GET / - 200 [MISS] (23.4ms)
```

### Scenario 2: Cache HIT vs MISS

**Di Laptop 3 (Client), jalankan 2x:**
```powershell
python client.py --mode tcp
# (tunggu 1 detik)
python client.py --mode tcp
```

**Cek di Laptop 2 (Proxy) Logs:**
```
[10:15:45.456] [CACHE_MISS] 192.168.1.103 - GET / - 200 [MISS] (45.2ms)
[10:15:46.456] [CACHE_HIT]  192.168.1.103 - GET / - 200 [HIT]  (1.3ms)
```

**Perhatikan:** HIT time jauh lebih cepat!

### Scenario 3: Multiple Concurrent Clients

**Di 3 terminal berbeda di Laptop 3, jalankan:**
```powershell
# Terminal 1
python client.py --mode tcp

# Terminal 2
python client.py --mode tcp

# Terminal 3
python client.py --mode tcp
```

**Cek di Laptop 2 (Proxy) Logs:**
- Semua request tercatat
- Tidak ada error
- Cache terdeteksi dengan benar

### Scenario 4: UDP QoS Test

**Di Laptop 3 (Client):**
```powershell
python client.py --mode udp
```

**Output UDP:**
```
Min RTT:             4.7ms
Avg RTT:             5.1ms
Max RTT:             5.8ms
Packet Loss:         0.0%
Avg Jitter:          0.3ms
Throughput:          1234.5 bytes/s
```

**Analisis:**
- RTT ~5ms karena network latency (normal untuk LAN)
- Packet Loss 0% = Network stabil
- Jitter kecil = Konsisten

---

## WIRESHARK CAPTURE (Optional but Recommended)

### Setup Wireshark

1. Install Wireshark di Laptop 3 (Client)
2. Run Wireshark
3. Start capture di network adapter
4. Filter: `tcp.port == 8080 or tcp.port == 8000 or udp.port == 9000`

### What You'll See

**TCP Flow (HTTP GET through Proxy):**
```
1. Client → Proxy (SYN)
2. Proxy → Client (SYN-ACK)
3. Client → Proxy (ACK, GET /)
4. Proxy → WebServer (GET /)
5. WebServer → Proxy (200 OK with HTML)
6. Proxy → Client (200 OK with HTML)
7. All close (FIN packets)
```

**UDP Flow (Echo):**
```
1. Client → Server (Ping 1 timestamp)
2. Server → Client (Echo: Ping 1 timestamp)
3. Client → Server (Ping 2 timestamp)
4. Server → Client (Echo: Ping 2 timestamp)
...
```

---

## PERFORMANCE METRICS

Expected values dengan LAN network:

| Metric | Expected |
|--------|----------|
| TCP MISS (first request) | 30-100ms |
| TCP HIT (second request) | 5-20ms |
| UDP RTT | 1-10ms |
| Cache improvement | 5-20x faster |
| Concurrent clients | 5+ simultaneously |
| Packet loss | <5% (good WiFi/LAN) |

---

## SECURITY NOTES

### Perhatian Penting

1. **Network Interface Binding**
   - Jangan gunakan 0.0.0.0 di public network
   - Untuk lab/testing saja yang aman

2. **Port Access**
   - Pastikan firewall terkonfigurasi
   - Hanya allow dari network yang diinginkan

3. **Data Privacy**
   - HTTP tidak encrypted
   - Jangan gunakan untuk data sensitif
   - Ini lab/educational purposes saja

---

## ADVANCED: BROWSER ACCESS

### Access dari Laptop Lain

Buka browser, akses:
```
http://192.168.1.100:8000/
http://192.168.1.100:8000/index.html
http://192.168.1.100:8000/page.html
http://192.168.1.100:8000/api/status
```

**Atau melalui Proxy:**
```
# Tidak bisa direct browser access ke Proxy
# Karena Proxy forward HTTP (tidak standar browser proxy)
# Gunakan client.py atau Wireshark untuk observe
```

---

## TROUBLESHOOTING CHECKLIST

Sebelum claim "tidak jalan":

- [ ] Web Server di Laptop 1 sudah start? (Check: "listening on 0.0.0.0:8000")
- [ ] Proxy Server di Laptop 2 sudah start? (Check: "listening on 0.0.0.0:8080")
- [ ] IP addresses benar? (Gunakan `ipconfig` verify)
- [ ] HOST config di proxy.py benar? (SERVER_HOST = IP Laptop 1)
- [ ] HOST config di client.py benar? (PROXY_HOST = IP Laptop 2)
- [ ] Firewall allow ports 8000, 8080, 9000?
- [ ] Network connectivity OK? (Ping test antar laptop)
- [ ] Python 3.6+ installed? (Check: `python --version`)
- [ ] Logs folder created? (Check: `logs/` folder exists)
- [ ] HTML files di place? (Check: `files/` folder exist)

---

## QUICK START CHEAT SHEET

### Laptop 1 (Web Server)
```powershell
# Edit webserver.py: HOST = '0.0.0.0'
cd C:\Jarkom-WebServer\python
python webserver.py
# Catat IP (ipconfig)
```

### Laptop 2 (Proxy)
```powershell
# Edit proxy.py:
# PROXY_HOST = '0.0.0.0'
# SERVER_HOST = '192.168.1.100' (IP Laptop 1)
cd C:\Jarkom-Proxy\python
python proxy.py
# Catat IP (ipconfig)
```

### Laptop 3 (Client)
```powershell
# Edit client.py:
# PROXY_HOST = '192.168.1.101' (IP Laptop 2)
# SERVER_HOST = '192.168.1.100' (IP Laptop 1)
cd C:\Jarkom-Client\python
python client.py --mode tcp
python client.py --mode udp
```

---

## NEXT STEPS

Setelah semua berjalan:

1. **Dokumentasi**: Catat IP addresses semua laptop
2. **Testing**: Run semua 4 scenarios di atas
3. **Wireshark**: Capture traffic dan analyze
4. **Statistics**: Perhatikan cache HIT/MISS dan response times
5. **Troubleshooting**: Jika ada error, check logs terlebih dahulu
6. **Presentation**: Siap present hasil testing

---

## EXPECTED FINAL OUTPUT

### Laptop 1 Terminal
```
[SUCCESS] TCP Server listening on 0.0.0.0:8000
[SUCCESS] UDP Server listening on 0.0.0.0:9000
[INFO] 192.168.1.103 - GET /
[SUCCESS] 192.168.1.103 - GET / - 200
```

### Laptop 2 Terminal
```
[SUCCESS] Proxy Server listening on 0.0.0.0:8080
[INFO] Forwarding to 192.168.1.100:8000
[CACHE_MISS] 192.168.1.103 - GET / - 200 [MISS] (45.2ms)
[CACHE_HIT] 192.168.1.103 - GET / - 200 [HIT] (1.3ms)
[INFO] CACHE STATS - Total: 6, Hits: 4, Misses: 2, Hit Rate: 66.7%
```

### Laptop 3 Terminal
```
[SUCCESS] TCP Mode - HTTP Client
[SUCCESS] GET / - HTTP/1.1 200 OK (45.2ms, 3456 bytes)
[SUCCESS] GET /index.html - HTTP/1.1 200 OK (1.3ms, 3456 bytes)

[SUCCESS] UDP Mode - QoS Monitoring
[PING] Ping 1 - RTT=5.2ms
Min RTT: 4.7ms
Avg RTT: 5.1ms
Packet Loss: 0.0%
```

---

**Status**: ✓ Siap untuk 3 Laptop Setup  
**Last Updated**: 2024-05-21  
**Difficulty**: Intermediate

ing Koneksi

### Scenario 1: View Task (GET)

1. Di **Laptop 3 (Client)**, pilih **"2. Lihat tugas"**
2. Tekan Enter

**Output yang diharapkan:**
```
===== DAFTAR TUGAS =====
Belum ada tugas.
```

### Scenario 2: Add Task (ADD)

1. Di **Laptop 3 (Client)**, pilih **"1. Tambah tugas"**
2. Masukkan:
   - Mata kuliah: `Jaringan Komputer`
   - Judul tugas: `Implementasi Proxy`
   - Deadline: `2026-05-25`
3. Tekan Enter

**Output yang diharapkan:**
```
SUCCESS: Tugas 'Implementasi Proxy' berhasil ditambahkan!
```

### Scenario 3: View Again (GET)

Pilih "2. Lihat tugas" lagi untuk melihat tugas yang baru ditambah:

```
===== DAFTAR TUGAS =====
1. Jaringan Komputer | Implementasi Proxy | 2026-05-25
```

---

## Troubleshooting

### ❌ Error: Connection refused

**Penyebab:**
- Proxy atau Server belum dijalankan
- IP address salah di konfigurasi

**Solusi:**
1. Pastikan Laptop 1 (Server) sudah jalankan `webserver.py`
2. Pastikan Laptop 2 (Proxy) sudah jalankan `proxy.py`
3. Verifikasi IP address di setiap file

### ❌ Error: No route to host

**Penyebab:**
- Laptop tidak terhubung ke jaringan yang sama
- IP address salah

**Solusi:**
1. Pastikan semua laptop terhubung ke Wi-Fi yang sama
2. Jalankan `ping` untuk test koneksi:
   ```bash
   ping 192.168.1.10
   ```

---

**Good luck untuk testing 3 laptop! 🚀**

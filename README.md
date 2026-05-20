# 🌐 Client-Proxy-Server Task Management System

**Tugas Besar Jaringan Komputer - Modul 8**

Implementasi lengkap sistem Client-Proxy-Server menggunakan TCP dan UDP dalam Python dengan error handling dan quality of service analysis.

---

## 📋 Daftar Isi

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Struktur Folder](#struktur-folder)
- [Dokumentasi](#dokumentasi)
- [Fitur](#fitur)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Sistem Task Manager berbasis jaringan dengan arsitektur Client-Proxy-Server:

- **Server** (port 8000 TCP, 5000 UDP) - Process requests & store data
- **Proxy** (port 8888 TCP) - Forward requests & responses
- **Client** - User interface untuk interact dengan system

### Karakteristik
- ✅ TCP communication untuk reliable delivery
- ✅ UDP support untuk fast response
- ✅ Error handling & input validation
- ✅ Multi-laptop deployment support
- ✅ Complete documentation dengan diagrams

---

## 🚀 Quick Start

### 1. Setup (Localhost - Single Machine)

```bash
# Terminal 1: Server
cd python
python webserver.py

# Terminal 2: Proxy (new terminal)
cd python
python proxy.py

# Terminal 3: Client (new terminal)
cd python
python client.py
```

### 2. Test
```
Menu 1: Tambah tugas
  Input: Jarkom | Tubes | 2026-05-25
  
Menu 2: Lihat tugas
  Output: List semua tugas

Menu 3: Reminder
  Output: Tasks dengan deadline dekat

Menu 4: Exit
```

### 3. For Multi-Laptop Setup
Update IP addresses di:
- `python/proxy.py` line 8: `SERVER_HOST = '192.168.1.X'`
- `python/client.py` line 4-5: `PROXY_HOST` & `SERVER_HOST`

Lihat: [dokumentasi/2_PANDUAN_3_LAPTOP.md](dokumentasi/2_PANDUAN_3_LAPTOP.md)

---

## 📂 Struktur Folder

```
Tubes Jarkom/
│
├── python/                    ← Code Python (siap jalankan)
│   ├── webserver.py
│   ├── proxy.py
│   └── client.py
│
├── dokumentasi/              ← Documentation (10 files)
│   ├── 0_INDEX_DOKUMENTASI.md
│   ├── 1_README.md
│   ├── 2_PANDUAN_3_LAPTOP.md
│   ├── 3_PANDUAN_IMPLEMENTASI_LENGKAP.md
│   ├── 4_LAPORAN_TUGAS_BESAR.md
│   ├── 5_ANALISIS_EROR_AWAL.md
│   ├── 6_SKEMA_ARSITEKTUR.md
│   ├── 7_CHECKLIST_PRESENTASI.md
│   ├── 8_QUICK_REFERENCE.md
│   └── 9_STRUKTUR_FOLDER.md
│
├── testing/                   ← Test artifacts
│   ├── screenshots/
│   └── logs/
│
└── .gitignore
```

---

## 🚀 Quick Start

### Prasyarat
- Python 3.6+
- 3 Laptop/PC dengan Wi-Fi yang sama

### Step 1: Jalankan Server (Laptop 1)
```bash
python webserver.py
```

**Output yang diharapkan:**
```
[SERVER] TCP listening di 0.0.0.0:8000
[SERVER] UDP listening di 0.0.0.0:5000
```

### Step 2: Jalankan Proxy (Laptop 2)
**Sebelumnya**, edit `proxy.py` dan ubah baris 8:
```python
SERVER_HOST = '192.168.1.10'  # UBAH ke IP Laptop 1
```

Lalu jalankan:
```bash
python proxy.py
```

**Output yang diharapkan:**
```
[PROXY] TCP listening di 0.0.0.0:8888
[PROXY] Akan forward ke server di 192.168.1.10:8000
```

### Step 3: Jalankan Client (Laptop 3)
**Sebelumnya**, edit `client.py` dan ubah baris 4-5:
```python
PROXY_HOST = '192.168.1.20'   # UBAH ke IP Laptop 2
SERVER_HOST = '192.168.1.10'  # UBAH ke IP Laptop 1
```

Lalu jalankan:
```bash
python client.py
```

**Output yang diharapkan:**
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

---

## 📝 Penjelasan 3 File Python

### 1. webserver.py (Backend Server)

**Fungsi:**
- Listen TCP connection di port 8000
- Listen UDP connection di port 5000
- Process request: ADD (tambah tugas), GET (lihat tugas), REMINDER (cek deadline)
- Simpan data tugas di memory (list)
- Kirim response ke proxy

**Port:**
- TCP: 8000
- UDP: 5000

**Request Format:**
```
ADD|matkul|judul|deadline    ← Tambah tugas
GET                           ← Lihat semua tugas
REMINDER                      ← Cek reminder deadline
```

**Response Format:**
```
HTTP/1.1 200 OK

[response body]
```

**Error Handling:**
- ✅ Validasi format request (panjang array)
- ✅ Validasi format tanggal (YYYY-MM-DD)
- ✅ Try-except untuk date parsing
- ✅ Try-except untuk TCP accept

**Contoh Penggunaan:**
```python
# User tambah tugas:
# Input: Jaringan Komputer | Tubes Jarkom | 2026-05-25
# Request dikirim: "ADD|Jaringan Komputer|Tubes Jarkom|2026-05-25"
# Server validate & simpan
# Response: "SUCCESS: Tugas 'Tubes Jarkom' berhasil ditambahkan!"
```

### 2. proxy.py (Middleware)

**Fungsi:**
- Listen TCP connection di port 8888 dari client
- Forward request ke server di port 8000
- Terima response dari server
- Forward response kembali ke client
- Handle connection errors dengan graceful

**Port:**
- Listen: 8888 (TCP)
- Forward ke: 8000 di SERVER_HOST (TCP)

**Alur Komunikasi:**
```
Client → Proxy:8888 → (forward) → Server:8000
Server → Proxy → (forward) → Client
```

**Error Handling:**
- ✅ Try-except untuk server connection
- ✅ Handle ConnectionRefusedError (server offline)
- ✅ Handle generic exceptions
- ✅ Graceful error messages (HTTP error responses)
- ✅ Proper cleanup dengan finally block

**Contoh Error Response:**
```
HTTP/1.1 503 Service Unavailable

ERROR: Server tidak tersedia
```

### 3. client.py (Frontend Client)

**Fungsi:**
- Display menu ke user
- Send request ke proxy via TCP port 8888
- Optional: Send request ke server via UDP port 5000
- Display response ke user
- Handle user input validation

**Port:**
- Connect to Proxy: 8888 (TCP)
- Connect to Server: 5000 (UDP) - optional

**Menu Options:**
```
1. Tambah tugas          → ADD|matkul|judul|deadline
2. Lihat daftar tugas    → GET
3. Cek reminder deadline → REMINDER
4. Keluar                → Exit program
```

**Error Handling:**
- ✅ Try-except untuk TCP connection ke proxy
- ✅ Try-except untuk UDP send/receive
- ✅ Graceful error messages
- ✅ Allow user retry jika connection fail

**Contoh Error Message:**
```
❌ ERROR: Tidak bisa connect ke Proxy di 192.168.1.20:8888
   Pastikan proxy.py sudah dijalankan!
```

---

## 🔧 Konfigurasi IP untuk 3 Laptop

### Identifikasi IP Setiap Laptop

**Windows:**
```bash
ipconfig
```

**Linux/Mac:**
```bash
ifconfig
```

### Edit Konfigurasi

#### File: proxy.py (Laptop 2)
```python
# Baris 8: Ubah ke IP Laptop 1 (Server)
SERVER_HOST = '192.168.1.10'
```

#### File: client.py (Laptop 3)
```python
# Baris 4: Ubah ke IP Laptop 2 (Proxy)
PROXY_HOST = '192.168.1.20'

# Baris 5: Ubah ke IP Laptop 1 (Server) - untuk UDP
SERVER_HOST = '192.168.1.10'
```

### Contoh Konfigurasi Valid

| Komponen | File | Baris | Konfigurasi | IP |
|----------|------|-------|-------------|-----|
| Server | webserver.py | 3 | `HOST = '0.0.0.0'` | 192.168.1.10 |
| Proxy | proxy.py | 8 | `SERVER_HOST = '192.168.1.10'` | 192.168.1.20 |
| Client | client.py | 4 | `PROXY_HOST = '192.168.1.20'` | 192.168.1.30 |
| Client | client.py | 5 | `SERVER_HOST = '192.168.1.10'` | (same as above) |

---

## 📊 Skema Alur Data

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   CLIENT    │         │    PROXY     │         │   SERVER    │
│  Laptop 3   │         │  Laptop 2    │         │  Laptop 1   │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                        │
       │  TCP REQUEST (8888)   │                        │
       ├──────────────────────>│                        │
       │                       │                        │
       │            TCP REQUEST (8000)                 │
       │            ├───────────────────────────────────>│
       │            │                                   │
       │            │           PROCESS                │
       │            │      & VALIDATE DATA             │
       │            │                                   │
       │            │        TCP RESPONSE (8000)       │
       │            │<───────────────────────────────────┤
       │                                                 │
       │  TCP RESPONSE (8888)                           │
       │<──────────────────────┤                        │
       │                       │                        │
       │                       │  UDP DIRECT (5000)    │
       │<──────────────────────────────────────────────┤
       │                       │                        │
```

---

## ✅ Testing Checklist

- [ ] Server running: `python webserver.py`
- [ ] Proxy running: `python proxy.py`
- [ ] Client running: `python client.py`
- [ ] Config IP benar di proxy.py & client.py
- [ ] Menu 1 (Tambah tugas) berhasil dengan deadline format YYYY-MM-DD
- [ ] Menu 2 (Lihat tugas) menampilkan tugas yang ditambah
- [ ] Menu 3 (Reminder) menampilkan tugas dengan deadline hari ini/besok
- [ ] Menu 4 (Keluar) menutup client dengan normal
- [ ] Error handling: Stop server, client tetap bisa retry
- [ ] Error handling: Invalid deadline format, server tidak crash

---

## 🐛 Troubleshooting

### ❌ Error: Connection refused

**Penyebab:**
- Server belum dijalankan
- Proxy belum dijalankan
- IP address salah di konfigurasi

**Solusi:**
1. Pastikan semua 3 file sudah running (check output di terminal)
2. Verifikasi IP dengan `ipconfig` atau `ifconfig`
3. Edit proxy.py & client.py dengan IP yang benar
4. Restart semua proses

### ❌ Error: Address already in use

**Penyebab:**
- Port 8000 atau 8888 sudah dipakai aplikasi lain

**Solusi:**
```bash
# Windows - Kill process yang pakai port 8000
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# Linux/Mac - Kill process yang pakai port 8000
lsof -i :8000
kill -9 [PID_NUMBER]
```

### ❌ Error: Invalid date format

**Penyebab:**
- Input deadline tidak sesuai format YYYY-MM-DD

**Solusi:**
- Gunakan format: `2026-05-25` (TAHUN-BULAN-HARI)
- Jangan gunakan format lain seperti `25-05-2026` atau `05/25/2026`

### ⚠️ Warning: UDP tidak tersedia

**Penyebab:**
- Server UDP tidak running
- Firewall memblokir UDP port 5000

**Solusi:**
- UDP adalah optional, sistem tetap berjalan dengan TCP saja
- Buka firewall untuk port UDP:5000 jika diperlukan

---

## 📚 Panduan Lengkap

Untuk informasi lebih detail, baca file-file berikut:

1. **PANDUAN_3_LAPTOP.md**
   - Setup lengkap untuk 3 laptop berbeda
   - Cara cari IP address
   - Step-by-step configuration

2. **PANDUAN_IMPLEMENTASI_LENGKAP.md**
   - Skema arsitektur dengan diagram
   - Source code lengkap dengan penjelasan
   - Error handling explanation

3. **LAPORAN_TUGAS_BESAR.md**
   - Template lengkap untuk presentasi
   - Include testing results & QoS analysis
   - Struktur laporan profesional untuk kelompok 3 orang

4. **ANALISIS_EROR_AWAL.md**
   - 4 error yang ditemukan & diperbaiki
   - Penjelasan masalah & solusi
   - Before-after code comparison

---

## 🎯 Untuk Presentasi

### Yang Harus Dipersiapkan:
1. ✅ Ketiga file python sudah diperbaiki
2. ✅ Konfigurasi IP sudah sesuai dengan 3 laptop
3. ✅ Ketiga file bisa running tanpa error
4. ✅ Laporan sudah lengkap (gunakan LAPORAN_TUGAS_BESAR.md sebagai template)
5. ✅ Screenshots testing sudah dikumpulkan
6. ✅ Penjelasan skema & alur data

### Demo Live:
1. Jalankan ketiga file di terminal terpisah
2. Test menu 1, 2, 3, 4
3. Tunjukkan error handling (test dengan deadline format salah)
4. Tunjukkan komunikasi data antar laptop di terminal

### Penjelasan:
1. Skema arsitektur (TCP/UDP)
2. Alur komunikasi client-proxy-server
3. Error handling yang ditambahkan
4. Hasil testing & QoS analysis
5. Pembagian tugas kelompok (3 orang)

---

## 📞 Informasi Kelompok

**Untuk Diisi:**

| No | Nama | NIM | Peran |
|----|------|-----|-------|
| 1 | _____________ | _____________ | Backend Lead (webserver.py) |
| 2 | _____________ | _____________ | Network Lead (proxy.py) |
| 3 | _____________ | _____________ | Testing Lead (client.py + UDP) |

---

## 📄 File Dokumentasi

| File | Isi |
|------|-----|
| README.md | File ini - overview & quick start |
| PANDUAN_3_LAPTOP.md | Setup untuk 3 laptop |
| PANDUAN_IMPLEMENTASI_LENGKAP.md | Detail lengkap implementasi |
| LAPORAN_TUGAS_BESAR.md | Template laporan presentasi |
| ANALISIS_EROR_AWAL.md | Analisis 4 error & perbaikan |

---

**Good Luck untuk Tugas Besar! 🚀**

Last Updated: May 21, 2026

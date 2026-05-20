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

## Testing Koneksi

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

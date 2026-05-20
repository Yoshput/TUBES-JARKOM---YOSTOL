# README - Tugas Besar Jaringan Komputer Modul 8

**Implementasi Client-Proxy-Server dengan TCP/UDP dalam Python**

## 📋 Daftar Isi
- [Quick Start](#quick-start)
- [Struktur Folder](#struktur-folder)
- [Deskripsi Sistem](#deskripsi-sistem)
- [Cara Menggunakan](#cara-menggunakan)
- [Dokumentasi](#dokumentasi)

---

## 🚀 Quick Start

### Untuk Localhost (1 Laptop)
```bash
# Terminal 1: Jalankan server
cd python
python webserver.py

# Terminal 2: Jalankan proxy
cd python
python proxy.py

# Terminal 3: Jalankan client
cd python
python client.py
```

### Untuk 3 Laptop Berbeda
Baca: [`2_PANDUAN_3_LAPTOP.md`](2_PANDUAN_3_LAPTOP.md)

---

## 📂 Struktur Folder

```
Tubes Jarkom/
├── python/                          ← KODE PYTHON
│   ├── webserver.py                (Server TCP:8000 + UDP:5000)
│   ├── proxy.py                    (Proxy TCP:8888 → TCP:8000)
│   └── client.py                   (Client TCP→Proxy + UDP→Server)
│
├── dokumentasi/                     ← DOKUMENTASI
│   ├── 0_INDEX_DOKUMENTASI.md      (Panduan baca doc)
│   ├── 1_README.md                 (File ini)
│   ├── 2_PANDUAN_3_LAPTOP.md       (Setup multi-laptop)
│   ├── 3_PANDUAN_IMPLEMENTASI_LENGKAP.md
│   ├── 4_LAPORAN_TUGAS_BESAR.md    (Template laporan)
│   ├── 5_ANALISIS_EROR_AWAL.md     (Error analysis)
│   ├── 6_SKEMA_ARSITEKTUR.md       (Diagrams)
│   ├── 7_CHECKLIST_PRESENTASI.md   (Prep checklist)
│   ├── 8_QUICK_REFERENCE.md        (Quick ref)
│   └── 9_STRUKTUR_FOLDER.md        (Folder guide)
│
├── testing/                         ← TEST ARTIFACTS
│   ├── screenshots/                (Test screenshots)
│   └── logs/                       (Test logs)
│
├── .gitignore                       (Git ignore rules)
├── README.md                        (File ini, di root)
└── Topik & Ketentuan Tugas Besar.pdf (Assignment requirements)
```

---

## 🎯 Deskripsi Sistem

Sistem Task Manager dengan arsitektur Client-Proxy-Server:

### Komponen
| Komponen | Port | Protokol | Fungsi |
|----------|------|----------|--------|
| **Server** | 8000 | TCP | Process requests, simpan tasks |
| **Server** | 5000 | UDP | Kirim response langsung ke client |
| **Proxy** | 8888 | TCP | Forward requests server ↔ client |
| **Client** | - | TCP | Send requests, display UI |

### Request Format
```
ADD|matkul|judul|deadline    ← Tambah tugas
GET                          ← Lihat semua tugas
REMINDER                     ← Cek deadline hari ini/besok
```

### Contoh Penggunaan
```
Menu 1: Tambah tugas
  Input: Jarkom | Tubes | 2026-05-25
  Output: SUCCESS: Tugas ditambahkan!

Menu 2: Lihat tugas
  Output: 1. Jarkom | Tubes | 2026-05-25

Menu 3: Reminder
  Output: ⚠️ Tubes (Jarkom) - BESOK!

Menu 4: Keluar
  Exit program
```

---

## 💾 Cara Menggunakan

### 1. Jalankan Server (Laptop 1 atau Terminal 1)
```bash
cd python
python webserver.py
```
**Output:**
```
[SERVER] TCP listening di 0.0.0.0:8000
[SERVER] UDP listening di 0.0.0.0:5000
```

### 2. Jalankan Proxy (Laptop 2 atau Terminal 2)
```bash
cd python
python proxy.py
```
**Output:**
```
[PROXY] TCP listening di 0.0.0.0:8888
[PROXY] Akan forward ke server di 127.0.0.1:8000
```

### 3. Jalankan Client (Laptop 3 atau Terminal 3)
```bash
cd python
python client.py
```
**Output:**
```
[CLIENT] Terhubung ke Proxy di 127.0.0.1:8888
[CLIENT] Server UDP di 127.0.0.1:5000

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

### 4. Test Setiap Menu
- Menu 1: Tambah tugas baru
- Menu 2: Lihat semua tugas
- Menu 3: Cek reminder
- Menu 4: Keluar

---

## 📚 Dokumentasi

### Baca Dalam Urutan Ini:
1. **Ini (README.md)** - Overview & quick start
2. **[0_INDEX_DOKUMENTASI.md](0_INDEX_DOKUMENTASI.md)** - Panduan baca doc
3. **[6_SKEMA_ARSITEKTUR.md](6_SKEMA_ARSITEKTUR.md)** - Pahami arsitektur
4. **[3_PANDUAN_IMPLEMENTASI_LENGKAP.md](3_PANDUAN_IMPLEMENTASI_LENGKAP.md)** - Detail kode
5. **[5_ANALISIS_EROR_AWAL.md](5_ANALISIS_EROR_AWAL.md)** - Error handling
6. **[2_PANDUAN_3_LAPTOP.md](2_PANDUAN_3_LAPTOP.md)** - Setup 3 laptop
7. **[4_LAPORAN_TUGAS_BESAR.md](4_LAPORAN_TUGAS_BESAR.md)** - Template laporan
8. **[7_CHECKLIST_PRESENTASI.md](7_CHECKLIST_PRESENTASI.md)** - Persiapan presentasi
9. **[8_QUICK_REFERENCE.md](8_QUICK_REFERENCE.md)** - Quick lookup

### Dokumentasi Fokus:

#### Untuk Mengerti Sistem:
- Baca: [6_SKEMA_ARSITEKTUR.md](6_SKEMA_ARSITEKTUR.md)
- Pelajari: Diagram alur TCP/UDP, port configuration

#### Untuk Setup 3 Laptop:
- Baca: [2_PANDUAN_3_LAPTOP.md](2_PANDUAN_3_LAPTOP.md)
- Ikuti: Step-by-step setup dengan IP configuration

#### Untuk Presentasi:
- Baca: [4_LAPORAN_TUGAS_BESAR.md](4_LAPORAN_TUGAS_BESAR.md) + [7_CHECKLIST_PRESENTASI.md](7_CHECKLIST_PRESENTASI.md)
- Siapkan: Slides, demo script, Q&A points

---

## ⚙️ Konfigurasi

### Untuk Localhost
Tidak perlu ubah - default `127.0.0.1` sudah bekerja

### Untuk 3 Laptop Berbeda
**Di `proxy.py` (Laptop 2):**
```python
SERVER_HOST = '192.168.1.10'  # Ganti dengan IP Laptop 1 (Server)
```

**Di `client.py` (Laptop 3):**
```python
PROXY_HOST = '192.168.1.20'   # Ganti dengan IP Laptop 2 (Proxy)
SERVER_HOST = '192.168.1.10'  # Ganti dengan IP Laptop 1 (Server)
```

Find IP:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

---

## 🐛 Error Handling

Sistem ini sudah diperbaiki dengan error handling untuk:
1. Array index out of bounds (request format validation)
2. Connection refused (server offline)
3. Invalid date format (deadline validation)

Baca detail: [5_ANALISIS_EROR_AWAL.md](5_ANALISIS_EROR_AWAL.md)

---

## 📊 Testing

### Quick Test Scenarios
```
Test 1: Add valid task          ✅ PASS
Test 2: Add invalid date        ✅ PASS (error handling)
Test 3: View tasks              ✅ PASS
Test 4: Check reminder          ✅ PASS
Test 5: Server offline error    ✅ PASS (graceful error)
```

Lihat: [8_QUICK_REFERENCE.md](8_QUICK_REFERENCE.md) - Test Scenarios section

---

## 📞 Troubleshooting

| Error | Solution |
|-------|----------|
| "Address already in use" | Kill existing process: `lsof -i :8000` |
| "Connection refused" | Server/Proxy belum running |
| "No route to host" | Cek IP address, verify network |
| "Format deadline salah" | Gunakan YYYY-MM-DD format |

Detail: [8_QUICK_REFERENCE.md](8_QUICK_REFERENCE.md) - Common Issues section

---

## ✅ Requirements Check

- ✅ Client-Proxy-Server architecture
- ✅ TCP protocol for reliable communication
- ✅ UDP support for fast response
- ✅ Error handling & input validation
- ✅ Can run on 3 laptops
- ✅ Complete documentation
- ✅ Ready for presentation

---

## 🎯 Next Steps

1. **Just Started?**
   - Baca dokumentasi urutan di atas
   - Run: `python python/webserver.py`, `proxy.py`, `client.py`
   - Test setiap menu

2. **For 3 Laptop?**
   - Find IP di setiap laptop
   - Update config di proxy.py & client.py
   - Follow: [2_PANDUAN_3_LAPTOP.md](2_PANDUAN_3_LAPTOP.md)

3. **For Presentation?**
   - Fill report: [4_LAPORAN_TUGAS_BESAR.md](4_LAPORAN_TUGAS_BESAR.md)
   - Checklist: [7_CHECKLIST_PRESENTASI.md](7_CHECKLIST_PRESENTASI.md)
   - Take screenshots & save logs

---

## 📄 License

Educational project for "Tugas Besar Jaringan Komputer Modul 8"

---

## 📝 Author

**Kelompok: [Nama Kelompok]**  
**NIM: [3 NIMs]**  
**Kelas: [Class Name]**  
**Tanggal: May 21, 2026**

---

**Happy Learning! 🚀**

# 💻 Panduan Testing pada 1 Laptop (Localhost)

Testing lengkap sistem Client-Proxy-Server pada satu mesin dengan 3 terminal terpisah.

---

## ✅ Keuntungan Testing 1 Laptop

- 🚀 **Setup Instant** - Default sudah localhost, tidak perlu konfigurasi IP
- ✅ **Mudah & Cepat** - Bisa dijalankan dalam 2 menit
- 🐛 **Debug Lebih Mudah** - Semua proses di satu mesin
- 📊 **Stabil** - Tidak ada network latency/packet loss
- ✅ **Test Logic** - Fokus pada functionality, error handling, input validation
- 🎯 **Ideal untuk**: Learning, development, quick testing

---

## ⚠️ Kekurangan (vs 3 Laptop)

- ❌ Tidak demo real networking (hanya loopback)
- ❌ Latency terlalu kecil (microsecond, tidak real)
- ❌ Tidak ada network topology yang visible
- ❌ Kurang impressive untuk presentasi

---

## 🚀 Quick Start (Copy-Paste Ready)

### LANGKAH 1: Buka 3 Command Prompt / PowerShell

Buka Command Prompt atau PowerShell **3 kali** (atau gunakan terminal di VS Code).

---

### LANGKAH 2: Terminal 1 - Jalankan Server

**Copy-paste ini:**
```bash
cd c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python
python webserver.py
```

**Expected Output:**
```
[SERVER] TCP listening di 0.0.0.0:8000
[SERVER] UDP listening di 0.0.0.0:5000
```

✅ **Jika output seperti ini, SERVER SUKSES RUNNING**

Biarkan terminal ini berjalan (jangan di-close).

---

### LANGKAH 3: Terminal 2 - Jalankan Proxy

**Di terminal baru, copy-paste ini:**
```bash
cd c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python
python proxy.py
```

**Expected Output:**
```
[PROXY] TCP listening di 0.0.0.0:8888
[PROXY] Akan forward ke server di 127.0.0.1:8000
```

✅ **Jika output seperti ini, PROXY SUKSES RUNNING**

Biarkan terminal ini berjalan (jangan di-close).

---

### LANGKAH 4: Terminal 3 - Jalankan Client

**Di terminal baru, copy-paste ini:**
```bash
cd c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python
python client.py
```

**Expected Output:**
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

✅ **Jika menu muncul, CLIENT SUKSES TERHUBUNG**

---

## 📝 Test Scenarios (Lakukan di Terminal 3 - Client)

### Test 1: Tambah Tugas (Valid)

**Input:**
```
1
Jaringan Komputer
Tubes Jarkom
2026-05-25
```

**Expected Output:**
```
Masukkan nama matkul: Jaringan Komputer
Masukkan judul tugas: Tubes Jarkom
Masukkan deadline (YYYY-MM-DD): 2026-05-25

✅ SUCCESS: Tugas 'Tubes Jarkom' berhasil ditambahkan!

========================================
   SISTEM MANAJEMEN TUGAS
========================================
Pilih menu (1-4): 
```

✅ **PASS** - Tugas ditambahkan & response TCP diterima

---

### Test 2: Tambah Tugas (Deadline Invalid - Error Handling)

**Input:**
```
1
Basis Data
Praktikum
25-05-2026
```

**Expected Output:**
```
Masukkan nama matkul: Basis Data
Masukkan judul tugas: Praktikum
Masukkan deadline (YYYY-MM-DD): 25-05-2026

❌ ERROR: Format tanggal salah. Gunakan YYYY-MM-DD (contoh: 2026-05-25)

========================================
   SISTEM MANAJEMEN TUGAS
========================================
Pilih menu (1-4): 
```

✅ **PASS** - Error handling bekerja (webserver.py validate date)

---

### Test 3: Lihat Semua Tugas

**Input:**
```
2
```

**Expected Output:**
```
========================================
    DAFTAR TUGAS
========================================

Tugas 1:
  Matkul: Jaringan Komputer
  Judul: Tubes Jarkom
  Deadline: 2026-05-25

Tugas 2:
  Matkul: Basis Data
  Judul: Praktikum
  Deadline: 2026-06-10

========================================
   SISTEM MANAJEMEN TUGAS
========================================
Pilih menu (1-4): 
```

✅ **PASS** - Server return task list

---

### Test 4: Cek Reminder (Deadline Dekat)

**Tambah tugas dengan deadline hari ini atau besok:**
```
1
Web Programming
Assignment
2026-05-21
```

**Lalu cek reminder:**
```
3
```

**Expected Output:**
```
========================================
    REMINDER DEADLINE
========================================

⏰ ALERT! Tugas dengan deadline dekat (≤1 hari):

Tugas 1:
  Matkul: Web Programming
  Judul: Assignment
  Deadline: 2026-05-21
  Hari tersisa: 0 hari (HARI INI!)

========================================
   SISTEM MANAJEMEN TUGAS
========================================
Pilih menu (1-4): 
```

✅ **PASS** - Reminder logic bekerja

---

### Test 5: Lihat Reminder (Tidak Ada Deadline Dekat)

Jika tidak ada deadline ≤1 hari:

**Expected Output:**
```
========================================
    REMINDER DEADLINE
========================================

✅ Tidak ada tugas dengan deadline dekat.

========================================
   SISTEM MANAJEMEN TUGAS
========================================
Pilih menu (1-4): 
```

✅ **PASS** - Conditional logic bekerja

---

### Test 6: Keluar dari Program

**Input:**
```
4
```

**Expected Output:**
```
Terima kasih! Keluar dari aplikasi.
```

**Terminal client menutup, prompt kembali**

✅ **PASS** - Exit handler bekerja

---

## 🐛 Error Handling Tests

### Test 7: Stop Server, Lalu Test Client

**Di Terminal 1:**
- Press `Ctrl+C` untuk stop server

**Di Terminal 3 (Client):**
```
1
Jarkom
Test
2026-05-25
```

**Expected Output:**
```
❌ ERROR: Tidak bisa connect ke Proxy di 127.0.0.1:8888
   Pastikan proxy.py sudah dijalankan di server!
```

✅ **PASS** - Error handling untuk connection fail

---

### Test 8: Invalid Request Format (Missing Data)

User langsung tekan Enter tanpa input nama matkul.

**Expected Behavior:**
- Client akan prompt ulang
- Atau server akan reject jika format salah

✅ **PASS** - Input validation bekerja

---

### Test 9: Array Index Test (Edge Case)

**Input (hanya 2 field, seharusnya 4):**
```
1
Jarkom
```

**Expected:**
- Server will validate `len(parts) != 4`
- Return ERROR

✅ **PASS** - Proteksi array index out of bounds

---

## 📊 Testing Checklist

Tandai ketika sudah test:

- [ ] **Server Starting** - Port 8000 listening
- [ ] **Proxy Starting** - Port 8888 listening
- [ ] **Client Starting** - Connected ke proxy
- [ ] **Test 1** - Tambah tugas valid
- [ ] **Test 2** - Tambah tugas invalid date
- [ ] **Test 3** - Lihat semua tugas
- [ ] **Test 4** - Cek reminder (ada deadline dekat)
- [ ] **Test 5** - Cek reminder (tidak ada)
- [ ] **Test 6** - Exit program
- [ ] **Test 7** - Error handling server offline
- [ ] **Test 8** - Input validation
- [ ] **Test 9** - Array index protection

---

## 💾 Dokumentasi Test Results

Setelah testing, catat hasilnya:

### Format Hasil Test

```
Testing Date: 21 Mei 2026
Tester: [Nama]
Machine: 1 Laptop (Localhost)

RESULTS:
✅ Test 1: PASS
✅ Test 2: PASS
✅ Test 3: PASS
✅ Test 4: PASS
✅ Test 5: PASS
✅ Test 6: PASS
✅ Test 7: PASS
✅ Test 8: PASS
✅ Test 9: PASS

Total: 9/9 PASS ✅

Notes:
- Semua functionality berjalan normal
- Error handling bekerja sesuai spec
- Response time cepat
```

---

## 🎯 Troubleshooting

### ❌ Error: "Address already in use"

**Masalah:** Port 8000 atau 8888 sudah dipakai program lain

**Solusi:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

netstat -ano | findstr :8888
taskkill /PID [PID_NUMBER] /F
```

Kemudian jalankan ulang server & proxy.

---

### ❌ Error: "ModuleNotFoundError: No module named 'socket'"

**Masalah:** Python tidak terinstall dengan benar

**Solusi:**
```bash
python --version
```

Harus menampilkan Python 3.6+ (contoh: Python 3.9.0)

---

### ❌ Client: "Connection refused"

**Masalah:** 
- Server/proxy belum running
- Port salah

**Solusi:**
1. Pastikan Terminal 1 & 2 menampilkan "listening" message
2. Jangan close Terminal 1 & 2 saat running Terminal 3

---

### ❌ Deadline format error terus

**Masalah:** Format input salah

**Solusi:**
```
Format BENAR:  2026-05-25 (YYYY-MM-DD)
Format SALAH:  25-05-2026
Format SALAH:  05/25/2026
Format SALAH:  May 25, 2026
```

---

## ⏱️ Estimated Testing Time

| Test | Duration |
|------|----------|
| Setup (3 terminal) | 1 menit |
| Start server | 10 detik |
| Start proxy | 10 detik |
| Start client | 10 detik |
| Test 1-9 | 5 menit |
| **Total** | **7-8 menit** |

---

## ✨ Success Criteria

Jika semua ini tercapai, testing **SUKSES**:

✅ Ketiga file running tanpa error  
✅ Client terhubung ke proxy  
✅ Menu tampil di client  
✅ Semua 9 test case pass  
✅ Error handling bekerja  
✅ Exit program normal  
✅ Tidak ada crash/hanging  

---

## 📸 Dokumentasi Screenshot (Optional)

Untuk presentasi lebih baik, capture:

1. **3 Terminal Running** - Screenshot menunjukkan ketiga terminal
2. **Test Add Task** - Input & output pada menu 1
3. **Test View Task** - Output menu 2
4. **Test Reminder** - Output menu 3
5. **Error Test** - Output ketika ada error

Save ke folder: `testing/screenshots/`

---

**Happy Testing! 🚀**

---

Version: 1.0  
Created: May 21, 2026  
For: Tugas Besar Jaringan Komputer Module 8

# 📖 Dokumentasi - Tugas Besar Jaringan Komputer

Folder ini berisi semua dokumentasi untuk Tugas Besar Jaringan Komputer (Modul 8).

## 📑 Daftar File Dokumentasi

### 1. **README.md** ⭐ (Mulai dari sini!)
   - Overview sistem
   - Quick start guide
   - Penjelasan 3 file Python
   - Konfigurasi IP
   - Troubleshooting basic

   **Waktu baca:** ~10 menit

---

### 2. **PANDUAN_3_LAPTOP.md** 🖥️
   - Setup untuk 3 laptop berbeda
   - Cara identifikasi IP
   - Step-by-step configuration
   - Testing scenarios di 3 laptop
   - Troubleshooting advanced

   **Waktu baca:** ~15 menit | **Waktu praktik:** ~30 menit

---

### 3. **PANDUAN_IMPLEMENTASI_LENGKAP.md** 💻
   - Skema arsitektur dengan diagram
   - Port & protocol configuration
   - Source code lengkap dengan penjelasan
   - Error handling yang ditambahkan
   - Pembagian tugas kelompok

   **Waktu baca:** ~20 menit | **Detail untuk review code**

---

### 4. **LAPORAN_TUGAS_BESAR.md** 📋 (IMPORTANT!)
   - Template laporan profesional
   - Struktur sesuai standard
   - Include testing results
   - QoS analysis template
   - Cocok untuk presentasi

   **Waktu baca:** ~25 menit | **Untuk membuat laporan presentasi**

---

### 5. **ANALISIS_EROR_AWAL.md** 🐛
   - Dokumentasi 4 error yang ditemukan
   - Penjelasan masalah & penyebab
   - Contoh crash & skenario
   - Solusi perbaikan untuk setiap error
   - Before-after code comparison

   **Waktu baca:** ~15 menit | **Untuk memahami error handling**

---

### 6. **SKEMA_ARSITEKTUR.md** 📊
   - Diagram topologi jaringan (ASCII art)
   - Alur komunikasi detail
   - Skenario 1: Add Task
   - Skenario 2: Get Tasks
   - Skenario 3: Error handling
   - Port & protocol configuration table
   - Error handling flow diagram

   **Waktu baca:** ~15 menit | **Visual reference**

---

## 🎯 Baca Sesuai Kebutuhan

### Scenario 1: "Saya baru pertama kali. Mau tahu overview sistem."
1. Baca: **README.md** (5 menit)
2. Lihat: **SKEMA_ARSITEKTUR.md** - Diagram topologi (5 menit)
3. Jalankan: Quick Start di README (15 menit)

**Total: ~25 menit**

---

### Scenario 2: "Saya mau test di 3 laptop berbeda."
1. Baca: **PANDUAN_3_LAPTOP.md** (15 menit)
2. Setup config di proxy.py & client.py (10 menit)
3. Run di 3 laptop & test (30 menit)
4. Capture screenshots untuk laporan (10 menit)

**Total: ~65 menit**

---

### Scenario 3: "Saya mau memahami implementasi detail kode."
1. Baca: **PANDUAN_IMPLEMENTASI_LENGKAP.md** (20 menit)
2. Review: Error handling di **ANALISIS_EROR_AWAL.md** (15 menit)
3. Review: Source code di `python/` folder (15 menit)

**Total: ~50 menit**

---

### Scenario 4: "Saya mau membuat laporan & presentasi."
1. Open: **LAPORAN_TUGAS_BESAR.md**
2. Fill: Identitas kelompok, deskripsi sistem, hasil testing
3. Attach: Screenshots dari testing
4. Include: QoS analysis results
5. Finalize: Kesimpulan & referensi

**Total: ~45 menit (+ testing time)**

---

### Scenario 5: "Ada error. Gimana troubleshoot?"
1. Check: Troubleshooting di **README.md** (5 menit)
2. Check: Troubleshooting di **PANDUAN_3_LAPTOP.md** (5 menit)
3. Check: Error flow di **SKEMA_ARSITEKTUR.md** (5 menit)
4. Check: Error details di **ANALISIS_EROR_AWAL.md** (5 menit)

**Total: ~20 menit**

---

## 📊 Dokumentasi Summary

| File | Fokus | Untuk Siapa |
|------|-------|-----------|
| README.md | Overview & Quick Start | Semua orang |
| PANDUAN_3_LAPTOP.md | Multi-laptop setup | Laptop 2 & 3 lead |
| PANDUAN_IMPLEMENTASI_LENGKAP.md | Code & architecture | Backend/Network lead |
| LAPORAN_TUGAS_BESAR.md | Report & presentation | Testing lead |
| ANALISIS_EROR_AWAL.md | Error handling | Programmer |
| SKEMA_ARSITEKTUR.md | Visual reference | Visual learner |

---

## 🔗 Hubungan Antar File

```
INDEX.md (Root)
    ├─→ README.md (Start here!)
    │   ├─→ PANDUAN_3_LAPTOP.md (For multi-laptop)
    │   ├─→ Troubleshooting section
    │   └─→ Configuration section
    │
    ├─→ PANDUAN_IMPLEMENTASI_LENGKAP.md (Detail)
    │   ├─→ SKEMA_ARSITEKTUR.md (Visual)
    │   └─→ python/ folder (Code)
    │
    ├─→ LAPORAN_TUGAS_BESAR.md (Report template)
    │   ├─→ Need ANALISIS_EROR_AWAL.md info
    │   └─→ Need SKEMA_ARSITEKTUR.md diagrams
    │
    └─→ ANALISIS_EROR_AWAL.md (Error reference)
        └─→ Explained in PANDUAN_IMPLEMENTASI_LENGKAP.md
```

---

## ✅ Reading Order (Recommended)

### For Complete Understanding:
1. **README.md** - Get overview
2. **SKEMA_ARSITEKTUR.md** - Understand architecture
3. **PANDUAN_IMPLEMENTASI_LENGKAP.md** - Deep dive code
4. **ANALISIS_EROR_AWAL.md** - Learn about errors
5. **PANDUAN_3_LAPTOP.md** - If testing with 3 laptops
6. **LAPORAN_TUGAS_BESAR.md** - For report writing

---

## 🎓 Learning Path

```
START HERE
    ↓
README.md (10 min)
    ├─→ Overview ✓
    ├─→ Quick Start ✓
    └─→ Basic Troubleshooting ✓
    
    ↓
SKEMA_ARSITEKTUR.md (15 min)
    ├─→ Network topology ✓
    ├─→ Communication flow ✓
    └─→ Port configuration ✓
    
    ↓
PANDUAN_IMPLEMENTASI_LENGKAP.md (20 min)
    ├─→ Architecture detail ✓
    ├─→ Code explanation ✓
    └─→ Error handling ✓
    
    ↓
ANALISIS_EROR_AWAL.md (15 min)
    ├─→ 4 errors found ✓
    ├─→ Solutions ✓
    └─→ Code comparison ✓
    
    ↓
PANDUAN_3_LAPTOP.md (15 min)
    ├─→ Multi-laptop setup ✓
    └─→ Testing scenarios ✓
    
    ↓
LAPORAN_TUGAS_BESAR.md (25 min)
    ├─→ Report structure ✓
    ├─→ Testing results ✓
    └─→ QoS analysis ✓
    
    ↓
READY FOR PRESENTATION! ✓
```

---

## 📚 Quick Reference Links

- **Jalankan testing:** See README.md → Quick Start
- **Setup 3 laptop:** See PANDUAN_3_LAPTOP.md → Step-by-Step
- **Pahami kode:** See PANDUAN_IMPLEMENTASI_LENGKAP.md → Implementation
- **Error handling:** See ANALISIS_EROR_AWAL.md → 4 Errors
- **Skema & diagram:** See SKEMA_ARSITEKTUR.md → Architecture
- **Buat laporan:** See LAPORAN_TUGAS_BESAR.md → Report

---

## 💡 Tips

1. **Jangan skip README.md** - Itu overview penting
2. **Buat screenshot saat testing** - Untuk laporan
3. **Update config sebelum multi-laptop** - Jangan lupa IP
4. **Test error scenarios** - Lihat ANALISIS_EROR_AWAL.md
5. **Fill laporan sambil testing** - Jangan tunggu presentasi

---

## 📝 Checklist

- [ ] Baca README.md
- [ ] Lihat SKEMA_ARSITEKTUR.md
- [ ] Test di localhost (Quick Start)
- [ ] Baca PANDUAN_IMPLEMENTASI_LENGKAP.md
- [ ] Review ANALISIS_EROR_AWAL.md
- [ ] Setup & test di 3 laptop (gunakan PANDUAN_3_LAPTOP.md)
- [ ] Capture screenshots
- [ ] Fill LAPORAN_TUGAS_BESAR.md
- [ ] Practice presentasi

---

**Good luck! 🎉**

Version: 1.0 | Last Updated: May 21, 2026

# ⚡ QUICK REFERENCE - Tugas Besar Jaringan Komputer

Referensi cepat untuk informasi penting tanpa harus membaca dokumentasi panjang.

---

## 🚀 Quick Start (3 Terminal)

### Terminal 1: Server
```bash
cd python
python webserver.py
```

### Terminal 2: Proxy
```bash
cd python
python proxy.py
```

### Terminal 3: Client
```bash
cd python
python client.py
```

---

## 📋 Request Format

```
ADD|matkul|judul|deadline    ← Tambah tugas
GET                          ← Lihat tugas
REMINDER                     ← Cek reminder
```

---

## 🔧 Configuration (untuk 3 Laptop)

### File: python/proxy.py (Laptop 2)
```python
SERVER_HOST = '192.168.1.10'  # UBAH ke IP Laptop 1
```

### File: python/client.py (Laptop 3)
```python
PROXY_HOST = '192.168.1.20'   # UBAH ke IP Laptop 2
SERVER_HOST = '192.168.1.10'  # UBAH ke IP Laptop 1
```

### Find IP Address

**Windows:**
```bash
ipconfig
```

**Linux/Mac:**
```bash
ifconfig
```

---

## 📌 Port Reference

| Component | Port | Protocol |
|-----------|------|----------|
| Server | 8000 | TCP |
| Server | 5000 | UDP |
| Proxy | 8888 | TCP |

---

## ⚠️ Common Issues & Quick Fix

| Issue | Fix |
|-------|-----|
| "Address already in use" | Kill process: `lsof -i :8000` |
| "Connection refused" | Pastikan server.py running |
| Proxy can't connect | Cek IP di SERVER_HOST |
| Client can't connect | Cek PROXY_HOST di client.py |
| Date format error | Gunakan YYYY-MM-DD |
| Array index error | Pastikan format request benar |

---

## 📊 Quick Test Scenarios

### Test 1: Add Valid Task
```
Input: Jarkom | Tubes | 2026-05-25
Expected: SUCCESS message
Status: ✅ PASS
```

### Test 2: Add Invalid Date
```
Input: Jarkom | Tubes | 25-05-2026
Expected: ERROR message
Status: ✅ PASS (Error handling)
```

### Test 3: View Tasks
```
Menu: 2
Expected: Task list
Status: ✅ PASS
```

### Test 4: Check Reminder
```
Menu: 3
Expected: Reminder list
Status: ✅ PASS
```

### Test 5: Server Offline
```
Stop server, run client
Expected: ERROR (graceful)
Status: ✅ PASS
```

---

## 📂 File Locations

| File | Location | Purpose |
|------|----------|---------|
| webserver.py | `python/` | Server |
| proxy.py | `python/` | Proxy |
| client.py | `python/` | Client |
| README | `dokumentasi/1_README.md` | Overview |
| 3 Laptop Setup | `dokumentasi/2_PANDUAN_3_LAPTOP.md` | Setup |
| Error Analysis | `dokumentasi/5_ANALISIS_EROR_AWAL.md` | Errors |
| Architecture | `dokumentasi/6_SKEMA_ARSITEKTUR.md` | Diagrams |

---

## 🎯 4 Errors Fixed

| # | Error | File | Fix |
|---|-------|------|-----|
| 1 | Array Index | webserver.py | Validate len |
| 2 | Connection Refused | proxy.py | Try-except |
| 3 | Connection Refused | client.py | Try-except |
| 4 | Invalid Date | webserver.py | Try-except |

---

## ✅ Pre-Presentation Checklist

- [ ] All 3 files run without error
- [ ] Test all menu (1, 2, 3, 4)
- [ ] Test error handling
- [ ] Capture screenshots
- [ ] Fill LAPORAN
- [ ] Review dokumentasi
- [ ] Practice presentation
- [ ] Prepare explanation

---

## 🏆 Success Criteria

✅ Code runs without error  
✅ All 3 files work together  
✅ Error handling implemented  
✅ Can test on 3 laptops  
✅ Documentation complete  
✅ Presentation ready  
✅ Group (3 people) all participate  

---

**Good luck! 🚀**

Version: 1.0 | Last Updated: May 21, 2026

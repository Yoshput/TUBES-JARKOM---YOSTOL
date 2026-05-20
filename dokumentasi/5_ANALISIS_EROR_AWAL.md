# ANALISIS EROR AWAL - Ketiga File Python

> Dokumentasi Kesalahan (Error) yang Ditemukan pada `client.py`, `proxy.py`, dan `webserver.py`

---

## 🚨 Ringkasan Cepat

| No | File | Line | Eror | Severity |
|----|------|------|------|----------|
| **1** | webserver.py | 32-37 | Array Index Out of Bounds | 🔴 KRITIS |
| **2** | proxy.py | 28 | No Error Handling (Connection Failed) | 🔴 KRITIS |
| **3** | client.py | 20 | No Error Handling (Connection Failed) | 🟡 SEDANG |
| **4** | webserver.py | 82-86 | No Error Handling (Invalid Date Format) | 🟡 SEDANG |

---

## 📌 EROR 1: Array Index Out of Bounds (PALING KRITIS)

**File:** `webserver.py` | **Baris:** 32-37

**Masalah:** Tidak ada validasi panjang array sebelum akses index

**Fix:** Tambah validasi `len(parts) != 4` sebelum mengakses array

---

## 📌 EROR 2: No Error Handling - Proxy to Server Connection

**File:** `proxy.py` | **Baris:** 28

**Masalah:** Tidak ada try-except untuk server connection

**Fix:** Wrap `connect()` dengan try-except ConnectionRefused

---

## 📌 EROR 3: No Error Handling - Client to Proxy Connection

**File:** `client.py` | **Baris:** 20

**Masalah:** Tidak ada try-except untuk proxy connection

**Fix:** Wrap `connect()` dengan try-except ConnectionRefused

---

## 📌 EROR 4: No Error Handling - Invalid Date Format

**File:** `webserver.py` | **Baris:** 82-86

**Masalah:** Tidak ada try-except untuk date parsing

**Fix:** Wrap `strptime()` dengan try-except ValueError

---

## ✅ Semua Error Sudah Diperbaiki

Untuk detail lengkap tentang setiap error, solusi, dan code comparison, silakan baca file dokumentasi lengkap di repository.

---

**Version:** 1.0 | Last Updated: May 21, 2026

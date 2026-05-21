# TEST SCENARIOS
## Skenario Pengujian Lengkap - Tugas Besar Jaringan Komputer

---

## SCENARIO 1: Basic HTTP GET Through Proxy

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2
python proxy.py

# Terminal 3
python client.py --mode tcp
```

### Expected Flow
```
CLIENT                      PROXY                    WEB SERVER
  |                           |                          |
  |----GET / ------->         |                          |
  |                   |----GET / ------->                |
  |                   |                    |--read file--|
  |                   |<----response--------|             |
  |<----response------|                                   |
  |
  |----(cache HIT)---->
  |<----response-----|
```

### Expected Output

**Web Server:**
```
[10:15:30.123] [SUCCESS] TCP Server listening on localhost:8000
[10:15:45.456] [INFO] 127.0.0.1 - GET /
[10:15:45.457] [SUCCESS] 127.0.0.1 - GET / - 200
```

**Proxy:**
```
[10:15:35.123] [SUCCESS] Proxy Server listening on localhost:8080
[10:15:45.456] [CACHE_MISS] 127.0.0.1 - GET / - 200 [MISS] (23.4ms)
[10:15:46.123] [CACHE_HIT] 127.0.0.1 - GET / - 200 [HIT] (1.2ms)
```

**Client:**
```
[10:15:45.456] [SUCCESS] GET / - HTTP/1.1 200 OK (23.5ms, 3456 bytes)
[10:15:46.123] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (1.3ms, 3456 bytes)
```

### Verification
- ✓ Response kembali ke client
- ✓ Cache MISS di request pertama
- ✓ Cache HIT di request kedua
- ✓ Response time lebih cepat saat HIT
- ✓ File cache tercipta di folder `cache/`

---

## SCENARIO 2: Multiple Concurrent Clients

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2
python proxy.py

# Terminal 3, 4, 5 (jalankan bersamaan)
python client.py --mode tcp
python client.py --mode tcp
python client.py --mode tcp
```

### Expected Behavior
- Semua client mendapat response
- Proxy handle concurrent requests
- No race condition
- Cache shared antar clients

### Expected Output di Proxy

```
[10:16:00.123] [INFO] 127.0.0.1 - GET /
[10:16:00.124] [INFO] 127.0.0.1 - GET /page.html
[10:16:00.125] [INFO] 127.0.0.1 - GET /
[10:16:00.234] [CACHE_MISS] 127.0.0.1 - GET / - 200 [MISS] (22.4ms)
[10:16:00.235] [CACHE_MISS] 127.0.0.1 - GET /page.html - 200 [MISS] (24.3ms)
[10:16:00.236] [CACHE_HIT] 127.0.0.1 - GET / - 200 [HIT] (1.1ms)
```

### Verification
- ✓ Semua request tercatat di log
- ✓ Tidak ada error
- ✓ Response terkirim ke semua client
- ✓ Cache HIT terdeteksi dengan benar

---

## SCENARIO 3: UDP QoS Testing

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2 (UDP echo di port 9000 sudah berjalan)

# Terminal 3
python client.py --mode udp
```

### Expected Output
```
[10:16:15.123] [SUCCESS] UDP Mode - QoS Monitoring
[10:16:15.124] [INFO] Sending 10 UDP packets to localhost:9000

[10:16:15.125] [PING] Ping 1 - RTT=0.8ms from localhost
[10:16:15.226] [PING] Ping 2 - RTT=0.9ms from localhost
[10:16:15.327] [PING] Ping 3 - RTT=0.7ms from localhost
[10:16:15.428] [PING] Ping 4 - RTT=1.0ms from localhost
[10:16:15.529] [PING] Ping 5 - RTT=0.8ms from localhost
[10:16:15.630] [PING] Ping 6 - RTT=0.9ms from localhost
[10:16:15.731] [PING] Ping 7 - RTT=0.7ms from localhost
[10:16:15.832] [PING] Ping 8 - RTT=0.8ms from localhost
[10:16:15.933] [PING] Ping 9 - RTT=1.1ms from localhost
[10:16:16.034] [PING] Ping 10 - RTT=0.9ms from localhost

======================================================================
UDP QoS STATISTICS
======================================================================
Packets sent:        10
Packets received:    10
Packets timeout:     0
Packet loss:         0.0%
Min RTT:             0.7ms
Avg RTT:             0.86ms
Max RTT:             1.1ms
Avg Jitter:          0.13ms
Throughput:          1234.5 bytes/s
======================================================================
```

### Verification
- ✓ Semua 10 packet terkirim
- ✓ Semua packet terima echo
- ✓ Packet loss = 0%
- ✓ RTT berkisar 0.7-1.1ms
- ✓ Jitter < 0.2ms
- ✓ Statistics calculated correctly

---

## SCENARIO 4: Cache Hit/Miss Comparison

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2
python proxy.py

# Terminal 3
python client.py --mode tcp
```

### Expected Behavior

1. First request: MISS (not cached)
   - Web Server process request
   - Proxy forward ke server
   - Response cached
   - Response time: ~20-50ms

2. Second request: HIT (from cache)
   - Proxy read dari cache
   - No server contact
   - Response time: ~1-5ms

### Verification di Proxy Log
```
[10:16:30.123] [CACHE_MISS] 127.0.0.1 - GET /index.html - 200 [MISS] (45.2ms)
[10:16:31.123] [CACHE_HIT]  127.0.0.1 - GET /index.html - 200 [HIT]  (1.3ms)
```

- ✓ MISS time > HIT time (30-40x lebih cepat)
- ✓ Cache file ada di folder `cache/`
- ✓ Content cache sama dengan response

---

## SCENARIO 5: Error Handling - 404 Not Found

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2
python proxy.py

# Terminal 3
# Modify client.py untuk request path yang tidak ada, atau:
```

### Manual Request
```powershell
# Terminal 3
$sock = New-Object System.Net.Sockets.TcpClient
$sock.Connect('localhost', 8080)
$stream = $sock.GetStream()
$msg = "GET /notfound.html HTTP/1.1`r`nHost: localhost:8080`r`n`r`n"
$stream.Write([text.encoding]::ASCII.GetBytes($msg), 0, $msg.Length)
$reader = New-Object System.IO.StreamReader($stream)
$reader.ReadToEnd()
```

### Expected Output
```
HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 14
Connection: close

404 Not Found
```

### Verification di Proxy Log
```
[10:16:40.123] [ERROR] 127.0.0.1 - GET /notfound.html - 404
```

---

## SCENARIO 6: Error Handling - 502 Bad Gateway

### Setup
1. Jangan run webserver.py
2. Jalankan proxy.py
3. Jalankan client

### Expected Output

**Client:**
```
[10:16:50.123] [ERROR] GET / - HTTP/1.1 502 Bad Gateway
```

**Proxy Log:**
```
[10:16:50.123] [ERROR] 127.0.0.1 - GET / - 502 BAD GATEWAY
```

### Verification
- ✓ Proxy detect server tidak connect
- ✓ Return 502 Bad Gateway
- ✓ Not hang or crash

---

## SCENARIO 7: Timeout Handling - 504 Gateway Timeout

### Setup
Modifikasi `webserver.py` agar delay response > REQUEST_TIMEOUT (5s), atau:
```python
# Di handle_tcp_client, tambah:
time.sleep(10)  # Lebih dari 5 detik
```

### Expected Behavior
Proxy timeout saat tunggu response dari server

### Expected Output

**Client:**
```
[10:16:55.123] [ERROR] GET / - HTTP/1.1 504 Gateway Timeout
```

**Proxy Log:**
```
[10:16:55.123] [ERROR] 127.0.0.1 - GET / - 504 RESPONSE TIMEOUT
```

### Verification
- ✓ Timeout detected
- ✓ Return 504 Gateway Timeout
- ✓ Client tidak hang

---

## SCENARIO 8: Cache Statistics Monitoring

### Setup
```powershell
# Terminal 1
python webserver.py

# Terminal 2
python proxy.py

# Lihat log untuk statistik (printed setiap 30 request atau ~30 detik)
```

### Expected Output di Proxy
```
[10:16:10.123] [INFO] CACHE STATS - Total: 3, Hits: 1, Misses: 2, Hit Rate: 33.3%, Avg Time: 15.2ms
[10:16:40.456] [INFO] CACHE STATS - Total: 6, Hits: 4, Misses: 2, Hit Rate: 66.7%, Avg Time: 12.1ms
[10:17:10.789] [INFO] CACHE STATS - Total: 9, Hits: 7, Misses: 2, Hit Rate: 77.8%, Avg Time: 10.5ms
```

### Verification
- ✓ Hit rate meningkat seiring request
- ✓ Average time menurun saat cache warm
- ✓ Statistics accurate

---

## SCENARIO 9: File Serving - Different Content Types

### Setup
```powershell
python client.py --mode tcp
```

### Expected Responses

1. GET / → 200 OK (text/html)
2. GET /index.html → 200 OK (text/html, 3456 bytes)
3. GET /page.html → 200 OK (text/html, 4521 bytes)
4. GET /api/status → 200 OK (application/json, ~50 bytes)

### Expected Output
```
[10:17:15.123] [SUCCESS] GET / - HTTP/1.1 200 OK (45.2ms, 3456 bytes)
[10:17:15.234] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (1.2ms, 3456 bytes)
[10:17:15.345] [SUCCESS] GET /page.html - HTTP/1.1 200 OK (22.3ms, 4521 bytes)
[10:17:15.456] [SUCCESS] GET /api/status - HTTP/1.1 200 OK (1.3ms, 48 bytes)
```

### Verification
- ✓ Semua path serve correctly
- ✓ Content-Type correct
- ✓ Content-Length correct
- ✓ Body not empty

---

## SCENARIO 10: Graceful Shutdown

### Setup
1. Run semua server
2. Run client
3. Tekan Ctrl+C di setiap terminal

### Expected Output

**Web Server:**
```
^C
[10:17:30.123] [WARNING] Shutdown signal received
[10:17:30.124] [INFO] Graceful shutdown...
[10:17:30.125] [WARNING] TCP Server shutdown
[10:17:30.126] [WARNING] UDP Server shutdown
```

**Proxy:**
```
^C
[10:17:30.123] [WARNING] Shutdown signal received
[10:17:30.124] [INFO] Graceful shutdown...
[10:17:30.125] [WARNING] Proxy Server shutdown
```

**Client:**
```
[10:17:30.123] [SUCCESS] UDP Mode - QoS Monitoring
... (complete normally atau Ctrl+C)
```

### Verification
- ✓ No hanging processes
- ✓ Clean shutdown messages
- ✓ No incomplete requests
- ✓ Port freed up (dapat run ulang)

---

## AUTOMATION TEST SCRIPT

Buat file `test_all.ps1`:

```powershell
# Start all servers
$p1 = Start-Process python -ArgumentList "python\webserver.py" -PassThru
$p2 = Start-Process python -ArgumentList "python\proxy.py" -PassThru
Start-Sleep -Seconds 2

# Run TCP test
Write-Host "=== Testing TCP Mode ===" -ForegroundColor Green
python python\client.py --mode tcp

# Run UDP test
Write-Host "`n=== Testing UDP Mode ===" -ForegroundColor Green
python python\client.py --mode udp

# Cleanup
Stop-Process -Id $p1.Id -ErrorAction SilentlyContinue
Stop-Process -Id $p2.Id -ErrorAction SilentlyContinue

Write-Host "`nAll tests completed!" -ForegroundColor Green
```

### Run:
```powershell
powershell -ExecutionPolicy Bypass -File test_all.ps1
```

---

## PERFORMANCE BENCHMARKS

Expected results di localhost:

| Test | Expected | Unit |
|------|----------|------|
| TCP Response (MISS) | 20-50 | ms |
| TCP Response (HIT) | 1-5 | ms |
| UDP RTT | <1 | ms |
| Concurrent Clients | 5+ | clients |
| Cache Hit Rate | 70-90% | % |
| Packet Loss (UDP) | 0-5 | % |
| Throughput | 1000+ | bytes/s |


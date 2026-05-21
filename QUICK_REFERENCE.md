# QUICK REFERENCE GUIDE
## Cheat Sheet untuk Tugas Besar Jaringan Komputer

---

## 🚀 STARTUP (Copy-Paste Ready)

### Terminal 1: Web Server
```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python webserver.py
```

### Terminal 2: Proxy Server
```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python proxy.py
```

### Terminal 3: Client TCP
```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python client.py --mode tcp
```

### Terminal 4: Client UDP
```powershell
cd "c:\Yossika\KULIAH SEMESTER 4\JARINGAN KOMPUTER\Tubes Jarkom\python"
python client.py --mode udp
```

---

## 🔗 HTTP ENDPOINTS

| Endpoint | Port | Expected |
|----------|------|----------|
| http://localhost:8000/ | 8000 | 200 OK (3456 bytes) |
| http://localhost:8000/index.html | 8000 | 200 OK (3456 bytes) |
| http://localhost:8000/page.html | 8000 | 200 OK (4521 bytes) |
| http://localhost:8000/api/status | 8000 | 200 OK (JSON) |
| http://localhost:8080/ | 8080 | Proxy redirect |

Browser: Open any of these URLs after starting servers

---

## 📊 PORTS REFERENCE

| Port | Service | Type | Function |
|------|---------|------|----------|
| 8000 | Web Server TCP | TCP | HTTP requests |
| 9000 | Web Server UDP | UDP | Echo/QoS |
| 8080 | Proxy Server | TCP | Caching & forwarding |

---

## 📝 COMMAND REFERENCE

### Run Everything at Once
```powershell
# Terminal 1
python webserver.py
# Ctrl+C to stop

# Terminal 2
python proxy.py
# Ctrl+C to stop

# Terminal 3
python client.py --mode tcp

# Terminal 4
python client.py --mode udp
```

### Testing Multiple Clients
```powershell
# Terminal 3, 4, 5
python client.py --mode tcp
python client.py --mode tcp
python client.py --mode tcp
```

### View Logs Real-Time
```powershell
# In a new terminal
Get-Content logs/webserver.log -Wait
Get-Content logs/proxy.log -Wait
```

### Check Cache
```powershell
# See what's cached
dir cache/
Get-ChildItem cache/ -Recurse

# View cache file content
cat cache/index.html.cache | more
```

### Check Port Usage
```powershell
netstat -ano | findstr ":8000\|:8080\|:9000"
```

---

## ✅ VERIFICATION CHECKLIST

Quick verification:
```powershell
# ✓ 1. Check files exist
ls python/client.py, python/proxy.py, python/webserver.py

# ✓ 2. Check HTML files
ls files/index.html, files/page.html

# ✓ 3. Start web server
cd python
python webserver.py
# Press Ctrl+C after confirming output

# ✓ 4. Check ports are available
netstat -ano | findstr ":8000\|:8080\|:9000"
# Should show nothing (ports free)

# ✓ 5. Run full test
python webserver.py &
python proxy.py &
python client.py --mode tcp
```

---

## 📊 EXPECTED OUTPUT EXAMPLES

### Web Server Starting
```
[2024-05-21 10:15:30.123] [SUCCESS] TCP Server listening on localhost:8000
[2024-05-21 10:15:30.124] [SUCCESS] UDP Server listening on localhost:9000
```

### Proxy Starting
```
[2024-05-21 10:15:35.123] [SUCCESS] Proxy Server listening on localhost:8080
[2024-05-21 10:15:35.124] [INFO] Forwarding to localhost:8000
```

### Client TCP Output
```
[10:15:45.456] [SUCCESS] GET / - HTTP/1.1 200 OK (45.2ms, 3456 bytes)
[10:15:45.589] [SUCCESS] GET /index.html - HTTP/1.1 200 OK (1.3ms, 3456 bytes)
```

### Client UDP Output
```
[10:16:15.125] [PING] Ping 1 - RTT=0.8ms from localhost
[10:16:15.226] [PING] Ping 2 - RTT=0.9ms from localhost
...
Min RTT:             0.7ms
Avg RTT:             0.86ms
Max RTT:             1.1ms
Packet Loss:         0.0%
```

### Proxy Cache Stats
```
[INFO] CACHE STATS - Total: 6, Hits: 4, Misses: 2, Hit Rate: 66.7%, Avg Time: 12.1ms
```

---

## 🔧 CONFIGURATION

Default settings in code:

```python
# webserver.py
HOST = 'localhost'
TCP_PORT = 8000
UDP_PORT = 9000

# proxy.py
PROXY_HOST = 'localhost'
PROXY_PORT = 8080
SERVER_HOST = 'localhost'
SERVER_PORT = 8000
REQUEST_TIMEOUT = 5

# client.py
PROXY_HOST = 'localhost'
PROXY_PORT = 8080
SERVER_HOST = 'localhost'
SERVER_UDP_PORT = 9000
REQUEST_TIMEOUT = 5
UDP_TIMEOUT = 1
```

To change: Edit these values in each file before running

---

## 🐛 TROUBLESHOOTING QUICK FIXES

### Problem: "Port already in use"
```powershell
# Find process using port
netstat -ano | findstr ":8000"
# Kill process
taskkill /PID <PID> /F
```

### Problem: "Connection refused"
- Make sure webserver.py is running in Terminal 1
- Make sure proxy.py is running in Terminal 2
- Wait 2 seconds after starting each server

### Problem: "No cache files created"
- Manually request same path twice in TCP mode
- First request = MISS, second = HIT
- Cache file appears in `cache/` folder

### Problem: "Colored output not showing"
- Windows 10+: Should work automatically
- Windows 7/8: Install ANSI support or run in Windows Terminal
- Alternative: Use Git Bash or PowerShell

### Problem: "ModuleNotFoundError"
- Check import statements have NO external libraries
- Only: socket, threading, os, time, datetime, sys, hashlib
- All are built-in, no pip install needed

---

## 📈 PERFORMANCE QUICK CHECK

Expected times on localhost:

```
TCP GET / (first time):    20-50ms  (MISS, cache created)
TCP GET / (second time):   1-5ms    (HIT, from cache)
TCP GET /index.html:       20-50ms  (MISS)
TCP GET /index.html:       1-5ms    (HIT)
UDP Ping RTT:              <1ms
UDP 10 packets:            ~1.2 seconds total
```

If times much longer:
- Check CPU usage (might be high)
- Check memory usage
- Reduce concurrent clients

---

## 📋 TESTING MATRIX

Quick test reference:

| Test | Command | Expected |
|------|---------|----------|
| TCP basic | `client.py --mode tcp` | 4 responses, 200 OK |
| UDP ping | `client.py --mode udp` | 10 packets, 0% loss |
| Cache HIT | 2nd TCP request | Time <5ms |
| 5 clients | Run 5 `client.py --mode tcp` | All get response |
| Error 404 | `GET /badpath` | 404 response |
| Error 502 | Kill webserver, test | 502 response |

---

## 📚 DOCUMENTATION MAP

```
PROJECT_README.md
├── Overview & setup
└── Links to:

SETUP_AND_RUNNING_GUIDE.md
├── Detailed setup steps
├── Configuration
└── Troubleshooting

COMPLIANCE_CHECKLIST.md
├── Requirements verification
├── Feature checklist
└── Quality metrics

TEST_SCENARIOS.md
├── 10 test scenarios
├── Expected output
└── Verification steps

WIRESHARK_GUIDE.md
├── Packet capture setup
├── Analysis techniques
└── Filter examples
```

---

## 🎯 FINAL CHECKLIST (Before Submission)

```
[ ] All 3 Python files present
[ ] Web server runs on port 8000
[ ] Proxy runs on port 8080
[ ] UDP echo on port 9000
[ ] Client TCP mode works
[ ] Client UDP mode shows statistics
[ ] Cache folder created when running
[ ] Logs folder created when running
[ ] HTML files serve from browser
[ ] Colored output visible
[ ] No external dependencies imported
[ ] Graceful shutdown works (Ctrl+C)
[ ] Concurrent clients work
[ ] Documentation complete
[ ] All scenarios tested
```

---

## 💡 TIPS & TRICKS

### Speed Up Testing
```powershell
# Start all in one go (use & to run in background)
python webserver.py &; python proxy.py &; python client.py --mode tcp
```

### Monitor Cache Size
```powershell
# Watch cache growing
while($true) { Clear-Host; dir cache/ -Recurse | Measure-Object -Sum Length | select Count, "Sum"; sleep 1 }
```

### Clear Cache Between Tests
```powershell
# Delete all cache files
rm cache/* -Force
```

### Capture with Wireshark
```
1. Start Wireshark
2. Select loopback interface
3. Filter: tcp.port == 8080 or tcp.port == 8000 or udp.port == 9000
4. Start capture
5. Run client.py
6. Stop capture
7. Analyze packets
```

---

## 🎓 LEARNING RESOURCES

**Concepts Used:**
- TCP/IP Protocol Suite
- HTTP/1.1 Protocol (RFC 7230-7237)
- Socket Programming
- Multithreading
- Caching Strategies
- Network Monitoring

**Python Topics:**
- `socket` module
- `threading` module
- `os` module for file operations
- Exception handling
- Context managers (with statement)
- String formatting

**Networking Concepts:**
- 3-way handshake
- TCP flags (SYN, ACK, PSH, FIN)
- UDP connectionless communication
- RTT measurement
- Packet loss calculation
- Jitter calculation

---

## 📞 EMERGENCY CONTACTS (For Help)

If code doesn't work:

1. **Check logs first**
   ```powershell
   cat logs/webserver.log
   cat logs/proxy.log
   ```

2. **Verify ports free**
   ```powershell
   netstat -ano | findstr ":8000\|:8080\|:9000"
   ```

3. **Check Python version**
   ```powershell
   python --version
   # Should be 3.6+
   ```

4. **Check file permissions**
   ```powershell
   # Should be able to read/write cache/ and logs/
   icacls cache
   icacls logs
   ```

5. **Reset everything**
   ```powershell
   # Kill all python processes
   Get-Process python | Stop-Process -Force
   
   # Delete cache and logs
   rm cache/* -Force
   rm logs/* -Force
   
   # Start fresh
   python webserver.py
   ```

---

## 📞 SUMMARY

**3 Files:**
- webserver.py (8000 TCP + 9000 UDP)
- proxy.py (8080 TCP + caching)
- client.py (--mode tcp/udp)

**5 Docs:**
- PROJECT_README.md (overview)
- SETUP_AND_RUNNING_GUIDE.md (setup)
- COMPLIANCE_CHECKLIST.md (verification)
- TEST_SCENARIOS.md (testing)
- WIRESHARK_GUIDE.md (analysis)

**Key Features:**
- Caching ✓
- Multithreading ✓
- Error handling ✓
- Logging ✓
- Statistics ✓

**Status**: Ready to submit ✓


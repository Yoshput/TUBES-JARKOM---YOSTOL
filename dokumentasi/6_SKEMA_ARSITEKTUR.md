# SKEMA ARSITEKTUR SISTEM - Client-Proxy-Server

## 🏗️ Diagram Topologi Jaringan

```
                          ┌─────────────────────────────┐
                          │       Wi-Fi Router          │
                          │      192.168.1.1            │
                          └──────────┬────────────────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
            ┌─────▼──────┐    ┌──────▼─────┐    ┌──────▼──────┐
            │  LAPTOP 1  │    │  LAPTOP 2  │    │  LAPTOP 3  │
            │  (Server)  │    │  (Proxy)   │    │  (Client)  │
            └─────┬──────┘    └──────┬─────┘    └──────┬──────┘
                  │                  │                  │
             192.168.1.10        192.168.1.20       192.168.1.30
                  │                  │                  │
                  │                  │                  │
           ┌──────┴──────┐      ┌────▼────┐             │
           │ TCP: 8000   │      │TCP: 8888│             │
           │ UDP: 5000   │      │         │             │
           └──────┬──────┘      └────┬────┘             │
                  │                  │                  │
                  │◄────────TCP──────►                  │
                  │     (Request)     │                  │
                  │                   │◄────TCP────────►│
                  │            (Forward Request)        │
                  │                   │                  │
                  │     ◄──TCP──(Response)──►           │
                  │              ◄────TCP───────────────┤
                  │         (Forward Response)          │
```

---

## 🔄 Alur Komunikasi Detail

### Skenario: Client Tambah Tugas

```
CLIENT                      PROXY                       SERVER
  │                          │                           │
  │ [1] TCP SYN (8888)       │                           │
  ├─────────────────────────>│                           │
  │                          │                           │
  │ [2] Send Request "ADD"   │                           │
  ├─────────────────────────>│                           │
  │                          │                           │
  │                          │ [3] TCP SYN (8000)        │
  │                          ├──────────────────────────>│
  │                          │                           │
  │                          │ [4] Forward Request       │
  │                          ├──────────────────────────>│
  │                          │                           │
  │                          │        [5] Process        │
  │                          │        & Validate         │
  │                          │        & Save             │
  │                          │                           │
  │                          │ [6] Send Response         │
  │                          │<──────────────────────────┤
  │                          │                           │
  │ [7] Receive Response     │                           │
  │<─────────────────────────┤                           │
  │                          │                           │
  │ [8] Display SUCCESS      │                           │
```

---

## 📡 Port & Protocol Configuration

### Port Assignment

| Component | Port | Protocol | Type |
|-----------|------|----------|------|
| **Server** | 8000 | TCP | Listen in-bound |
| **Server** | 5000 | UDP | Listen in-bound |
| **Proxy** | 8888 | TCP | Listen in-bound |
| **Proxy** | 8000 | TCP | Connect out-bound |
| **Client** | 8888 | TCP | Connect out-bound |
| **Client** | 5000 | UDP | Connect out-bound |

---

## 📊 Data Flow Diagram

### Request Processing

```
USER INPUT
   │
   ├─ Menu 1: ADD request
   ├─ Menu 2: GET request
   ├─ Menu 3: REMINDER request
   └─ Menu 4: Exit
   
        ▼
   
   CLIENT VALIDATION
   │
   ├─ Check empty input
   ├─ Format request
   └─ Send to PROXY
   
        ▼
   
   PROXY RECEIVE
   │
   ├─ Accept connection
   ├─ Receive request
   └─ Try connect to SERVER
   
        ▼ (Success)                ▼ (Failure)
   
   FORWARD TO SERVER         SEND ERROR RESPONSE
   │                         │
   ├─ Send request           └─ HTTP 503
   ├─ Receive response           Error: Server unavailable
   └─ Forward to client
   
        ▼
   
   SERVER PROCESS
   │
   ├─ Validate format
   ├─ Validate data
   ├─ Process request
   ├─ Save to database
   └─ Send response
   
        ▼
   
   RESPONSE BACK TO CLIENT
```

---

## 🔒 Error Handling Flow

### Server Side

```
IF ADD request:
  ├─ Split by "|"
  ├─ Check len(parts) == 4
  │  └─ IF NO: Return error format
  ├─ Validate date format
  │  └─ IF INVALID: Return error date
  └─ Append to tasks & return SUCCESS

IF GET request:
  └─ Generate list & return

IF REMINDER request:
  ├─ For each task:
  │  ├─ Parse date safely
  │  └─ Check deadline
  └─ Return reminder list
```

### Proxy Side

```
TRY:
  ├─ Accept client connection
  ├─ Connect to server
  ├─ Forward request
  ├─ Forward response
  └─ Close connection

EXCEPT ConnectionRefused:
  └─ Send HTTP 503 error

EXCEPT Generic:
  └─ Send HTTP 500 error

FINALLY:
  └─ Clean up connections
```

### Client Side

```
TRY:
  ├─ Connect to proxy
  ├─ Send request
  ├─ Receive response
  └─ Display response

EXCEPT ConnectionRefused:
  └─ Show error message
  └─ Allow retry from menu
```

---

## 🎯 Implementation Checklist

- [ ] All 3 Python files configured & tested
- [ ] IP addresses set correctly
- [ ] All ports accessible (firewall configured)
- [ ] Error handling implemented
- [ ] Input validation working
- [ ] TCP/UDP both functional
- [ ] Testing scenarios completed
- [ ] Documentation complete

---

**Version:** 1.0 | Last Updated: May 21, 2026

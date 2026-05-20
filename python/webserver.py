import socket
from datetime import datetime

# ============ KONFIGURASI ============
TCP_HOST = '0.0.0.0'
TCP_PORT = 8000
UDP_HOST = '0.0.0.0'
UDP_PORT = 5000

# Database lokal (in-memory)
tasks = []

# ============ FUNGSI HELPER ============
def validate_date(date_string):
    """Validasi format tanggal YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def process_add_request(request_data):
    """Proses request ADD dengan validasi"""
    try:
        parts = request_data.split("|")
        
        # EROR FIX 1: Validasi panjang array
        if len(parts) != 4:
            return "ERROR: Format salah. Gunakan: ADD|matkul|judul|deadline"
        
        matkul = parts[1].strip()
        judul = parts[2].strip()
        deadline = parts[3].strip()
        
        # EROR FIX 4: Validasi format tanggal
        if not validate_date(deadline):
            return f"ERROR: Format deadline salah. Gunakan: YYYY-MM-DD (Anda kirim: {deadline})"
        
        # Simpan ke database
        tasks.append({
            "matkul": matkul,
            "judul": judul,
            "deadline": deadline
        })
        
        print(f"[SERVER] Tugas ditambahkan: {matkul} - {judul}")
        return f"SUCCESS: Tugas '{judul}' berhasil ditambahkan!"
    
    except Exception as e:
        return f"ERROR: {str(e)}"

def process_get_request():
    """Proses request GET"""
    response = "===== DAFTAR TUGAS =====\n"
    
    if len(tasks) == 0:
        response += "Belum ada tugas."
    else:
        for i, task in enumerate(tasks, start=1):
            response += f"{i}. {task['matkul']} | {task['judul']} | {task['deadline']}\n"
    
    return response

def process_reminder_request():
    """Proses request REMINDER dengan error handling"""
    today = datetime.now().date()
    response = "===== REMINDER DEADLINE =====\n"
    found = False
    
    for task in tasks:
        try:
            # EROR FIX 4: Error handling untuk date parsing
            deadline_date = datetime.strptime(task['deadline'], "%Y-%m-%d").date()
            selisih = (deadline_date - today).days
            
            if selisih <= 1:
                found = True
                status = "HARI INI!" if selisih == 0 else "BESOK!"
                response += f"⚠️  {task['judul']} ({task['matkul']}) - {status}\n"
        
        except ValueError:
            response += f"⚠️  {task['judul']} - Format deadline invalid\n"
    
    if not found:
        response += "✓ Tidak ada reminder hari ini."
    
    return response

# ============ TCP SERVER ============
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind((TCP_HOST, TCP_PORT))
tcp_socket.listen(5)
print(f"[SERVER] TCP listening di {TCP_HOST}:{TCP_PORT}")

# ============ UDP SERVER ============
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_HOST, UDP_PORT))
print(f"[SERVER] UDP listening di {UDP_HOST}:{UDP_PORT}")


# ============ MAIN LOOP ============
while True:
    try:
        # Terima TCP request dari proxy
        client_socket, client_address = tcp_socket.accept()
        print(f"[SERVER] TCP Connection dari {client_address}")
        
        request = client_socket.recv(4096).decode()
        print(f"[SERVER] Request: {request}")
        
        # Process request
        if request.startswith("ADD"):
            response = process_add_request(request)
        elif request.startswith("GET"):
            response = process_get_request()
        elif request.startswith("REMINDER"):
            response = process_reminder_request()
        else:
            response = "ERROR: Request tidak dikenali"
        
        # Kirim response via TCP
        tcp_response = f"HTTP/1.1 200 OK\n\n{response}\n"
        client_socket.send(tcp_response.encode())
        client_socket.close()
        
        print(f"[SERVER] Response dikirim\n")
    
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        try:
            client_socket.close()
        except:
            pass

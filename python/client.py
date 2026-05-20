import socket

# ============ KONFIGURASI CLIENT ============
PROXY_HOST = '127.0.0.1'  # UBAH ke IP Laptop Proxy
PROXY_PORT = 8888

SERVER_HOST = '127.0.0.1'  # UBAH ke IP Laptop Server
SERVER_UDP_PORT = 5000

# ============ FUNGSI HELPER ============
def send_tcp_request(request):
    """Kirim request ke proxy via TCP"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # EROR FIX 3: Error handling untuk connection
        try:
            client_socket.connect((PROXY_HOST, PROXY_PORT))
        except ConnectionRefusedError:
            print(f"\n❌ ERROR: Tidak bisa connect ke Proxy di {PROXY_HOST}:{PROXY_PORT}")
            print("   Pastikan proxy.py sudah dijalankan!")
            return None
        
        client_socket.send(request.encode())
        response = client_socket.recv(4096).decode()
        client_socket.close()
        
        return response
    
    except Exception as e:
        print(f"❌ ERROR (TCP): {e}")
        return None

def send_udp_request(request):
    """Kirim request ke server via UDP (alternative)"""
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            udp_socket.sendto(request.encode(), (SERVER_HOST, SERVER_UDP_PORT))
            response, _ = udp_socket.recvfrom(4096)
            udp_socket.close()
            return response.decode()
        
        except Exception as e:
            print(f"⚠️  UDP tidak tersedia: {e}")
            return None
    
    except Exception as e:
        print(f"❌ ERROR (UDP): {e}")
        return None

def display_menu():
    """Tampilkan menu"""
    print("\n" + "="*40)
    print("   SISTEM MANAJEMEN TUGAS")
    print("="*40)
    print("1. Tambah tugas")
    print("2. Lihat daftar tugas")
    print("3. Cek reminder deadline")
    print("4. Keluar")
    print("="*40)

# ============ MAIN CLIENT LOOP ============
print("[CLIENT] Terhubung ke Proxy di {}:{}".format(PROXY_HOST, PROXY_PORT))
print("[CLIENT] Server UDP di {}:{}\n".format(SERVER_HOST, SERVER_UDP_PORT))

while True:
    display_menu()
    pilihan = input("\nPilih menu (1-4): ").strip()
    
    if pilihan == "1":
        # TAMBAH TUGAS
        print("\n--- TAMBAH TUGAS ---")
        matkul = input("Mata kuliah: ").strip()
        judul = input("Judul tugas: ").strip()
        deadline = input("Deadline (YYYY-MM-DD): ").strip()
        
        request = f"ADD|{matkul}|{judul}|{deadline}"
        
        print("\n[CLIENT] Mengirim request...")
        response = send_tcp_request(request)
        
        if response:
            print("\n[SERVER RESPONSE]")
            print(response)
        else:
            print("❌ Tidak ada response dari server")
    
    elif pilihan == "2":
        # LIHAT TUGAS
        print("\n--- DAFTAR TUGAS ---")
        request = "GET"
        
        print("[CLIENT] Mengirim request...")
        response = send_tcp_request(request)
        
        if response:
            print("\n[SERVER RESPONSE]")
            print(response)
        else:
            print("❌ Tidak ada response dari server")
    
    elif pilihan == "3":
        # REMINDER
        print("\n--- CEK REMINDER ---")
        request = "REMINDER"
        
        print("[CLIENT] Mengirim request...")
        response = send_tcp_request(request)
        
        if response:
            print("\n[SERVER RESPONSE]")
            print(response)
        else:
            print("❌ Tidak ada response dari server")
    
    elif pilihan == "4":
        # KELUAR
        print("\n[CLIENT] Program selesai. Terima kasih!")
        break
    
    else:
        print("❌ Menu tidak valid. Coba lagi!")

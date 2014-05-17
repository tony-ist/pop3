import socket
import base64

class msglist:
    def __init__(self, str):
        lines = str.splitlines()
        self.num = len(lines)-2
        self.size = []
        for i in lines[1:-1]:
            self.size.append(i[2:])

class msgheader:
    def __init__(self, str):
        lines = str.splitlines()

def receive(sock, encoding = "UTF8"):
    result = ""
    while True:
        buffer = sock.recv(512)
        result += buffer.decode(encoding)
        if result.endswith(".\r\n"): break
    return result

if __name__ == "__main__":
    server = "pop.mail.ru"
    port = 110

    user = "pop3mailtester@mail.ru"
    passw = "testermail3pop"
    debug = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.settimeout(5)
    s.connect((server, port))

    ans = s.recv(512).decode()
    if debug: print(ans)

    s.send(("user " + user + "\n").encode())
    ans = s.recv(512).decode()
    if debug: print(ans)

    s.send(("pass " + passw + "\n").encode())
    ans = s.recv(512).decode()
    if debug: print(ans)

    s.send("LIST\n".encode())
    ans = receive(s)
    # ans += s.recv(512).decode()
    if debug: print(ans)

    ml = msglist(ans)

    for i in range(1, ml.num+1):
        s.send(("TOP " + str(i) + " 0\n").encode())
        ans = receive(s)
        if debug: print(ans)
        mes = msgheader(ans)

    # s.send((input()+'\n').encode())

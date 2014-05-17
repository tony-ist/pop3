import socket
import base64

class msglist:
    def __init__(self, str):
        lines = str.splitlines()
        self.num = len(lines)-2
        lines.pop(0)
        for i in lines:
            self.size = []
            self.size.append(i[2:])

class msgheader:
    def __init__(self, str):
        lines = str.splitlines()
        self.From = lines[1] + lines[2]

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

    s.send(("STAT\n").encode())
    ans = s.recv(512).decode()
    if debug: print(ans)

    n = int(ans.split()[1])

    for i in range(1, n+1):
        s.send(("TOP " + str(i) + " 0\n").encode())
        ans = s.recv(1024).decode()
        if debug: print(ans)
        mes = msgheader(ans)
        if debug: print(ans)

    # s.send((input()+'\n').encode())

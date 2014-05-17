import socket
import base64
import re
import sys

class msglist:
    msgs = []

    def __init__(self, str):
        lines = str.splitlines()
        self.num = len(lines)-2
        self.size = []
        for i in lines[1:-1]:
            self.size.append(i[2:])

    class msgheader:
        def __init__(self, str):
            self.lines = re.split(r"\r\n(?=^[a-zA-Z0-9-_]+:)", str, flags=re.MULTILINE)

        def get(self, field):
            field = field.lower()
            for i in self.lines:
                if(i.lower().startswith(field)):
                    result = re.sub(r"=[?](.+?)[?][bB][?](.+?)[?]=", b64repl, i)
                    result = re.sub(r"\r\n\s{0,1}", "", result)
                    return result
            return "'" + field + "' information not found"

def b64repl(match):
    encoding = match.group(1)
    code = match.group(2)
    binary = base64.standard_b64decode(code.encode(encoding, 'replace'))
    result = binary.decode(encoding, 'replace')
    return result

def receive(sock, encoding = "koi8-r"):
    result = ""
    while True:
        buffer = sock.recv(512)
        result += buffer.decode(encoding, 'replace')
        if result.endswith(".\r\n"): break
    return result

if __name__ == "__main__":
    usage = "Usage: pop3 username password"

    server = "pop.mail.ru"
    port = 110

    user = "pop3mailtester@mail.ru"
    passw = "testermail3pop"
    debug = False

    sys.argv.pop(0)
    if len(sys.argv) == 2:
        user = sys.argv[0]
        passw = sys.argv[1]
    elif sys.argv:
        print(usage)
        exit()

    print("Server:", server)
    print("Port:", port)
    print("Checking mail for", user)

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
    if debug: print(ans)

    ml = msglist(ans)
    # ml.num = 30

    for i in range(1, ml.num+1):
        s.send(("TOP " + str(i) + " 0\n").encode())
        ans = receive(s)
        if debug: print(ans)
        ml.msgs.append(msglist.msgheader(ans))

    for i in range(len(ml.msgs)):
        print(i+1, ml.msgs[i].get("From:"))
        print(" ", ml.msgs[i].get("Subject:"))
        print("  Size: ", ml.size[i])
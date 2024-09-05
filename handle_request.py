import socket
import ssl

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        self.view_source = False
        if "view-source" in self.scheme:
            self.view_source = True
            _, self.scheme = self.scheme.split(":", 1)
        assert self.scheme in ['http', 'https', 'file']
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        elif self.scheme == "file":
            self.port = 21

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if ":" in self.host:
            self.host, port = self.host.split(":", 2)
            self.port = int(port)

    def request(self):
        if self.scheme == "file":
            return self.request_file()
        if self.view_source:
            return self.request_view_source()
        return self.request_net()
    
    def request_view_source(self):
        ret = self.request_net()
        for c in ret:
            if c == "<":
                c = "&lt"
            elif c == ">":
                c = "&gt"
            yield c

    def request_file(self):
        return f"This is your host {self.host}. With scheme {self.scheme}"

    def request_net(self):

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

        request = f"GET {self.path} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        request += "Connection: close\r\n"
        request += "User-Agent: The Matrix\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()
        return content
    
def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            if c == "&lt":
                c = "<"
            elif c == "&gt":
                c = ">"
            text += c
    return text

def load(url):
    body = url.request()
    return lex(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
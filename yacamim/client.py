
import cgi
import mailcap
import os
import socket
import ssl
import tempfile
import textwrap
import urllib.parse

class GeminiClient:
    def __init__(self):
        self.caps = mailcap.getcaps()
        self.menu = []
        self.hist = []

    def absolutise_url(self, base, relative):
        if "://" not in relative:
            base = base.replace("gemini://", "http://")
            relative = urllib.parse.urljoin(base, relative)
            relative = relative.replace("http://", "gemini://")
        return relative

    def get_url(self, cmd):
        if cmd.isnumeric():
            try:
                return self.menu[int(cmd) - 1]
            except IndexError:
                print("Índice inválido, tente novamente")
                return None
        elif cmd.lower() == "b":
            return self.hist.pop() if self.hist else None
        else:
            return "gemini://" + cmd if "://" not in cmd else cmd

    def create_ssl_socket(self, parsed_url):
        socket_object = socket.create_connection((parsed_url.netloc, 1965))
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context.wrap_socket(socket_object, server_hostname=parsed_url.netloc)

    def send_request(self, socket_object, url):
        socket_object.sendall((url + "\r\n").encode("UTF-8"))
        return socket_object.makefile("rb")

    def handle_input_request(self, mime, url):
        query = input("INPUT" + mime + "> ")
        return url + "?" + urllib.parse.quote(query)

    def handle_redirect(self, url, mime):
        return self.absolutise_url(url, mime)

    def handle_gemini_link(self, line, url):
        bits = line[2:].strip().split(maxsplit=1)
        link_url = self.absolutise_url(url, bits[0])
        self.menu.append(link_url)
        text = bits[1] if len(bits) == 2 else link_url
        print(f"[{len(self.menu)}] {text}")

    def handle_gemini_map(self, body, url):
        self.menu = []
        preformatted = False
        for line in body.splitlines():
            if line.startswith("```"):
                preformatted = not preformatted
            elif preformatted:
                print(line)
            elif line.startswith("=>") and line[2:].strip():
                self.handle_gemini_link(line, url)
            else:
                print(textwrap.fill(line, 80))

    def handle_text_response(self, fp, url, mime):
        mime, mime_opts = cgi.parse_header(mime)
        body = fp.read().decode(mime_opts.get("charset", "UTF-8"))
        if mime == "text/gemini":
            self.handle_gemini_map(body, url)
        else:
            print(body)

    def handle_non_text_response(self, fp, mime):
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmpfp:
            tmpfp.write(fp.read())
        cmd_str, _ = mailcap.findmatch(self.caps, mime, filename=tmpfp.name)
        os.system(cmd_str)
        os.unlink(tmpfp.name)

    def process_gemini_response(self, fp, url, mime):
        if mime.startswith("text/"):
            self.handle_text_response(fp, url, mime)
        else:
            self.handle_non_text_response(fp, mime)

    def gemini_transaction(self, url):
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme != "gemini":
            print("Ops, apenas aceitamos links Gemini.")
            return None

        try:
            while True:
                with self.create_ssl_socket(parsed_url) as socket_object:
                    fp = self.send_request(socket_object, url)
                    header = fp.readline().decode("UTF-8").strip()
                    status, mime = header.split()

                    if status.startswith("1"):
                        url = self.handle_input_request(mime, url)
                    elif status.startswith("3"):
                        url = self.handle_redirect(url, mime)
                        parsed_url = urllib.parse.urlparse(url)
                    else:
                        break

            if not status.startswith("2"):
                print(f"Error {status}: {mime}")
                return None

            self.process_gemini_response(fp, url, mime)
            return url

        except Exception as err:
            print(f"Error: {err}")
            return None

    def handle_user_input(self):
        cmd = input("> ").strip()
        if cmd.lower() == "q":
            print("Boa viagem!")
            return None
        return self.get_url(cmd)

    def start(self):
        while True:
            url = self.handle_user_input()
            if url is None:
                break
            result_url = self.gemini_transaction(url)
            if result_url:
                self.hist.append(result_url)

if __name__ == "__main__":
    client = GeminiClient()
    client.start()
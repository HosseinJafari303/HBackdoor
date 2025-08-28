# Server.py
import socket
import argparse
from colorama import Fore, init
import os
import sys

init(autoreset=True)

# Set args

parser = argparse.ArgumentParser(description='Connect to the target server.')
parser.add_argument('-c', '--create', required=True, help="Create room with IP:PORT")
argv = parser.parse_args()

class Server:
    def __init__(self):
        try:
            host, port_str = argv.create.split(':', 1)
            port = int(port_str)
            if not (0 <= port <= 65535):
                raise ValueError()
        except Exception:
            print(f"[{Fore.RED}ERROR{Fore.RESET}] Invalid address/port. Expected format IP:PORT")
            sys.exit(1)

        address = (host, port)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(address)
        self.server.listen(1)
        print(f"[{Fore.GREEN}*{Fore.RESET}] Server successfully created...")
        print(f"[{Fore.GREEN}*{Fore.RESET}] Listening on {address[0]}:{address[1]}...")

        self.conn, self.addr = self.server.accept()
        print(f"[{Fore.GREEN}*{Fore.RESET}] Connection from {self.addr}")

        try:
            while True:
                prompt = input(f"<{address[0]} {getattr(self, 'cwd', '/')}> ").strip()
                if prompt in ("cls", "clear"):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue

                if prompt == 'disconnect':
                    self.conn.send(prompt.encode())
                    break

                self.conn.send(prompt.encode())
                data = self.conn.recv(4096)
                if not data:
                    print(f"[{Fore.RED}!{Fore.RESET}] Client disconnected.")
                    break

                decoded = data.decode()
                if "<cwd>" in decoded and "</cwd>" in decoded:
                    before, cwd = decoded.split("<cwd>", 1)
                    cwd, after = cwd.split("</cwd>", 1)
                    self.cwd = cwd.strip()
                    output = before.strip() + after.strip()
                else:
                    output = decoded

                if output.strip():
                    print(output)

        finally:
            try:
                self.conn.close()
            except:
                pass
            try:
                self.server.close()
            except:
                pass

if __name__ == "__main__":
    try:
        Server()
    except ConnectionResetError:
        print(f"[{Fore.RED}!{Fore.RESET}] Client disconnected...")

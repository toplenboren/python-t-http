import socket
import sys

import utilitary


class Request():
    def __init__(self, srvaddr, port, size):
        self.content = self.socket.recv(size)
        self.server_addr = srvaddr
        self.port = port
        self.socket = socket.socket()
        self.socket.connect((srvaddr, port))
        # self.request_header = 'GET / HTTP/1.0\r\nHost:'+ srvaddr +'\r\n\r\n'

    # todo: do encoding
    def send(self, request):
        self.socket.send(bytes(request, encoding='UTF-8', errors='strict'))


def launch_utilitary_function():
    if len(sys.argv) == 1:
        # utilitary.print_usage()
        return False
    else:
        argument = sys.argv[1]

        if argument == '-h':
            utilitary.print_light_help()
            return True
        elif argument == '--help':
            utilitary.print_full_help()
            return True
    return False


def http_client():

    request = Request(srvaddr='kadm.imkn.urfu.ru', port=80, size=1024, request=)
    request.content

    sock = socket.socket()
    sock.connect(('kadm.imkn.urfu.ru', 80))

    request_header = 'GET / HTTP/1.0\r\nHost: kadm.imkn.urfu.ru\r\n\r\n'
    sock.send(bytes(request_header, encoding='UTF-8', errors='strict'))

    data = sock.recv(1024)
    sock.close()

    print(str(data))


def main():
    if not launch_utilitary_function():
        http_client()
    else:
        return


if __name__ == '__main__':
    main()

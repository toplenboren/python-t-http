import sys
import socket
import utilitary

ENCODINGS = ['utf-8', 'Windows-1251']
ENCODING = 'utf-8'
DEFAULT_LISTENING_PORT = 80

def launch_utilitary_function():
    if len(sys.argv) == 1:
        utilitary.print_usage()
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


def write_to_html(data, header):
    f = open(header + '.html', "w+", encoding='utf-8')
    f.write(data)
    f.close()


class http_client:

    def __init__(self):
        self.reroute()

    def reroute(self):
        print("Currently implemented functions:")
        print("1. Download HTML page on provided ADDRESS")
        print("2. Send custom HTTP Request")
        print("Please - choose function")
        inp = input()
        if inp == '1':
            self.download_html_page()
        elif inp == '2':
            self.send_custom_request()


    def send_custom_request(self):
        print('building up your Request, hold on...')
        print('please enter the server')
        serv = input()
        print('please enter the port')
        port = int(input())
        sock = socket.socket()
        sock.connect((serv, port))
        print('plese enter the request:')
        request = input()
        print('please enter the size of the recievement')
        size = int(input())
        sock.send(bytes(request, encoding='utf-8', errors='strict'))
        data = sock.recv(size)
        sock.close()

        data_dec = data.decode('utf-8')

        print('output')
        print(str(data_dec))
        print('save?')
        print('y/N')
        save = input()
        if save == 'y':
            write_to_html(str(data_dec), "custom_request" )
            return
        else:
            print(':(')
            return
            

    def download_html_page(self):
        print('building up your Request, hold on...')
        print('please enter the requested html page: *kadm.imkn.urfu.ru/news.php')

        inp = input()
        inp = inp.split('/')
        host = inp[0]
        addr = "/" + "/".join(inp[1::])

        sock = socket.socket()
        sock.connect((host, DEFAULT_LISTENING_PORT))
        request_header = 'GET ' + addr + ' HTTP/1.0\r\nHost: ' + host + ' \r\n\r\n'

        sock.send(bytes(request_header, encoding='utf-8', errors='strict'))
        data = sock.recv(10000)
        sock.close()

        for enc in ENCODINGS:
            try:
                data_dec = data.decode(enc)
                ENCODING = enc
            except Exception:
                continue

        print('output')
        print(str(data_dec))
        print('save?')
        print('y/N')
        save = input()
        if save == 'y':
            write_to_html(str(data_dec), host)
            return
        else:
            print(':(')
            return


def main():
    # if not launch_utilitary_function():
    #     http_client()
    # else:
    #     return
    client = http_client()


if __name__ == '__main__':
    main()

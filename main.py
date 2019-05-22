import socket
import sys

import utilitary

ENCODINGS = ['utf-8', 'utf-16', 'Windows-1251']
ENCODING = 'utf-8'


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


def write_to_html(data, header):
    f = open(header + '.html', "w+", encoding=ENCODING)
    f.write(data)
    f.close()


def http_client():

    print('building up your Request, hold on...')
    print('please enter the requested html page: *kadm.imkn.urfu.ru/news.php')

    inp = input()
    inp = inp.split('/')
    host = inp[0]
    addr = "/" + "/".join(inp[1::])

    sock = socket.socket()
    sock.connect((host, 80))
    request_header = 'GET ' + addr + ' HTTP/1.0\r\nHost: ' + host + ' \r\n\r\n'

    sock.send(bytes(request_header, encoding='utf-8', errors='strict'))
    data = sock.recv(10000)
    sock.close()

    for enc in ENCODINGS:
        try:
            data_dec = data.decode(enc)
            data_enc = data_dec
            ENCODING = enc
        except Exception:
            continue

    print('output')
    print(str(data_enc))
    print('save?')
    print('y/N')
    save = input()
    if save == 'y':
        write_to_html(str(data_enc), host)
        return
    else:
        print(':(')
        return


def main():
    # if not launch_utilitary_function():
    #     http_client()
    # else:
    #     return
    http_client()


if __name__ == '__main__':
    main()

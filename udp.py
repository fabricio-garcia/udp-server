import argparse
import socket

MAX_SIZE_BYTES = 65535  # Maximum size of a UDP datagram


def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Listening at {}'.format(s.getsockname()))
    while True:
        data, client_address = s.recvfrom(MAX_SIZE_BYTES)
        message = data.decode('ascii')
        upper_case_message = message.upper()
        print('The client at {} says {!r}'.format(client_address, message))
        data = upper_case_message.encode('ascii')
        s.sendto(data, client_address)


def client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = input('Input lowercase sentence:')
    data = message.encode('ascii')
    s.sendto(data, ('127.0.0.1', port))
    print('The OS assigned the address {} to me'.format(s.getsockname()))
    data, address = s.recvfrom(MAX_SIZE_BYTES)
    text = data.decode('ascii')
    print('The server {} replied with {!r}'.format(address, text))


if __name__ == '__main__':
    funcs = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='UDP client and server')
    parser.add_argument('functions', choices=funcs, help='client or server')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000,
                        help='UDP port (default 3000)')
    args = parser.parse_args()
    function = funcs[args.functions]
    function(args.p)

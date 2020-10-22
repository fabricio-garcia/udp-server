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
    hosts = []
    while True:
        host = input('Enter host address: ')
        hosts.append((host, port))
        message = input('Enter lowercase sentence: ')
        data = message.encode('ascii')
        s.sendto(data, (host, port))
        print('Assigned IP address is: {}'.format(s.getsockname()))
        data, address = s.recvfrom(MAX_SIZE_BYTES)
        text = data.decode('ascii')
        if address in hosts:
            print('The server {} replied with {!r}'.format(address, text))
            hosts.remove(address)
        else:
            print('message {!r} from unexpected host {}!'.format(text, address))


if __name__ == '__main__':
    funcs = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='UDP client and server')
    parser.add_argument('functions', choices=funcs, help='client or server')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000,
                        help='UDP port (default 3000)')
    args = parser.parse_args()
    function = funcs[args.functions]
    function(args.p)

import socket
import sys


def establish(ip_str, port):
    # create an AF_INET, STREAM socket (TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket. ')
        sys.exit()
    print('Socket created')

    # Connect to remote server
    try:
        s.connect((ip_str, port))
    except socket.error as e:
        print('Failed to connect. Reason: {0}'.format(e.strerror))
        sys.exit()
    print('Socket Connected to {0} @ {1}'.format(ip_str, port))

    return s


def emit(s, message, ip_str, port):
    try:
        s.sendto(message.encode(encoding="utf-8"), (ip_str, port))
        return True
    except Exception:
        s.close()
        return False  # Fatal

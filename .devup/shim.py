
import socket
import os

_original_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(host, port, *args, **kwargs):
    if host in ['localhost', '127.0.0.1', 'db', 'database']:
        if port == 3306: host = 'mysql'
        elif port == 5432: host = 'postgres'
        elif port == 27017: host = 'mongodb'
        elif port == 6379: host = 'redis'
    return _original_getaddrinfo(host, port, *args, **kwargs)

socket.getaddrinfo = patched_getaddrinfo

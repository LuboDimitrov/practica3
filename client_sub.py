import errno
import socket
import sys
import select
import random
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

broker_address = ('localhost', 10000)
# BASE PORT
port = 10001


## intentar fer un bucle fins que no se conecti seguir intentant
try:
    sock.bind(("127.0.0.1", port))
except socket.error as e:
    if e.errno == errno.EADDRINUSE:
        port = random.randint(10002, 65535)
        print("Port is already in use")

messageA = b'sub:id:%i' % port
messageB = b'sub:topic:game'

try:
    # Send data
    print('sending {!r}'.format(messageA))
    sent = sock.sendto(messageA, broker_address)
    print('sending {!r}'.format(messageB))
    sent = sock.sendto(messageB, broker_address)
finally:
    print('closing socket')
    sock.close()

# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', port)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
while True:
    print('\nwaiting to receive message')
    rlist, _, _ = select.select([sock], [], [])
    data, address = sock.recvfrom(1024)
    # Do stuff with data, fill this up with your code
    print('received {} bytes from {}'.format(len(data), address))
    print(data)

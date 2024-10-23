import argparse
from my_socket import MySocket

HOST = 'stackoverflow.nordquant.com'
PORT = 2730

parser = argparse.ArgumentParser()
parser.add_argument('-W', '--window', required=False, default=5, help='window length')
parser.add_argument('-S', '--slide', required=False, default=1, help='sliding interval')
ARGS = parser.parse_args()

my_socket = MySocket(int(ARGS.window), int(ARGS.slide))
my_socket.connect(HOST, PORT)
my_socket.process()
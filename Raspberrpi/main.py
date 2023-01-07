# test BLE Scanning software
# jcs 6/8/2014

"""
https://hybridego.net/2337

애플워치 식별번호 180A
"""
import blescan
import sys

import bluetooth._bluetooth as bluez
import socket

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = ("192.168.1.2", 7720)

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 5)
	print "----------"
	for beacon in returnedList:
		if beacon[:17] == '60:7c:c0:98:bd:e1' or beacon[:17] == '68:10:69:e1:16:12' or beacon[:17] == '46:bd:e7:50:e7:e1':
			print beacon
			send_sock.sendto(beacon, dest)


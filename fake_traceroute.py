#!/usr/bin/env python3

import os, platform, ipaddress, socket


def what_type_of_ipv4(myipaddress):
	if ipaddress.ip_address(myipaddress).is_private:
		return "Private"
	if ipaddress.ip_address(myipaddress).is_global:
		return "Global"
	if ipaddress.ip_address(myipaddress) in ipaddress.ip_network('100.115.92.0/24'):
		# for example 100.115.92.193
		return "Chromebook / Android"
	
	if ipaddress.ip_address(myipaddress) in ipaddress.ip_network('100.64.0.0/10'):
		return "CGNAT"
	return "Unknown"
	

def localipv4():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_ipv4:
            # Option: use 100.64.1.1 (IANA-Reserved IPv4 Prefix for Shared Address Space)
            s_ipv4.connect(("10.255.255.255", 80))
            ipv4 = s_ipv4.getsockname()[0]
    except socket.error:
        ipv4 = None
    return ipv4
    


host = "8.8.8.8"
print(platform.system())
print(os.name)

#print(what_type_of_ipv4('100.115.92.193'))

#os.system("ping " + ("-n 1 " if  platform.system().lower()=="windows" else "-c 1 ") + host)

number_of_hops = 20
done = False

ipv4address = localipv4()
print("local " + ipv4address + " " + what_type_of_ipv4(ipv4address))

for ttl in range(1,number_of_hops):
	if platform.system() == "Linux":
		#print(ttl)
		cmd = "ping -c1 -n -W2 -t" + str(ttl) + " 1.1.1.1"
		#print(cmd)
		#bla = os.system(cmd)
		ipv4address = None
		for thisline in os.popen(cmd).readlines():
			if thisline.find("Time to live exceeded") >= 0:
				ipv4address = thisline.split()[1]
				#print(ipv4address + " ",end ='')
				print(ipv4address + " " + what_type_of_ipv4(ipv4address))
			if thisline.find("bytes from") >= 0:
				# 64 bytes from 1.1.1.1: icmp_seq=1 ttl=56 time=7.34 ms
				# so ... reached the end destination!
				ipv4address = thisline.split()[3].replace(":", "")
				print(ipv4address + " " + what_type_of_ipv4(ipv4address))
				done = True
				break
		if not ipv4address:
			print("time-out on hop", ttl)
	if done:
		break
				
	if platform.system() == 'Windows':
		cmd = "ping -n 1 -i " + ttl + " 1.1.1.1" 
		for thisline in os.popen(cmd).readlines():
			if thisline.find("TTL expired in transit") >= 0:
				print(thisline.split()[2].replace(":",""))


'''
Linux:

$ ping -c1 -t2 -n 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
From 149.143.62.241 icmp_seq=1 Time to live exceeded



sander@zwart2204:~$ ping -c1 -t1 -n 1.1.1.1 | grep exceeded
From 192.168.1.254 icmp_seq=1 Time to live exceeded
sander@zwart2204:~$ ping -c1 -t2 -n 1.1.1.1 | grep exceeded
From 149.143.62.241 icmp_seq=1 Time to live exceeded
sander@zwart2204:~$ ping -c1 -t3 -n 1.1.1.1 | grep exceeded
From 62.45.255.193 icmp_seq=1 Time to live exceeded
sander@zwart2204:~$ ping -c1 -t4 -n 1.1.1.1 | grep exceeded
'''

'''
Windows (NB: spaces needed!!!)

C:\>ping -n 1 -i 2 1.1.1.1

Pinging 1.1.1.1 with 32 bytes of data:
Reply from 149.143.62.241: TTL expired in transit.

'''

'''

>>> ipaddress.ip_address("192.168.1.1").is_private
True


ipaddress.ip_address('100.64.5.5') in ipaddress.ip_network('100.64.0.0/10')
True
'''





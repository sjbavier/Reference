import socket
import os

# host to listen on
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)

# check for OS and bind socket to public interface
# Windows will allow the sniffing of all protocols
# whereas Linux lets you specify ICMP
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

# create raw socket
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# set the option to include headers
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# if we are using windows we need to send an IOCTL
# to set up promiscuous mode

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# read a single packet
print("sniffing ICMP packets")
print(sniffer.recvfrom(65565))

# if using Windows turn off promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
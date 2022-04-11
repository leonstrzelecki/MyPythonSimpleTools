#     WELCOME TO Open_Ports_Scaner
#     Script is written for UNIX OS. Running on Windows may cause problems with UTF-8 encoding
#     requirements   python3, scapy
#     use -h flag to get help

from sys import argv
from scapy.all import *
from scapy import volatile, config
from scapy.layers.inet import TCP, IP, ICMP

def targetAvailableCheck(target):
    try:
        scapy.config.conf.verb = 0
        packet = IP(dst=target)/ICMP()
        resp = sr1(packet, timeout=3)
        if resp:
            return True

    except Exception as error:
        print(error)
        return False

def scanport(port, target):
    src = scapy.volatile.RandShort()
    scapy.config.conf.verb = 0
    packet = IP(dst=target) / TCP(sport=src, dport=port, flags="S")
    synPkt = sr1(packet, timeout=0.5)

    if synPkt is None:
        return False
    elif synPkt.haslayer(TCP) == False:
        return False
    else:
        if synPkt[TCP].flags == 0x12 :
            packet2 = IP(dst=target) / TCP(sport=src, dport=port, flags="R")
            resp = sr(packet2, timeout=0.5)
            return True

if __name__ == '__main__':
    args = sys.argv
    if "-h" in args or len(args)<2 or len(args)>4:
        print("USAGE:   python Open_Ports_scaner.py <targetIP>\nOPTIONAL: set port range -r <min>,<max> (default is 1,1024)")
    else:
        target = args[1]
        openPorts = []
        if "-r" in args:
            rang = args[args.index("-r") + 1].split(",")
            registeredPorts = range(int(rang[0]), int(rang[1])+1)
        else:
            registeredPorts = range(1, 1024)

        checkAV = targetAvailableCheck(target)
        if checkAV == True:
            print('target host is UP!')
            for port in registeredPorts:
                status = scanport(port, target)
                if status == True:
                    openPorts.append(port)
                    print(f"PORT {port} is open!")
            print(f"Scan finished....{len(openPorts)} ports are open.")

        else:
            print("target host seems dead...")

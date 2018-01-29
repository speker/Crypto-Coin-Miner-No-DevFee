#!/usr/bin/env python
#-*-encoding:UTF-8-*-
import json
import sys
import ctypes
import os
import time
import logging.handlers
import signal


count=0
datetimeformat="%d/%m/%Y %H:%M:%S";
debug_level=0

LOG_FILENAME = time.strftime("%Y%m%d%H%M%S")+"_no_dev_fee.log"
LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=300)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def sigint_handler(signal, frame):
    print 'Interrupted'
    logger.error('Interrupted')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

try:
 is_admin = os.getuid() == 0
except AttributeError:
 is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if len(sys.argv) < 4:
    print("Invalid or Missing command line")
    print("Usage : python no_dev_fee.py coin_adres stratum_port worker_delemiter debug_level")
    print("Eg: python no_dev_fee.py 0xe9473918c1122276203677860fad70ef2b4522af 3333 . 0")
    logger.error('Invalid or Missing sys.argv : %s ' % (str(sys.argv)))
    os.system("pause")
    exit(0)
else:
    address = sys.argv[1]
    port = sys.argv[2]
    delemiter = sys.argv[3]

if len(sys.argv) == 5:
    debug_level = sys.argv[4]

if is_admin==False:
    print("Administrator privileges must be need")
    logger.error('Missing administrator rights : %s ' % (str(is_admin)))
    os.system("pause")
    exit(0)
else:
    import pydivert

logger.info('Application started to watch DevFee connections. Address : %s Port : %s Delemiter : %s' % (address, port,delemiter))

print(time.strftime(datetimeformat) +' Start to watch mining network connections.')
print('Replace developer address to => %s listening port => %s' % (address, port)+'\r\n')

with pydivert.WinDivert("tcp.DstPort == %s and tcp.PayloadLength > 0" % port ) as w:
    for packet in w:
        try:
            if packet == None or packet.tcp == None or packet.tcp.payload == None:
                w.send(packet)
                continue
            payload = packet.tcp.payload
            if debug_level=="1":
                logger.info('Orginal Tcp Packet = dst_addr : %s dst_port : %s src_addr : %s src_port : %s paylod : %s' % (str(packet.dst_addr),str(packet.dst_port),str(packet.src_addr),str(packet.src_port),str(packet.tcp.payload).strip('\n')))
                print(str(payload).strip('\n'))
            if payload.find(address) < 0:
                if payload.find('mining.submit') > 0 or payload.find('mining.authorize') > 0:
                    json_data = json.loads(payload)
                    count += 1
                    print('%s  Found Developer Zec Address => %s' % (time.strftime(datetimeformat),json_data['params'][0]) )
                    logger.info('Found Developer Zec Address => %s' % (json_data['params'][0]) )
                    if json_data['params'] and len(json_data['params']) > 0:
                        originAddr = json_data['params'][0]
                        newParam = address
                        if originAddr.find(delemiter) > 0:
                            newParam = address + originAddr[originAddr.find(delemiter):]
                        json_data['params'][0] = newParam
                    print('%s : Zec replace with new address => %s' % (str(count),newParam))
                    logger.info('%s : Zec replace with new address => %s' % (str(count),newParam))
                    payload = json.dumps(json_data)
                    if debug_level == "1":
                        logger.info('Replaced Tcp Payload : %s' % (str(payload).strip('\n')))
                if payload.find('eth_submitLogin') > 0:
                    json_data = json.loads(payload)
                    count += 1
                    print('%s Found Developer Eth/Etc Address => %s' % (time.strftime(datetimeformat),json_data['params'][0]) )
                    logger.info('Found Developer Eth/Etc Address => %s' % (json_data['params'][0]))
                    if json_data['params'] and len(json_data['params']) > 0:
                        originAddr = json_data['params'][0]
                        newParam = address
                        if originAddr.find(delemiter) > 0:
                            newParam = address + originAddr[originAddr.find(delemiter):]
                        json_data['params'][0] = newParam
                    print('%s : Eth/Etc replace with new address => %s' % (str(count),newParam))
                    logger.info('%s : Eth/Etc replace with new address => %s' % (str(count),newParam))
                    payload = json.dumps(json_data)
                    if debug_level == "1":
                        logger.info('Replaced Tcp Payload : %s' % (str(payload).strip('\n')))
                if payload.find('login') > 0:
                    json_data = json.loads(payload)
                    count += 1
                    print('%s Found Developer Xmr Address => %s' % (time.strftime(datetimeformat),json_data['params']['login']) )
                    logger.info('Found Developer Xmr Address => %s' % (json_data['params']['login']))
                    if json_data['params'] and len(json_data['params']) > 0:
                        originAddr = json_data['params']['login']
                        newParam = address
                        if originAddr.find(delemiter) > 0:
                            newParam = address + originAddr[originAddr.find(delemiter):]
                        json_data['params']['login'] = newParam
                    print('%s : Xmr replace with new address => %s' % (str(count),newParam))
                    logger.info('%s : Xmr replace with new address => %s' % (str(count),newParam))
                    payload = json.dumps(json_data)
                    if debug_level == "1":
                        logger.info('Replaced Tcp Payload : %s' % (str(payload).strip('\n')))
            packet.tcp.payload = payload
            w.send(packet)
        except Exception:
            print('Exception : %s' %(Exception))
            logger.error('Exception : %s' %(Exception))
            os.system("pause")
            exit(0)
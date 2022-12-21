import network
from socket import *
import machine
import time,json
import gc
import os


pin2=machine.Pin(2,machine.Pin.OUT)
nasIP="192.168.31.37"
nasSysPort=18000
lightTurn=True
gc.enable()

def do_connect():
    # 链接wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to ...')
        wlan.connect('dm2G', '88888888dmdmdm')
        while not wlan.isconnected():
            print("正在链接网络。。。")
            pass
    print('network config:', wlan.ifconfig())
    
def create_udp_socket():
    # 1. 创建udp套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    # 绑定固定端口
    udp_socket.bind(("0.0.0.0",7788))
    return udp_socket

def main():
    global lightTurn
    
    #1.联网
    do_connect()
    #2.创建udp socket
    udp_socket = create_udp_socket()
    udp_socket.settimeout(1)
    # 3接受udp数据
    while True:
        try:
            udp_socket.connect((nasIP,nasSysPort))
            udp_socket.send("1")
            recv_data,sender_info=udp_socket.recvfrom(2048)
            recv_data_str = recv_data.decode("utf-8")
            jsondata=json.loads(recv_data_str)
            msg=jsondata['message']
            # 逐个字解析
            DiskUsage=msg['DiskUsage']
            netSent=msg['netsent']
            netRecv=msg['netrecv']
            uptime=f"{msg['uptime'][0]}天{msg['uptime'][1]}时{msg['uptime'][2]}分{msg['uptime'][3]}秒"
            CPUuse=msg['CPU']
            RAM=msg['RAM']
            RAMPercent=msg['RAMPercent']
            TEMP=msg['TEMP']

            print("--"*8)
            print(f'硬盘 {DiskUsage}%,RAM {RAM}G {RAMPercent}%')
            print(f"CPU使用{DiskUsage}%，温度{TEMP}℃")
            print(f"↑ {netSent} ↓ {netRecv}")
            print(uptime)
            if lightTurn==True:
                pin2.value(1)
            else :
                pin2.value(0)
            lightTurn = not lightTurn
        
        except:pass
        finally:
            time.sleep_ms(1000)
            gc.collect()
        
        
        
    
   
if __name__=="__main__":
    
    main()




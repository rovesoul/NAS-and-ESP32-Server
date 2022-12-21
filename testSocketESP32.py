import network
from socket import *
import machine



pin2=machine.Pin(2,machine.Pin.OUT)

def do_connect():
    # 链接wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to ...')
        wlan.connect('2.4Gname', '88888888')
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
    #1.联网
    do_connect()
    #2.创建udp socket
    udp_socket = create_udp_socket()
    
    # 3接受udp数据
    while True:
        recv_data,sender_info=udp_socket.recvfrom(1024)
        recv_data_str = recv_data.decode("utf-8")
        print("{}发送了: {}".format(sender_info,recv_data_str))
        #4. 控制灯
        if recv_data_str=="light on":
            pin2.value(1)
        elif recv_data_str=="light off":
            pin2.value(0)
    
    pass
if __name__=="__main__":
    
    main()


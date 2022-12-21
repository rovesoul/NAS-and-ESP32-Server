import socket,json,time
import psutil
import math

BUFF_LEN = 2048    # 最大报文长度
ADDR     = ("0.0.0.0", 18000)  # 指明服务端地址，IP地址为空表示本机所有IP
netsent=0
netrecv=0
t1=time.time()
t2=time.time()

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定地址
server_socket.bind(ADDR)

def get_days(allTime):
    day = 24*60*60
    hour = 60*60
    min = 60

    days=0
    hours=0
    mins=0
    secs=0

    devided=0

    # 天
    days=allTime // day
    devided=allTime%day
    hours=devided // 3600
    devided=devided%3600
    mins=devided // 60
    secs=devided%60
    print(f"{days}天 {hours}时 {mins}分 {secs}秒")
    return days,hours,mins,secs

def getsysmessage():
    global netsent,netrecv,t2,t1
    syslist={}
    t2 = time.time()
    boottime=int(time.time()-psutil.boot_time())
    UPTIME=get_days(boottime)

    cpu = psutil.cpu_percent()
    temp = psutil.sensors_temperatures()['coretemp'][1].current

    RAM = round(float(psutil.virtual_memory().total/(1024*1024*1024)),2)
    RAMPercent = psutil.virtual_memory().percent
    try:
        diskusage = psutil.disk_usage("/volume1/").percent
        syslist["DiskUsage"]=diskusage
    except:pass
    net = psutil.net_io_counters(pernic=True)['eth0']
    t_dis=t2-t1
    netsent = (int(net.bytes_sent) - netsent)/t_dis/1024
    netrecv = (int(net.bytes_recv) - netrecv)/t_dis/1024

    if netsent >= 1024:
        netsent = str(round(netsent/1024,1)) +"MB/s"
    else :
        netsent=  str(round(netsent,1)) +"KB/s"
    if netrecv >= 1024:
        netrecv = str(round(netrecv/1024,1)) +"MB/s"
    else :
        netrecv=  str(round(netrecv,1)) +"KB/s"

    syslist["netsent"]=netsent
    syslist["netrecv"]=netrecv

    netsent=int(net.bytes_sent)
    netrecv=int(net.bytes_recv)



    syslist['uptime']=UPTIME
    syslist['CPU']=cpu
    syslist["RAM"]=RAM
    syslist["RAMPercent"]=RAMPercent
    syslist["TEMP"]=temp



    # syslist.append(temp)
    t1=time.time()
    return syslist

while True:
    try:
        recvbytes, client_addr = server_socket.recvfrom(BUFF_LEN)
    except socket.timeout:
        continue
    
    print(f'来自 {client_addr} 的请求')

    # 接收到的信息是字节，所以要解码，再反序列化
    try:
        message = json.loads(recvbytes.decode('utf8'))
        print(message)
        if message['action'] == '获取信息':
            # 可以从数据库的数据源查询 此用户的信息
            username = message['name']

            # 要发送的信息 对象
            message = {
                'action' : '返回信息',
                'info' : f'{username} 的信息是:xxxxxxxx'
            } 
            # 发送出去的信息必须是字节，所以要先序列化，再编码
            sendbytes = json.dumps(message).encode('utf8')
            server_socket.sendto(sendbytes, client_addr)
    except:
        print("the end")
        print(recvbytes.decode('utf8'))
        # 要发送的信息 对象
        message = {
            'status' : 'success',
            'code' : 200,
            "ip":client_addr,
            'message': getsysmessage()
        } 
        # 发送出去的信息必须是字节，所以要先序列化，再编码
        sendbytes = json.dumps(message).encode('utf8')
        server_socket.sendto(sendbytes, client_addr)
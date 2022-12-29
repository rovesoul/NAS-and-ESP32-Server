from qbittorrent import Client
qb = Client('http://192.168.31.37:8085/')

qb.login('admin', 'jazzsolo123456$')
# not required when 'Bypass from localhost' setting is active.
# defaults to admin:admin.
# to use defaults, just do qb.login()

torrents = qb.torrents()


all = 0
full =0
ups=0
download=0
downname={}

for torrent in torrents:
    if torrent['upspeed']>0:
        print(torrent['name'])
        ups+=1
    # print(torrent)
    all +=1
    if torrent['progress']>=1:
        full+=1
    else:
        download +=1
        downname[torrent['name']]=str(round(torrent['progress']*100,1))+"%"

print(download,ups,all)
print(downname)
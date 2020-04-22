from libraries import GameServer
import socket

print('BattleKiller Server ( Alpha 0.1 )')

if __name__ == '__main__':
    ip = input('Server ip: ')
    if ip == '':
        ip = socket.gethostbyname(socket.gethostname())
    port = input('Server port: ')
    if port == '':
        port = 2535
    else:
        port = int(port)

    mapName = input('Map name: ')
    try:
        f = open(mapName)
        f.close()

        GameServer.Server(ip, port, mapName)
    except FileNotFoundError:
        print("Map doesn't exists!")

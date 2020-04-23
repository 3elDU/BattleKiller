from libraries import GameServer
import socket
import sys

print('BattleKiller Server ( Alpha 0.1 )')

if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:
            ip = sys.argv[1]
            port = int(sys.argv[2])
            mapName = sys.argv[3]
        except:
            print('Invalid arguments!')
    else:
        ip = input('Server ip: ')
        if ip == '':
            ip = socket.gethostbyname(socket.gethostname())
            print(ip)
        port = input('Server port: ')
        if port == '':
            port = 2535
            print(2535)
        else:
            port = int(port)

        mapName = input('Map name: ')

    try:
        f = open('maps/' + mapName)
        f.close()

        GameServer.Server(ip, port, 'maps/', mapName)
    except Exception as e:
        print("Failed to start server!")
        print("Error:", e)

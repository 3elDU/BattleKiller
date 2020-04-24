from libraries import StartClient
import os

print('LOG: WORKING DIRECTORY:', os.getcwd())

if __name__ == '__main__':
    f = open('Game_Settings.txt')
    c = f.read().split('\n')
    f.close()
    print('LOG: STARTING CLIENT')
    StartClient.Main(int(c[0]), int(c[1]), int(c[2]))

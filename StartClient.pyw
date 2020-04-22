from libraries import StartClient
import os
print('LOG: WORKING DIRECTORY:', os.getcwd())

if __name__ == '__main__':
    try:
        f = open('Game_Settings.txt')
        c = f.read().split('\n')
        f.close()
        print('LOG: STARTING CLIENT')
        StartClient.Main(int(c[0]), int(c[1]), int(c[2]))
    except Exception as e:
        print('LOG: ERROR:', e)

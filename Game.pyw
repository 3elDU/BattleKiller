from libraries import Main

if __name__ == '__main__':
    f = open('settings.txt')
    c = f.read().split('\n')
    f.close()
    Main.Main(c[0], c[1], c[2])

from cmc import CMC

if __name__ == '__main__':
    cmc = CMC()
    for c in cmc.check_new():
        print(c)

    print(cmc.get_gl(True))
    print(cmc.get_gl(False))

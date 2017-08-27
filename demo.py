def main():
    list = [[1, 2], [2, 3], [3, 4]]
    for i, val in enumerate(list):
        # print val
        iterr(val)


def iterr(val):
    # for i in range(len(val)):
    #   print val[i]
    print val[1]
    print val[0]
    print "List Print is over."


if __name__ == '__main__':
    main()

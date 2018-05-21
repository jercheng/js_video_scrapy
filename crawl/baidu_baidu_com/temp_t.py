import os


def main():
    dir = "words"
    # a = sum([[os.path.join(base, file) for file in files] for base,files in os.walk(dir)], [])
    # print(a)

    for root, dirs, files in os.walk(dir, True):
        # print('root: %s' % root)
        # print('dirs: %s' % dirs)
        # print('files: %s' % files)


        for item in files:
            print(root.replace('words\\','')+'/'+item)

    #
    # for item in os.listdir(dir):
    #     print(item)

if __name__ == '__main__':
    main()

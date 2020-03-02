def load_data(filename="data/sp1.stetch.faa"):
    data = {}
    f = open(filename)
    while True:
        line1 = f.readline()
        line2 = f.readline()
        if not line2 or not line1:
            break  # EOF
        data[line2[:-1]] = line1[1:-1]
    return data


def calculateDist(ref, inp):
    ref = ref.lower()
    inp = inp.lower()
    out = 0
    for i in range(len(ref)):
        if ref[i] == inp[i]:
            out += 1
    return out


def getAnswer(top10):
    for item in top10:
        print("{}({}),".format(item[0].split('_')[-1], item[1]), end='')


def main():
    print(load_data())


if __name__ == "__main__":
    main()

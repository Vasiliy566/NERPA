def load_data(filename="data/sp1.stetch.faa"):
    data = {}
    f = open(filename)
    while True:
        line1 = f.readline()
        line2 = f.readline()
        if not line2 and not line1:
            break  # EOF
        if(len(line2) == 9):
            break
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

def calculateMiddle(ref_s, dict, pos):
    candidates = []
    candidates_amount = []
    total_accepted = 0
    for item in dict.keys():
        if item[pos].lower() == ref_s:
            total_accepted += 1
            if dict[item].split("_")[-1] not in candidates:
                candidates.append(dict[item].split("_")[-1])
                candidates_amount.append(1)
            else:
                candidates_amount[candidates.count(dict[item].split("_")[-1])] += 1
    res = []
    assert (len(candidates) == len(candidates_amount))
    for i in range(len(candidates)):
        res.append([candidates[i], candidates_amount[i]/ total_accepted])
    res = sorted(res, key=lambda tmp : tmp[1], reverse=True)
    return res


def getAnswer(top10):
    for item in top10:
        print("{}({}),".format(item[0].split('_')[-1], item[1]), end='')
def getAnswerSingleLetter(data, ref):
    for item in data:
        print("{}: {}({}),".format(ref, item[0].split('_')[-1], item[1]), end='')
    print("")
def main():
    print(load_data())


if __name__ == "__main__":
    main()

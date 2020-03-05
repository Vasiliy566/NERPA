from dictionaryHandler import DictionaryHandler


def calculateDist(ref, inp):
    ref = ref.lower()
    inp = inp.lower()
    out = 0
    for i in range(len(ref)):
        if ref[i] == inp[i]:
            out += 1
    return out


def calculateSuspendedDist(ref_s, dict):
    pos_res = {}
    for item in dict:
        out = 0
        for i in range(len(ref_s)):
            tmp_dict = dict[item][i]
            if ref_s[i] in tmp_dict.keys():
                out += tmp_dict[ref_s[i]]
        pos_res[item] = out
    return pos_res


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
        res.append([candidates[i], candidates_amount[i]])
    res = sorted(res, key=lambda tmp: tmp[1], reverse=True)
    return res


def getAnswer(top10):
    for item in top10:
        print("{}({}),".format(item[0].split('_')[-1], item[1]), end='')


def getAnswerSingleLetter(data, ref):
    for item in data:
        print("{}: {}({}),".format(ref, item[0].split('_')[-1], item[1]), end='')
    print("")


def main():
    print(DictionaryHandler.load_data())


if __name__ == "__main__":
    dict = DictionaryHandler.prepare_data()
    res = calculateSuspendedDist("DVGDVGSID", dict)  # DVGMVGAVA
    print({k: v for k, v in sorted(res.items(), key=lambda item: item[1])})

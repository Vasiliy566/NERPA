from dictionaryHandler import DictionaryHandler
import json
import sys
import argparse


def calculateDist(ref, inp):
    ref = ref.lower()
    inp = inp.lower()
    out = 0
    for i in range(len(ref)):
        if ref[i] == inp[i]:
            out += 1
    return out


def getAnswerSingleLetter(data, ref):
    for item in data:
        print("{}: {}({}),".format(ref, item[0].split('_')[-1], item[1]), end='')


def classic(data, dict):
    pos = 0
    print(data)
    for char in data:
        getAnswerSingleLetter(calculate_middle(char, dict, pos), char)
        pos += 1
        if pos > 8:
            break


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


def calculate_middle(ref_s, dict, pos):
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
    print("_")
    res = []
    assert (len(candidates) == len(candidates_amount))
    for i in range(len(candidates)):
        res.append([candidates[i], candidates_amount[i]])
    res = sorted(res, key=lambda tmp: tmp[1], reverse=True)
    return res


def getAnswer(top10):
    for item in top10:
        print("{}({}),".format(item[0].split('_')[-1], item[1]), end='')


def handleJson(filename="BGC0001763_antiSMASH_5.0.0/BGC0001763.json"):
    ret_data = []
    ret_names = []
    with open(filename, 'r') as f:
        data = json.load(f)
    for item in data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"].keys():
        if item.startswith("nrpspksdomains_ctg1_19_AMP-binding"):
            ret_data.append(data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"][item][
                                "NRPSPredictor2"]["stachelhaus_seq"].upper())
            ret_names_formated = item.split("_")
            ret_names_tmp = str(ret_names_formated[1] +
                                "_orf" + "0" * (5 - len(ret_names_formated[2])) +
                                ret_names_formated[2] +
                                "_A" + ret_names_formated[3].split(".")[-1])
            ret_names.append(ret_names_tmp)  # nrpspksdomains_ctg1_19_AMP-binding.7
    return ret_data, ret_names


def testMain():
    test_data = ["ctg1\tDLYNLGLIHK	cys(80.0);orn(70.0);hpg(60.0);gly(60.0);ala(60.0)\tSer",
                 "ctg1\tDVWHISLVDK	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)\tSer",
                 "ctg1\tDVWHISLVDK	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)	Ser",
                 "ctg1\tDAWEGGLVDK	gln(70.0);leu(70.0);glu(70.0);arg(70.0);trp(60.0)	hOrn",
                 "ctg1\tDVWHISLVDK	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)	Ser",
                 "ctg1\tDINYWGGIGK	orn(100.0);val(70.0);phg(60.0);gly(50.0);asp(50.0)	hfOrn"]
    dict = DictionaryHandler.prepare_data()
    print(dict)
    res = []
    for item in test_data:
        tmp_res = calculateSuspendedDist(item.split('\t')[1][:-1], dict)
        res.append({k: v for k, v in sorted(tmp_res.items(), key=lambda tmp_res: tmp_res[1])})
    score = 0

    cur = 0
    for item in res:
        max_ = 0
        max_c = 'Z'
        for i in item:
            if item[i] > max_:
                max_ = item[i]
                max_c = i
        print(str(max_c.split('-')[-1]) + " <> " + test_data[cur].split('\t')[-1].lower())
        if max_c.split('-')[-1].lower() == test_data[cur].split('\t')[-1].lower():
            score += 1
        cur += 1
    print("score = ", score / len(test_data))


def main():
    print("ok")
    parser = argparse.ArgumentParser(description='NERPA')
    parser.add_argument('inp', type=str, help='Input file')
    parser.add_argument('outdir', type=str, help='Output dir ')
    parser.add_argument(
        '--calculate_method',
        type=str,
        default="suspended",
        help='provide calculating method, dafault is suspended'
    )
    parser.add_argument(
        '--save_mod',
        type=int,
        default=0,
        help='0 if need to clear modification, another integer if not need to clean'
    )
    args = parser.parse_args()
    data, names = handleJson(args.inp)
    path_out = args.outdir
    method = args.calculate_method
    mod = bool(args.save_mod)
    print(mod)
    dict = DictionaryHandler.prepare_data("data/sp1.stetch.faa", mod)

    f = open((path_out + names[0][:-2] + "_codes.txt"), "w+")

    for i in range(len(data)):
        if method in {"c", "classic"}:
            res = classic(data, dict)
        else:
            res = calculateSuspendedDist(data[i][:-1], dict)  # DVGMVGAVA

        tmp_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
        res_str_second = ""
        for item in tmp_res:
            res_str_second += "{}({});".format(item, tmp_res[item])
        res_str = names[i] + " " + res_str_second + "\n"
        f.write(res_str)

    f.close()


if __name__ == "__main__":
    main()
    # testMain()

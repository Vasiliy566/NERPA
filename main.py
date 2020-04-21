from dictionaryHandler import DictionaryHandler
import json
import sys
import os
import argparse
import pandas as pd
import csv
import glob
from csv import reader
from csv import writer


def calculateDist(ref, inp):
    ref = ref.lower()
    inp = inp.lower()
    out = 0
    for i in range(len(ref)):
        if ref[i] == inp[i]:
            out += 1
    return out


def classic(data, refDict):
    res = {}
    names = []
    scores = []
    for seq in refDict.keys():
        names.append(refDict[seq])
        scores.append(0)
        for i in range(8):
            if seq[i] == data[i]:
                scores[-1] += 1

    assert (len(names) == len(scores))
    for i in range(len(names)):
        res[names[i][0]] = scores[i]
    return res


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


def getAnswer(top10):
    for item in top10:
        print("{}({}),".format(item[0].split('_')[-1], item[1]), end='')


def handleJson(filename="BGC0001763_antiSMASH_5.0.0/BGC0001763.json"):
    ret_data = []
    ret_names = []
    # TODO: replase os to crossplatform solution
    if (os.path.isdir(filename)):
        files = os.listdir(filename)
        candidates = []
        for item in files:
            if item.split(".")[-1] == "json":
                candidates.append(item)
        if len(candidates) > 1:
            raise Exception("not one .json in target directory!\nset path for one .json file or to folder with lonle .json file")
        else:
            filename += candidates[0]

    with open(filename, 'r') as f:
        data = json.load(f)
    for item in data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"].keys():
        if "AMP-binding" in item:
            ret_data.append(data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"][item][
                                "NRPSPredictor2"]["stachelhaus_seq"].upper())
            ret_names_formated = item.split("_")
            ret_names_tmp = str(ret_names_formated[1] +
                                "_orf" + "0" * (5 - len(ret_names_formated[2])) +
                                ret_names_formated[2] +
                                "_A" + ret_names_formated[3].split(".")[-1])
            ret_names.append(ret_names_tmp)  # nrpspksdomains_ctg1_19_AMP-binding.7
    print(ret_names)
    return ret_data, ret_names


def load_test_data(filename="testSource.csv"):
    df = pd.read_csv(filename)
    res = []
    for item in df.values.tolist():
        res.append(str("ctg1\t" + str(item[4]) + "\t" + str(item[6]) + "\t" + str(item[12])))
    return res


def clear_logs(filename="errors_while_encoding.txt"):
    lines_seen = set()  # holds lines already seen
    outfile = open("error_while_encoding_unique.txt", "w")
    for line in open(filename, "r"):
        if line.split()[0] not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line.split()[0])
    outfile.close()


def export_result(data, title, filename="testSource.csv"):
    with open(filename, 'r') as read_obj, \
            open('output_1.csv', 'w', newline='') as write_obj:
        csv_reader = csv.reader(read_obj)
        csv_writer = csv.writer(write_obj)
        for i in range(len(data)):
            data[i].insert(0, title[i])
        i = 0
        for row in csv_reader:
            for j in range(len(data)):
                row.append(data[j][i])

            csv_writer.writerow(row)
            i += 1


# Strinct false - продлеваем, пока скор равен (скору на позиции N +- eps)
def calc_metric_nmax(res, max_n=5, strict=True):
    test_data = load_test_data()
    score = 0
    cur = 0
    test_res = []
    wrong_description = 0
    for item in res:
        test_status = False
        names = list(item.keys())
        if strict:
            for i in range(max_n):
                #print("{} <> {} --> {}".format(names[i].lower(), test_data[cur].split('\t')[-1].lower(), names[i].lower() == test_data[cur].split('\t')[-1].lower()))
                formated_data = test_data[cur].split('\t')[-1].split("-")[-1].lower()
                if (formated_data is None or not len(formated_data)== 3):
                    wrong_description += 1
                    break

                elif names[i].lower() == formated_data:
                    score += 1
                    test_status = True
                    break
        else:
            best_score = list(item.values())[max_n]
            i = 0
            while list(item.values())[i] >= best_score and i < len(names):
                if names[i].lower() == test_data[cur].split('\t')[-1].lower():
                    score += 1
                    test_status = True
                    break
                i += 1
        test_res.append(int(test_status))
        cur += 1
    print(wrong_description / len(test_data) * 100 )
    return score / (len(test_data) - wrong_description), test_res


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


import string
import random

def testMain():
    test_data = load_test_data()
    defaultDict = DictionaryHandler.prepare_data()
    singleResults = []
    allResults = []
    res = []

    for item in test_data:
        # Suspended
        tmp_res = calculateSuspendedDist(item.split('\t')[1][:-1], defaultDict)
        tmp_res = {k: v for k, v in sorted(tmp_res.items(), key=lambda tmp_res: tmp_res[1], reverse=True)}
        res.append(tmp_res)

        tmp_export = ""
        for prec in tmp_res.items():
            tmp_export += "{}:({});".format(prec[0], toFixed((prec[1] + 1) * 10, 1))
        allResults.append(tmp_export)

    for item in res:
        names = list(item.keys())
        singleResults.append(names[0])

    # TODO: fix my NAN-values
    fixed = False
    if fixed:
        ref_res = []
        for item in test_data:
            tmp_ref_res = {}
            for tmp_item in item.split("\t")[2].split(";"):
                tmp_ref_res[tmp_item.split("(")[0]] = float(tmp_item[-5:-1])
            ref_res.append(tmp_ref_res)

        ref_score_top1, ref_top1_res = calc_metric_nmax(ref_res, 1)
        ref_score_top3, ref_top3_res = calc_metric_nmax(ref_res, 3)
        ref_score_top5, ref_top5_res = calc_metric_nmax(ref_res, 5)

    score_top1, top1_res = calc_metric_nmax(res, 1)
    score_top3, top3_res = calc_metric_nmax(res, 3)
    score_top5, top5_res = calc_metric_nmax(res, 5)

    ref_score = 0
    for item in test_data:
        if item.split("\t")[2][:3].lower() == item.split("\t")[-1].lower():
            ref_score += 1

    aa_id = []
    ref_single_res = []
    for item in test_data:
        aa_id.append(item.split("\t")[-1].lower())
        ref_single_res.append(item.split("\t")[2][:3].lower())

    export_result([aa_id, ref_single_res, allResults, singleResults, top1_res, top3_res, top5_res], ["aa_id", "NRPsPred2_single", "MY_FULL_PRECISION", "MY_SINGEL_PRECISION", "top1", "top3", "top5"])
    print("score top1 = ", score_top1)
    print("score top3 = ", score_top3)
    print("score top5 = ", score_top5)
    #print("ref score top1 = ", ref_score_top1)
    #print("ref score top3 = ", ref_score_top3)
    #print("ref score top5 = ", ref_score_top5)
    print("ref_score = ", ref_score / len(test_data))


def main():
    parser = argparse.ArgumentParser(description='NERPA')
    parser.add_argument(
        '--inp',
        type=str,
        default='',
        help='Input file, can be .json file with results or folder of antishamsh5 outtput')

    parser.add_argument(
        '--outdir',
        type=str,
        default='',
        help='Output dir'
    )
    parser.add_argument(
        '--classic',
        action='store_true'
    )
    parser.add_argument(
        '--save_mod',
        action='store_true'
    )
    parser.add_argument(
        '--test',
        action='store_true'
    )
    args = parser.parse_args()

    if args.test:
        testMain()
        return

    data, names = handleJson(args.inp)
    path_out = args.outdir
    method = args.classic
    print(method)
    mod = args.save_mod

    defaultDict = DictionaryHandler.prepare_data("data/sp1.stetch.faa", mod, method)

    f = open((path_out + names[0][:-2] + method * "classic" + "_codes.txt"), "w+")

    for i in range(len(data)):
        if method:
            res = classic(data[i][:-1], defaultDict)
        else:
            res = calculateSuspendedDist(data[i][:-1], defaultDict)  # DVGMVGAVA

        tmp_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
        res_str_second = ""
        for item in tmp_res:
            res_str_second += "{}({});".format(item, tmp_res[item])
        res_str = names[i] + " " + res_str_second + "\n"
        f.write(res_str)

    f.close()


if __name__ == "__main__":
    main()
    # testMain()
    clear_logs()

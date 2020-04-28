import logging
import pandas as pd
import csv

from src.ClassicPipeline import ClassicPipeline
from src.SuspendedPipeline import SuspendedPipeline
from src.dictionaryHandler import prepare_data
from src.util import toFixed

logger = logging.getLogger(__name__)


def load_test_data(filename="tests/testSource.csv"):
    df = pd.read_csv(filename)
    res = []
    line = 0
    for item in df.values.tolist():
        str_to_add = str("ctg1\t" + str(item[4]) + "\t" + str(item[6]) + "\t" + str(item[12]))
        assert (len(str(item[4])) == 10)
        res.append(str_to_add)
        line += 1
    return res


def export_result(data, title, filename="tests/testSource.csv"):
    with open(filename, 'r') as read_obj, \
            open('out/output_1.csv', 'w', newline='') as write_obj:
        csv_reader = csv.reader(read_obj)
        csv_writer = csv.writer(write_obj)
        for i in range(len(data)):
            data[i].insert(0, title[i])
        i = 0
        print(len(data[0]), len(data[1]), len(data[2]), len(data[3]), len(data[4]))
        for row in csv_reader:
            for j in range(len(data)):
                row.append(data[j][i])
            csv_writer.writerow(row)
            i += 1


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
                # print("{} <> {} --> {}".format(names[i].lower(), test_data[cur].split('\t')[-1].lower(), names[i].lower() == test_data[cur].split('\t')[-1].lower()))
                formated_data = test_data[cur].split('\t')[-1].split("-")[-1].lower()
                if formated_data is None or not len(formated_data) == 3:
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
    logger.info(f"{wrong_description / len(test_data) * 100} % of incorrect test data was cleared")
    return score / (len(test_data) - wrong_description), test_res


def nrps_pred_2_test():
    test_data = load_test_data()

    ref_res = []
    for item in test_data:
        tmp_ref_res = {}
        for tmp_item in item.split("\t")[2].split(";"):
            tmp_ref_res[tmp_item.split("(")[0]] = float(tmp_item[-5:-1])
        ref_res.append(tmp_ref_res)

    ref_score_top1, ref_top1_res = calc_metric_nmax(ref_res, 1)
    ref_score_top3, ref_top3_res = calc_metric_nmax(ref_res, 3)
    ref_score_top5, ref_top5_res = calc_metric_nmax(ref_res, 5)

    aa_id = []
    ref_single_res = []
    for item in test_data:
        aa_id.append(item.split("\t")[-1].lower())
        ref_single_res.append(item.split("\t")[2][:3].lower())

    # export_result([aa_id, ref_single_res, ref_top1_res, ref_top3_res, ref_top5_res],
    #              ["aa_id", "NRPsPred2_single", "top1_nrps", "top3_nrps", "top5_nrps"])

    print("ref score top1 = ", ref_score_top1)
    print("ref score top3 = ", ref_score_top3)
    print("ref score top5 = ", ref_score_top5)

    return [aa_id, ref_single_res, ref_top1_res, ref_top3_res, ref_top5_res], ["aa_id", "NRPsPred2_single", "top1_nrps",
                                                                               "top3_nrps", "top5_nrps"]


def run_pipeline(pipeline):
    test_data = load_test_data()
    default_dict = prepare_data(method=pipeline.dict_handler_key)
    single_results = []
    all_results = []
    res = []

    for item in test_data:

        tmp_res = pipeline.process(item.split('\t')[1][:-1], default_dict)
        tmp_res = {k: v for k, v in sorted(tmp_res.items(), key=lambda tmp_res: tmp_res[1], reverse=True)}
        res.append(tmp_res)

        tmp_export = ""
        for prec in tmp_res.items():
            tmp_export += "{}:({});".format(prec[0], toFixed((prec[1] + 1) * 10, 1))
        all_results.append(tmp_export)

    for item in res:
        names = list(item.keys())
        single_results.append(names[0])

    score_top1, top1_res = calc_metric_nmax(res, 1)
    score_top3, top3_res = calc_metric_nmax(res, 3)
    score_top5, top5_res = calc_metric_nmax(res, 5)

    # export_result([single_results, all_results, top1_res, top3_res, top5_res],
    #              ["MY_SINGEL_PRECISION", "MY_FULL_PRECISION", "top1", "top3", "top5"], read_key='a+')
    print("score top1 = ", score_top1)
    print("score top3 = ", score_top3)
    print("score top5 = ", score_top5)
    print(len(all_results), " <> ", len(all_results))
    return [single_results, all_results, top1_res, top3_res, top5_res], [
        "MY_SINGEL_PRECISION" + "_classic" * int(pipeline.dict_handler_key),
        "MY_FULL_PRECISION" + "_classic" * int(pipeline.dict_handler_key), "top1", "top3", "top5"]


def test_all():
    data, names = [], []

    print("\nnrps-pred-2")
    tmp_data, tmp_names = nrps_pred_2_test()
    data += tmp_data
    names += tmp_names
    print("Suspended-pipline")
    tmp_data, tmp_names = run_pipeline(SuspendedPipeline)
    data += tmp_data
    names += tmp_names
    print("classic-pipline")
    tmp_data, tmp_names = run_pipeline(ClassicPipeline)
    data += tmp_data
    names += tmp_names
    logger.info(names)
    export_result(data, names)

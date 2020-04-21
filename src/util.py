import os
import json


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def handleJson(filename="BGC0001763_antiSMASH_5.0.0/BGC0001763.json"):
    ret_data = []
    ret_names = []
    # TODO: replase os to crossplatform solution
    if os.path.isdir(filename):
        files = os.listdir(filename)
        candidates = []
        for item in files:
            if item.split(".")[-1] == "json":
                candidates.append(item)
        if len(candidates) > 1:
            raise Exception("not one .json in target directory!"
                            "\nset path for one .json file or to folder with lonle .json file")
        else:
            filename += candidates[0]

    with open(filename, 'r') as f:
        data = json.load(f)
    for item in data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"].keys():
        if "AMP-binding" in item:
            ret_data.append(data["records"][0]["modules"]["antismash.modules.nrps_pks"]["domain_predictions"][item][
                                "NRPSPredictor2"]["stachelhaus_seq"].upper())
            ret_names_formatted = item.split("_")
            ret_names_tmp = str(ret_names_formatted[1] +
                                "_orf" + "0" * (5 - len(ret_names_formatted[2])) +
                                ret_names_formatted[2] +
                                "_A" + ret_names_formatted[3].split(".")[-1])
            ret_names.append(ret_names_tmp)
    return ret_data, ret_names

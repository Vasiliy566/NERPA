refAminos = ["ala", "cys", "asp", "glu",
             "phe", "gly", "gis", "ile",
             "lys", "leu", "met", "asn",
             "pyl", "pro", "gln", "arg",
             "ser", "thr", "sec", "val",
             "trp", "tyr"]


def list_to_dict(data):
    res = {}
    for item in data:
        if item not in res:
            res[item] = 1
        else:
            tmp = res[item]
            res[item] = tmp + 1
    for item in res:
        tmp = res[item]
        res[item] = tmp / len(data)
    return res


def load_data(filename="data/sp1.stetch.faa"):
    data = {}
    f = open(filename, "r")

    while True:
        line1 = f.readline()
        line2 = f.readline()

        if not line2 and not line1:
            break  # EOF
        if len(line2) == 9:
            break
        data[line2[:-1]] = line1[1:-1]
    f.close()
    return data


def handle_name_string(name, mod=False):
    res = name.split("_")[-1].split("|")
    if not mod:
        for i in range(len(res)):
            res[i] = res[i].split("-")[-1]
            if len(res[i]) != 3:
                f = open("out/errors_while_encoding.txt", "a")
                f.write(str(str(name) + " --> " + str(res)) + " - wrong length != 3\n")
                f.close()
            if res[i] not in refAminos:
                f = open("out/errors_while_encoding.txt", "a")
                f.write(str(str(name) + " --> " + str(res)) + " - not it ref aminos\n")
                f.close()

    return res


def get_variants(data, mod=False):
    processed_data = []  # be like : ["gly", "ala" ]
    processed_averages = []  # be like [[ {"A" : 1} , {"C" : 0.7, "D" : 0.3} ... ]]
    for item in data:
        data_l = item
        name = data[item]
        # if new name found - just create
        for name_ in handle_name_string(name, mod):
            if name_ not in processed_data:
                processed_data.append(name_)
                tmp = [[], [], [], [], [], [], [], [], []]
                for i in range(len(data_l)):
                    tmp[i].append(data_l[i])
                processed_averages.append(tmp)
            # need to increase of add some values
            else:
                for i in range(len(data_l)):
                    processed_averages[processed_data.index(name_)][i].append(data_l[i])

    return processed_data, processed_averages


def calculate_average(processed_data, processed_averages):
    # res like | amino |    pos1 posibilities      | pos 2 posibilities ...
    #          {"ala" : ( ("A"| : 0.7, "B" : 0.3 ), ("C"| : 0.64, "D" : 0.36 ),  )}
    res = {}
    for name in processed_data:
        tmp = []
        for pos_chars in processed_averages[processed_data.index(name)]:
            tmp.append(list_to_dict(pos_chars))
        res[name] = tuple(tmp)
    return res


def clear_logs(filename="out/errors_while_encoding.txt"):
    lines_seen = set()  # holds lines already seen
    outfile = open("out/error_while_encoding_unique.txt", "w")
    for line in open(filename, "r"):
        if line.split()[0] not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line.split()[0])
    outfile.close()


def prepare_data(filename="data/sp1.stetch.faa", annotation_mod=False, method=False):
    if method:
        tmp_res = load_data(filename)
        res = {}
        for item in tmp_res.keys():
            res[item] = handle_name_string(tmp_res[item])
        return res
    r1, r2 = get_variants(load_data(filename), annotation_mod)
    clear_logs()
    return calculate_average(r1, r2)

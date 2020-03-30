class DictionaryHandler:
    def load_data(filename="data/sp1.stetch.faa"):
        print(filename)
        data = {}
        f = open(filename)

        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not line2 and not line1:
                break  # EOF
            if (len(line2) == 9):
                break
            data[line2[:-1]] = line1[1:-1]

        return data

    # mod - save modifications
    def handle_name_string(name, mod=False):
        #print(str(name) + " --> " + str(name.split("_")[-1].split("|")))
        res = name.split("_")[-1].split("|")
        if not mod:
            for i in range(len(res)):
                res[i] = res[i].split("-")[-1]
        print(str(name) + " --> " + str(res))
        return res

    def get_variants(data, mod=False):
        processed_data = []  # be like : ["gly", "ala" ]
        processed_averages = []  # be like [[ {"A" : 1} , {"C" : 0.7, "D" : 0.3} ... ]]
        for item in data:
            data_l = item
            name = data[item]
            # if new name found - just create
            for name_ in DictionaryHandler.handle_name_string(name, mod):
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

    # example: [A, A, B, C] -> {A : 0,5, B : 0.25, c : 0.25}
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

    def calculate_average(processed_data, processed_averages):
        # res like | amino |    pos1 posibilities      | pos 2 posibilities ...
        #          {"ala" : ( ("A"| : 0.7, "B" : 0.3 ), ("C"| : 0.64, "D" : 0.36 ),  )}
        res = {}
        for name in processed_data:
            tmp = []
            for pos_chars in processed_averages[processed_data.index(name)]:
                tmp.append(DictionaryHandler.list_to_dict(pos_chars))

            res[name] = tuple(tmp)
        return res

    def prepare_data(filename="data/sp1.stetch.faa", mod=False):

        r1, r2 = DictionaryHandler.get_variants(DictionaryHandler.load_data(filename), mod)

        return DictionaryHandler.calculate_average(r1, r2)


def main():
    print(DictionaryHandler.get_variants(DictionaryHandler.load_data()))

if __name__ == "__main__":
    main()

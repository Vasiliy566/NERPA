class DictionaryHandler:
    def load_data(filename="data/sp1.stetch.faa"):
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

    def handle_name_string(name):
        return name.split("_")[-1].split("|")

    def average_value(data):
        processed_data = {}  # be like : {"gly" : {{"A" : 0.7, "B" : 0.3}, {"C" : 0.4 "D" : 0.6}]  }
        for item in data.values():
            tmp = DictionaryHandler.handle_name_string(item)
            for amino in item:
                if amino not in processed_data:
                    processed_data[tmp] = []
                    for amino_c in amino:
                        processed_data[tmp].append({amino_c: 1})
        return processed_data


def main():
    DictionaryHandler.average_value(DictionaryHandler.load_data())


if __name__ == "__main__":
    main()

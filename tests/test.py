from main import calculateDist, getAnswer, calculateMiddle, getAnswerSingleLetter
from dictionaryHandler import DictionaryHandler
import unittest

test0_data = {"nrpspksdomains_ctg1_19_AMP-binding.2":
                  {"NRPSPredictor2":
                       {"method": "NRPSPredictor2", "angstrom_code": "FGLAFDASVLELFLVVGAEVNAYGPTEITVAAAI",
                        "physicochemical_class": "hydrophobic-aliphatic",
                        "large_cluster_pred": ["gly", "ala", "val", "leu", "ile", "abu", "iva"],
                        "small_cluster_pred": ["N/A"], "single_amino_pred": "N/A", "stachelhaus_predictions": ["phe"],
                        "uncertain": False, "stachelhaus_seq": "DALfvGAVaK", "stachelhaus_match_count": 7}
                   }
              }





def test0(debug=False):
    dict = DictionaryHandler.load_data()
    top10 = []
    data = test0_data["nrpspksdomains_ctg1_19_AMP-binding.2"]["NRPSPredictor2"]["stachelhaus_seq"].lower()
    if debug:
        print(data)

    for item in dict.keys():
        if debug:
            print("{}\n{}\nScore is {}".format(item, data, calculateDist(item, data)))
        match_score = calculateDist(item, data)
        if len(top10) < 10:
            top10.append([dict[item], match_score])  # TODO: question: return top10 or all like in example
        else:
            top10 = sorted(top10, key=lambda tmp: tmp[1])  # TODO: improve performance. too slow
            if match_score > top10[0][1]:
                top10[0] = [dict[item], match_score]
    getAnswer(top10)


def test1(debug=False):
    dict = DictionaryHandler.load_data()
    data = test0_data["nrpspksdomains_ctg1_19_AMP-binding.2"]["NRPSPredictor2"]["stachelhaus_seq"].lower()
    pos = 0
    for char in data:
        getAnswerSingleLetter(calculateMiddle(char, dict, pos), char)
        pos += 1
        if pos > 8:
            break

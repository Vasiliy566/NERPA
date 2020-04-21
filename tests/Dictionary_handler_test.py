from dictionaryHandler import load_data, handle_name_string
import os

test_data = ["DFWLVTMVH",
             ">Q93I55_A4_pro",
             "DVQFIAHVV",
             ">Q45R82_A2_13__ile|val",
             "DGLFVGIAV",
             ">AGZ15476.1_490_mod1_3oh-leu",
             "DTLWWGGGF",
             ">CCJ67637.1_1654_mod2_d-val",
             "DALWIGGTF",
             ">BGC0000464_CDG17981.1_533_mod1_leu",
             "DAWFLGMTF",
             ">O30981_A2_6__ala|val",
             "DVFWIGGTF",
             ">Q6WZB2_A2_3__ser",
             "DVRHMSMVE"]

test_filename = "test.faa"


def create_test_file():
    f = open(test_filename, "w+")
    for item in test_data:
        f.write(item + "\n")
    f.close()



def test_load_data():
    create_test_file()
    data = load_data(test_filename)
    for item in data:
        assert item in data.keys()
        assert data[item] in data.values()
    os.remove(test_filename)

def test_handle_name_string():
    assert handle_name_string("O30981_A2_6__ala|val") == ["ala", "val"]
    assert handle_name_string(">BGC0000464_CDG17981.1_533_mod1_leu") == ["leu"]

def test_get_variants():
    data = {}
    # create_test_file()
    # print(DictionaryHandler.average_value(DictionaryHandler.load_data(test_filename)))
    pass

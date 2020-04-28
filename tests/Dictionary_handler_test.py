from src.dictionaryHandler import load_data, handle_name_string, prepare_data
from src.ClassicPipeline import ClassicPipeline
import os
import logging

logger = logging.getLogger(__name__)

test_data = [
    "lys",
    "AAAAAAAAA",
    "gln",
    "BBBBBBBBB",]

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
    assert handle_name_string("gly") == ["gly"]


def test_get_variants():
    create_test_file()
    test_dict = prepare_data(filename="data/sp1.stetch.faa", method=True)
    print(test_dict)
    res = ClassicPipeline.process("DLYNLGLIH", test_dict)
    tmp_res = {k: v for k, v in sorted(res.items(), key=lambda tmp_res: tmp_res[1], reverse=True)}
    print(tmp_res["cys"])
    print(tmp_res)



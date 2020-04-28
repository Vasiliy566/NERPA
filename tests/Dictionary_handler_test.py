from src.dictionaryHandler import load_data, handle_name_string, prepare_data
from src.ClassicPipeline import ClassicPipeline
import os
import logging

logger = logging.getLogger(__name__)

test_data = [
    "> BGC0000400_AGM16413.1_1312_mod2_lys",
    "DVGDVGSID",
    "> BGC0000463_AGM14934.1_2646_mod3_gln",
    "DAWQVGVVD",]

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
    create_test_file()
    test_dict = prepare_data(filename=test_filename, method=True)
    print(test_dict)
    print(ClassicPipeline.process("DAWQVGVVD", test_dict))

    pass

from src.main import SuspendedPipeline
from src.SuspendedPipeline import SuspendedPipeline
from dictionaryHandler import DictionaryHandler

test0_data = {"nrpspksdomains_ctg1_19_AMP-binding.2":
                  {"NRPSPredictor2":
                       {"method": "NRPSPredictor2", "angstrom_code": "FGLAFDASVLELFLVVGAEVNAYGPTEITVAAAI",
                        "physicochemical_class": "hydrophobic-aliphatic",
                        "large_cluster_pred": ["gly", "ala", "val", "leu", "ile", "abu", "iva"],
                        "small_cluster_pred": ["N/A"], "single_amino_pred": "N/A", "stachelhaus_predictions": ["phe"],
                        "uncertain": False, "stachelhaus_seq": "DALfvGAVaK", "stachelhaus_match_count": 7}
                   }
              }
test_data =[ "ctg1	cys(80.0);orn(70.0);hpg(60.0);gly(60.0);ala(60.0)   Ser",
    "ctg1	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)   Ser",
    "ctg1	DVWHISLVDK	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)	Ser",
    "ctg1	DAWEGGLVDK	gln(70.0);leu(70.0);glu(70.0);arg(70.0);trp(60.0)	hOrn",
    "ctg1   DVWHISLVDK	ser(90.0);arg(70.0);ala(60.0);glu(60.0);orn(60.0)	Ser",
    "ctg1	orf00010	A2	DINYWGGIGK	orn(100.0);val(70.0);phg(60.0);gly(50.0);asp(50.0)	hfOrn"]

def testMain():
    dict = DictionaryHandler.prepare_data()
    for item in test_data:
        SuspendedPipeline.process(item.split('\t')[-1][:-1], dict)
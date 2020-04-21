import argparse
import logging

from ClassicPipeline import ClassicPipeline
from SuspendedPipeline import SuspendedPipeline
from dictionaryHandler import prepare_data
from util import toFixed, handleJson
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='NERPA')
    parser.add_argument(
        '--inp',
        type=str,
        default='',
        help='Input file, can be .json file with results or folder of antishamsh5 outtput')

    parser.add_argument(
        '--outdir',
        type=str,
        default='',
        help='Output dir'
    )
    parser.add_argument(
        '--classic',
        action='store_true'
    )
    parser.add_argument(
        '--save_mod',
        action='store_true'
    )

    args = parser.parse_args()

    data, names = handleJson(args.inp)
    path_out = args.outdir
    method = args.classic
    mod = args.save_mod

    default_dict = prepare_data("data/sp1.stetch.faa", mod, method)

    f = open((path_out + names[0][:-2] + method * "classic" + "_codes.txt"), "w+")

    for i in range(len(data)):
        if method:
            res = ClassicPipeline.process(data[i][:-1], default_dict)
        else:
            res = SuspendedPipeline.process(data[i][:-1], default_dict)

        tmp_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
        res_str_second = ""
        for item in tmp_res:
            res_str_second += "{}({});".format(item, toFixed((tmp_res[item] + 1) * 10, 1))
        res_str = names[i] + " " + res_str_second + "\n"
        f.write(res_str)

    f.close()


if __name__ == "__main__":
    main()

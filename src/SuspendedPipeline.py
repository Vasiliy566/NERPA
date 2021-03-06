import logging

logger = logging.getLogger(__name__)


class SuspendedPipeline:
    # TODO: replace with enum when it will be a few piplines
    dict_handler_key = False
    @staticmethod
    def process(ref_s, ref_dict):
        ref_s = ref_s[1:]
        pos_res = {}
        for item in ref_dict:
            out = 0
            for i in range(len(ref_s)):
                tmp_dict = ref_dict[item][i]
                if ref_s[i] in tmp_dict.keys():
                    out += tmp_dict[ref_s[i]]
            pos_res[item] = out
        return pos_res

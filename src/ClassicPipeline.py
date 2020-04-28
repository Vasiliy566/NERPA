import logging

logger = logging.getLogger(__name__)


class ClassicPipeline:
    # TODO: replace with enum when it will be a few piplines
    dict_handler_key = True

    @staticmethod
    def process(data, ref_dict):
        # Classic algorithm like in nrps-predictor 2
        res = {}
        names = []
        scores = []
        if len(data) == 9:
            logger.info(f"{data} 1st symbol was trimmed ")
            data = data[1:]

        for seq in ref_dict.keys():
            if ref_dict[seq] not in names:
                names.append(ref_dict[seq])
                scores.append(0)

            if len(seq) == 9:
                logger.info(f"{seq} 1st symbol was trimmed ")
                seq = seq[1:]
            tmp_score = 0
            assert len(data) == len(seq)
            for i in range(8):
                if seq[i] == data[i]:
                    tmp_score += 1
            if scores[names.index(ref_dict[seq])] < tmp_score:
                scores[names.index(ref_dict[seq])] = tmp_score

        logger.debug(f"classic finished work with {data}")

        for i in range(len(names)):
            res[names[i][0]] = scores[i]
        return res

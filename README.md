вероятность аминокислоты.

Задачи:
0) Полутренировочная: дан выход antiSMASH5 (в упрощенном варианте вообще руками выдернуты конкретные коды из большого JSON) и табличка всех известных кодов (наверное такая лучше всех), требуется выдать список предсказаний аминокислот со скорами (“antiSMASH3-style”). Т.е. просто считаем для каждого текущего 9(10)-аа кода число общих букв со всеми кодами из таблички, вычисляем скоры и выдаем их как список вида phe(80.0);tyr(50.0);leu(50.0); -- примеры ниже.

1) Пошаговая разработка алгоритма: 
Простая версия: смотреть сколько букв отличается от эталонной последовательности для  аминокислоты (см. задачу 0)
Улучшенная версия: брать усредненную последовательность для каждой буквы из последовательности, смотреть на взвешенное отличие
Ещё более умная версия: нужно придумать
2) Подготовка данных для работы:
Научиться запускать antiSMASH5 и получать 9 буквенные коды (парсить их из JSON)
Найти данные с сопоставление аминокислот и 9AA-кодами (см. ссылку выше и ниже тоже есть)
3) Тестирование:
Подготовить датасет на основе размеченного MiBig, с ответами какая аминокислота должна предсказывать
Подобрать разумную метрику качества предсказаний. 
4) Сравнение результата с конкуретнами:
nrpsPredictor2
minowa
sandpuma
PRISM
5) Интеграция с Nerpa и посмотреть, как изменились результаты
Полезные фразы/ссылки и т.п.
(из переписки с Марниксом и др)

The Stachelhaus code is still being matched, and, in principle, you could relatively easily modify the source code to save/output e.g. the top 10 matches.
The code for this is here: https://github.com/antismash/antismash/blob/master/antismash/modules/nrps_pks/nrps_predictor.py (lines 181-187 in particular).

> (2) Am I right that the currently best list of Stachelhaus codes is here
https://github.com/antismash/antismash/blob/master/antismash/modules/nrps_pks/external/NRPSPredictor2/data/labeled_sigs
Sounds about right.

> (3) Also, a side question regarding the list of codes from (2). Most
> of the abbreviations there are trivial but some are not, e.g. "aad", "pip", etc.
> Is there any legend/explanation for them?
The NRPSPredictor papers should have them. But
https://github.com/antismash/antismash/blob/master/antismash/modules/nrps_pks/data/aaSMILES.txt
 might help, we recently added comments with the substance names to our
SMILES list where appropriate.
-----
Примеры (к задаче 0)
В архивах внутри https://drive.google.com/open?id=1o4fqVJGUNXVb3XmXywCfywML69MHNsRy 

BGC0001763_antiSMASH_5.0.0/BGC0001763.json  -- так теперь, например: 
"nrpspksdomains_ctg1_19_AMP-binding.2": {"NRPSPredictor2": {"method": "NRPSPredictor2", "angstrom_code": "FGLAFDASVLELFLVVGAEVNAYGPTEITVAAAI", "physicochemical_class": "hydrophobic-aliphatic", "large_cluster_pred": ["gly", "ala", "val", "leu", "ile", "abu", "iva"], "small_cluster_pred": ["N/A"], "single_amino_pred": "N/A", "stachelhaus_predictions": ["phe"], "uncertain": false, "stachelhaus_seq": "DALfvGAVaK", "stachelhaus_match_count": 7}},

BGC0001763_antiSMASH_3.0.5/nrpspks_predictions_txt/ctg1_nrpspredictor2_codes.txt -- как было (удобно):
ctg1_orf00029_A2        phe     phe(70.0);tyr(70.0);leu(70.0);hty(70.0);trp(60.0);asn(60.0);bht(60.0);arg(60.0);cha(60.0);gly(50.0);glu(50.0);asp(50.0);thr(50.0);gln(50.0);pro(50.0);ile(50.0);val(50.0);ala(50.0);tcl(50.0);hpg(50.0);lys(50.0);bmt(50.0);ala-d(50.0);cit(50.0);end(50.0);uda(50.0);orn(50.0);dht(40.0);ser(40.0);vol(40.0);dhpg(40.0);dpg(40.0);dhp(40.0);abu(40.0);pip(40.0);hyv(40.0);ahp(40.0);met(40.0);apa(40.0);gua(40.0);allothr(40.0);apc(40.0);cys(30.0);dhb(30.0);dab(30.0);phg(30.0);aad(30.0);aeo(30.0);his(30.0);hse(30.0);sal(20.0);b-ala(20.0)

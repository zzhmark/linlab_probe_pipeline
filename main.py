from pathlib import Path
from cellexplorer import cell_metrics_gen
from kilosort import kilosort
from probe_gen import set_probe_for
from preproc import preprocess
from rhd_selection import SignalSelector


if __name__ == '__main__':
    s = SignalSelector('data')
    re = s.choose_and_concat(200000, 201000, 'RHD2000 amplifier channel')
    re2 = preprocess(re)
    re.get_probe()
    of = 'data/output'
    kilosort(re2, of)
    cell_metrics_gen(of)


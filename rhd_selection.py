from pathlib import Path
import pandas as pd
import spikeinterface.extractors as se
from spikeinterface import concatenate_recordings


class SignalSelector:
    def __init__(self, rhd_dir, load_key='0'):
        self.rhd_files = [*Path(rhd_dir).glob('*.rhd')]

    def choose_and_concat(self, t1, t2, stream_name):
        files = [se.read_intan(i, stream_name=stream_name) for i in self.data.index[to_include]]
        print(files)
        re = concatenate_recordings(files)
        return re.frame_slice(start_frame=t1, end_frame=t2)


if __name__ == '__main__':
    s = SignalSelector('data')
    print(s.choose_and_concat(200000, 201000, 'RHD2000 amplifier channel'))

from pathlib import Path
import pandas as pd
import spikeinterface.extractors as se
from spikeinterface import concatenate_recordings

class SignalSelector:
    def __init__(self, path):
        rhd_files = [*Path(path).glob('*.rhd')]
        rhd_info = [i.stem.split('_') for i in rhd_files]
        # assume filename is like day2_230623_102551.rhd
        # prefix: day2
        # t1: 102551
        # t2: 230623
        # the index is the path to the rhd file
        self.data = pd.DataFrame({
            'prefix': [i[0] for i in rhd_info],
            't2': [float(i[1]) for i in rhd_info],
            't1': [float(i[2]) for i in rhd_info]
        }, index=rhd_files).sort_values('t1')

    def choose_and_concat(self, t1, t2, stream_name):
        to_include = (self.data['t1'] >= t1) & (self.data['t2'] <= t2)
        to_include |= (self.data['t1'] <= t1) & (self.data['t2'] >= t1)
        to_include |= (self.data['t1'] <= t2) & (self.data['t2'] >= t2)
        files = [se.read_intan(i, stream_name=stream_name) for i in self.data.index[to_include]]
        print(files)
        re = concatenate_recordings(files)
        return re.frame_slice(start_frame=t1, end_frame=t2)


if __name__ == '__main__':
    s = SignalSelector('data')
    print(s.choose_and_concat(200000, 201000, 'RHD2000 amplifier channel'))

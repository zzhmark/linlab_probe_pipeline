import spikeinterface.widgets as sw
import spikeinterface.extractors as se
import matplotlib.pyplot as plt
import spikeinterface as si
from spikeinterface import concatenate_recordings


if __name__ == '__main__':
    r1 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102551.rhd', stream_name='RHD2000 amplifier channel')
    r2 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102552.rhd', stream_name='RHD2000 amplifier channel')
    re = concatenate_recordings([r1, r2])
    print(re.get_channel_ids())
    w_ts = sw.plot_timeseries(re, time_range=(0, 120), channel_ids=['3', '4', '5', '6'])
    plt.show()
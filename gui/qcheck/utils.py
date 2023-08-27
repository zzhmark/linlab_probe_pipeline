import pandas as pd
import spikeinterface as si



def resolve_impedance_table(tab: pd.DataFrame):
    """
    Convert the table so that the impedance can be retrieved.

    :param tab: a table from the instrument that contains the impedance level for each probe
    :return: a series mapping the probe id to their impedance
    """
    names = []
    for i in tab['Channel Name']:
        id = 0 if i.startswith('A') else 64
        id += int(i.split('-')[1])
        names.append(str(id))
    s = tab['Impedance Magnitude at 1000 Hz (ohms)']
    s.index = names
    return s


def clean_mechanical_noise(recording: si.BaseRecording):
    pass
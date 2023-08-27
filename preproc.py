import spikeinterface.preprocessing as spre


def preprocess(recording, low, high, verbose=False):
    recording_f = spre.filter(recording, band=[low, high])
    if verbose:
        print(recording_f)
    recording_cmr = spre.common_reference(recording_f, reference='global', operator='median')
    if verbose:
        print(recording_cmr)
    recording_preprocessed = recording_cmr.save(format='binary')
    if verbose:
        print(recording_preprocessed)
    return recording_preprocessed


if __name__ == '__main__':
    from rhd_selection import *
    s = SignalSelector('data')
    re = s.choose_and_concat(200000, 201000, 'RHD2000 amplifier channel')
    re2 = preprocess(re, verbose=True)

import spikeinterface.sorters as ss


def kilosort(recording, output_folder=None, docker=False, verbose=False):
    sorting_KS2 = ss.run_sorter(sorter_name="kilosort2_5", recording=recording, output_folder=output_folder,
                                docker_image=docker, verbose=verbose)
    if verbose:
        print(sorting_KS2)
    return sorting_KS2


if __name__ == '__main__':
    from preproc import *
    s = SignalSelector('data')
    re = s.choose_and_concat(200000, 201000, 'RHD2000 amplifier channel')
    re2 = preprocess(re)
    re3 = kilosort(re2, verbose=True)
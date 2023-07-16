import matlab.engine


def cell_metrics_gen(kilosort_folder):
    eng = matlab.engine.start_matlab() # can use a different way to connect to matlab
    eng.cell_metrics_probe(kilosort_folder)


if __name__ == '__main__':
    pass
function cell_metrics = cell_metrics_probe(kilosort_folder)
sess = my_session(kilosort_folder);
sess = gui_session(sess);
cell_metrics = ProcessCellMetrics('session', sess,'excludeMetrics',{'monoSynaptic_connections'},'showWaveforms',false,'sessionSummaryFigure',false);
cell_metrics = CellExplorer('metrics',cell_metrics);

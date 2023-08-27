# This Python file uses the following encoding: utf-8
import os
from pathlib import Path

import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader
import spikeinterface.widgets as sw
import spikeinterface.preprocessing as spre
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from utils import *


class QCheck(QWidget):
    def __init__(self, recording: si.BaseRecording):
        super(QCheck, self).__init__()
        self.input = recording
        self.output: si.BaseRecording = recording
        self.load_ui()
        self.setWindowTitle('Time Series Quality Check (by zzh)')

        self.max_time = recording.get_duration()
        self.channel_count = recording.get_num_channels()
        self.impedance: pd.Series = None

        w = self.findChild(QWidget, 'fig')
        self.fig = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        vb = QVBoxLayout()
        vb.addWidget(self.canvas)
        w.setLayout(vb)
        w = self.findChild(QWidget, 'toolbar')
        vb = QVBoxLayout()
        self.tb = NavigationToolbar2QT(self.canvas, w)
        vb.addWidget(self.tb)
        w.setLayout(vb)

        # time selection for rendering
        self.end_time = self.findChild(QDoubleSpinBox, 'end_time')
        self.slider_end = self.findChild(QSlider, 'slider_end')
        self.start_time = self.findChild(QDoubleSpinBox, 'start_time')
        self.slider_start = self.findChild(QSlider, 'slider_start')
        self.start_time.setMaximum(self.max_time)
        self.end_time.setMaximum(self.max_time)
        self.end_time.setValue(self.max_time)
        self.slider_end.setValue(self.slider_end.maximum())
        self.slider_end.sliderMoved.connect(self.update_end_time)
        self.end_time.valueChanged.connect(self.update_slider_end)
        self.slider_start.sliderMoved.connect(self.update_start_time)
        self.start_time.valueChanged.connect(self.update_slider_start)

        # channel selection for rendering
        self.left_scroll = self.findChild(QSlider, 'left_scroll')
        self.right_scroll = self.findChild(QSlider, 'right_scroll')
        self.left_ch = self.findChild(QSpinBox, 'left_ch')
        self.right_ch = self.findChild(QSpinBox, 'right_ch')
        self.left_scroll.setMaximum(self.channel_count)
        self.right_scroll.setMaximum(self.channel_count)
        self.right_scroll.setValue(self.channel_count)
        self.left_ch.setMaximum(self.channel_count)
        self.right_ch.setMaximum(self.channel_count)
        self.right_ch.setValue(self.channel_count)
        self.left_ch.valueChanged.connect(self.update_left_scroll)
        self.right_ch.valueChanged.connect(self.update_right_scroll)
        self.left_scroll.valueChanged.connect(self.update_left_ch)
        self.right_scroll.valueChanged.connect(self.update_right_ch)

        # buttons & boxes
        self.findChild(QPushButton, 'update_fig').clicked.connect(self.update_figure)
        self.findChild(QPushButton, 'apply').clicked.connect(self.apply)
        self.findChild(QCheckBox, 'channel').stateChanged.connect(self.checkbox_state_update)
        self.findChild(QCheckBox, 'mech').stateChanged.connect(self.checkbox_state_update)
        self.findChild(QCheckBox, 'butter').stateChanged.connect(self.checkbox_state_update)
        self.findChild(QCheckBox, 'neighbor').stateChanged.connect(self.checkbox_state_update)
        self.findChild(QCheckBox, 'reref').stateChanged.connect(self.checkbox_state_update)
        self.checkbox_state_update()

    @Slot()
    def checkbox_state_update(self):
        self.findChild(QWidget, 'group_channel').setEnabled(self.findChild(QCheckBox, 'channel').isChecked())
        self.findChild(QWidget, 'group_mech').setEnabled(self.findChild(QCheckBox, 'mech').isChecked())
        self.findChild(QWidget, 'group_filter').setEnabled(self.findChild(QCheckBox, 'butter').isChecked())
        self.findChild(QWidget, 'group_reref').setEnabled(self.findChild(QCheckBox, 'reref').isChecked())
        self.findChild(QWidget, 'group_neighbor').setEnabled(self.findChild(QCheckBox, 'neighbor').isChecked())

    @Slot(int)
    def update_end_time(self, v):
        val = v / self.slider_end.maximum() * self.max_time
        self.end_time.setValue(val)
        self.start_time.setValue(min(self.start_time.value(), val))

    @Slot(int)
    def update_start_time(self, v):
        val = v / self.slider_start.maximum() * self.max_time
        self.start_time.setValue(val)
        self.end_time.setValue(max(self.end_time.value(), val))

    @Slot(float)
    def update_slider_end(self, v):
        val = int(v / self.max_time * self.slider_end.maximum())
        self.slider_end.setValue(val)
        self.slider_start.setValue(min(val, self.slider_start.value()))

    @Slot(float)
    def update_slider_start(self, v):
        val = int(v / self.max_time * self.slider_start.maximum())
        self.slider_start.setValue(val)
        self.slider_end.setValue(max(val, self.slider_end.value()))

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    @Slot(int)
    def update_left_ch(self, v):
        self.left_ch.setValue(v)
        self.right_ch.setValue(max(v, self.right_ch.value()))

    @Slot(int)
    def update_right_ch(self, v):
        self.right_ch.setValue(v)
        self.left_ch.setValue(min(v, self.left_ch.value()))

    @Slot(int)
    def update_left_scroll(self, v):
        self.left_scroll.setValue(v)
        self.right_scroll.setValue(max(v, self.right_scroll.value()))

    @Slot(int)
    def update_right_scroll(self, v):
        self.right_scroll.setValue(v)
        self.left_scroll.setValue(min(v, self.left_scroll.value()))

    @Slot()
    def update_figure(self):
        self.fig.clear()
        self.ax = self.fig.subplots()
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        channels = self.output.get_channel_ids()[self.left_ch.value(): self.right_ch.value()]
        sw.plot_timeseries(self.output, ax=self.ax, show_channel_ids=True, channel_ids=channels,
                           time_range=(self.start_time.value(), self.end_time.value()), add_legend=False)
        self.canvas.draw()

    @Slot()
    def apply(self):
        p = self.findChild(QProgressBar, 'progress')
        p.setValue(0)
        re = self.input

        # 1. filter by impedance
        check = self.findChild(QCheckBox, 'channel')
        if check.isChecked():
            if self.impedance is None:
                QMessageBox('Critical', 'No Impedance Table', 'No impedance for filtering probe IDs.').exec()
                return
            imp_thr = self.findChild(QDoubleSpinBox, 'impedance').value()
            re = re.remove_channels([i for i in re.get_channel_ids() if self.impedance[i] > imp_thr])
        p.setValue(20)

        # 2. filter by neighborhood
        check = self.findChild(QCheckBox, 'neighbor')
        if check.isChecked():
            bd, lb = spre.detect_bad_channels(re, 'neighborhood_r2',
                                          neighborhood_r2_threshold=self.findChild(QDoubleSpinBox, 'r2_thr').value(),
                                          neighborhood_r2_radius_um=self.findChild(QDoubleSpinBox, 'rad_um').value(),
                                          highpass_filter_cutoff=self.findChild(QDoubleSpinBox, 'hp_cutoff').value(),
                                          num_random_chunks=self.findChild(QSpinBox, 'n_rand').value(),
                                          welch_window_ms=self.findChild(QDoubleSpinBox, 'welch').value(),
                                          chunk_duration_s=self.findChild(QDoubleSpinBox, 'chunk').value())
            re = re.remove_channels(bd)
        p.setValue(40)

        # 3. clean mechanical noise
        check = self.findChild(QCheckBox, 'mech')
        if check.isChecked():
            pass
        p.setValue(60)

        # 4. butterworth
        check = self.findChild(QCheckBox, 'butter')
        if check.isChecked():
            lp = self.findChild(QDoubleSpinBox, 'low').value()
            hp = self.findChild(QDoubleSpinBox, 'high').value()
            order = self.findChild(QSpinBox, 'order').value()
            iter = self.findChild(QSpinBox, 'iter').value()
            step = 33 / iter
            for i in range(iter):
                re = spre.filter(re, [lp, hp], 'bandpass', order)
                p.setValue(60 + int(step * (i + 1)))
        p.setValue(80)

        # 5. rereference
        check = self.findChild(QCheckBox, 'reref')
        if check.isChecked():
            spre.common_reference(re, operator=self.findChild(QComboBox, 'operator').value(),
                                  reference=self.findChild(QCheckBox, 'reference').value())
        p.setValue(100)

        self.output = re
        QMessageBox('Information', 'QC Success', 'You can rerender the figure to visualize the new recording.').exec()

    @Slot()
    def open_table(self):
        fn = QFileDialog.getOpenFileName(self, "Open Image", None, "Table (*.csv)")
        tab = pd.read_csv(fn)
        s = resolve_impedance_table(tab)
        if not pd.Series(self.input.get_channel_ids()).isin(s.index).all():
            QMessageBox('Critical', 'Impedance Table Invalid',
                        'The table fails to cover the probe IDs provided.').exec()
            return
        self.findChild(QLineEdit, 'line').setText(fn)
        self.impedance = s


if __name__ == "__main__":
    import spikeinterface.extractors as se
    # from spikeinterface import concatenate_recordings
    app = QApplication([])
    spre.phase_shift
    test_recording, sorting = se.toy_example(duration=60, num_channels=16, seed=0, num_segments=1)

    # r1 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102551.rhd',
    #                    stream_name='RHD2000 amplifier channel')
    # r2 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102552.rhd',
    #                    stream_name='RHD2000 amplifier channel')
    # test_recording = concatenate_recordings([r1, r2]).channel_slice(['3', '4', '5', '6'])

    widget = QCheck(test_recording)
    widget.show()
    with open(os.fspath(Path(__file__).resolve().parent / "style.qss"), "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    app.exec()
    spre.detect_bad_channels()
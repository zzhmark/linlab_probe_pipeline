# This Python file uses the following encoding: utf-8
import os
from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader
import spikeinterface.widgets as sw
import spikeinterface as si
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# class ChannelItem(QAbstractListModel):
#     def __init__(self, channel_ids, *args, **kwargs):
#         super(ChannelItem, self).__init__(*args, **kwargs)
#         self.ids = channel_ids
#
#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             status, text = self.ids[index.row()]
#             return text
#
#     def rowCount(self, index):
#         return len(self.ids)



class TimeSelection(QWidget):
    def __init__(self, recording: si.BaseRecording):
        super(TimeSelection, self).__init__()
        self.recording = recording
        self.load_ui()

        self.max_time = recording.get_duration()
        self.channel_count = recording.get_num_channels()
        self.yes = False
        self.left_line: Rectangle = None
        self.right_line: Rectangle = None
        self.bg = None

        w = self.findChild(QWidget, 'fig')
        self.fig = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.tb = NavigationToolbar2QT(self.canvas, w)
        vb = QVBoxLayout()
        vb.addWidget(self.canvas)
        vb.addWidget(self.tb)
        w.setLayout(vb)
        plt.tight_layout()

        self.end_time = self.findChild(QDoubleSpinBox, 'end_time')
        self.slider_end = self.findChild(QSlider, 'slider_end')
        self.start_time = self.findChild(QDoubleSpinBox, 'start_time')
        self.slider_start = self.findChild(QSlider, 'slider_start')
        self.start_time.setMaximum(self.max_time)
        self.end_time.setMaximum(self.max_time)
        self.end_time.setValue(self.max_time)
        self.slider_end.sliderMoved.connect(self.update_end_time)
        self.end_time.valueChanged.connect(self.update_slider_end)
        self.slider_start.sliderMoved.connect(self.update_start_time)
        self.start_time.valueChanged.connect(self.update_slider_start)

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

        self.update_fig = self.findChild(QPushButton, 'update_fig')
        self.update_fig.clicked.connect(self.update_figure)

        self.ok = self.findChild(QDialogButtonBox, 'ok')
        self.ok.accepted.connect(self.acc)
        self.ok.rejected.connect(self.close)

        # self.select_list = self.findChild(QListView, 'select_list')
        # self.drop_list = self.findChild(QListView, 'drop_list')
        # self.select_list.sestModel()

        self.update_figure()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

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
        self.update_line_right()

    @Slot(float)
    def update_slider_start(self, v):
        val = int(v / self.max_time * self.slider_start.maximum())
        self.slider_start.setValue(val)
        self.slider_end.setValue(max(val, self.slider_end.value()))
        self.update_line_left()

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
    def acc(self):
        self.yes = True
        self.close()

    @Slot()
    def update_figure(self):
        self.fig.clear()
        self.ax = self.fig.subplots()
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        channels = self.recording.get_channel_ids()[self.left_ch.value() - 1: self.right_ch.value()]
        sw.plot_timeseries(self.recording, ax=self.ax, show_channel_ids=True, channel_ids=channels,
                           time_range=(0, self.max_time), add_legend=False)
        self.canvas.draw()
        self.bg = self.canvas.copy_from_bbox(self.fig.bbox)

        yt = plt.ylim()
        # self.left_line = plt.vlines(self.start_time.value(), yt[0], yt[-1], colors='r')
        # self.right_line = plt.vlines(self.end_time.value(), yt[0], yt[-1], colors='r')
        self.left_line = Rectangle((0, yt[0]), self.start_time.value(), yt[-1], alpha=.3, color='r', animated=True)
        self.right_line = Rectangle((self.end_time.value(), yt[0]), self.max_time - self.end_time.value(),
                                    yt[-1], alpha=.3, color='r', animated=True)
        self.ax.add_patch(self.left_line)
        self.ax.add_patch(self.right_line)
        self.ax.draw_artist(self.left_line)
        self.ax.draw_artist(self.right_line)
        # plt.ylim(*yt)
        self.canvas.blit(self.fig.bbox)
        self.canvas.flush_events()

    def update_line_left(self):
        v = self.start_time.value()
        self.canvas.restore_region(self.bg)
        # yt = plt.ylim()
        # self.left_line.remove()
        # self.left_line = plt.vlines(v, yt[0], yt[-1], color='r')
        self.left_line.set_width(v)
        if v > self.right_line.get_x():
            self.right_line.set_width(self.max_time - v)
            self.right_line.set_x(v)
        # plt.ylim(*yt)
        # self.canvas.draw()
        self.ax.draw_artist(self.left_line)
        self.ax.draw_artist(self.right_line)
        self.canvas.blit(self.fig.bbox)
        self.canvas.flush_events()

    def update_line_right(self):
        v = self.end_time.value()
        self.canvas.restore_region(self.bg)
        # yt = plt.ylim()
        # self.right_line.remove()
        # self.right_line = plt.vlines(v, yt[0], yt[-1], colors='r')
        if v < self.left_line.get_width():
            self.left_line.set_width(v)
        self.right_line.set_width(self.max_time - v)
        self.right_line.set_x(v)
        # plt.ylim(*yt)
        # self.canvas.draw()
        self.ax.draw_artist(self.left_line)
        self.ax.draw_artist(self.right_line)
        self.canvas.blit(self.fig.bbox)
        self.canvas.flush_events()

    def get_channels(self):
        return self.recording.get_channel_ids()

    def get_range(self):
        return self.start_time.value(), self.end_time.value()


if __name__ == "__main__":
    import spikeinterface.extractors as se
    from spikeinterface import concatenate_recordings
    app = QApplication([])
    # test_recording, sorting = se.toy_example(duration=60, num_channels=128, seed=0, num_segments=1)

    r1 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102551.rhd',
                       stream_name='RHD2000 amplifier channel')
    r2 = se.read_intan(r'D:\GitHub\linlab_probe_pipeline\data\day2_230623_102552.rhd',
                       stream_name='RHD2000 amplifier channel')
    test_recording = concatenate_recordings([r1, r2]).channel_slice(['3', '4', '5', '6'])

    widget = TimeSelection(test_recording)
    widget.show()
    with open(os.fspath(Path(__file__).resolve().parent / "style.qss"), "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    app.exec()
    print(widget.get_range())

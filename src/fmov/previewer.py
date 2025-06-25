import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from PIL import Image

class VideoPreviewer(QtWidgets.QWidget):
    def __init__(self, frame_count, frame_func, video_obj, fps=30, width=640, height=480):
        super().__init__()
        self.setWindowTitle(f"fmov | {video_obj.get_path()}")
        self.frame_count = frame_count
        self.frame_func = frame_func
        self.video_obj = video_obj
        self.fps = fps
        self.width = width
        self.height = height
        self.current_frame = 0
        self.playing = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.frame_cache = {}
        self.init_ui()
        self.setMinimumSize(320, 240)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.resize(self.width, self.height + 80)

    def init_ui(self):
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.frame_count - 1)
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal { height: 6px; background: #444; border-radius: 3px; }
            QSlider::handle:horizontal { background: #fff; border: 1px solid #888; width: 16px; margin: -6px 0; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #2196F3; border-radius: 3px; }
            QSlider::add-page:horizontal { background: #222; border-radius: 3px; }
        ''')
        self.slider.valueChanged.connect(self.slider_changed)
        self.play_button = QtWidgets.QPushButton(self)
        self.play_button.setText('▶')
        self.play_button.setFixedSize(40, 40)
        self.play_button.setStyleSheet('''
            QPushButton { background: #222; color: #fff; border: none; border-radius: 20px; font-size: 20px; }
            QPushButton:pressed { background: #444; }
        ''')
        self.play_button.clicked.connect(self.toggle_play)
        self.frame_label = QtWidgets.QLabel(f'frame: 0 / {self.frame_count-1}', self)
        self.frame_label.setStyleSheet('color: #aaa;')
        self.time_label = QtWidgets.QLabel('00:00:00.000', self)
        self.time_label.setStyleSheet('color: #aaa;')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.image_label)
        controls = QtWidgets.QHBoxLayout()
        controls.addWidget(self.play_button)
        controls.addWidget(self.slider)
        layout.addLayout(controls)
        label_row = QtWidgets.QHBoxLayout()
        label_row.addWidget(self.frame_label)
        label_row.addWidget(self.time_label)
        layout.addLayout(label_row)
        self.setLayout(layout)
        self.update_frame(0)

    def resizeEvent(self, event):
        self.update_frame(self.current_frame)
        super().resizeEvent(event)

    def slider_changed(self, value):
        self.current_frame = value
        self.update_frame(value)

    def update_frame(self, idx):
        if idx in self.frame_cache:
            arr = self.frame_cache[idx]
        else:
            img = self.frame_func(idx, self.video_obj)
            if not isinstance(img, Image.Image):
                raise TypeError('Frame function must return a PIL.Image')
            arr = np.array(img.convert('RGB'))
            self.frame_cache[idx] = arr
        qimg = QtGui.QImage(arr.data, arr.shape[1], arr.shape[0], 3 * arr.shape[1], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        label_size = self.image_label.size()
        self.image_label.setPixmap(pixmap.scaled(label_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.frame_label.setText(f'Frame: {idx}/{self.frame_count-1}')
        ms = int((idx / self.fps) * 1000)
        h = ms // 3600000
        m = (ms % 3600000) // 60000
        s = (ms % 60000) // 1000
        ms_rem = ms % 1000
        self.time_label.setText(f'{h:02}:{m:02}:{s:02}.{ms_rem:03}')
        self.slider.blockSignals(True)
        self.slider.setValue(idx)
        self.slider.blockSignals(False)
        QtWidgets.QApplication.processEvents()

    def toggle_play(self):
        if self.playing:
            self.timer.stop()
            self.play_button.setText('▶')
        else:
            self.timer.start(int(1000 / self.fps))
            self.play_button.setText('⏸')
        self.playing = not self.playing

    def next_frame(self):
        if self.current_frame < self.frame_count - 1:
            self.current_frame += 1
            self.update_frame(self.current_frame)
        else:
            self.toggle_play()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.toggle_play()
        elif event.key() == QtCore.Qt.Key_Right:
            if self.current_frame < self.frame_count - 1:
                self.current_frame += 1
                self.update_frame(self.current_frame)
        elif event.key() == QtCore.Qt.Key_Left:
            if self.current_frame > 0:
                self.current_frame -= 1
                self.update_frame(self.current_frame)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()


def preview_video(frame_count, frame_func, video_obj):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    viewer = VideoPreviewer(frame_count, frame_func, video_obj, video_obj.fps, video_obj.width, video_obj.height)
    viewer.show()
    app.exec_()

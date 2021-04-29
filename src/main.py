import sys
from pathlib import Path
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QImage, QPixmap
import qt_utils

import create_saturated_image.with_python as image_processor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from plot_utils import *
import plot_saturation


def config_axis(ax):
    ax.set_title("Saturation Histogram", color=txtcolour)
    ax.set_xlabel("Saturation (%)", color=txtcolour)
    ax.set_ylabel("% of image", color=txtcolour)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(axColour)
    ax.spines['bottom'].set_color(axColour)

    ax.set_xticks([0, 255 * 0.25, 255 * 0.5, 255 * 0.75, 255])
    ax.set_xticklabels([0, 25, 50, 75, 100])
    ax.tick_params(colors=axColour, labelcolor=txtcolour)

    ax.set_xlim([0, 255])

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        screen_size = app.primaryScreen().size()
        self.resize(screen_size.width() / 1.2,
                      screen_size.height() / 1.2)

        # Set layout
        h_layout = QtWidgets.QHBoxLayout(self)
        lhs_layout = QtWidgets.QVBoxLayout()
        rhs_layout = QtWidgets.QVBoxLayout()
        h_layout.addLayout(lhs_layout)
        h_layout.addLayout(rhs_layout)

        self.src_img_lbl = QtWidgets.QLabel(self)
        rhs_layout.addWidget(self.src_img_lbl)
        self.out_img_lbl = QtWidgets.QLabel(self)
        rhs_layout.addWidget(self.out_img_lbl)

        process_file_button = QtWidgets.QPushButton("Load Image")
        process_file_button.clicked.connect(self.select_image_and_process)
        lhs_layout.addWidget(process_file_button)

        self.save_button = QtWidgets.QPushButton("Save Saturation Image")
        self.save_button.clicked.connect(self.save_image)
        lhs_layout.addWidget(self.save_button)

        self.canvas = QtWidgets.QWidget()
        lhs_layout.addWidget(self.canvas)

        self.saturated_image = QImage()

        fig = Figure(
            # figsize=(7, 5),
            # dpi=150,
            facecolor=imageBgColour,
            edgecolor=imageBgColour,
            frameon=True
        )

        self.ax = fig.add_subplot(111, facecolor=imageBgColour)
        config_axis(self.ax)

        self.canvas = FigureCanvas(fig)
        lhs_layout.addWidget(self.canvas)
        self.canvas.draw()


    def select_image_and_process(self):
        # Select image
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")
        if filepath:
            # Load image and display
            image = QImage(filepath)
            pixmap = QPixmap(image)\
                .scaled(self.size().width()/2, self.size().height()/2,
                        QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.src_img_lbl.setPixmap(pixmap)

            # Process image
            arr = qt_utils.qt_image_to_array(image)
            sat_img_arr = image_processor.create(arr)

            self.saturated_image = QImage(sat_img_arr.copy().data, sat_img_arr.shape[1], sat_img_arr.shape[0], sat_img_arr.strides[0], QImage.Format_RGBA8888)
            # Display saturated image
            pixmap2 = QPixmap.fromImage(self.saturated_image) \
                .scaled(self.size().width() / 2, self.size().height()/2, QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.FastTransformation)
            self.out_img_lbl.setPixmap(pixmap2)

            plot_saturation.create_single_channel_histogram(sat_img_arr, self.ax)

            config_axis(self.ax)

            self.canvas.draw()


    def save_image(self):
        if not self.saturated_image.isNull():
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", str(Path.home()),
                                                                    "Image Files (*.png *.jpg *.bmp)")
            if filepath:
                self.saturated_image.save(filepath)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


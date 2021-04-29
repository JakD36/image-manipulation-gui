import sys
from pathlib import Path
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QImage, QPixmap
import qt_utils

import create_saturated_image.with_python as image_processor


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


    def select_image_and_process(self):
        # Select image
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")

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

    def save_image(self):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", str(Path.home()),
                                                                "Image Files (*.png *.jpg *.bmp)")
        self.saturated_image.save(filepath)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


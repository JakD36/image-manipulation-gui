import sys
from pathlib import Path
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QImage, QPixmap
import create_sat_image
import numpy as np

def qt_image_to_array(img):
    img = img.convertToFormat(QtGui.QImage.Format.Format_RGB32)

    width = img.width()
    height = img.height()

    ptr = img.constBits()
    arr = np.array(ptr).reshape(height, width, 4)
    return arr

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
        self.out_img_lbl = QtWidgets.QLabel(self)
        rhs_layout.addWidget(self.src_img_lbl)
        rhs_layout.addWidget(self.out_img_lbl)

        self.load_button = QtWidgets.QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        lhs_layout.addWidget(self.load_button)

        self.save_button = QtWidgets.QPushButton("Save Saturation Image")
        self.save_button.clicked.connect(self.save_image)
        lhs_layout.addWidget(self.save_button)

        self.canvas = QtWidgets.QWidget()
        lhs_layout.addWidget(self.canvas)


        # Load images
        image = QImage()
        src_pixmap = QPixmap(image).scaled(self.size().width()/2, self.size().height()/2, QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        self.src_img_lbl.setPixmap(src_pixmap)

        # Get the sat image
        # arr = qt_image_to_array(image)
        # _, sat_img = create_sat_image.create_sat_and_lum_image(arr)
        #
        # self.q_sat_img = QImage(sat_img.copy().data, sat_img.shape[1], sat_img.shape[0],
        #                         sat_img.strides[0], QImage.Format_RGBA8888)
        #
        # pixmap2 = QPixmap.fromImage(self.q_sat_img) \
        #     .scaled(self.size().width()/2, self.size().height()/2,
        #             QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
        #
        # self.out_img_lbl.setPixmap(pixmap2)


    def load_image(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", str(Path.home()),
                                                            "Image Files (*.png *.jpg *.bmp)")
        image = QImage(filepath)
        pixmap = QPixmap(image)\
            .scaled(self.size().width()/2, self.size().height()/2,
                    QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.src_img_lbl.setPixmap(pixmap)

        arr = qt_image_to_array(image)
        _, sat_img = create_sat_image.create_sat_and_lum_image(arr)
        self.q_sat_img = QImage(sat_img.copy().data, sat_img.shape[1], sat_img.shape[0], sat_img.strides[0],
                        QImage.Format_RGBA8888)

        pixmap2 = QPixmap.fromImage(self.q_sat_img) \
            .scaled(self.size().width() / 2, self.size().height()/2, QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.FastTransformation)
        self.out_img_lbl.setPixmap(pixmap2)

    def save_image(self):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", str(Path.home()),
                                                                "Image Files (*.png *.jpg *.bmp)")
        self.q_sat_img.save(filepath)


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    widget = MainWindow()

    widget.show()

    sys.exit(app.exec_())


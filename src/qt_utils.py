import numpy as np
from PySide2 import QtGui

def qt_image_to_array(img):
    img = img.convertToFormat(QtGui.QImage.Format.Format_RGB32)

    width = img.width()
    height = img.height()

    ptr = img.constBits()
    arr = np.array(ptr).reshape(height, width, 4)
    return arr
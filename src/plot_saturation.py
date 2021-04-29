from matplotlib.axes import Axes
import numpy as np

def create_single_channel_histogram(img: np.array, ax : Axes, bucket: int=256):
    pixel_count = img.shape[0] * img.shape[1]
    hist_arr, _ = np.histogram(img[0:int(len(img)/4)], bins=bucket)
    vals = hist_arr / pixel_count * 100
    ax.cla()
    ax.stackplot(range(0, len(vals)), vals)
from plot_utils import *

def create_single_channel_histogram(img):
    hist_arr = img.split()[0].histogram()
    setup2d()
    stackplot(range(0, 256), hist_arr)
    xticks([0, 255 * 0.25, 255 * 0.5, 255 * 0.75, 255], [0, 25, 50, 75, 100])
    yticks([], [])
    ylabel("Frequency", color=txtcolour)
    xlim([0, 255])
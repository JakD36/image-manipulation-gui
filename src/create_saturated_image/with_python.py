import colorsys
import numpy as np

def rgb_to_hsl_255(rgb: [int, int, int]) -> [int, int, int]:
    hsl = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    return [int(hsl[0] * 255), int(hsl[1] * 255), int(hsl[2] * 255)]

def channel_to_3(channel: int) -> [int, int, int]:
    return [channel, channel, channel]

def create(img: np.array) -> np.array:
    img_sat = img.copy()
    for y in range(0, img.shape[0]):
        for x in range(0, img.shape[1]):
            rgb = img[y,x]
            hsl = rgb_to_hsl_255(rgb)

            img_sat[y, x] = [*channel_to_3(hsl[2]), 255]

    return img_sat

"""
Copyright (c) 2021 Tag Games Ltd. All rights reserved
"""

import pyopencl as cl
from PIL import Image
from plot_utils import *


def create_sat_and_lum_image(img):
    platforms = cl.get_platforms()
    platform = platforms[0]
    devices = platform.get_devices(cl.device_type.GPU)
    device = devices[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx, device)

    shape = img.T.shape[1:]
    img_lum = np.empty_like(img)
    img_sat = np.empty_like(img)

    buf_in = cl.Image(ctx, cl.mem_flags.READ_ONLY, cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8), shape=shape)
    buf_out_lum = cl.Image(ctx, cl.mem_flags.WRITE_ONLY,
                           cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8), shape=shape)
    buf_out_sat = cl.Image(ctx, cl.mem_flags.WRITE_ONLY,
                           cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8), shape=shape)

    program = cl.Program(ctx, open("kernels/kernel.cl", "r").read()).build()

    kernel = cl.Kernel(program, "pull_sat_from_rgb")
    kernel.set_arg(0, buf_in)
    kernel.set_arg(1, buf_out_lum)
    kernel.set_arg(2, buf_out_sat)

    cl.enqueue_copy(queue, buf_in, img, origin=(0, 0), region=shape)
    cl.enqueue_nd_range_kernel(queue, kernel, shape, None)
    cl.enqueue_copy(queue, img_lum, buf_out_lum, origin=(0, 0), region=shape)
    cl.enqueue_copy(queue, img_sat, buf_out_sat, origin=(0, 0), region=shape)

    return img_lum, img_sat


def create_single_channel_histogram(img: Image):
    hist_arr = img.split()[0].histogram()
    setup2d()
    stackplot(range(0, 256), hist_arr)
    xticks([0, 255 * 0.25, 255 * 0.5, 255 * 0.75, 255], [0, 25, 50, 75, 100])
    yticks([], [])
    ylabel("Frequency", color=txtcolour)
    xlim([0, 255])

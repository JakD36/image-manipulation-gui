import pyopencl as cl
import numpy as np

def create(img):
    platforms = cl.get_platforms()
    platform = platforms[0]
    devices = platform.get_devices(cl.device_type.GPU)
    device = devices[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx, device)

    shape = img.T.shape[1:]
    img_sat = np.empty_like(img)

    buf_in = cl.Image(ctx, cl.mem_flags.READ_ONLY, cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8), shape=shape)
    buf_out_sat = cl.Image(ctx, cl.mem_flags.WRITE_ONLY,
                           cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8), shape=shape)

    program = cl.Program(ctx, open("kernels/kernel.cl", "r").read()).build()

    kernel = cl.Kernel(program, "pull_sat_from_rgb")
    kernel.set_arg(0, buf_in)
    kernel.set_arg(1, buf_out_sat)

    cl.enqueue_copy(queue, buf_in, img, origin=(0, 0), region=shape)
    cl.enqueue_nd_range_kernel(queue, kernel, shape, None)
    cl.enqueue_copy(queue, img_sat, buf_out_sat, origin=(0, 0), region=shape)

    return img_sat



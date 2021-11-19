import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


if __name__ == '__main__':
    filepath = '/home/haoyuan/workspace/alfred/DepthDebug/SampleScene_1_depth.png'
    image = cv2.imread(filepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image, dtype=np.float32)
    print('shape:', image.shape)

    image_depth_out = (
            image[:, :, 0]
            + image[:, :, 1] / np.float32(256)
            + image[:, :, 2] / np.float32(256 ** 2)
    )

    camera_far_plane = 20.0
    camera_near_plane = 0.1
    image_depth_out = image_depth_out * (camera_far_plane - camera_near_plane) / 255.0

    print('depth shape:', image_depth_out.shape)
    print('depth max', image_depth_out.max())
    print('depth min', image_depth_out.min())

    x_low = 0
    x_high = 512
    y_low = 0
    y_high = 512

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    xs = np.arange(x_low, x_high, 1)
    xs = np.repeat(xs, y_high - y_low, axis=0)
    ys = np.arange(y_low, y_high, 1)
    ys = ys.reshape((1, y_high - y_low))
    ys = np.repeat(ys, x_high - x_low, axis=0)
    ys = ys.reshape((-1))
    print(xs.shape)
    print(ys.shape)
    depths = image_depth_out[x_low:x_high, y_low:y_high].reshape((-1,))
    print(depths.shape)

    valid_coordinates = (depths < 1).astype(np.bool)
    print(valid_coordinates.shape)

    ax.scatter(xs[valid_coordinates], ys[valid_coordinates], depths[valid_coordinates])

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()

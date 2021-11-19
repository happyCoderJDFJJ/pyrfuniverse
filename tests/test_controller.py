from pyrfuniverse.utils import RFUniverseController
import pybullet as p
import math
import time


if __name__ == '__main__':
    controller = RFUniverseController('franka', render=True)
    y_euler = 0
    while True:
        time.sleep(0.5)
        y_euler += math.pi / 6
        controller.calculate_ik([-0.5, 0.5, 0], eef_orn=p.getQuaternionFromEuler([math.pi / 2, 0, math.pi / 2]))


from pyrfuniverse.envs import FrankaPushEnv
import numpy as np
import math
import copy
from pyrfuniverse.utils.controller import RFUniverseController


def get_open_gripper_action(joints_state: list) -> np.ndarray:
    action = copy.deepcopy(joints_state)
    action.append(0.08)
    return np.array(action)


def get_close_gripper_action(joints_state: list, width=0.0) -> np.ndarray:
    action = copy.deepcopy(joints_state)
    action.append(width)
    return np.array(action)


def convert_joints_state(joints_state: list) -> list:
    for i, (state) in enumerate(joints_state):
        joints_state[i] = -180 * state / math.pi

    return joints_state


if __name__ == '__main__':
    env = FrankaPushEnv()

    init_joints_state = [0, 45, 0, 135, 0, -90, -45]

    o = {}
    while o == {}:
        o = env._get_obs()
        env._step()

    object_pos = o[0]['position']
    object_pos.append(0)
    a = np.array(object_pos)

    o = env.step(a)
    print(o)

    # while 1:
    #     env._step()

    # Push
    for i in range(10):
        a[2] -= 0.05
        o = env.step(a)
        print(o)

    # o = env.step(get_close_gripper_action(init_joints_state))
    # print(o)

    env.close()

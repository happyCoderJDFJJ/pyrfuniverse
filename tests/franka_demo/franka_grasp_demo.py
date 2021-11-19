from pyrfuniverse.envs import FrankaGraspEnv
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
    # env = FrankaGraspEnv('D:\\GitHub\\rfuniverse\\RFUniverse\\Build\\Franka_Grasp\\RFUniverse.exe')
    env = FrankaGraspEnv()
    controller = RFUniverseController('franka')

    init_joints_state = [0, 0, 0, 0, 0, 0, 0]
    final_joints_state = [0, 45, 0, 135, 0, -90, -45]

    o = env.step(get_open_gripper_action(final_joints_state))
    print(o)

    # while 1:
    #     env._step()

    object_pos = np.array(o[0]['position'])
    object_pos[0] += 0.05
    object_pos[1] += 0.08
    object_pos[2] += 0.01

    grasp_joints_state = controller.calculate_ik(object_pos)

    o = env.step(get_open_gripper_action(grasp_joints_state))
    print(o)

    object_pos[1] -= 0.04
    grasp_joints_state = controller.calculate_ik(object_pos)

    o = env.step(get_open_gripper_action(grasp_joints_state))
    print(o)

    o = env.step(get_close_gripper_action(grasp_joints_state, 0))
    print(o)

    object_pos[1] += 0.3
    object_pos[0] += 0.1
    grasp_joints_state = controller.calculate_ik(object_pos)

    o = env.step(get_close_gripper_action(grasp_joints_state, 0))
    print(o)

    # o = env.step(get_close_gripper_action(final_joints_state, 0.04))
    # print(o)

    current_eef_pos = controller.get_link_state(controller.end_effector_id)
    current_eef_pos[1] += 0.3
    grasp_joints_state = controller.calculate_ik(current_eef_pos)
    o = env.step(get_close_gripper_action(grasp_joints_state, 0))

    object_pos[0] -= 0.2
    object_pos[2] -= 0.8
    grasp_joints_state = controller.calculate_ik(object_pos)

    o = env.step(get_close_gripper_action(grasp_joints_state, 0))
    print(o)

    o = env.step(get_open_gripper_action(grasp_joints_state))
    print(o)

    object_pos[1] += 0.1
    grasp_joints_state = controller.calculate_ik(object_pos)

    o = env.step(get_open_gripper_action(grasp_joints_state))
    print(o)

    o = env.step(get_open_gripper_action(final_joints_state))
    print(o)

    env.close()

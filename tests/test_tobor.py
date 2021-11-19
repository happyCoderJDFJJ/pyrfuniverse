from pyrfuniverse.utils import RFUniverseToborController
from pyrfuniverse.envs import RFUniverseBaseEnv
import math
import pybullet as p
import numpy as np
import time


class TestArticulationChannelEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="59ba36ae-f9c5-11eb-b925-18c04d443e7d",
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()


def log(prefix, data_list):
    print(prefix)
    for data in data_list:
        print(data)
    print('')


if __name__ == '__main__':
    controller = RFUniverseToborController(
        urdf_folder='/home/haoyuan/workspace/tobor',
        render=True
    )
    left_joint_positions = [0] * 7
    right_joint_positions = [0] * 7

    counter = 0

    left_joint_positions = controller.calculate_ik('left', [-0.3, 0.8, 1], eef_orn=p.getQuaternionFromEuler([0, 0, 0]))
    right_joint_positions = controller.calculate_ik('right', [0.3, 0.8, 1], eef_orn=p.getQuaternionFromEuler([0, 0, 0]))
    log('pybullet left:', controller.get_all_link_positions('left'))
    log('pybullet right', controller.get_all_link_positions('right'))

    env = TestArticulationChannelEnv()
    env.reset()
    env.articulation_channel.set_action(
        'SetJointPositionDirectly',
        index=0,
        joint_positions=list(left_joint_positions)
    )
    env._step()

    env.articulation_channel.set_action(
        'SetJointPositionDirectly',
        index=1,
        joint_positions=list(right_joint_positions)
    )
    env._step()

    rfuniverse_data = env.articulation_channel.data
    log('rfuniverse left:', rfuniverse_data[0]['positions'][1:] + [rfuniverse_data[2]['positions'][-1]])
    log('rfuniverse right:', rfuniverse_data[1]['positions'][1:] + [rfuniverse_data[3]['positions'][-1]])

    while True:
        env._step()
        continue

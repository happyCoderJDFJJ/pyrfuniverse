from pyrfuniverse.envs import RFUniverseBaseEnv
from pyrfuniverse.utils import RFUniverseToborController
import pybullet as p
import math


class FullToborEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="15dd9c7e-37db-11ec-bd30-18c04d443e7d",
            game_object_channel_id=None,
        )
        self.ik_controller = RFUniverseToborController(
            urdf_folder='/home/haoyuan/workspace/tobor',
            left_hand='robotiq85',
            right_hand='robotiq85',
            left_init_joint_positions=[0] * 7,
            right_init_joint_positions=[0] * 7,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()

    def set_left_arm(self, position, rotation):
        orn = p.getQuaternionFromEuler(rotation)
        joint_positions = self.ik_controller.calculate_ik(
            'left',
            unity_eef_pos=position,
            eef_orn=orn
        )
        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=1,
            joint_positions=joint_positions
        )
        self._step()

    def set_right_arm(self, position, rotation):
        orn = p.getQuaternionFromEuler(rotation)
        joint_positions = self.ik_controller.calculate_ik(
            'right',
            unity_eef_pos=position,
            eef_orn=orn
        )
        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=3,
            joint_positions=joint_positions
        )
        self._step()

    def close_left_gripper(self):
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=2,
            joint_positions=[50, 50, -50, 50, 50, -50]
        )
        self._step()

    def close_right_gripper(self):
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=4,
            joint_positions=[50, 50, -50, 50, 50, -50]
        )
        self._step()

    def set_left_gripper_width(self, width):
        angle = self._gripper_width2angle(width)
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=2,
            joint_positions=[angle, angle, -1 * angle] * 2
        )
        self._step()

    def set_right_gripper_width(self, width):
        angle = self._gripper_width2angle(width)
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=4,
            joint_positions=[angle, angle, -1 * angle] * 2
        )
        self._step()

    def _gripper_width2angle(self, width):
        angle_rad = 0.715 - math.asin((width - 0.01) / 0.1143)
        angle_deg = angle_rad * 180 / math.pi

        return angle_deg


if __name__ == '__main__':
    env = FullToborEnv()

    # env.set_left_arm(
    #     [0, 0.8, 0.8],
    #     [0, -math.pi / 2, 0]
    # )
    #
    # env.set_right_arm(
    #     [0, 0.8, 0.8],
    #     [0, math.pi / 2, 0]
    # )

    env.close_left_gripper()

    env.close_right_gripper()

    # point_1 = env.articulation_channel.data[2]['positions'][11]
    # point_2 = env.articulation_channel.data[4]['positions'][11]
    # print(point_1)
    # print(point_2)

    # env.articulation_channel.set_action(
    #     'SetJointPositionDirectly',
    #     index=1,
    #     joint_positions=[90, -90, 0, 0, 0, 0, 0]
    # )
    # env._step()

    # env.articulation_channel.set_action(
    #     'SetJointPositionDirectly',
    #     index=3,
    #     joint_positions=[45, 90, 0, 0, 0, 0, 0]
    # )
    # env._step()
    #
    # point_1 = env.articulation_channel.data[3]['positions'][2]
    # point_2 = env.articulation_channel.data[4]['positions'][11]
    # print(point_1)
    # print(point_2)

    # Microwave
    # env.set_left_arm(
    #     [-0.376798093,0.698300004,0.831152856],
    #     [-math.pi / 3, 0, math.pi / 2]
    # )
    # env.close_left_gripper()

    distance = 0
    rotation = 0
    lift_distance = 0
    head_rotation_1 = 0
    head_rotation_2 = 0

    def step():
        env.articulation_channel.set_action(
            'SetJointPosition',
            index=0,
            joint_positions=[distance, rotation, lift_distance, head_rotation_1, head_rotation_2]
        )
        for i in range(10):
            env._step()
    #
    # def freeze():
    #     for i in range(20):
    #         env._step()
    #
    # # Navigation
    # for i in range(30):
    #     step()
    #     distance += 0.05
    # freeze()
    #
    # # Base rotate
    # for i in range(30):
    #     step()
    #     rotation += 1
    # freeze()
    #
    # # Navigation
    # for i in range(30):
    #     step()
    #     distance += 0.05
    # freeze()
    #
    # Lifting
    # for i in range(50):
    #     step()
    #     lift_distance += 0.3
    # freeze()
    #
    # for i in range(20):
    #     step()
    #     lift_distance -= 0.01
    # freeze()
    #
    # for i in range(30):
    #     step()
    #     head_rotation_1 += 1
    # freeze()
    #
    # for i in range(30):
    #     step()
    #     head_rotation_2 += 1
    # freeze()

    while True:
        env._step()

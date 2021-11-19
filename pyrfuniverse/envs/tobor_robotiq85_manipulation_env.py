from pyrfuniverse.envs import RFUniverseBaseEnv
from pyrfuniverse.utils import RFUniverseToborController
import numpy as np
import math
import pybullet as p


class ToborRobotiq85ManipulationEnv(RFUniverseBaseEnv):
    def __init__(
            self,
            task_name,
            executable_file=None,
            only_calculate=False,
            left_init_joint_positions=[0] * 7,
            right_init_joint_positions=[0] * 7
    ):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="284bd13e-1786-11ec-a470-18c04d443e7d",
            game_object_channel_id=None,
        )

        self.ik_controller = RFUniverseToborController(
            urdf_folder='/home/haoyuan/workspace/tobor',
            left_hand='robotiq85',
            right_hand='robotiq85',
            left_init_joint_positions=left_init_joint_positions,
            right_init_joint_positions=right_init_joint_positions,
        )

        # Init joint positions
        self.left_init_joint_positions = left_init_joint_positions
        self.left_joint_positions = self.left_init_joint_positions.copy()
        self.right_init_joint_positions = right_init_joint_positions
        self.right_joint_positions = self.right_init_joint_positions.copy()

        self.left_gripper_open = True
        self.right_gripper_open = True
        self.task_name = task_name
        self.record_file = '/home/haoyuan/workspace/rfuniverse/rfuniverse/RFUniverse/tobor_manipulation_{}.txt'.format(self.task_name)
        self.only_calculate = only_calculate
        with open(self.record_file, 'w') as f:
            f.close()

    def step(self, mode, position: np.ndarray, orientation=None):
        if mode == 'left':
            # Robotiq85
            current_position = np.array(self.articulation_channel.data[2]['positions'][11])
        else:
            # Robotiq85
            current_position = np.array(self.articulation_channel.data[3]['positions'][11])

        distance = position - current_position
        time_steps = int(np.abs(distance / 0.05).max()) + 1
        unit_distance = distance / time_steps

        for i in range(time_steps):
            target_position = current_position + unit_distance * (i + 1)
            joint_positions = self.ik_controller.calculate_ik(
                mode,
                target_position,
                orientation
            )

            if mode == 'left':
                self.left_joint_positions = joint_positions
                if not self.only_calculate:
                    self.articulation_channel.set_action(
                        'SetJointPosition',
                        index=0,
                        joint_positions=list(joint_positions),
                    )
            else:
                self.right_joint_positions = joint_positions
                if not self.only_calculate:
                    self.articulation_channel.set_action(
                        'SetJointPosition',
                        index=1,
                        joint_positions=list(joint_positions),
                    )

            for j in range(20):
                if not self.only_calculate:
                    self._step()
                self.write()


    def double_step(self, left_pos, right_pos, left_orn=None, right_orn=None):
        left_current_pos = np.array(self.articulation_channel.data[2]['positions'][11])
        left_distance = left_pos - left_current_pos
        left_time_steps = int(np.abs(left_distance / 0.05).max()) + 1

        right_current_pos = np.array(self.articulation_channel.data[3]['positions'][11])
        right_distance = right_pos - right_current_pos
        right_time_steps = int(np.abs(right_distance / 0.05).max()) + 1

        time_steps = max(left_time_steps, right_time_steps)
        left_unit_distance = left_distance / time_steps
        right_unit_distance = right_distance / time_steps

        for i in range(time_steps):
            left_target_position = left_current_pos + left_unit_distance * (i + 1)
            right_target_position = right_current_pos + right_unit_distance * (i + 1)
            left_joint_positions = self.ik_controller.calculate_ik(
                'left',
                left_target_position,
                left_orn
            )
            self.left_joint_positions = left_joint_positions
            right_joint_positions = self.ik_controller.calculate_ik(
                'right',
                right_target_position,
                right_orn
            )
            self.right_joint_positions = right_joint_positions

            if not self.only_calculate:
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=0,
                    joint_positions=list(left_joint_positions),
                )
                self._step()
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=1,
                    joint_positions=list(right_joint_positions),
                )

            for j in range(20):
                if not self.only_calculate:
                    self._step()
                self.write()

    def double_close(self):
        if not self.only_calculate:
            self.articulation_channel.set_action(
                'SetJointPosition',
                index=2,
                joint_positions=[50, 50],
            )
            self.left_gripper_open = False
            self._step()
            self.articulation_channel.set_action(
                'SetJointPosition',
                index=3,
                joint_positions=[50, 50],
            )
            self.right_gripper_open = False
            self._step()

        for i in range(20):
            if not self.only_calculate:
                self._step()
            self.write()

    def double_open(self):
        if not self.only_calculate:
            self.articulation_channel.set_action(
                'SetJointPosition',
                index=2,
                joint_positions=[0, 0],
            )
            self.left_gripper_open = True
            self._step()
            self.articulation_channel.set_action(
                'SetJointPosition',
                index=3,
                joint_positions=[0, 0],
            )
            self.right_gripper_open = True
            self._step()

        for i in range(20):
            if not self.only_calculate:
                self._step()
            self.write()

    def reset(self):
        self.env.reset()
        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=0,
            joint_positions=self.left_init_joint_positions
        )
        self._step()
        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=1,
            joint_positions=self.right_init_joint_positions
        )
        self._step()

    def close_gripper(self, mode):
        if not self.only_calculate:
            if mode == 'left':
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=2,
                    joint_positions=[50, 50],
                )
                self.left_gripper_open = False
            else:
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=3,
                    joint_positions=[50, 50],
                )
                self.right_gripper_open = False
        for i in range(20):
            if not self.only_calculate:
                self._step()
            self.write()


    def open_gripper(self, mode):
        if not self.only_calculate:
            if mode == 'left':
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=2,
                    joint_positions=[0, 0],
                )
                self.left_gripper_open = True
            else:
                self.articulation_channel.set_action(
                    'SetJointPosition',
                    index=3,
                    joint_positions=[0, 0],
                )
                self.right_gripper_open = True
        for i in range(20):
            if not self.only_calculate:
                self._step()
            self.write()


    def wait(self, n_timesteps):
        for i in range(n_timesteps):
            if not self.only_calculate:
                self._step()
            self.write()


    def write(self):
        with open(self.record_file, 'a+') as f:
            line = ''
            for joint_position in self.left_joint_positions:
                line += str(joint_position) + ','
            for joint_position in self.right_joint_positions:
                line += str(joint_position) + ','

            if self.left_gripper_open:
                line += '0,0,'
            else:
                line += '50,50,'

            if self.right_gripper_open:
                line += '0,0\n'
            else:
                line += '50,50\n'

            f.write(line)

    def write_raw(self, raw_str):
        with open(self.record_file, 'a+') as f:
            f.write(raw_str)

    def get_current_position(self, mode):
        if mode == 'left':
            return np.array(self.articulation_channel.data[2]['positions'][11])
        elif mode == 'right':
            return np.array(self.articulation_channel.data[3]['positions'][11])


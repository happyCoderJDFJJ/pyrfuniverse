from pyrfuniverse.envs import RFUniverseGymGoalWrapper
from pyrfuniverse.utils.ur5_controller import RFUniverseUR5Controller
import numpy as np
from gym import spaces
from gym.utils import seeding
import math
import copy
import pybullet as p


class Ur5DrawerEnv(RFUniverseGymGoalWrapper):
    metadata = {'render.modes': ['human']}

    def __init__(
            self,
            max_steps,
            reward_type='dense',
            min_open_distance=0.08,
            seed=None,
            executable_file=None,
    ):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id='a55063c8-4460-11ec-b808-18c04d443e7d',
            game_object_channel_id=None,
        )
        self.max_steps = max_steps
        self.reward_type = reward_type
        self.min_open_distance = min_open_distance

        self.seed(seed)
        self.ik_controller = RFUniverseUR5Controller(
            robot_urdf='/home/haoyuan/workspace/rfuniverse/rfuniverse/external_assets/urdf/urdf/ur5_robotiq_85.urdf',
            init_joint_positions=[90, -60, 60, 90, 90, 0],
        )
        self.t = 0
        self.goal = np.array([self.min_open_distance])
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32
        )
        obs = self._get_obs()
        self.observation_space = spaces.Dict({
            'observation': spaces.Box(-np.inf, np.inf, shape=obs['observation'].shape, dtype=np.float32),
            'desired_goal': spaces.Box(-np.inf, np.inf, shape=obs['desired_goal'].shape, dtype=np.float32),
            'achieved_goal': spaces.Box(-np.inf, np.inf, shape=obs['achieved_goal'].shape, dtype=np.float32)
        })
        self.eef_orn = p.getQuaternionFromEuler([math.pi, 0, 0])

    def step(self, action: np.ndarray):
        action_ctrl = action.copy()
        pos_ctrl = action_ctrl[:3] * 0.05
        curr_pos = self._get_gripper_position()
        pos_ctrl = pos_ctrl + curr_pos
        joint_positions = self.ik_controller.calculate_ik_recursive(pos_ctrl, eef_orn=self.eef_orn)

        gripper_width = self._get_gripper_width()
        gripper_width_ctrl = np.clip(gripper_width + action_ctrl[3] * 0.2, 0, 0.085)
        gripper_angle = self._compute_gripper_angle(gripper_width_ctrl)
        joint_positions.append(gripper_angle)

        self._set_ur5_robotiq85_joints(joint_positions)
        self.t += 1

        obs = self._get_obs()
        done = False
        info = {
            'is_success': self._check_success(obs)
        }
        reward = self.compute_reward(obs['achieved_goal'], obs['desired_goal'], info)

        if self.t == self.max_steps:
            obs = self.reset()
            done = True

        return obs, reward, done, info

    def reset(self):
        super().reset()
        self.env.reset()
        self.ik_controller.reset()
        self.t = 0

        handle_position = np.array(self.articulation_channel.data[2]['positions'][3])
        joint_positions = self.ik_controller.calculate_ik_recursive(handle_position, eef_orn=self.eef_orn)
        gripper_angle = self._compute_gripper_angle(0.085)
        joint_positions.append(gripper_angle)
        self._set_ur5_robotiq85_joints_directly(joint_positions)

        return self._get_obs()

    def seed(self, seed=1234):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human'):
        self._step()

    def compute_reward(self, achieved_goal, desired_goal, info):
        if self.reward_type == 'dense':
            return float(achieved_goal)
        else:
            overhead_angle = achieved_goal - desired_goal
            return float(overhead_angle[0] > 0)

    def _get_obs(self):
        gripper_position = self._get_gripper_position()
        gripper_width = self._get_gripper_width()

        robot_obs = np.concatenate((gripper_position, [gripper_width]))

        handle_position = np.array(self.articulation_channel.data[2]['positions'][3])
        drawer_open_distance = np.array([self.articulation_channel.data[2]['joint_positions'][0]])

        object_obs = np.concatenate((handle_position, drawer_open_distance))

        obs = np.concatenate((robot_obs, object_obs))

        return {
            'observation': obs.copy(),
            'achieved_goal': drawer_open_distance.copy(),
            'desired_goal': self.goal.copy()
        }

    def _get_gripper_position(self):
        return np.array(self.articulation_channel.data[1]['positions'][11])

    def _get_gripper_width(self):
        right_inner_finger_pos = np.array(self.articulation_channel.data[1]['positions'][5])
        left_inner_finger_pos = np.array(self.articulation_channel.data[1]['positions'][10])
        width = self._compute_distance(right_inner_finger_pos, left_inner_finger_pos)

        # The position is at the center of inner_finger, so we must get rid of the width of inner finger,
        # to get accurate gripper width
        width = width - 0.00635

        return width

    def _compute_gripper_angle(self, width):
        angle_rad = 0.715 - math.asin((width - 0.01) / 0.1143)
        angle_deg = angle_rad * 180 / math.pi

        return angle_deg

    def _set_ur5_robotiq85_joints(self, joint_positions):
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=0,
            joint_positions=list(joint_positions[:6])
        )
        self._step()

        self.articulation_channel.set_action(
            'SetJointPosition',
            index=1,
            joint_positions=[joint_positions[6], joint_positions[6]],
        )
        self._step()

    def _set_ur5_robotiq85_joints_directly(self, joint_positions):
        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=0,
            joint_positions=list(joint_positions[:6])
        )
        self._step()

        self.articulation_channel.set_action(
            'SetJointPositionDirectly',
            index=1,
            joint_positions=[joint_positions[6], joint_positions[6]],
        )
        self._step()

    def _compute_distance(self, point_a, point_b):
        return np.linalg.norm(point_a - point_b, axis=-1)

    def _check_success(self, obs):
        achieved_goal = obs['achieved_goal'][0]
        desired_goal = obs['desired_goal'][0]

        return (desired_goal < achieved_goal).astype(np.float32)

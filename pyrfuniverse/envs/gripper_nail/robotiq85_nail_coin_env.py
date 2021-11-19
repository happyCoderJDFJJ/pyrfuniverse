from pyrfuniverse.envs import RFUniverseBaseEnv
from pyrfuniverse.envs import RFUniverseGymGoalWrapper
import numpy as np
from gym import spaces
from gym.utils import seeding
import copy


class Robotiq85NailCoinEnv(RFUniverseGymGoalWrapper):
    def __init__(
            self,
            rotation_factor=5,
            vertical_movement_factor=0.01,
            gripper_movement_factor=100,
            nail_movement_factor=0.01,
            goal_baseline=0.05,
            executable_file=None,
    ):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id="44fe03fb-0021-11ec-b7f2-18c04d443e7d",
            articulation_channel_id="44fe03fc-0021-11ec-b7f2-18c04d443e7d",
            game_object_channel_id="44fe03fa-0021-11ec-b7f2-18c04d443e7d",
        )
        self.rotation_factor = rotation_factor
        self.vertical_movement_factor = vertical_movement_factor
        self.gripper_movement_factor = gripper_movement_factor
        self.nail_movement_factor = nail_movement_factor
        self.bit_wise_factor = np.array([
            self.rotation_factor,
            self.vertical_movement_factor,
            self.gripper_movement_factor,
            self.nail_movement_factor
        ])
        self.goal_baseline = goal_baseline

        self.t = 0
        self.goal = self._sample_goal()
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32
        )
        obs = self._get_obs()
        self.observation_space = spaces.Dict({
            'observation': spaces.Box(-np.inf, np.inf, shape=obs['observation'].shape, dtype=np.float32),
            'desired_goal': spaces.Box(-np.inf, np.inf, shape=obs['desired_goal'].shape, dtype=np.float32),
            'achieved_goal': spaces.Box(-np.inf, np.inf, shape=obs['achieved_goal'].shape, dtype=np.float32)
        })

    def step(self, a: np.ndarray):
        action = a.copy()
        action_ctrl = action * self.bit_wise_factor
        curr_state = self._get_gripper_extra_param()
        target_state = curr_state + action_ctrl

        self._set_target_state(target_state)
        self.t += 1

        obs = self._get_obs()
        done = False
        info = {
            'is_success': self._check_success(obs)
        }
        reward = self.compute_reward(obs['achieved_goal'], obs['desired_goal'], info)

        return obs, reward, done, info

    def reset(self):
        super().reset()
        self.env.reset()
        self._reset_object()

        self.t = 0
        self.goal = self._sample_goal()

        return self._get_obs()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human'):
        self._step()

    def compute_reward(self, achieved_goal, desired_goal, info):
        higher_distance = achieved_goal - desired_goal
        return float(-1 * (higher_distance[0] < 0))

    def _get_obs(self):
        gripper_position = np.array(self.articulation_channel.data[0]['positions'][16])
        gripper_velocity = np.array(self.articulation_channel.data[0]['velocities'][16])
        gripper_extra_param = self._get_gripper_extra_param()

        object_pos = np.array(self.rigidbody_channel.data[0]['position'])
        object_rotation = np.array(self.rigidbody_channel.data[0]['rotation'])
        object_velocity = np.array(self.rigidbody_channel.data[0]['velocity'])
        object_angular_vel = np.array(self.rigidbody_channel.data[0]['angular_vel'])

        achieved_goal = np.array([object_pos[1]])

        obs = np.concatenate((
            gripper_position, gripper_velocity, gripper_extra_param, object_pos,
            object_velocity, object_rotation, object_angular_vel
        ))

        return {
            'observation': obs.copy(),
            'achieved_goal': achieved_goal.copy(),
            'desired_goal': self.goal.copy()
        }

    def _reset_object(self):
        obj_rot = [0, 90, 0]
        if self.rotation_factor != 0:
            obj_rot[1] = self._generate_random_float(0, 180)
        self.rigidbody_channel.set_action(
            'SetTransform',
            index=0,
            position=[0, 0.0065, 0],
            rotation=obj_rot
        )
        self.game_object_channel.set_action(
            'SetTransform',
            index=0,
            position=[0, self.goal_baseline, 0],
            rotation=obj_rot
        )

        self._step()

    def _generate_random_float(self, min: float, max: float) -> float:
        assert min < max, \
            'Min value is {}, while max value is {}.'.format(min, max)
        random_float = np.random.rand()
        random_float = random_float * (max - min) + min

        return random_float

    def _get_gripper_extra_param(self):
        joint_positions = np.array(self.articulation_channel.data[0]['joint_positions'])
        rotation = joint_positions[0]
        vertical_movement = joint_positions[1]
        gripper_state = (joint_positions[2] + joint_positions[4]) / 2
        nail_length = (joint_positions[3] + joint_positions[5]) / 2

        return np.array([rotation, vertical_movement, gripper_state, nail_length])

    def _set_target_state(self, target_state):
        joint_positions = [target_state[0], target_state[1], target_state[2], target_state[3], \
                           target_state[2], target_state[3]]
        self.articulation_channel.set_action(
            'SetJointPosition',
            index=0,
            joint_positions=joint_positions
        )
        self._step()

    def _sample_goal(self):
        return np.array([self.goal_baseline])

    def _check_success(self, obs):
        higher_distance = obs['achieved_goal'] - obs['desired_goal']
        return (higher_distance > 0).astype(np.float32)

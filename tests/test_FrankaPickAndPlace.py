import pyrfuniverse.envs
import gym
from pyrfuniverse.envs.robotics import FrankaPickAndPlaceEnv
import numpy as np
import panda_gym


def test(env, n=10):
    obs = env.reset()
    obs = obs.copy()
    obs = obs['observation']

    # print('Gripper pos', obs[:3])
    # print('Gripper velocity', obs[3:6])
    # print('Gripper width', obs[6])
    # print('Object pos', obs[7:10])
    # print('Object rot', obs[10:13])
    # print('Object velocity', obs[13:16])
    # print('Object angular velocity', obs[16:19])

    print('=======================')

    gripper_target_pos = obs[:3].copy()
    error = np.array([0, 0, 0], dtype=np.float64)

    for i in range(n):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        gripper_target_pos = gripper_target_pos + action[:3] * 0.05
        # print('Target:', gripper_target_pos, 'Get:', obs['observation'][:3])
        error += abs(gripper_target_pos - obs['observation'][:3])

    print('Average error:', error / n)

    env.close()


def movable_in_one_step(target_pos, curr_pos):
    distance = target_pos - curr_pos
    for i in range(3):
        if abs(distance[i]) > 0.05:
            return False

    return True


def slow_move(env):
    pass

env1 = FrankaPickAndPlaceEnv(
    executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/FrankaRoboticsServer/RFUniverse.x86_64',
    max_episode_length=50,
    reward_type='sparse',
    asset_bundle_file='/home/haoyuan/rfuniverse/rfuniverse_build/AssetBundles/rigidbody'
)
# env1 = gym.make('PandaPickAndPlace-v1', render=True)
#
# test(env1, 100)
# test(env2, 100)

obs = env1.reset()
slow_move_freq = False

while 1:
    # move to the object
    # for i in range(20):
    #     target_pos = obs['observation'][7:10]
    #     curr_pos = obs['observation'][:3]
    #     move_distance = target_pos - curr_pos
    #     action = np.clip(move_distance / 0.05, np.array([-1, -1, -1]), np.array([1, 1, 1]))
    #     action = np.concatenate((action, np.array([1])))
    #     obs, rew, done, info = env1.step(action)
    #     if slow_move_freq:
    #         for i in range(100):
    #             env1.step(np.array([0, 0, 0, 0]))

    # pick
    for i in range(5):
        action = np.array([0, 0, 0, -1])
        obs, rew, done, info = env1.step(action)
        if slow_move_freq:
            for i in range(100):
                env1.step(np.array([0, 0, 0, 0]))

    # place to target
    for i in range(15):
        target_pos = obs['desired_goal']
        curr_pos = obs['observation'][:3]
        move_distance = target_pos - curr_pos
        action = np.clip(move_distance / 0.05, np.array([-1, -1, -1]), np.array([1, 1, 1]))
        action = np.concatenate((action, np.array([-1])))
        obs, rew, done, info = env1.step(action)
        if slow_move_freq:
            for i in range(100):
                env1.step(np.array([0, 0, 0, 0]))

    print(info)
    env1.reset()

from pyrfuniverse.envs.gripper_nail import Robotiq85NailCardEnv
import numpy as np
from stable_baselines3.common.env_checker import check_env
import gym


# env = Robotiq85NailCardEnv(
#     # rotation_factor=0,
#     # nail_movement_factor=0
# )
waiting = False

env = gym.make('Robotiq85NailCard-v3')

# Check environment
# check_env(env)
# exit()

obs = env.reset()

for i in range(5):
    action = np.array([0, 1, 0, -1])
    obs, reward, done, info = env.step(action)
    if waiting:
        for j in range(10):
            env._step()

for i in range(3):
    action = np.array([0, 0, 1, 0])
    obs, reward, done, info = env.step(action)
    if waiting:
        for j in range(10):
            env._step()

for i in range(9):
    action = np.array([0, -1, 0.1, 1])
    obs, reward, done, info = env.step(action)
    if waiting:
        for j in range(10):
            env._step()
    if info['is_success'] > 0:
        print('Success', reward)

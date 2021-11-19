from pyrfuniverse.envs import NailCardEnv
import numpy as np
from stable_baselines3.common.env_checker import check_env
import gym


env = NailCardEnv(
    rotation_factor=0,
    goal_baseline=0.02,
)

# Check environment
# check_env(env)
# exit()

env.reset()

for i in range(10):
    action = np.array([0, -1, 0, 1])
    obs, reward, done, info = env.step(action)
    # for i in range(10):
    #     env._step()

for i in range(2):
    action = np.array([0, 0, -1, 0])
    obs, reward, done, info = env.step(action)
    # for i in range(3):
    #     env._step()

for i in range(5):
    action = np.array([0, 1, -0.1, 0])
    obs, reward, done, info = env.step(action)
    # for i in range(10):
    #     env._step()
    if info['is_success'] > 0:
        print('Success')

import gym
import numpy as np
from pyrfuniverse.envs.gripper_nail import Robotiq85NailCoinEnv

env = Robotiq85NailCoinEnv(
    # rotation_factor=0,
    nail_movement_factor=0
)
waiting = False

# env = gym.make('Robotiq85NailCard-v3')

# Check environment
# check_env(env)
# exit()

obs = env.reset()

for i in range(10):
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

for i in range(5):
    action = np.array([0, -1, 0.1, 1])
    obs, reward, done, info = env.step(action)
    if waiting:
        for j in range(10):
            env._step()
    if info['is_success'] > 0:
        print('Success', reward)

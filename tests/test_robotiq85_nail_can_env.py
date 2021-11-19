from stable_baselines3.common.env_checker import check_env
from pyrfuniverse.envs.gripper_nail import Robotiq85NailCanEnv
import numpy as np


env = Robotiq85NailCanEnv()
env.reset()

for i in range(10):
    action = np.array([0, 1, 0, 0])
    env.step(action)

for i in range(5):
    env.step(np.array([0, 0, 0, 0]))

for i in range(5):
    action = np.array([1, 0, 0, 0])
    env.step(action)

for i in range(5):
    action = np.array([0, -1, 0, 0])
    env.step(action)

while True:
    env._step()

from pyrfuniverse.envs.gripper_nail import Robotiq85NailBookEnv
from stable_baselines3.common.env_checker import check_env
import numpy as np


env = Robotiq85NailBookEnv()

check_env(env)

env.reset()

while True:
    action = env.action_space.sample()
    obs, _, _, _ = env.step(action)
    print(obs)


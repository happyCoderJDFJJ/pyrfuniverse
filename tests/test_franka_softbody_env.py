from pyrfuniverse.envs.robotics import FrankaSoftbodyEnv
import numpy as np
from stable_baselines3.common.env_checker import check_env
import pyrfuniverse.envs
import gym


env = FrankaSoftbodyEnv(
    asset_bundle_file='/home/haoyuan/workspace/OBITest/Assets/AssetBundles/Linux/softbody',
    reward_type='sparse',
    # executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/FrankaSoftbody/RFUniverse.x86_64',
    # open_gripper=False
)

env.reset()


while True:
    for i in range(50):
        action = env.action_space.sample()
        env.step(action)

from pyrfuniverse.envs.robotics import FrankaClothEnv
import numpy as np
from stable_baselines3.common.env_checker import check_env


env = FrankaClothEnv(
    '/home/haoyuan/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/obi_cloth',
    tolerance=0.08,
    reward_type='dense'
)

# while True:
#     env.reset()
#     for i in range(50):
#         action = env.action_space.sample()
#         env.step(action)

check_env(env)

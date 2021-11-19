from pyrfuniverse.envs.multi_agent import CleanerEnv
from stable_baselines3.common.env_checker import check_env
import numpy as np


env = CleanerEnv(
    asset_bundle_file='/home/haoyuan/rfuniverse/rfuniverse_build/AssetBundles/rigidbody',
    # reset_on_collision=False,
    collision_multiplier=2000
)
# check_env(env)

env.reset()
while True:
    # action = np.array([1, 1, 1, 1, 1, 1])
    action = env.action_space.sample()
    env.step(action)

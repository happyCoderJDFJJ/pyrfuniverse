from pyrfuniverse.envs.robotics import FrankaClothFoldEnv
import numpy as np


env = FrankaClothFoldEnv(
    asset_bundle_file='/home/haoyuan/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/obi_cloth'
)

while True:
    obs = env.reset()

    for i in range(2):
        env.step(np.array([0, 0, 0, -1]))

    for i in range(2):
        obs, _, _, _ = env.step(np.array([0, 0.5, 0, -1]))

    target = obs['desired_goal']
    grasp = obs['achieved_goal']

    distance = target - grasp
    time_steps = int(np.abs(distance / 0.05).max()) + 1
    unit_distance = distance / time_steps / 0.05

    for i in range(time_steps * 2):
        env.step(np.concatenate((unit_distance, np.array([-1]))))


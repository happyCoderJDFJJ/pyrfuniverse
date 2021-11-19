from pyrfuniverse.envs.gripper_nail import Robotiq85InsertEnv
import numpy as np


env = Robotiq85InsertEnv(
    hole_range=0
)
env.reset()

while True:
    action = np.array([0, 0, 1])
    obs, reward, _, _ = env.step(action)
    print(reward)


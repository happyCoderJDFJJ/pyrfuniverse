from pyrfuniverse.envs.tobor_robotics import ToborPushPullEnv
import numpy as np
import math


if __name__ == '__main__':
    env = ToborPushPullEnv(
        max_steps=50,
        pull=True,
        asset_bundle_file='/home/haoyuan/workspace/rfuniverse/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/articulation',
    )
    env.reset()

    env.step(np.array([0, 0, -1, 0, 0]))
    for i in range(50):
        env._step()
    env.step(np.array([0, 0, -1, 0, 0]))
    for i in range(50):
        env._step()

    for i in range(10):
        for i in range(50):
            env._step()
        env.step(np.array([-1, 0, 0, 0, 0]))

    # pos = env._get_tobor_eef_position('left')
    # # pos = pos + np.array([0, 0.2, 0])
    #
    # deg = 0
    # for i in range(10):
    #     for _ in range(50):
    #         env._step()
    #
    #     env._set_tobor_arm_directly(
    #         'left',
    #         pos,
    #         [deg, 0, math.pi / 2]
    #     )
    #     deg -= math.pi / 20

    while 1:
        env._step()

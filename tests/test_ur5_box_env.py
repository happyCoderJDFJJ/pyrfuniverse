from pyrfuniverse.envs import Ur5BoxEnv
import numpy as np
import math
import pybullet as p


env = Ur5BoxEnv(
    max_steps=50,
    min_open_angle=10,
    reward_type='sparse'
)
# env.reset()

env.set_ur5_arm(
    [0.130700007,0.469000012,-0.379999995],
    # p.getQuaternionFromEuler([0, math.pi, math.pi / 4])
    None
)
env.set_robotiq85_width(0.03)

# env.test_ik_direct(np.array([-0.0693000033, 0.1039, -0.496]))
# for i in range(30):
#     env._step()
#
# env.robotiq85_close()
# for i in range(30):
#     env._step()
#
# env.test_ik(np.array([-0.0693000033, 0.1239, -0.496]))
# for i in range(10):
#     env._step()
# env.test_ik(np.array([-0.0693000033, 0.1439, -0.496]))
# for i in range(10):
#     env._step()
# env.test_ik(np.array([-0.0693000033, 0.1639, -0.496]))
# for i in range(10):
#     env._step()

# env.reset()

while True:
    env._step()
    # env.reset()
    # env.step(np.array([1, 0, 1, 0]))
    # env.step(np.array([1, 0, 1, 0]))
    # env.step(np.array([1, 0, 1, 0]))
    # env.step(np.array([1, 0, 1, 0]))
    # env.step(np.array([1, 0, 0, 0]))
    # env.step(np.array([1, 0, 0, 0]))
    # env.step(np.array([1, 0, 0, 0]))

    # for i in range(10):
    #     env.step(np.array([0, 0, 0, 0]))
    #
    # for i in range(20):
    #     env.step(np.array([0, 0, 0, -1]))
    #
    # for i in range(15):
    #     obs, reward, done, info = env.step(np.array([0, 0.2, 0, 0]))
    #     if info['is_success']:
    #         print('success', reward)
    #     else:
    #         print('failure', reward)
    #
    # for i in range(10):
    #     env.step(np.array([0, 0, 0, 0]))

# while True:
#     env._step()

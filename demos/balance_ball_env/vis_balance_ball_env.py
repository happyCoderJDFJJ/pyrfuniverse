from pyrfuniverse.envs import BalanceBallEnv
import numpy as np


if __name__ == '__main__':
    env = BalanceBallEnv()
    env.reset()
    while 1:
        try:
            env.step(np.random.rand(2) * 4 - 2)
            # Action space is [(-2, -2), (2, 2)]
        except:
            env.close()

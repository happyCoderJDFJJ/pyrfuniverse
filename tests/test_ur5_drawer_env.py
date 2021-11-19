from pyrfuniverse.envs import Ur5DrawerEnv
import numpy as np


if __name__ == '__main__':
    env = Ur5DrawerEnv(
        max_steps=50,
        reward_type='sparse'
    )

    while True:
        env.reset()

        for i in range(10):
            env._step()

        for i in range(10):
            env.step(np.array([0, 0, 0, -1]))

        for i in range(10):
            _, r, _, _ = env.step(np.array([1, 0, 0, -1]))
            print(r)

        for i in range(50):
            env._step()

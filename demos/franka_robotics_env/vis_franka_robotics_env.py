from pyrfuniverse.envs.robotics import FrankaReachEnv
import numpy as np
import math

if __name__ == '__main__':
    env = FrankaReachEnv(
        executable_file='../../RFUniverse/Build/FrankaRobotics/RFUniverse.x86_64',
        max_episode_length=200,
        reward_type='sparse'
    )

    env.reset()

    radius = 0.25
    delta = 5
    last_x = 0
    last_z = 0
    curr_degree = 0

    while 1:
        try:
            x = radius * math.cos(math.radians(curr_degree)) - radius
            z = radius * math.sin(math.radians(curr_degree))
            _1, _2, done, _3 = env.step(np.array([(x - last_x) / 0.05, 0, (z - last_z) / 0.05, 0]))
            if done:
                curr_degree = 0
                last_x = 0
                last_z = 0
                env.reset()
            else:
                last_x = x
                last_z = z
                curr_degree += delta
        except:
            env.close()

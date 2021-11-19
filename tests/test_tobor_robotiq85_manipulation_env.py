from pyrfuniverse.envs import ToborRobotiq85ManipulationEnv
import numpy as np
import pybullet as p
import math


if __name__ == '__main__':
    env = ToborRobotiq85ManipulationEnv(
        'tamp',
        left_init_joint_positions=[-90, 45, 0, 75, 0, 60, 0],
        right_init_joint_positions=[-90, -45, 0, -75, 0, -60, 0]
    )
    env.reset()

    pi = math.pi

    # move a gripper to a position with an orientation
    env.step('left', np.array([-0.7, 0.5, 0.7]), orientation=p.getQuaternionFromEuler([pi / 2, 0, 0]))

    # If you need to change orientation, I recommend turning gripper first
    # In this example, I want to change gripper's orientation to [pi / 2, pi / 2, 0]
    n_time_steps = 6
    for i in range(n_time_steps):
        env.step('left', np.array([-0.7, 0.5, 0.7]),
                 orientation=p.getQuaternionFromEuler([pi / 2, pi / n_time_steps / 2 * (i + 1), 0]))

    # Close gripper
    env.close_gripper('left')

    # Open gripper
    env.open_gripper('left')

    # Move two arms together
    env.double_step(
        left_pos=np.array([-0.6, 1.0, 1.0]),
        right_pos=np.array([0.6, 1.0, 1.0]),
        left_orn=p.getQuaternionFromEuler([pi / 2, 0, 0]),
        right_orn=p.getQuaternionFromEuler([pi / 2, 0, 0]),
    )

    while True:
        env._step()

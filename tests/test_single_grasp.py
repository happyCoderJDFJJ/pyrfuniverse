from pyrfuniverse.actions import SingleGrasp
from pyrfuniverse.actions import SingleTransport
from pyrfuniverse.actions import SinglePlace
from pyrfuniverse.envs import ToborRobotiq85ManipulationEnv
import numpy as np


if __name__ == '__main__':
    env = ToborRobotiq85ManipulationEnv(
        'tamp',
        left_init_joint_positions=[-90, 45, 0, 75, 0, 60, 0],
        right_init_joint_positions=[-90, -45, 0, -75, 0, -60, 0]
    )
    env.reset()

    grasp_action = SingleGrasp(env)
    transport_action = SingleTransport(env)
    place_action = SinglePlace(env)

    grasp_action.heuristics(np.array([-0.35, 0.8, 1]))
    grasp_action.execute()

    transport_action.set_wavepoints([np.array([0.113, 1.2, 0.85]), np.array([0.113, 1, 0.85])])
    transport_action.execute()

    place_action.set_wavepoints([np.array([0.113, 1.2, 0.85]), np.array([-0.35, 1.1, 1])])
    place_action.execute()

    while True:
        env._step()

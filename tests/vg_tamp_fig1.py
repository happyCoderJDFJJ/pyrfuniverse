from test_tobor_full import FullToborEnv
import math


def Vector3(x, y, z):
    return [x, y, z]


if __name__ == '__main__':
    env = FullToborEnv()

    # Image 1, initial state
    env.set_left_arm(
        [-0.1, 1, 0.8],
        [0, -math.pi / 2, 0]
    )

    # env.set_right_arm(
    #     [0.1, 1, 0.8],
    #     [0, math.pi / 2, 0]
    # )


    # Image 2, put hand near
    # env.set_right_arm(
    #     position=Vector3(0.108999997,0.888199985,0.881900012),
    #     rotation=[math.pi / 2, math.pi / 6, math.pi / 4]
    # )

    # Image 3, close hand and pick up the clock
    # env.set_right_arm(
    #     position=[0.0769999996,1.01460004,0.7296],
    #     rotation=[math.pi / 2, 0, 0]
    # )
    # env.set_right_gripper_width(0.01)

    # Image 4, image during navigation and picking the alarm clock


    # Image 5, put the alarm clock down on the table

    # env.set_right_arm(
    #     position=Vector3(0.188999996,0.95599997,0.869000018),
    #     rotation=[math.pi / 2, math.pi / 7, 0]
    # )
    # env.set_right_gripper_width(0.085)

    # Image 6, before Image 5, put alarm clock on table, keeping hand closed
    env.set_right_arm(
        position=Vector3(0.188999996,0.95599997,0.869000018),
        rotation=[math.pi / 2, math.pi / 7, 0]
    )
    env.set_right_gripper_width(0.005)

    while 1:
        env._step()

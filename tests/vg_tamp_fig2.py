from test_tobor_full import FullToborEnv
import math


def Vector3(x, y, z):
    return [x, y, z]


if __name__ == '__main__':
    env = FullToborEnv()

    # Image 1, initial state
    # env.set_left_arm(
    #     [-0.1, 1, 0.8],
    #     [0, -math.pi / 2, 0]
    # )

    # env.set_right_arm(
    #     [0.1, 1, 0.8],
    #     [0, math.pi / 2, 0]
    # )


    # Image 2, Bottle in hand
    # env.set_right_arm(
    #     position=Vector3(0,0.407000005,1.2615),
    #     rotation=[math.pi / 2, math.pi / 6, math.pi / 4]
    # )
    # env.set_right_gripper_width(0.01)


    # Image 3, open microwave and put bottle into it
    # env.set_right_arm(
    #     position=Vector3(0.074000001,1.39100003,0.778299987),
    #     rotation=[-math.pi / 6, 0, -math.pi / 2]
    # )
    # env.set_right_gripper_width(0.07)
    #
    # env.set_left_arm(
    #     position=Vector3(-0.141000003,1.39100003,0.568099976),
    #     rotation=[-5 * math.pi / 18, 0, math.pi / 2]
    # )
    # env.set_left_gripper_width(0.03)

    # Image 4, close microwave and wait
    # env.set_left_arm(
    #     [-0.1, 1.2, 0.8],
    #     [0, -math.pi / 2, 0]
    # )
    #
    # env.set_right_arm(
    #     [0.1, 1.2, 0.8],
    #     [0, math.pi / 2, 0]
    # )

    # Image 5, get bottle and put it down, keeping microwave door open
    # Vector3(-0.189300001, 1.41849995, 0.763599992)
    # env.set_right_arm(
    #     position=Vector3(0.0419999994,0.556999981,1.15390003),
    #     rotation=[0, 0, math.pi / 2]
    # )
    # env.set_right_gripper_width(0.07)
    #
    # env.set_left_arm(
    #     Vector3(-0.162100002,1.34679997,0.754400015),
    #     rotation=[-math.pi / 3, 0, math.pi / 2]
    # )
    # env.set_left_gripper_width(0.03)

    # Image 6, a navigation process
    env.set_left_arm(
        [-0.1, 1, 0.8],
        [0, -math.pi / 2, 0]
    )
    env.set_right_arm(
        Vector3(0.190899998, 0.80400002, 1.05200005),
        [0, 0, -math.pi / 2]
    )
    env.set_right_gripper_width(0.07)

    while 1:
        env._step()

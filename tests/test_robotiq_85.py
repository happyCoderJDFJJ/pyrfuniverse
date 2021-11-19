from pyrfuniverse.envs import RFUniverseBaseEnv
import math
import pybullet as p
import pybullet_data


class TestArticulationChannelEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="59ba36ae-f9c5-11eb-b925-18c04d443e7d",
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()

    def wait(self, n):
        for i in range(n):
            self._step()


if __name__ == '__main__':
    env = TestArticulationChannelEnv()
    env.reset()

    env.wait(10)
    # for i in range(10):
    #     env.articulation_channel.set_action(
    #         'SetJointPosition',
    #         index=0,
    #         joint_positions=[5 * i, 5 * i]
    #     )
    #     env.wait(5)
    env.articulation_channel.set_action(
            'SetJointPosition',
            index=1,
            joint_positions=[55, 55]
        )
    print('Close')

    env.wait(500)
    env.articulation_channel.set_action(
        'SetJointPosition',
        index=1,
        joint_positions=[0, 0]
    )
    print('Open')

    while True:
        env.wait(1)

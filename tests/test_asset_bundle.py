from pyrfuniverse.envs import RFUniverseBaseEnv


class RigidbodyChannelTestEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id='622f0a70-4f87-11ea-a6bf-784f4387d1f7',
            rigidbody_channel_id='621f0a70-4f87-11ea-a6bf-784f4387d1f7',
            articulation_channel_id=None,
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()


def sleep(env, time_step=10):
    for i in range(time_step):
        env.step()


if __name__ == '__main__':
    env = RigidbodyChannelTestEnv()
    env.reset()

    env.rigidbody_channel.set_action(
        'LoadRigidbody',
        filename='../RFUniverse/Assets/AssetBundles/Windows/rigidbody',
        name='Test1',
        position=[0.0, 3, 0.0],
    )
    env.step()
    sleep(env, 10)

    env.close()

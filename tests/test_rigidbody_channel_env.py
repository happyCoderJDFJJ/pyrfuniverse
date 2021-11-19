from pyrfuniverse.envs import RFUniverseBaseEnv
from test_tools import sleep


class TestRigidbodyChannelEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id="7c60784e-f453-11eb-9b86-54ee75cfa697",
            articulation_channel_id=None,
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()


if __name__ == '__main__':
    env = TestRigidbodyChannelEnv()
    env.reset()

    print('Load 002_master_chef_can')
    env.rigidbody_channel.set_action(
        'LoadRigidbody',
        filename='Assets/AssetBundles/Linux/rigidbody',
        name='002_master_chef_can',
        vhacd=True,
        position=[0.0, 3, 0.0],
    )
    env.step()
    print('current count:', env.rigidbody_channel.count)
    sleep(env, 20)

    print('Load 003_cracker_box')
    env.rigidbody_channel.set_action(
        'LoadRigidbody',
        filename='Assets/AssetBundles/Linux/rigidbody',
        name='003_cracker_box',
        vhacd=True,
        position=[0.0, 5, 0.0],
        rotation=[0.0, 90, 0.0]
    )
    env.step()
    print('current count:', env.rigidbody_channel.count)
    sleep(env, 20)

    print('Add force to index 0.')
    env.rigidbody_channel.set_action(
        'AddForce',
        index=0,
        force=[0.0, 5.0, 0.0],
    )
    env.step()
    sleep(env, 10)

    print('Add force to index 1.')
    env.rigidbody_channel.set_action(
        'AddForce',
        index=0,
        force=[0.0, -5.0, 0.0],
    )
    env.step()
    sleep(env, 10)

    print('Set transform.')
    env.rigidbody_channel.set_action(
        'SetTransform',
        index=1,
        position=[0.0, 5, 0.0],
        rotation=[0.0, 90, 0.0]
    )
    env.step()
    sleep(env, 10)

    print('Set velocity.')
    env.rigidbody_channel.set_action(
        'SetVelocity',
        index=0,
        velocity=[0.0, 5.0, 0.0]
    )
    env.step()
    sleep(env, 10)

    print('Destroy index 0.')
    env.rigidbody_channel.set_action(
        'Destroy',
        index=0
    )
    env.step()
    sleep(env, 10)

    print('Destroy index 1.')
    env.rigidbody_channel.set_action(
        'Destroy',
        index=0
    )
    env.step()
    sleep(env, 10)

    env.close()

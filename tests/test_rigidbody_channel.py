from pyrfuniverse.environment import UnityEnvironment
from pyrfuniverse.rfuniverse_channel import RigidbodyChannel
from pyrfuniverse.rfuniverse_channel import CameraChannel
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


def test_behavior_specs(env):
    print(list(env.behavior_specs.keys()))
    return list(env.behavior_specs.keys())[0]


def sleep(env, time_step=10):
    for i in range(time_step):
        env.step()


if __name__ == '__main__':
    env = RigidbodyChannelTestEnv()
    env.reset()

    # behavior_name = test_behavior_specs(env)
    # print(behavior_name)

    env.rigidbody_channel.set_action(
        'LoadRigidbody',
        filename='../RFUniverse/Assets/AssetBundles/Windows/rigidbody',
        name='002_master_chef_can',
        position=[0.0, 3, 0.0],
    )
    env.step()
    print(env.rigidbody_channel.count)
    sleep(env, 5)

    env.rigidbody_channel.set_action(
        'LoadRigidbody',
        filename='../RFUniverse/Assets/AssetBundles/Windows/rigidbody',
        name='003_cracker_box',
        position=[0.0, 5, 0.0],
    )
    env.step()
    print(env.rigidbody_channel.count)
    sleep(env, 5)

    env.rigidbody_channel.set_action(
        'AddForce',
        index=0,
        force=[0.0, 5.0, 0.0],
    )
    env.step()
    sleep(env, 10)

    env.rigidbody_channel.set_action(
        'AddForce',
        index=0,
        force=[0.0, -5.0, 0.0],
    )
    env.step()
    sleep(env, 10)

    env.close()

from pyrfuniverse.envs import RFUniverseBaseEnv


class TestLoadArticulationEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="59ba36ae-a9c5-11eb-b925-18c04d443e7d",
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()


if __name__ == '__main__':
    env = TestLoadArticulationEnv()
    env.articulation_channel.set_action(
        'LoadArticulationBody',
        filename='/home/haoyuan/workspace/rfuniverse/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/articulation',
        name='Microwave_1',
        position=[0, 0, 0],
        rotation=[0, 0, 0]
    )
    env.step()

    # env.articulation_channel.set_action(
    #     'SetJointPositionDirectly',
    #     index=0,
    #     joint_positions=[45]
    # )

    while True:
        env.step()

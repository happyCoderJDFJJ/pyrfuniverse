from pyrfuniverse.envs import RFUniverseBaseEnv


class PoseTrackerDemoEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            game_object_channel_id='557cf89f-5555-4dbb-9f5a-67faafe83d46',
            rigidbody_channel_id='00c188e2-138b-46f2-afd8-2caab6797864',
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()
        print(self.rigidbody_channel.data)
        # print(self.game_object_channel.data)

from pyrfuniverse.envs.robotics import FrankaRoboticsEnv


class FrankaPushEnv(FrankaRoboticsEnv):

    def __init__(
        self,
        executable_file,
        max_episode_length,
        reward_type,
        asset_bundle_file=None,
        seed=None
    ):
        super().__init__(
            executable_file=executable_file,
            max_episode_length=max_episode_length,
            reward_type=reward_type,
            seed=seed,
            tolerance=0.05,
            load_object=True,
            target_in_air=False,
            block_gripper=True,
            target_range=0.08,
            object_range=0.08,
            asset_bundle_file=asset_bundle_file
        )

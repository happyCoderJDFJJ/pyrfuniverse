from pyrfuniverse.envs.robotics import FrankaRoboticsEnv


class FrankaReachEnv(FrankaRoboticsEnv):

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
            load_object=False,
            target_in_air=True,
            block_gripper=True,
            target_range=0.15,
            object_range=0.15,
            asset_bundle_file=None
        )

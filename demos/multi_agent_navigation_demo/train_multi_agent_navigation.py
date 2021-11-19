from pyrfuniverse.envs.multi_agent import navigation_env

from stable_baselines3 import SAC
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DDPG

import supersuit as ss
from supersuit.vector.sb3_vector_wrapper import SB3VecEnvWrapper
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--algo', choices=['ppo', 'a2c'], type=str, required=True)
    parser.add_argument('--logdir', type=str, required=True)
    parser.add_argument('--timesteps', type=int, default=5000000)
    parser.add_argument('--strength', type=float, default=1000)
    parser.add_argument('--collision_multiplier', type=float, default=5)

    config = parser.parse_args()
    return config


if __name__ == '__main__':
    config = parse_args()
    config.logdir = config.logdir + '_' + str(config.strength) + '_' + str(config.collision_multiplier)

    if os.path.exists(config.logdir):
        print('Error: Log dir {} has existed!'.format(config.logdir))
        exit(-1)

    env = navigation_env.parallel_env(
        num_agents=5,
        log_dir=config.logdir,
        asset_bundle_file='/home/haoyuan/rfuniverse/rfuniverse_build/AssetBundles/rigidbody',
        max_episode_length=100,
        executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/NavigationServer/RFUniverse.x86_64',
        strength=config.strength,
        collision_multiplier=config.collision_multiplier
    )

    env = ss.pettingzoo_env_to_vec_env_v0(env)
    env = SB3VecEnvWrapper(env)

    model = None
    if config.algo == 'ppo':
        model = PPO(
            'MlpPolicy',
            env,
            verbose=1,
        )

    elif config.algo == 'a2c':
        model = A2C(
            'MlpPolicy',
            env,
            verbose=1,
        )

    model.learn(total_timesteps=config.timesteps)

    model.save('{}/policy'.format(config.logdir))

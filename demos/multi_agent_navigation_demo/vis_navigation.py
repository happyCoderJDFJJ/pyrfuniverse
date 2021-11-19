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
    parser.add_argument('--episodes', type=int, default=5)

    config = parser.parse_args()
    return config


if __name__ == '__main__':
    config = parse_args()

    env = navigation_env.env(
        num_agents=5,
        log_dir=config.logdir,
        asset_bundle_file='/home/haoyuan/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/rigidbody',
        max_episode_length=100,
        executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/Navigation/RFUniverse.x86_64',
        log_monitor=False
    )

    model = None
    if config.algo == 'ppo':
        model = PPO.load('{}/policy'.format(config.logdir))
    elif config.algo == 'a2c':
        model = A2C.load('{}/policy'.format(config.logdir))

    for i in range(config.episodes):
        total_reward = 0
        env.reset()
        for agent in env.agent_iter():
            obs, reward, done, info = env.last()
            total_reward += reward
            act = model.predict(obs, deterministic=True)[0] if not done else None
            env.step(act)
            env.render()
        print('Episodic Reward for episode {}: {}'.format(i, total_reward))

    env.close()

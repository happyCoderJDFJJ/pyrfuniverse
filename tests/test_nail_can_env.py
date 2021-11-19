from stable_baselines3.common.env_checker import check_env
from pyrfuniverse.envs import NailCanEnv


env = NailCanEnv()
env.reset()

while True:
    action = env.action_space.sample()
    env.step(action)

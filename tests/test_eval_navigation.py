from pyrfuniverse.envs import MultiAgentNavigationEnv
from pyrfuniverse.envs.multi_agent import navigation_env
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import SAC
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3 import PPO
import supersuit as ss

env = navigation_env.env(
    num_agents=5,
    asset_bundle_file='/home/haoyuan/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/rigidbody',
    max_episode_length=100,
    executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/Navigation/RFUniverse.x86_64'
)

model = PPO.load('policy')

while 1:
    env.reset()
    for agent in env.agent_iter():
        obs, reward, done, info = env.last()
        print(obs, reward, done, info)
        act = model.predict(obs, deterministic=True)[0] if not done else None
        env.step(act)

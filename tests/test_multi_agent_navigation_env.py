from pyrfuniverse.envs import MultiAgentNavigationEnv
from pyrfuniverse.envs.multi_agent import navigation_env
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import SAC
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3 import PPO
import supersuit as ss
from supersuit.vector.sb3_vector_wrapper import SB3VecEnvWrapper
from pyrfuniverse.utils.callbacks import SaveOnBestTrainingRewardCallback

env = navigation_env.parallel_env(
    num_agents=5,
    log_dir='ppo',
    asset_bundle_file='/home/haoyuan/rfuniverse/RFUniverse/Assets/AssetBundles/Linux/rigidbody',
    max_episode_length=100,
    executable_file='/home/haoyuan/rfuniverse/rfuniverse_build/NavigationServer/RFUniverse.x86_64'
)

env = ss.pettingzoo_env_to_vec_env_v0(env)
env = SB3VecEnvWrapper(env)

model = PPO(
    MlpPolicy,
    env,
    verbose=3,
    gamma=0.95,
    n_steps=256,
    ent_coef=0.0905168,
    learning_rate=0.00062211,
    vf_coef=0.042202,
    max_grad_norm=0.9,
    gae_lambda=0.99,
    n_epochs=5,
    clip_range=0.3,
    batch_size=256,
)

# model.learn(total_timesteps=1000000, callback=SaveOnBestTrainingRewardCallback(check_freq=100, log_dir='log_1'))
model.learn(total_timesteps=5000000)

model.save('policy')

from stable_baselines3.ppo import CnnPolicy
from stable_baselines3 import PPO, SAC
from stable_baselines3.common.monitor import Monitor
from pettingzoo.butterfly import pistonball_v4
import supersuit as ss


env = pistonball_v4.parallel_env(n_pistons=20, local_ratio=0, time_penalty=-0.1, continuous=True, random_drop=True, random_rotate=True, ball_mass=0.75, ball_friction=0.3, ball_elasticity=1.5, max_cycles=125)
env = ss.color_reduction_v0(env, mode='B')
env = ss.resize_v0(env, x_size=84, y_size=84)
env = ss.frame_stack_v1(env, 3)

env = ss.pettingzoo_env_to_vec_env_v0(env)
env = ss.concat_vec_envs_v0(env, 8, num_cpus=4, base_class='stable_baselines3')

model = PPO('CnnPolicy', env)
model.learn(total_timesteps=2000000)
model.save('policy')

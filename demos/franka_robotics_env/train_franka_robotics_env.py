from pyrfuniverse.envs.robotics import FrankaReachEnv, FrankaPushEnv, FrankaPickAndPlaceEnv
from pyrfuniverse.utils.callbacks import SaveOnBestTrainingRewardCallback
from pyrfuniverse.utils.os_utils import make_sb3_model_dir
from stable_baselines3 import SAC
from stable_baselines3 import HER
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter
from stable_baselines3.common.results_plotter import plot_results
import argparse
import matplotlib.pyplot as plt


def arg_parser():
    parser = argparse.ArgumentParser(description='Training balance ball environment parser')
    parser.add_argument('--timesteps', type=int, default=1000)
    parser.add_argument('--task', type=str, choices=['Reach', 'Push', 'PickAndPlace'], default='Reach')
    parser.add_argument('--episode_length', type=int, default=50)
    parser.add_argument('--model_dir', type=str, default='franka_robotics_model')
    parser.add_argument('--check_freq', type=int, default=1000)
    parser.add_argument('--reward_type', type=str, default='sparse')
    parser.add_argument('--seed', type=int, default=1234)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    config = arg_parser()
    config.model_dir = config.model_dir + '_' + config.task.lower()
    config.model_dir = make_sb3_model_dir(config.model_dir)

    env = eval('Franka' + config.task + 'Env')(
        executable_file='../../RFUniverse/Build/Franka_Robotics_Env/RFUniverse.exe',
        max_episode_length=config.episode_length,
        reward_type=config.reward_type
    )
    env = Monitor(env, config.model_dir)

    callback = SaveOnBestTrainingRewardCallback(config.check_freq, config.model_dir)
    model = HER('MlpPolicy', env, SAC, max_episode_length=config.episode_length)
    model.learn(total_timesteps=config.timesteps, callback=callback)

    plot_results([config.model_dir], config.timesteps, results_plotter.X_TIMESTEPS, 'FrankaRobotics-SAC')
    plt.show()

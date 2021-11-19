import argparse
import os
import matplotlib.pyplot as plt
from pyrfuniverse.envs import BalanceBallEnv
from pyrfuniverse.utils.callbacks import SaveOnBestTrainingRewardCallback

from stable_baselines3.sac import SAC
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import plot_results



def arg_parser():
    parser = argparse.ArgumentParser(description='Training balance ball environment parser')
    parser.add_argument('--timesteps', type=int, default=1000)
    parser.add_argument('--monitor-log', type=str, default='./sac_balance_ball')
    parser.add_argument('--tensorboard-log', type=str, default='./balance_ball_tensorboard')
    parser.add_argument('--model-dir', type=str, default='balance_ball_model')
    parser.add_argument('--model-name', type=str, default='sac_balance_ball')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    config = arg_parser()
    os.makedirs(config.model_dir, exist_ok=True)

    callback = SaveOnBestTrainingRewardCallback(1000, config.model_dir)
    env = BalanceBallEnv()
    env = Monitor(env, config.model_dir)

    model = SAC('MlpPolicy', env, tensorboard_log=config.tensorboard_log)
    model.learn(total_timesteps=config.timesteps, callback=callback)

    plot_results([config.model_dir], config.timesteps, results_plotter.X_TIMESTEPS, 'BalanceBall-SAC')
    plt.show()

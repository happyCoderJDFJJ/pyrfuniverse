from pyrfuniverse.envs import BalanceBallEnv
from stable_baselines3.sac import SAC
from stable_baselines3.common.evaluation import evaluate_policy


if __name__ == '__main__':
    env = BalanceBallEnv()
    model = SAC.load('./balance_ball_model/best_model.zip', env=env)
    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
    print('Mean reward:', mean_reward)
    print('Std reward:', std_reward)

    obs = env.reset()
    for i in range(1000):
        action, _status = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)

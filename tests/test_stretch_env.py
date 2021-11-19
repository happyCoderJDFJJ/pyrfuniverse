from pyrfuniverse.envs.stretch_env import StretchEnv


if __name__ == '__main__':
    env = StretchEnv()
    height = 0
    extension = 0
    while True:
        env.step(height, extension)
        height += 0.01
        extension += 0.001

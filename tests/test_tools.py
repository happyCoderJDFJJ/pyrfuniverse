
def sleep(env, time_step=10):
    for i in range(time_step):
        env.step()

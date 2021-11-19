from pose_tracker_demo_env import PoseTrackerDemoEnv

if __name__ == '__main__':
    env = PoseTrackerDemoEnv(None)
    while 1:
        try:
            env.step()
        except KeyboardInterrupt:
            env.close()
            exit()

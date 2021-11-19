from pyrfuniverse.environment import UnityEnvironment
from pyrfuniverse.rfuniverse_channel import GameObjectChannel


def sleep(env, time_step=10):
    for i in range(time_step):
        env.step()


def main():
    channel = GameObjectChannel('624f0a70-4f87-11ea-a6bf-784f4387d1f7')
    env = UnityEnvironment(side_channels=[channel])
    env.reset()

    channel.set_action(
        'LoadGameObject',
        filename='../RFUniverse/Assets/AssetBundles/game_object',
        name='002_master_chef_can_game_object',
        position=[0, 3, 0]
    )
    sleep(env, 10)

    channel.set_action(
        'SetTransform',
        index=0,
        position=[0, 3, -8],
        rotation=[90, 0, 0]
    )
    sleep(env, 10)

    channel.set_action(
        'Translate',
        index=0,
        translation=[1, 1, 1]
    )
    sleep(env, 10)

    channel.set_action(
        'Rotate',
        index=0,
        rotation=[20, 0, 0]
    )
    sleep(env, 10)

    channel.set_action(
        'Destroy',
        index=0
    )

    while 1:
        env.step()


if __name__ == '__main__':
    main()

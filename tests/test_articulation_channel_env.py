from pyrfuniverse.envs import RFUniverseBaseEnv
import math
import pybullet as p
import pybullet_data


class TestArticulationChannelEnv(RFUniverseBaseEnv):
    def __init__(self, executable_file=None):
        super().__init__(
            executable_file=executable_file,
            camera_channel_id=None,
            rigidbody_channel_id=None,
            articulation_channel_id="59ba36ae-f9c5-11eb-b925-18c04d443e7d",
            game_object_channel_id=None,
        )

    def step(self):
        # In each time step, this function must be called to make sure Unity works well.
        self._step()

    def reset(self):
        self.env.reset()


class PyBulletVisualization:
    def __init__(self):
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, -9.8, 0)
        self.robot = p.loadURDF('franka_panda/panda.urdf', [0, 0, 0], p.getQuaternionFromEuler([0, 0, 0]),
                                  useFixedBase=True)
        self.revolute_joint_ids = []
        self.end_effector_id = 11
        self.ee_link_state = None
        for i in range(p.getNumJoints(self.robot)):
            info = p.getJointInfo(self.robot, i)
            joint_type = info[2]
            if (joint_type == p.JOINT_REVOLUTE):
                self.revolute_joint_ids.append(i)

    def set_joint_positions(self, joint_positions):
        for i, (idx) in enumerate(self.revolute_joint_ids):
            p.resetJointState(self.robot, idx, joint_positions[i])

        self.ee_link_state = p.getLinkState(self.robot, self.end_effector_id)

    def get_ee_position(self):
        return self.ee_link_state[0]

    def get_ee_orientation(self):
        return self.ee_link_state[1]

    def get_ee_orientation_euler(self):
        euler_rad = p.getEulerFromQuaternion(self.ee_link_state[1])
        euler_deg = [0, 0, 0]
        for i, (rad) in enumerate(euler_rad):
            euler_deg[i] = rad * 180 / math.pi

        return euler_deg


def get_unity_joint_pos_from_pybullet(pybullet_joint_pos: list) -> list:
    pybullet_joint_pos = list(pybullet_joint_pos)
    for i, (joint_pos) in enumerate(pybullet_joint_pos):
        pybullet_joint_pos[i] = -180 * joint_pos / math.pi

    return pybullet_joint_pos


if __name__ == '__main__':
    env = TestArticulationChannelEnv(executable_file='../RFUniverse/Build/TestArticulationChannel/RFUniverse.x86_64')
    # env = TestArticulationChannelEnv()
    env.reset()

    bullet_env = PyBulletVisualization()

    raw_joint_positions = [-2.5998955725827737, 1.7628, -1.859603309046057, -2.1717169993748184, 1.2655794256913953, 1.427691554789833, -1.0205860683532562]
    target_joint_positions = get_unity_joint_pos_from_pybullet(raw_joint_positions)
    bullet_env.set_joint_positions(raw_joint_positions)
    env.articulation_channel.set_action(
        'SetJointPosition',
        index=0,
        joint_positions=target_joint_positions
    )
    env.step()

    for i in range(50):
        env.step()

    print(env.articulation_channel.data[1]['positions'][3])
    print(bullet_env.get_ee_position())
    print(env.articulation_channel.data[1]['rotations'][3])
    # print(bullet_env.get_ee_orientation())
    print(bullet_env.get_ee_orientation_euler())

    for i in range(15000):
        env.step()

    env.close()
    exit()

    raw_joint_positions = [-2.8973, -0.8477989865724896, 2.6336106266767243, -2.5939362749816364, 2.049974074687139, 3.656791872672859, 1.8861794132444973]
    target_joint_positions = get_unity_joint_pos_from_pybullet(raw_joint_positions)

    env.articulation_channel.set_action(
        'SetJointPosition',
        index=0,
        joint_positions=target_joint_positions
    )
    env.step()

    for i in range(150):
        env.step()

    raw_joint_positions = [-0.8036368522569843, -1.1556760632877243, -2.326750737200364, -2.1332362440610932, -2.8973, 1.577228113676319, -0.4447488569861174]
    target_joint_positions = get_unity_joint_pos_from_pybullet(raw_joint_positions)

    env.articulation_channel.set_action(
        'SetJointPosition',
        index=0,
        joint_positions=target_joint_positions
    )
    env.step()

    for i in range(150):
        env.step()

    raw_joint_positions = [1.8424663153580172, -0.8177307417887943, 0.5825902093069698, -1.6206685988144005, 0.5550207619716024, 0.2300185792514769, 2.3883157378812587]
    target_joint_positions = get_unity_joint_pos_from_pybullet(raw_joint_positions)

    env.articulation_channel.set_action(
        'SetJointPosition',
        index=0,
        joint_positions=target_joint_positions
    )
    env.step()

    for i in range(150):
        env.step()

    env.close()

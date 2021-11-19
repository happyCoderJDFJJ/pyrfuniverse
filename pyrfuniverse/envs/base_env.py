from abc import ABC
from pyrfuniverse.environment import UnityEnvironment
from pyrfuniverse.side_channel.environment_parameters_channel import EnvironmentParametersChannel
from pyrfuniverse.rfuniverse_channel import RigidbodyChannel
from pyrfuniverse.rfuniverse_channel import CameraChannel
from pyrfuniverse.rfuniverse_channel import ArticulationChannel
from pyrfuniverse.rfuniverse_channel import GameObjectChannel
from pyrfuniverse.rfuniverse_channel import ObiClothChannel
from pyrfuniverse.rfuniverse_channel import ObiClothWithGraspingChannel
from pyrfuniverse.rfuniverse_channel import ObiSoftbodyChannel
import gym
import os
import platform
import time


def get_rfuniverse_log_dir():
    platform_name = platform.platform()
    assert 'Linux' in platform_name or 'Windows' in platform_name, \
        'Currently, we only support Linux and Windows.'

    rfuniverse_log_dir = ''
    curr_path = os.getcwd()

    if 'Linux' in platform_name:
        paths = curr_path.split('/')
        assert len(paths) >= 3 and paths[1] == 'home', \
            'Invalid path. Please set your path to /home/USER_NAME/xxx'

        rfuniverse_log_dir = '/home/{}/.rfuniverse'.format(paths[2])
    else:
        rfuniverse_log_dir = os.path.join(curr_path, '.rfuniverse')

    return rfuniverse_log_dir


def select_available_worker_id():
    worker_id_log_dir = get_rfuniverse_log_dir()
    if not os.path.exists(worker_id_log_dir):
        os.makedirs(worker_id_log_dir)
    log_file = os.path.join(worker_id_log_dir, 'worker_id_log')

    worker_id = 1
    worker_id_in_use = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            worker_ids = f.readlines()
            for line in worker_ids:
                worker_id_in_use.append(int(line))
        while worker_id in worker_id_in_use:
            worker_id += 1

    worker_id_in_use.append(worker_id)
    with open(log_file, 'w') as f:
        for id in worker_id_in_use:
            f.write(str(id) + '\n')

    return worker_id


def delete_worker_id(worker_id):
    worker_id_log_dir = get_rfuniverse_log_dir()
    log_file = os.path.join(worker_id_log_dir, 'worker_id_log')

    worker_id_in_use = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            worker_ids = f.readlines()
            for line in worker_ids:
                worker_id_in_use.append(int(line))

    worker_id_in_use.remove(worker_id)
    with open(log_file, 'w') as f:
        for id in worker_id_in_use:
            f.write(str(id) + '\n')


class RFUniverseBaseEnv(ABC):
    """
    This class is the base class for RFUniverse environments. In RFUniverse, every environment will be
    packaged in the Gym-like environment class. For custom environments, users will have to implement
    step(), reset(), seed(), _get_obs().
    """

    def __init__(
        self,
        executable_file: str = None,
        camera_channel_id: str = None,
        rigidbody_channel_id: str = None,
        articulation_channel_id: str = None,
        game_object_channel_id: str = None,
        obi_cloth_channel_id: str=None,
        obi_cloth_with_grasping_channel_id: str=None,
        obi_softbody_channel_id: str=None,
        custom_channels: list = [],
    ):
        # time step
        self.t = 0
        self.worker_id = select_available_worker_id()

        # initialize rfuniverse channels
        self.channels = custom_channels.copy()
        self.camera_channel_id = camera_channel_id
        self.rigidbody_channel_id = rigidbody_channel_id
        self.articulation_channel_id = articulation_channel_id
        self.game_object_channel_id = game_object_channel_id
        self.obi_cloth_channel_id = obi_cloth_channel_id
        self.obi_cloth_with_grasping_channel_id = obi_cloth_with_grasping_channel_id
        self.obi_softbody_channel_id = obi_softbody_channel_id
        self._init_channels()

        # initialize environment
        self.executable_file = executable_file
        self._init_env()

    def _init_env(self):
        if self.executable_file is not None:
            self.env = UnityEnvironment(
                worker_id=self.worker_id,
                file_name=self.executable_file,
                side_channels=self.channels
            )
        else:
            self.env = UnityEnvironment(
                worker_id=0,
                side_channels=self.channels
            )
        self.env.reset()

    def _init_channels(self):
        # Environment parameters channel is compulsory
        self.env_param_channel = EnvironmentParametersChannel()
        self.channels.append(self.env_param_channel)

        if self.camera_channel_id is not None:
            self.camera_channel = CameraChannel(self.camera_channel_id)
            self.channels.append(self.camera_channel)
        else:
            self.camera_channel = None

        if self.rigidbody_channel_id is not None:
            self.rigidbody_channel = RigidbodyChannel(self.rigidbody_channel_id)
            self.channels.append(self.rigidbody_channel)
        else:
            self.rigidbody_channel = None

        if self.articulation_channel_id is not None:
            self.articulation_channel = ArticulationChannel(self.articulation_channel_id)
            self.channels.append(self.articulation_channel)
        else:
            self.articulation_channel = None

        if self.game_object_channel_id is not None:
            self.game_object_channel = GameObjectChannel(self.game_object_channel_id)
            self.channels.append(self.game_object_channel)
        else:
            self.game_object_channel = None

        if self.obi_cloth_channel_id is not None:
            self.obi_cloth_channel = ObiClothChannel(self.obi_cloth_channel_id)
            self.channels.append(self.obi_cloth_channel)
        else:
            self.obi_cloth_channel = None

        if self.obi_cloth_with_grasping_channel_id is not None:
            self.obi_cloth_with_grasping_channel = ObiClothWithGraspingChannel(self.obi_cloth_with_grasping_channel_id)
            self.channels.append(self.obi_cloth_with_grasping_channel)
        else:
            self.obi_cloth_with_grasping_channel= None

        if self.obi_softbody_channel_id is not None:
            self.obi_softbody_channel = ObiSoftbodyChannel(self.obi_softbody_channel_id)
            self.channels.append(self.obi_softbody_channel)
        else:
            self.obi_softbody_channel = None

    def _step(self):
        self.env.step()

    def close(self):
        delete_worker_id(self.worker_id)
        self.env.close()


class RFUniverseGymWrapper(gym.Env, RFUniverseBaseEnv):

    def __init__(
            self,
            executable_file: str = None,
            camera_channel_id: str = None,
            rigidbody_channel_id: str = None,
            articulation_channel_id: str = None,
            game_object_channel_id: str = None,
            obi_cloth_channel_id: str = None,
            obi_cloth_with_grasping_channel_id: str = None,
            obi_softbody_channel_id: str = None,
            custom_channels: list = [],
    ):
        RFUniverseBaseEnv.__init__(
            self,
            executable_file=executable_file,
            camera_channel_id=camera_channel_id,
            rigidbody_channel_id=rigidbody_channel_id,
            articulation_channel_id=articulation_channel_id,
            game_object_channel_id=game_object_channel_id,
            obi_cloth_channel_id=obi_cloth_channel_id,
            obi_cloth_with_grasping_channel_id=obi_cloth_with_grasping_channel_id,
            obi_softbody_channel_id=obi_softbody_channel_id,
            custom_channels=custom_channels
        )

    def close(self):
        RFUniverseBaseEnv.close(self)


class RFUniverseGymGoalWrapper(gym.GoalEnv, RFUniverseBaseEnv):

    def __init__(
            self,
            executable_file: str = None,
            camera_channel_id: str = None,
            rigidbody_channel_id: str = None,
            articulation_channel_id: str = None,
            game_object_channel_id: str = None,
            obi_cloth_channel_id: str = None,
            obi_cloth_with_grasping_channel_id: str = None,
            obi_softbody_channel_id: str=None,
    ):
        RFUniverseBaseEnv.__init__(
            self,
            executable_file=executable_file,
            camera_channel_id=camera_channel_id,
            rigidbody_channel_id=rigidbody_channel_id,
            articulation_channel_id=articulation_channel_id,
            game_object_channel_id=game_object_channel_id,
            obi_cloth_channel_id=obi_cloth_channel_id,
            obi_cloth_with_grasping_channel_id=obi_cloth_with_grasping_channel_id,
            obi_softbody_channel_id=obi_softbody_channel_id,
        )

    def reset(self):
        gym.GoalEnv.reset(self)

    def close(self):
        RFUniverseBaseEnv.close(self)

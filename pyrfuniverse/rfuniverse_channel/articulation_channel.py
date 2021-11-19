from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel
import time


class ArticulationChannel(RFUniverseChannel):

    def __init__(self, channel_id: str) -> None:
        super().__init__(channel_id)
        self.count = 0
        self.data = {}

    def _parse_message(self, msg: IncomingMessage) -> None:
        title = msg.read_string()
        assert title == 'Articulationbody Info', \
            'The information %s is not for articulation body, please check uuid to avoid repeat.' % title
        count = msg.read_int32()
        self.count = count
        for i in range(count):
            id = msg.read_int32()
            this_object_data = {}
            name = msg.read_string()
            if name[-7:] == '(Clone)':
                name = name[:-7]
            this_object_data['name'] = name
            # Position
            raw_positions = msg.read_float32_list()
            this_object_data['positions'] = self._parse_raw_list(raw_positions)
            # Rotation
            raw_rotations = msg.read_float32_list()
            this_object_data['rotations'] = self._parse_raw_list(raw_rotations)
            # Velocity
            raw_velocities = msg.read_float32_list()
            this_object_data['velocities'] = self._parse_raw_list(raw_velocities)
            # Number of joints
            this_object_data['number_of_joints'] = msg.read_int32()
            # Each joint position
            this_object_data['joint_positions'] = msg.read_float32_list()
            # Each joint velocity
            this_object_data['joint_velocities'] = msg.read_float32_list()
            # Whether all parts are stable
            this_object_data['all_stable'] = msg.read_bool()

            self.data[id] = this_object_data

        # self.vis_data(self.data)

    def _parse_raw_list(self, raw_list):
        length = len(raw_list)
        assert length % 3 == 0
        number_of_parts = length // 3
        norm_list = []
        for j in range(number_of_parts):
            transform = [raw_list[3 * j], raw_list[3 * j + 1], raw_list[3 * j + 2]]
            norm_list.append(transform)

        return norm_list

    def LoadArticulationBody(self, kwargs: dict) -> None:
        """
        Args:
            Compulsory:
            filename: The path of an assetbundle file.
            name: The object's name, defined in Unity.

            Optional:
            position: A 3-d list inferring object's position, in [x,y,z] order.
            rotation: A 3-d list inferring object's rotation, in [x,y,z] order.
        """
        compulsory_params = ['filename', 'name']
        optional_params = ['position', 'rotation']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        # msgSign
        msg.write_string('sssffffff')
        # Action name
        msg.write_string('LoadArticulationBody')
        # Action arguments
        msg.write_string(kwargs['filename'])
        msg.write_string(kwargs['name'])

        if 'position' in kwargs.keys():
            msg.write_float32(kwargs['position'][0])
            msg.write_float32(kwargs['position'][1])
            msg.write_float32(kwargs['position'][2])
        else:
            msg.write_float32(0)
            msg.write_float32(0)
            msg.write_float32(0)

        if 'rotation' in kwargs.keys():
            msg.write_float32(kwargs['rotation'][0])
            msg.write_float32(kwargs['rotation'][1])
            msg.write_float32(kwargs['rotation'][2])
        else:
            msg.write_float32(0)
            msg.write_float32(0)
            msg.write_float32(0)

        self.send_message(msg)

    def SetJointPosition(self, kwargs: dict) -> None:
        """Set the target positions for each joint in a specified articulation body.
        Args:
            Compulsory:
            index: The index of articulation body, specified in returned message.
            joint_positions: A list inferring each joint's position in the specified acticulation body.

            Optional:
            speed_scales: A list inferring each joint's speed scale. The length must be the same with joint_positions.
        """
        compulsory_params = ['index', 'joint_positions']
        optional_params = ['speed_scales']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        joint_positions = kwargs['joint_positions']
        num_joints = len(joint_positions)
        msg_sign = 'siill'
        for i in range(num_joints):
            msg_sign += 'f'

        msg.write_string(msg_sign)
        msg.write_string('SetJointPosition')
        msg.write_int32(kwargs['index'])
        msg.write_int32(num_joints)
        msg.write_float32_list(kwargs['joint_positions'])
        if 'speed_scales' in kwargs.keys():
            assert num_joints == len(kwargs['speed_scales']), \
                'The length of joint_positions and speed_scales are not equal.'
            msg.write_float32_list(kwargs['speed_scales'])
        else:
            msg.write_float32_list([1.0 for i in range(num_joints)])

        self.send_message(msg)

    def SetJointPositionDirectly(self, kwargs: dict) -> None:
        """Set the target positions for each joint in a specified articulation body. Note that this function will move
           all joints directrly to its target joint position, and ignoring the physical effects during moving.
        Args:
            Compulsory:
            index: The index of articulation body, specified in returned message.
            joint_positions: A list inferring each joint's position in the specified acticulation body.
        """
        compulsory_params = ['index', 'joint_positions']
        optional_params = []
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        joint_positions = kwargs['joint_positions']
        num_joints = len(joint_positions)
        msg_sign = 'siill'
        for i in range(num_joints):
            msg_sign += 'f'

        msg.write_string(msg_sign)
        msg.write_string('SetJointPositionDirectly')
        msg.write_int32(kwargs['index'])
        msg.write_int32(num_joints)
        msg.write_float32_list(kwargs['joint_positions'])

        self.send_message(msg)

    def Destroy(self, kwargs: dict) -> None:
        compulsory_params = ['index']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('si')
        msg.write_string('Destroy')
        msg.write_int32(kwargs['index'])

        self.send_message(msg)

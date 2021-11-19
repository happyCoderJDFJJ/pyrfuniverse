from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel
import base64
from io import BytesIO
from PIL import Image
from enum import Enum


class RenderingMode(Enum):
    RGB = -1
    MASK = 0
    DEPTH = 2
    NORMALS = 4


class CameraChannel(RFUniverseChannel):

    def __init__(self, channel_id: str) -> None:
        super().__init__(channel_id)
        self.rgbs = []
        self.masks = []
        self.depths = []
        self.counter = 0

    def _parse_message(self, msg: IncomingMessage) -> None:
        self.counter += 1
        title = msg.read_string()
        assert title == 'Camera Info', \
            'The information %s is not for camera, please check uuid to avoid repeat.' % title

        count = msg.read_int32()
        if (msg.read_bool()):
            for i in range(count):
                image = msg.read_string()
                bytes = base64.b64decode(image)
                img = Image.open(BytesIO(bytes))
                # print('Image coming')

    def AddCamera(self, kwargs: dict):
        """Add a camera into scene, with given position and rotation. This camera can use an existing camera as its
        parent transform or don't use parent transform. A camera can render using one of the following 4 modes: rgb,
        mask, depth, normals. The modes are reprensented in RenderingMode.
        Args:
            Compulsory:
            position: A 3-d list inferring camera's position, in [x,y,z] order.
            rotation: A 3-d list inferring camera's rotation, in [x,y,z] order.
            rendering_mode: An element in RenderingMode, inferring this camera's rendering mode.

            Optional:
            parent_camera_idx: The index of parent camera, which is this camera's parent transform.
        """
        compulsory_params = ['position', 'rotation', 'rendering_mode']
        optional_params = ['parent_camera_idx']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        # msgSign
        msg.write_string('sffffffii')
        # Action name
        msg.write_string('AddCamera')
        # Action arguments
        msg.write_float32(kwargs['position'][0])
        msg.write_float32(kwargs['position'][1])
        msg.write_float32(kwargs['position'][2])

        msg.write_float32(kwargs['rotation'][0])
        msg.write_float32(kwargs['rotation'][1])
        msg.write_float32(kwargs['rotation'][2])

        msg.write_int32(kwargs['rendering_mode'].value)
        if 'parent_camera_idx' in kwargs.keys():
            msg.write_int32(kwargs['parent_camera_idx'])
        else:
            msg.write_int32(-1)

        self.send_message(msg)

    def ResetCamera(self, kwargs: dict):
        """Reset an existing camera, specified by index. Camera's position, rotation and rendering mode can be reset.
        Args:
            Compulsory:
            index: The index of camera, specified in returned message.

            Optional:
            position: A 3-d list inferring the camera's new position, in [x,y,z] order.
            rotation: A 3-d list inferring the camera's new rotation, in [x,y,z] order.
            rendering_mode: An element in RenderingMode, inferring the camera's new rendering mode.
        """
        compulsory_params = ['index']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        position = None
        reset_position = False
        rotation = None
        reset_rotation = False
        rendering_mode = None
        reset_rendering_mode = False
        msgSign = 'sibbb'

        if 'position' in kwargs.keys():
            position = kwargs['position']
            msgSign += 'fff'
            reset_position = True
            assert type(position) == list and len(position) == 3, \
                'Argument position must be a 3-d list.'

        if 'rotation' in kwargs.keys():
            rotation = kwargs['rotation']
            msgSign += 'fff'
            reset_rotation = True
            assert type(rotation) == list and len(rotation) == 3, \
                'Argument rotation must be a 3-d list.'

        if 'rendering_mode' in kwargs.keys():
            rendering_mode = kwargs['rendering_mode']
            msgSign += 'i'
            reset_rendering_mode = True
            assert type(rendering_mode) == RenderingMode, \
                'Argument rendering_mode must be RenderingMode'

        msg.write_string(msgSign)
        msg.write_string('ResetCamera')
        msg.write_int32(kwargs['index'])
        msg.write_bool(reset_position)
        msg.write_bool(reset_rotation)
        msg.write_bool(reset_rendering_mode)

        if reset_position:
            msg.write_float32(position[0])
            msg.write_float32(position[1])
            msg.write_float32(position[2])

        if reset_rotation:
            msg.write_float32(rotation[0])
            msg.write_float32(rotation[1])
            msg.write_float32(rotation[2])

        if reset_rendering_mode:
            msg.write_int32(rendering_mode.value)

        self.send_message(msg)

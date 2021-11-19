from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel


class RigidbodyChannel(RFUniverseChannel):

    def __init__(self, channel_id: str) -> None:
        super().__init__(channel_id)
        self.count = 0
        self.data = {}

    def _parse_message(self, msg: IncomingMessage) -> None:
        title = msg.read_string()
        assert title == 'Rigidbody Info', \
            'The information %s is not for rigidbody, please check uuid to avoid repeat.' % title
        count = msg.read_int32()
        self.count = count
        for i in range(count):
            id = msg.read_int32()
            this_object_data = {}
            name = msg.read_string()
            if name[-7:] == '(Clone)':
                name = name[:-7]
            this_object_data['name'] = name
            this_object_data['position'] = [msg.read_float32() for i in range(3)]
            this_object_data['rotation'] = [msg.read_float32() for i in range(3)]
            this_object_data['velocity'] = [msg.read_float32() for i in range(3)]
            this_object_data['angular_vel'] = [msg.read_float32() for i in range(3)]
            self.data[id] = this_object_data

        # print(self.data)

    def LoadRigidbody(self, kwargs: dict):
        """Load a rigidbody object into scene based on assetbundles. Note that the attributes of this object should
           be defined in Unity and complied into assetbundle. A rigid body should have 'rigidbody' component.
        Args:
            Compulsory:
            filename: The path of an assetbundle file.
            name: The object's name, defined in Unity.

            Optional:
            position: A 3-d list inferring object's position, in [x,y,z] order.
            rotation: A 3-d list inferring object's rotation, in [x,y,z] order.
            vhacd: A bool value to decide using VHACD mesh decomposition or not.
        """
        compulsory_params = ['filename', 'name']
        optional_params = ['position', 'rotation', 'vhacd']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        # msgSign
        msg.write_string('sssffffffb')
        # Action name
        msg.write_string('LoadRigidbody')
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

        if 'vhacd' in kwargs.keys():
            msg.write_bool(kwargs['vhacd'])
        else:
            msg.write_bool(False)

        self.send_message(msg)

    def LoadRigidbodyWithName(self, kwargs: dict):
        """Load a rigidbody object into scene based on assetbundles. Note that the attributes of this object should
           be defined in Unity and complied into assetbundle. A rigid body should have 'rigidbody' component.
        Args:
            Compulsory:
            filename: The path of an assetbundle file.
            name: The object's name, defined in Unity.
            replace_name: The object's target name, will replace `name` in Unity

            Optional:
            position: A 3-d list inferring object's position, in [x,y,z] order.
            rotation: A 3-d list inferring object's rotation, in [x,y,z] order.
            vhacd: A bool value to decide using VHACD mesh decomposition or not.
        """
        compulsory_params = ['filename', 'name', 'replace_name']
        optional_params = ['position', 'rotation', 'vhacd']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        # msgSign
        msg.write_string('sssffffffbs')
        # Action name
        msg.write_string('LoadRigidbodyWithName')
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

        if 'vhacd' in kwargs.keys():
            msg.write_bool(kwargs['vhacd'])
        else:
            msg.write_bool(False)

        msg.write_string(kwargs['replace_name'])

        self.send_message(msg)

    def AddForce(self, kwargs: dict):
        """Add a constant force on a rigidbody. The rigidbody must be loaded into the scene and
        is distinguished by index.
        Args:
            Compulsory:
            index: The index of rigidbody, specified in returned message.
            force: A 3-d list inferring the force, in [x,y,z] order.
        """
        compulsory_params = ['index', 'force']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('sifff')
        msg.write_string('AddForce')

        msg.write_int32(kwargs['index'])
        msg.write_float32(kwargs['force'][0])
        msg.write_float32(kwargs['force'][1])
        msg.write_float32(kwargs['force'][2])

        self.send_message(msg)

    def SetTransform(self, kwargs: dict):
        """Set the transform of a rigidbody, specified by index.
        Args:
            Compulsory:
            index: The index of game object.

            Optional:
            position: A 3-d list inferring object's position, in [x,y,z] order.
            rotation: A 3-d list inferring object's rotation, in [x,y,z] order.
        """
        compulsory_params = ['index']
        optional_params = ['position', 'rotation']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        position = None
        set_position = False
        rotation = None
        set_rotation = False
        msg_sign = 'sibb'

        if optional_params[0] in kwargs.keys():  # position
            position = kwargs[optional_params[0]]
            msg_sign += 'fff'
            set_position = True
            assert type(position) == list and len(position) == 3, \
                'Argument position must be a 3-d list.'

        if optional_params[1] in kwargs.keys():  # rotation
            rotation = kwargs[optional_params[1]]
            msg_sign += 'fff'
            set_rotation = True
            assert type(rotation) == list and len(rotation) == 3, \
                'Argument rotation must be a 3-d list.'

        msg.write_string(msg_sign)
        msg.write_string('SetTransform')
        msg.write_int32(kwargs['index'])
        msg.write_bool(set_position)
        msg.write_bool(set_rotation)

        if set_position:
            for i in range(3):
                msg.write_float32(position[i])

        if set_rotation:
            for i in range(3):
                msg.write_float32(rotation[i])

        self.send_message(msg)

    def SetVelocity(self, kwargs: dict):
        """Set the velocity of a rigidbody. The rigidbody must be loaded into the scene and
        is distinguished by index.
        Args:
            Compulsory:
            index: The index of rigidbody, specified in returned message.
            velocity: A 3-d float list inferring the velocity, in [x,y,z] order.
        """
        compulsory_params = ['index', 'velocity']
        optional_params = []
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('sifff')
        msg.write_string('SetVelocity')

        msg.write_int32(kwargs['index'])
        msg.write_float32(kwargs['velocity'][0])
        msg.write_float32(kwargs['velocity'][1])
        msg.write_float32(kwargs['velocity'][2])

        self.send_message(msg)

    def SetAttributes(self, kwargs: dict):
        """
        Mass, mass center, etc.
        """
        pass

    def Destroy(self, kwargs: dict):
        """Destroy a rigidbody inferred by the index
        Args:
            Compulsory:
            index: The index of rigidbody, specified in returned message.
        """
        compulsory_params = ['index']
        optional_params = []
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('si')
        msg.write_string('Destroy')
        msg.write_int32(kwargs['index'])

        self.send_message(msg)

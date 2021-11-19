from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel


class GameObjectChannel(RFUniverseChannel):

    def __init__(self, channel_id: str) -> None:
        super().__init__(channel_id)
        self.count = 0
        self.data = {}

    def _parse_message(self, msg: IncomingMessage) -> None:
        title = msg.read_string()
        assert title == 'GameObject Info', \
            'The information %s is not for game_object, please check uuid to avoid repeat.' % title
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
            this_object_data['quaternion'] = [msg.read_float32() for i in range(4)] # [x,y,z,w] order
            self.data[id] = this_object_data

    def LoadGameObject(self, kwargs: dict) -> None:
        """Load a game object into scene based on assetbundles. Note that the attributes of this object should be
           defined in Unity and compiled into assetbundle. A game object should not contain any physical components
           like 'rigid body' or 'articulation body'.
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
        msg.write_string('sssffffff')
        msg.write_string('LoadGameObject')
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

    def SetTransform(self, kwargs: dict) -> None:
        """Set the transform of a game object, specified by index.
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

        if optional_params[0] in kwargs.keys(): # position
            position = kwargs[optional_params[0]]
            msg_sign += 'fff'
            set_position = True
            assert type(position) == list and len(position) == 3, \
                'Argument position must be a 3-d list.'

        if optional_params[1] in kwargs.keys(): # rotation
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

    def Translate(self, kwargs: dict) -> None:
        """Translate a game object by a given distance, in meter format. Note that this command will translate the
           object relative to the current position.
        Args:
            Compulsory:
            index: The index of object, specified in returned message.
            translation: A 3-d list inferring the relative translation, in [x,y,z] order.
        """
        compulsory_params = ['index', 'translation']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('sifff')
        msg.write_string('Translate')
        msg.write_int32(kwargs['index'])
        for i in range(3):
            msg.write_float32(kwargs['translation'][i])

        self.send_message(msg)

    def Rotate(self, kwargs: dict) -> None:
        """Rotate a game object by a given rotation, in euler angle format. Note that this command will rotate the
           object relative to the current state. The rotation order will be z axis first, x axis next, and z axis last.
        Args:
            Compulsory:
            index: The index of object, specified in returned message.
            rotation: A 3-d list inferring the relative rotation, in [x,y,z] order.
        """
        compulsory_params = ['index', 'rotation']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('sifff')
        msg.write_string('Rotate')
        msg.write_int32(kwargs['index'])
        for i in range(3):
            msg.write_float32(kwargs['rotation'][i])

        self.send_message(msg)

    def Destroy(self, kwargs: dict):
        """Destroy an object in the scene. The object is specified by an index.
        Args:
            Compulsory:
            index: The index of the game object waiting to be destroied.
        """
        compulsory_params = ['index']
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('si')
        msg.write_string('Destroy')
        msg.write_int32(kwargs['index'])

        self.send_message(msg)

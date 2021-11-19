from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel


class ObiClothChannel(RFUniverseChannel):

    def __init__(self, channel_id: str) -> None:
        super().__init__(channel_id)
        self.count = 0
        self.data = {}

    def _parse_message(self, msg: IncomingMessage) -> None:
        title = msg.read_string()
        assert title == 'ObiCloth Info', \
            'The information %s is not for obi cloth, please check uuid to avoid repeat.' % title
        count = msg.read_int32()
        self.count = count
        for i in range(count):
            id = msg.read_int32()
            this_object_data = {}
            name = msg.read_string()
            if name[-7:] == '(Clone)':
                name = name[:-7]
            this_object_data['name'] = name
            # Number of particles
            number_of_particles = msg.read_int32()
            this_object_data['number_of_particles'] = number_of_particles
            # Positions
            raw_positions = msg.read_float32_list()
            this_object_data['positions'] = self._parse_raw_list(raw_positions)

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

    def LoadObiCloth(self, kwargs: dict) -> None:
        """Load an obi cloth into the scene based on assetbundles. Actually, what we load is an obi solver
           in current stage, because there's only one obi cloth, so this doesn't matter. We will further fix
           this in the future.
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
        msg.write_string('LoadObiCloth')
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

    def Destroy(self, kwargs: dict):
        """Destroy an obi cloth inferred by the index
        Args:
            Compulsory:
            index: The index of obi cloth, specified in returned message.
        """
        compulsory_params = ['index']
        optional_params = []
        super()._check_kwargs(kwargs, compulsory_params)

        msg = OutgoingMessage()
        msg.write_string('si')
        msg.write_string('Destroy')
        msg.write_int32(kwargs['index'])

        self.send_message(msg)

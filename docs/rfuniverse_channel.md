# pyrfuniverse.rfuniverse_channel

`pyrfuniverse.rfuniverse_channel` is the communicator between Unity environment and python end. Each channel will only be
declared once in an environment, and it will be responsible for managing only one kind of objects. For example, class 
`RigidbodyChannel` will only manage rigid bodies. We provide the following channels to interact with different kinds of 
objects.

## pyrfuniverse.rfuniverse_channel.RFUniverseChannel

This is the base class of all channels in `pyrfuniverse`. It inherits from `pyrfuniverse.side_channel`, thus uses a 
`uuid` to represent uniqueness. 



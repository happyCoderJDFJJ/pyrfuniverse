# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pyrfuniverse/communicator_objects/header.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pyrfuniverse/communicator_objects/header.proto',
  package='communicator_objects',
  syntax='proto3',
  serialized_pb=_b('\n.pyrfuniverse/communicator_objects/header.proto\x12\x14\x63ommunicator_objects\".\n\x0bHeaderProto\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\tB+\xaa\x02(Robotflow.RFUniverse.CommunicatorObjectsb\x06proto3')
)




_HEADERPROTO = _descriptor.Descriptor(
  name='HeaderProto',
  full_name='communicator_objects.HeaderProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='communicator_objects.HeaderProto.status', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='communicator_objects.HeaderProto.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=118,
)

DESCRIPTOR.message_types_by_name['HeaderProto'] = _HEADERPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HeaderProto = _reflection.GeneratedProtocolMessageType('HeaderProto', (_message.Message,), dict(
  DESCRIPTOR = _HEADERPROTO,
  __module__ = 'pyrfuniverse.communicator_objects.header_pb2'
  # @@protoc_insertion_point(class_scope:communicator_objects.HeaderProto)
  ))
_sym_db.RegisterMessage(HeaderProto)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002(Robotflow.RFUniverse.CommunicatorObjects'))
# @@protoc_insertion_point(module_scope)

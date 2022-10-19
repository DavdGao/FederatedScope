# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gRPC_comm_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17gRPC_comm_manager.proto\x12\x06\x66scomm\"|\n\x0eMessageRequest\x12,\n\x03msg\x18\x01 \x03(\x0b\x32\x1f.fscomm.MessageRequest.MsgEntry\x1a<\n\x08MsgEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.fscomm.MsgValue:\x02\x38\x01\"\xc8\x01\n\x08MsgValue\x12%\n\nsingle_msg\x18\x01 \x01(\x0b\x32\x0f.fscomm.mSingleH\x00\x12!\n\x08list_msg\x18\x02 \x01(\x0b\x32\r.fscomm.mListH\x00\x12\x37\n\x12\x64ict_msg_stringkey\x18\x03 \x01(\x0b\x32\x19.fscomm.mDict_keyIsStringH\x00\x12\x31\n\x0f\x64ict_msg_intkey\x18\x04 \x01(\x0b\x32\x16.fscomm.mDict_keyIsIntH\x00\x42\x06\n\x04type\"R\n\x07mSingle\x12\x15\n\x0b\x66loat_value\x18\x01 \x01(\x02H\x00\x12\x13\n\tint_value\x18\x02 \x01(\x05H\x00\x12\x13\n\tstr_value\x18\x03 \x01(\tH\x00\x42\x06\n\x04type\"-\n\x05mList\x12$\n\nlist_value\x18\x01 \x03(\x0b\x32\x10.fscomm.MsgValue\"\x95\x01\n\x11mDict_keyIsString\x12<\n\ndict_value\x18\x01 \x03(\x0b\x32(.fscomm.mDict_keyIsString.DictValueEntry\x1a\x42\n\x0e\x44ictValueEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.fscomm.MsgValue:\x02\x38\x01\"\x8f\x01\n\x0emDict_keyIsInt\x12\x39\n\ndict_value\x18\x01 \x03(\x0b\x32%.fscomm.mDict_keyIsInt.DictValueEntry\x1a\x42\n\x0e\x44ictValueEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.fscomm.MsgValue:\x02\x38\x01\"\x1e\n\x0fMessageResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t2T\n\x10gRPCComServeFunc\x12@\n\x0bsendMessage\x12\x16.fscomm.MessageRequest\x1a\x17.fscomm.MessageResponse\"\x00\x62\x06proto3')



_MESSAGEREQUEST = DESCRIPTOR.message_types_by_name['MessageRequest']
_MESSAGEREQUEST_MSGENTRY = _MESSAGEREQUEST.nested_types_by_name['MsgEntry']
_MSGVALUE = DESCRIPTOR.message_types_by_name['MsgValue']
_MSINGLE = DESCRIPTOR.message_types_by_name['mSingle']
_MLIST = DESCRIPTOR.message_types_by_name['mList']
_MDICT_KEYISSTRING = DESCRIPTOR.message_types_by_name['mDict_keyIsString']
_MDICT_KEYISSTRING_DICTVALUEENTRY = _MDICT_KEYISSTRING.nested_types_by_name['DictValueEntry']
_MDICT_KEYISINT = DESCRIPTOR.message_types_by_name['mDict_keyIsInt']
_MDICT_KEYISINT_DICTVALUEENTRY = _MDICT_KEYISINT.nested_types_by_name['DictValueEntry']
_MESSAGERESPONSE = DESCRIPTOR.message_types_by_name['MessageResponse']
MessageRequest = _reflection.GeneratedProtocolMessageType('MessageRequest', (_message.Message,), {

  'MsgEntry' : _reflection.GeneratedProtocolMessageType('MsgEntry', (_message.Message,), {
    'DESCRIPTOR' : _MESSAGEREQUEST_MSGENTRY,
    '__module__' : 'gRPC_comm_manager_pb2'
    # @@protoc_insertion_point(class_scope:fscomm.MessageRequest.MsgEntry)
    })
  ,
  'DESCRIPTOR' : _MESSAGEREQUEST,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.MessageRequest)
  })
_sym_db.RegisterMessage(MessageRequest)
_sym_db.RegisterMessage(MessageRequest.MsgEntry)

MsgValue = _reflection.GeneratedProtocolMessageType('MsgValue', (_message.Message,), {
  'DESCRIPTOR' : _MSGVALUE,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.MsgValue)
  })
_sym_db.RegisterMessage(MsgValue)

mSingle = _reflection.GeneratedProtocolMessageType('mSingle', (_message.Message,), {
  'DESCRIPTOR' : _MSINGLE,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.mSingle)
  })
_sym_db.RegisterMessage(mSingle)

mList = _reflection.GeneratedProtocolMessageType('mList', (_message.Message,), {
  'DESCRIPTOR' : _MLIST,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.mList)
  })
_sym_db.RegisterMessage(mList)

mDict_keyIsString = _reflection.GeneratedProtocolMessageType('mDict_keyIsString', (_message.Message,), {

  'DictValueEntry' : _reflection.GeneratedProtocolMessageType('DictValueEntry', (_message.Message,), {
    'DESCRIPTOR' : _MDICT_KEYISSTRING_DICTVALUEENTRY,
    '__module__' : 'gRPC_comm_manager_pb2'
    # @@protoc_insertion_point(class_scope:fscomm.mDict_keyIsString.DictValueEntry)
    })
  ,
  'DESCRIPTOR' : _MDICT_KEYISSTRING,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.mDict_keyIsString)
  })
_sym_db.RegisterMessage(mDict_keyIsString)
_sym_db.RegisterMessage(mDict_keyIsString.DictValueEntry)

mDict_keyIsInt = _reflection.GeneratedProtocolMessageType('mDict_keyIsInt', (_message.Message,), {

  'DictValueEntry' : _reflection.GeneratedProtocolMessageType('DictValueEntry', (_message.Message,), {
    'DESCRIPTOR' : _MDICT_KEYISINT_DICTVALUEENTRY,
    '__module__' : 'gRPC_comm_manager_pb2'
    # @@protoc_insertion_point(class_scope:fscomm.mDict_keyIsInt.DictValueEntry)
    })
  ,
  'DESCRIPTOR' : _MDICT_KEYISINT,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.mDict_keyIsInt)
  })
_sym_db.RegisterMessage(mDict_keyIsInt)
_sym_db.RegisterMessage(mDict_keyIsInt.DictValueEntry)

MessageResponse = _reflection.GeneratedProtocolMessageType('MessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGERESPONSE,
  '__module__' : 'gRPC_comm_manager_pb2'
  # @@protoc_insertion_point(class_scope:fscomm.MessageResponse)
  })
_sym_db.RegisterMessage(MessageResponse)

_GRPCCOMSERVEFUNC = DESCRIPTOR.services_by_name['gRPCComServeFunc']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGEREQUEST_MSGENTRY._options = None
  _MESSAGEREQUEST_MSGENTRY._serialized_options = b'8\001'
  _MDICT_KEYISSTRING_DICTVALUEENTRY._options = None
  _MDICT_KEYISSTRING_DICTVALUEENTRY._serialized_options = b'8\001'
  _MDICT_KEYISINT_DICTVALUEENTRY._options = None
  _MDICT_KEYISINT_DICTVALUEENTRY._serialized_options = b'8\001'
  _MESSAGEREQUEST._serialized_start=35
  _MESSAGEREQUEST._serialized_end=159
  _MESSAGEREQUEST_MSGENTRY._serialized_start=99
  _MESSAGEREQUEST_MSGENTRY._serialized_end=159
  _MSGVALUE._serialized_start=162
  _MSGVALUE._serialized_end=362
  _MSINGLE._serialized_start=364
  _MSINGLE._serialized_end=446
  _MLIST._serialized_start=448
  _MLIST._serialized_end=493
  _MDICT_KEYISSTRING._serialized_start=496
  _MDICT_KEYISSTRING._serialized_end=645
  _MDICT_KEYISSTRING_DICTVALUEENTRY._serialized_start=579
  _MDICT_KEYISSTRING_DICTVALUEENTRY._serialized_end=645
  _MDICT_KEYISINT._serialized_start=648
  _MDICT_KEYISINT._serialized_end=791
  _MDICT_KEYISINT_DICTVALUEENTRY._serialized_start=725
  _MDICT_KEYISINT_DICTVALUEENTRY._serialized_end=791
  _MESSAGERESPONSE._serialized_start=793
  _MESSAGERESPONSE._serialized_end=823
  _GRPCCOMSERVEFUNC._serialized_start=825
  _GRPCCOMSERVEFUNC._serialized_end=909
# @@protoc_insertion_point(module_scope)

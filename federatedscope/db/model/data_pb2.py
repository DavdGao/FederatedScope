# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ndata.proto\"6\n\x04\x43\x65ll\x12\x0b\n\x01i\x18\x01 \x01(\x03H\x00\x12\x0b\n\x01\x66\x18\x02 \x01(\x01H\x00\x12\x0b\n\x01s\x18\x03 \x01(\tH\x00\x42\x07\n\x05value\"\x1a\n\x03Row\x12\x13\n\x04\x63\x65ll\x18\x01 \x03(\x0b\x32\x05.Cell\"\x19\n\x04Rows\x12\x11\n\x03row\x18\x01 \x03(\x0b\x32\x04.Row\"\x8f\x01\n\tAttribute\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x17\n\x04type\x18\x02 \x01(\x0e\x32\t.DataType\x12\x11\n\thas_range\x18\x03 \x01(\x08\x12\x18\n\tmin_value\x18\x04 \x01(\x0b\x32\x05.Cell\x12\x18\n\tmax_value\x18\x05 \x01(\x0b\x32\x05.Cell\x12\x14\n\x05\x64\x65lta\x18\x06 \x01(\x0b\x32\x05.Cell\"\'\n\x06Schema\x12\x1d\n\tattribute\x18\x01 \x03(\x0b\x32\n.Attribute\"4\n\x04\x44\x61ta\x12\x17\n\x06schema\x18\x01 \x01(\x0b\x32\x07.Schema\x12\x13\n\x04rows\x18\x02 \x01(\x0b\x32\x05.Rows\"*\n\x05Table\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x05.Data**\n\x08\x44\x61taType\x12\x07\n\x03INT\x10\x00\x12\t\n\x05\x46LOAT\x10\x01\x12\n\n\x06STRING\x10\x02\x62\x06proto3')
)

_DATATYPE = _descriptor.EnumDescriptor(
  name='DataType',
  full_name='DataType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FLOAT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRING', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=410,
  serialized_end=452,
)
_sym_db.RegisterEnumDescriptor(_DATATYPE)

DataType = enum_type_wrapper.EnumTypeWrapper(_DATATYPE)
INT = 0
FLOAT = 1
STRING = 2



_CELL = _descriptor.Descriptor(
  name='Cell',
  full_name='Cell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='i', full_name='Cell.i', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='f', full_name='Cell.f', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s', full_name='Cell.s', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='Cell.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=14,
  serialized_end=68,
)


_ROW = _descriptor.Descriptor(
  name='Row',
  full_name='Row',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cell', full_name='Row.cell', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=96,
)


_ROWS = _descriptor.Descriptor(
  name='Rows',
  full_name='Rows',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='row', full_name='Rows.row', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=123,
)


_ATTRIBUTE = _descriptor.Descriptor(
  name='Attribute',
  full_name='Attribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Attribute.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='Attribute.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_range', full_name='Attribute.has_range', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_value', full_name='Attribute.min_value', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_value', full_name='Attribute.max_value', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delta', full_name='Attribute.delta', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=126,
  serialized_end=269,
)


_SCHEMA = _descriptor.Descriptor(
  name='Schema',
  full_name='Schema',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='attribute', full_name='Schema.attribute', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=271,
  serialized_end=310,
)


_DATA = _descriptor.Descriptor(
  name='Data',
  full_name='Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='schema', full_name='Data.schema', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rows', full_name='Data.rows', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=312,
  serialized_end=364,
)


_TABLE = _descriptor.Descriptor(
  name='Table',
  full_name='Table',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Table.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Table.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=366,
  serialized_end=408,
)

_CELL.oneofs_by_name['value'].fields.append(
  _CELL.fields_by_name['i'])
_CELL.fields_by_name['i'].containing_oneof = _CELL.oneofs_by_name['value']
_CELL.oneofs_by_name['value'].fields.append(
  _CELL.fields_by_name['f'])
_CELL.fields_by_name['f'].containing_oneof = _CELL.oneofs_by_name['value']
_CELL.oneofs_by_name['value'].fields.append(
  _CELL.fields_by_name['s'])
_CELL.fields_by_name['s'].containing_oneof = _CELL.oneofs_by_name['value']
_ROW.fields_by_name['cell'].message_type = _CELL
_ROWS.fields_by_name['row'].message_type = _ROW
_ATTRIBUTE.fields_by_name['type'].enum_type = _DATATYPE
_ATTRIBUTE.fields_by_name['min_value'].message_type = _CELL
_ATTRIBUTE.fields_by_name['max_value'].message_type = _CELL
_ATTRIBUTE.fields_by_name['delta'].message_type = _CELL
_SCHEMA.fields_by_name['attribute'].message_type = _ATTRIBUTE
_DATA.fields_by_name['schema'].message_type = _SCHEMA
_DATA.fields_by_name['rows'].message_type = _ROWS
_TABLE.fields_by_name['data'].message_type = _DATA
DESCRIPTOR.message_types_by_name['Cell'] = _CELL
DESCRIPTOR.message_types_by_name['Row'] = _ROW
DESCRIPTOR.message_types_by_name['Rows'] = _ROWS
DESCRIPTOR.message_types_by_name['Attribute'] = _ATTRIBUTE
DESCRIPTOR.message_types_by_name['Schema'] = _SCHEMA
DESCRIPTOR.message_types_by_name['Data'] = _DATA
DESCRIPTOR.message_types_by_name['Table'] = _TABLE
DESCRIPTOR.enum_types_by_name['DataType'] = _DATATYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cell = _reflection.GeneratedProtocolMessageType('Cell', (_message.Message,), dict(
  DESCRIPTOR = _CELL,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Cell)
  ))
_sym_db.RegisterMessage(Cell)

Row = _reflection.GeneratedProtocolMessageType('Row', (_message.Message,), dict(
  DESCRIPTOR = _ROW,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Row)
  ))
_sym_db.RegisterMessage(Row)

Rows = _reflection.GeneratedProtocolMessageType('Rows', (_message.Message,), dict(
  DESCRIPTOR = _ROWS,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Rows)
  ))
_sym_db.RegisterMessage(Rows)

Attribute = _reflection.GeneratedProtocolMessageType('Attribute', (_message.Message,), dict(
  DESCRIPTOR = _ATTRIBUTE,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Attribute)
  ))
_sym_db.RegisterMessage(Attribute)

Schema = _reflection.GeneratedProtocolMessageType('Schema', (_message.Message,), dict(
  DESCRIPTOR = _SCHEMA,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Schema)
  ))
_sym_db.RegisterMessage(Schema)

Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), dict(
  DESCRIPTOR = _DATA,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Data)
  ))
_sym_db.RegisterMessage(Data)

Table = _reflection.GeneratedProtocolMessageType('Table', (_message.Message,), dict(
  DESCRIPTOR = _TABLE,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:Table)
  ))
_sym_db.RegisterMessage(Table)


# @@protoc_insertion_point(module_scope)

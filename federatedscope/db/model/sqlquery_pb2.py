# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sqlquery.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (
    lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

import federatedscope.db.model.data_pb2 as data__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name='sqlquery.proto',
    package='',
    syntax='proto3',
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0esqlquery.proto\x1a\naccessor.proto\"\x91\x01\n\nExpression\x12\x1b\n\x08operator\x18\x01 \x01(\x0e\x32\t.Operator\x12\x1d\n\x08\x63hildren\x18\x02 \x03(\x0b\x32\x0b.Expression\x12\x17\n\x04type\x18\x03 \x01(\x0e\x32\t.DataType\x12\x0b\n\x01i\x18\n \x01(\x03H\x00\x12\x0b\n\x01\x66\x18\x0b \x01(\x02H\x00\x12\x0b\n\x01s\x18\x0c \x01(\tH\x00\x42\x07\n\x05value\"\xa4\x01\n\rBasicSchedule\x12\x1f\n\nexp_select\x18\x01 \x03(\x0b\x32\x0b.Expression\x12\x12\n\ntable_name\x18\x02 \x01(\t\x12\x1e\n\texp_where\x18\x03 \x03(\x0b\x32\x0b.Expression\x12\x1c\n\x07\x65xp_agg\x18\x04 \x03(\x0b\x32\x0b.Expression\x12 \n\x08\x63hildren\x18\x05 \x03(\x0b\x32\x0e.BasicSchedule*a\n\x08Operator\x12\x07\n\x03REF\x10\x00\x12\x07\n\x03LIT\x10\x01\x12\x06\n\x02GE\x10\n\x12\x06\n\x02GT\x10\x0b\x12\x06\n\x02LE\x10\x0c\x12\x06\n\x02LT\x10\r\x12\x06\n\x02\x45Q\x10\x0e\x12\t\n\x05\x43OUNT\x10\x64\x12\x07\n\x03SUM\x10\x65\x12\x07\n\x03\x41VG\x10\x66\x62\x06proto3'
    ),
    dependencies=[
        data__pb2.DESCRIPTOR,
    ])

_OPERATOR = _descriptor.EnumDescriptor(
    name='Operator',
    full_name='Operator',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name='REF',
                                        index=0,
                                        number=0,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='LIT',
                                        index=1,
                                        number=1,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='GE',
                                        index=2,
                                        number=10,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='GT',
                                        index=3,
                                        number=11,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='LE',
                                        index=4,
                                        number=12,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='LT',
                                        index=5,
                                        number=13,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='EQ',
                                        index=6,
                                        number=14,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='COUNT',
                                        index=7,
                                        number=100,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='SUM',
                                        index=8,
                                        number=101,
                                        serialized_options=None,
                                        type=None),
        _descriptor.EnumValueDescriptor(name='AVG',
                                        index=9,
                                        number=102,
                                        serialized_options=None,
                                        type=None),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=345,
    serialized_end=442,
)
_sym_db.RegisterEnumDescriptor(_OPERATOR)

Operator = enum_type_wrapper.EnumTypeWrapper(_OPERATOR)
REF = 0
LIT = 1
GE = 10
GT = 11
LE = 12
LT = 13
EQ = 14
COUNT = 100
SUM = 101
AVG = 102

_EXPRESSION = _descriptor.Descriptor(
    name='Expression',
    full_name='Expression',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(name='operator',
                                    full_name='Expression.operator',
                                    index=0,
                                    number=1,
                                    type=14,
                                    cpp_type=8,
                                    label=1,
                                    has_default_value=False,
                                    default_value=0,
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='children',
                                    full_name='Expression.children',
                                    index=1,
                                    number=2,
                                    type=11,
                                    cpp_type=10,
                                    label=3,
                                    has_default_value=False,
                                    default_value=[],
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='type',
                                    full_name='Expression.type',
                                    index=2,
                                    number=3,
                                    type=14,
                                    cpp_type=8,
                                    label=1,
                                    has_default_value=False,
                                    default_value=0,
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='i',
                                    full_name='Expression.i',
                                    index=3,
                                    number=10,
                                    type=3,
                                    cpp_type=2,
                                    label=1,
                                    has_default_value=False,
                                    default_value=0,
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='f',
                                    full_name='Expression.f',
                                    index=4,
                                    number=11,
                                    type=2,
                                    cpp_type=6,
                                    label=1,
                                    has_default_value=False,
                                    default_value=float(0),
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='s',
                                    full_name='Expression.s',
                                    index=5,
                                    number=12,
                                    type=9,
                                    cpp_type=9,
                                    label=1,
                                    has_default_value=False,
                                    default_value=_b("").decode('utf-8'),
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(name='value',
                                    full_name='Expression.value',
                                    index=0,
                                    containing_type=None,
                                    fields=[]),
    ],
    serialized_start=31,
    serialized_end=176,
)

_BASICSCHEDULE = _descriptor.Descriptor(
    name='BasicSchedule',
    full_name='BasicSchedule',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(name='exp_select',
                                    full_name='BasicSchedule.exp_select',
                                    index=0,
                                    number=1,
                                    type=11,
                                    cpp_type=10,
                                    label=3,
                                    has_default_value=False,
                                    default_value=[],
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='table_name',
                                    full_name='BasicSchedule.table_name',
                                    index=1,
                                    number=2,
                                    type=9,
                                    cpp_type=9,
                                    label=1,
                                    has_default_value=False,
                                    default_value=_b("").decode('utf-8'),
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='exp_where',
                                    full_name='BasicSchedule.exp_where',
                                    index=2,
                                    number=3,
                                    type=11,
                                    cpp_type=10,
                                    label=3,
                                    has_default_value=False,
                                    default_value=[],
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='exp_agg',
                                    full_name='BasicSchedule.exp_agg',
                                    index=3,
                                    number=4,
                                    type=11,
                                    cpp_type=10,
                                    label=3,
                                    has_default_value=False,
                                    default_value=[],
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
        _descriptor.FieldDescriptor(name='children',
                                    full_name='BasicSchedule.children',
                                    index=4,
                                    number=5,
                                    type=11,
                                    cpp_type=10,
                                    label=3,
                                    has_default_value=False,
                                    default_value=[],
                                    message_type=None,
                                    enum_type=None,
                                    containing_type=None,
                                    is_extension=False,
                                    extension_scope=None,
                                    serialized_options=None,
                                    file=DESCRIPTOR),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=179,
    serialized_end=343,
)

_EXPRESSION.fields_by_name['operator'].enum_type = _OPERATOR
_EXPRESSION.fields_by_name['children'].message_type = _EXPRESSION
_EXPRESSION.fields_by_name['type'].enum_type = data__pb2._DATATYPE
_EXPRESSION.oneofs_by_name['value'].fields.append(
    _EXPRESSION.fields_by_name['i'])
_EXPRESSION.fields_by_name['i'].containing_oneof = _EXPRESSION.oneofs_by_name[
    'value']
_EXPRESSION.oneofs_by_name['value'].fields.append(
    _EXPRESSION.fields_by_name['f'])
_EXPRESSION.fields_by_name['f'].containing_oneof = _EXPRESSION.oneofs_by_name[
    'value']
_EXPRESSION.oneofs_by_name['value'].fields.append(
    _EXPRESSION.fields_by_name['s'])
_EXPRESSION.fields_by_name['s'].containing_oneof = _EXPRESSION.oneofs_by_name[
    'value']
_BASICSCHEDULE.fields_by_name['exp_select'].message_type = _EXPRESSION
_BASICSCHEDULE.fields_by_name['exp_where'].message_type = _EXPRESSION
_BASICSCHEDULE.fields_by_name['exp_agg'].message_type = _EXPRESSION
_BASICSCHEDULE.fields_by_name['children'].message_type = _BASICSCHEDULE
DESCRIPTOR.message_types_by_name['Expression'] = _EXPRESSION
DESCRIPTOR.message_types_by_name['BasicSchedule'] = _BASICSCHEDULE
DESCRIPTOR.enum_types_by_name['Operator'] = _OPERATOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Expression = _reflection.GeneratedProtocolMessageType(
    'Expression',
    (_message.Message, ),
    dict(DESCRIPTOR=_EXPRESSION,
         __module__='sqlquery_pb2'
         # @@protoc_insertion_point(class_scope:Expression)
         ))
_sym_db.RegisterMessage(Expression)

BasicSchedule = _reflection.GeneratedProtocolMessageType(
    'BasicSchedule',
    (_message.Message, ),
    dict(DESCRIPTOR=_BASICSCHEDULE,
         __module__='sqlquery_pb2'
         # @@protoc_insertion_point(class_scope:BasicSchedule)
         ))
_sym_db.RegisterMessage(BasicSchedule)

# @@protoc_insertion_point(module_scope)

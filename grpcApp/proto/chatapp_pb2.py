# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chatapp.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatapp.proto\x12\x07\x63hatapp\"3\n\x07\x41\x63\x63ount\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x03 \x01(\x08\"\x1b\n\x0b\x41\x63\x63ountName\x12\x0c\n\x04name\x18\x01 \x01(\t\"<\n\tAccountID\x12\n\n\x02id\x18\x01 \x01(\x05\x12#\n\x05reply\x18\x02 \x01(\x0b\x32\x14.chatapp.ServerReply\"\x1e\n\x0bServerReply\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"%\n\x04\x43hat\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1e\n\x0c\x46ilterString\x12\x0e\n\x06\x66ilter\x18\x01 \x01(\t2\x98\x03\n\x07\x43hatApp\x12;\n\rcreateAccount\x12\x14.chatapp.AccountName\x1a\x12.chatapp.AccountID\"\x00\x12\x33\n\x05logIn\x12\x12.chatapp.AccountID\x1a\x14.chatapp.ServerReply\"\x00\x12\x36\n\x0clistAccounts\x12\x0e.chatapp.Empty\x1a\x14.chatapp.ServerReply\"\x00\x12?\n\x0e\x66ilterAccounts\x12\x15.chatapp.FilterString\x1a\x14.chatapp.ServerReply\"\x00\x12\x34\n\x06logOut\x12\x12.chatapp.AccountID\x1a\x14.chatapp.ServerReply\"\x00\x12\x34\n\x0bsendMessage\x12\r.chatapp.Chat\x1a\x14.chatapp.ServerReply\"\x00\x12\x36\n\x11listenForMessages\x12\x0e.chatapp.Empty\x1a\r.chatapp.Chat\"\x00\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatapp_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACCOUNT._serialized_start=26
  _ACCOUNT._serialized_end=77
  _ACCOUNTNAME._serialized_start=79
  _ACCOUNTNAME._serialized_end=106
  _ACCOUNTID._serialized_start=108
  _ACCOUNTID._serialized_end=168
  _SERVERREPLY._serialized_start=170
  _SERVERREPLY._serialized_end=200
  _EMPTY._serialized_start=202
  _EMPTY._serialized_end=209
  _CHAT._serialized_start=211
  _CHAT._serialized_end=248
  _FILTERSTRING._serialized_start=250
  _FILTERSTRING._serialized_end=280
  _CHATAPP._serialized_start=283
  _CHATAPP._serialized_end=691
# @@protoc_insertion_point(module_scope)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class AccountID(_message.Message):
    __slots__ = ["id", "reply"]
    ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    id: int
    reply: ServerReply
    def __init__(self, id: _Optional[int] = ..., reply: _Optional[_Union[ServerReply, _Mapping]] = ...) -> None: ...

class AccountName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class FilterString(_message.Message):
    __slots__ = ["filter"]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: str
    def __init__(self, filter: _Optional[str] = ...) -> None: ...

class LoginReply(_message.Message):
    __slots__ = ["message", "success", "username"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    message: str
    success: bool
    username: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["message", "recipientID", "senderID", "senderName"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTID_FIELD_NUMBER: _ClassVar[int]
    SENDERID_FIELD_NUMBER: _ClassVar[int]
    SENDERNAME_FIELD_NUMBER: _ClassVar[int]
    message: str
    recipientID: int
    senderID: int
    senderName: str
    def __init__(self, senderID: _Optional[int] = ..., senderName: _Optional[str] = ..., message: _Optional[str] = ..., recipientID: _Optional[int] = ...) -> None: ...

class ServerReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

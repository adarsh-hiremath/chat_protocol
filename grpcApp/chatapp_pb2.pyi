from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ["username"]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

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
    __slots__ = ["message", "recipientName", "senderName"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTNAME_FIELD_NUMBER: _ClassVar[int]
    SENDERNAME_FIELD_NUMBER: _ClassVar[int]
    message: str
    recipientName: str
    senderName: str
    def __init__(self, senderName: _Optional[str] = ..., message: _Optional[str] = ..., recipientName: _Optional[str] = ...) -> None: ...

class ServerReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

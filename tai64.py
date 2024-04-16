"""TAI64, TAI64N, TAI64NA implementations for Python.
"""
from __future__ import annotations

import binascii
import struct

try:
    from typing import Self  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import Self

EPOCH = 2**62  # 1970-01-01 00:00:00 TAI
MIN = 0
MAX = 2**63 - 1
UNIX_EPOCH = EPOCH + 10  # 1970-01-01 00:00:10 TAI <-> 1970-01-01 00:00:00 UTC

class tai:
    __slots__ = ('_sec')
    _struct = struct.Struct('>Q')
    _sec: int

    def __new__(cls, sec:int):
        sec = int(sec)
        if not MIN <= sec <= MAX:
            raise ValueError(f'sec must be in 0..2**63-1', sec)
        self = object.__new__(cls)
        self._sec = sec
        return self

    @classmethod
    def from_hex(cls, s:str|bytes|bytearray|memoryview) -> Self:
        buf = binascii.a2b_hex(s[0:cls._struct.size*2])
        return cls.unpack(buf)

    @classmethod
    def unpack(cls, buf:bytes|bytearray|memoryview) -> Self:
        sec, = cls._struct.unpack(buf)
        return cls(sec)

    @property
    def sec(self) -> int:
        return self._sec

    def hex(self) -> str:
        return self.pack().hex()

    def pack(self) -> bytes:
        return self._struct.pack(self.sec)

    def __eq__(self, other):
        if isinstance(other, tai): return self.sec == other.sec
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, tai): return self.sec <= other.sec
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, tai): return self.sec < other.sec
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, tai): return self.sec >= other.sec
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, tai): return self.sec > other.sec
        return NotImplemented

    def __float__(self):
        return float(self.sec)

    def __int__(self):
        return self.sec

    def __hash__(self):
        # TODO Should hash(tai(...)) == hash(taia(..., 0, 0))?
        return hash((self.__class__, self.sec))

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}({self.sec})'


class tain:
    __slots__ = ('_sec', '_nano')
    _struct = struct.Struct('>QL')
    _sec: int
    _nano: int

    def __new__(cls, sec:int, nano:int):
        sec = int(sec)
        nano = int(nano)
        if not MIN <= sec <= MAX:
            raise ValueError(f'sec must be in 0..2**63-1', sec)
        if not 0 <= nano < 10**9:
            raise ValueError(f'nano must be in 0..999_999_999', nano)
        self = object.__new__(cls)
        self._sec = sec
        self._nano = nano
        return self

    @classmethod
    def from_hex(cls, s:str|bytes|bytearray|memoryview) -> Self:
        buf = binascii.a2b_hex(s[0:cls._struct.size*2])
        return cls.unpack(buf)

    @classmethod
    def from_tai(cls, t:tai) -> Self:
        return cls(t.sec, 0)

    @classmethod
    def unpack(cls, buf:bytes|bytearray|memoryview) -> Self:
        sec, nano = cls._struct.unpack(buf)
        return cls(sec, nano)

    @property
    def sec(self) -> int:
        return self._sec

    @property
    def nano(self) -> int:
        return self._nano

    def frac(self) -> float:
        return self.nano/1e9

    def hex(self) -> str:
        return self.pack().hex()

    def pack(self) -> bytes:
        return self._struct.pack(self.sec, self.nano)

    def __eq__(self, other):
        if isinstance(other, tain):     return (self.sec, self.nano) == (other.sec, other.nano)
        if isinstance(other, tai):      return (self.sec, self.nano) == (other.sec, 0)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, tain):     return (self.sec, self.nano) <= (other.sec, other.nano)
        if isinstance(other, tai):      return (self.sec, self.nano) <= (other.sec, 0)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, tain):     return (self.sec, self.nano) < (other.sec, other.nano)
        if isinstance(other, tai):      return (self.sec, self.nano) < (other.sec, 0)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, tain):     return (self.sec, self.nano) >= (other.sec, other.nano)
        if isinstance(other, tai):      return (self.sec, self.nano) >= (other.sec, 0)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, tain):     return (self.sec, self.nano) > (other.sec, other.nano)
        if isinstance(other, tai):      return (self.sec, self.nano) > (other.sec, 0)
        return NotImplemented

    def __float__(self):
        return float(self.sec) + self.frac()

    def __hash__(self):
        # TODO Should hash(tai(...)) == hash(taia(..., 0, 0))?
        return hash((self.__class__, self.sec, self.nano))

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}({self.sec}, {self.nano})'


class taia:
    __slots__ = ('_sec', '_nano', '_atto')
    _struct = struct.Struct('>QLL')
    _sec: int
    _nano: int
    _atto: int

    def __new__(cls, sec:int, nano:int, atto:int):
        sec = int(sec)
        nano = int(nano)
        atto = int(atto)
        if not MIN <= sec <= MAX:
            raise ValueError(f'sec must be in 0..2**63-1', sec)
        if not 0 <= nano < 10**9:
            raise ValueError(f'nano must be in 0..999_999_999', nano)
        if not 0 <= atto < 10**9:
            raise ValueError(f'atto must be in 0..999_999_999', atto)
        self = object.__new__(cls)
        self._sec = sec
        self._nano = nano
        self._atto = atto
        return self

    @classmethod
    def from_hex(cls, s:str|bytes|bytearray|memoryview) -> Self:
        buf = binascii.a2b_hex(s[0:cls._struct.size*2])
        return cls.unpack(buf)

    @classmethod
    def from_tai(cls, t:tai) -> Self:
        return cls(t.sec, 0, 0)

    @classmethod
    def from_tain(cls, t:tain) -> Self:
        return cls(t.sec, t.nano, 0)

    @classmethod
    def unpack(cls, buf:bytes|bytearray|memoryview) -> Self:
        sec, nano, atto = cls._struct.unpack(buf)
        return cls(sec, nano, atto)

    @property
    def sec(self) -> int:
        return self._sec

    @property
    def nano(self) -> int:
        return self._nano

    @property
    def atto(self) -> int:
        return self._atto

    def frac(self) -> float:
        return self.nano/1e9 + self.atto/1e18

    def hex(self) -> str:
        return self.pack().hex()

    def pack(self) -> bytes:
        return self._struct.pack(self.sec, self.nano, self.atto)

    def __eq__(self, other):
        if isinstance(other, taia):
            return (self.sec, self.nano, self.atto) == (other.sec, other.nano, other.atto)
        if isinstance(other, tain):
            return (self.sec, self.nano, self.atto) == (other.sec, other.nano, 0)
        if isinstance(other, tai):
            return (self.sec, self.nano, self.atto) == (other.sec, 0, 0)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, taia):
            return (self.sec, self.nano, self.atto) <= (other.sec, other.nano, other.atto)
        if isinstance(other, tain):
            return (self.sec, self.nano, self.atto) <= (other.sec, other.nano, 0)
        if isinstance(other, tai):
            return (self.sec, self.nano, self.atto) <= (other.sec, 0, 0)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, taia):
            return (self.sec, self.nano, self.atto) < (other.sec, other.nano, other.atto)
        if isinstance(other, tain):
            return (self.sec, self.nano, self.atto) < (other.sec, other.nano, 0)
        if isinstance(other, tai):
            return (self.sec, self.nano, self.atto) < (other.sec, 0, 0)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, taia):
            return (self.sec, self.nano, self.atto) >= (other.sec, other.nano, other.atto)
        if isinstance(other, tain):
            return (self.sec, self.nano, self.atto) >= (other.sec, other.nano, 0)
        if isinstance(other, tai):
            return (self.sec, self.nano, self.atto) >= (other.sec, 0, 0)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, taia):
            return (self.sec, self.nano, self.atto) > (other.sec, other.nano, other.atto)
        if isinstance(other, tain):
            return (self.sec, self.nano, self.atto) > (other.sec, other.nano, 0)
        if isinstance(other, tai):
            return (self.sec, self.nano, self.atto) > (other.sec, 0, 0)
        return NotImplemented

    def __float__(self):
        return float(self.sec) + self.frac()

    def __hash__(self):
        # TODO Should hash(tai(...)) == hash(taia(..., 0, 0))?
        return hash((self.__class__, self.sec, self.nano, self.atto))

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}({self.sec}, {self.nano}, {self.atto})'


__all__ = (
    'EPOCH',
    'MIN',
    'MAX',
    'UNIX_EPOCH',
    tai.__name__,
    tain.__name__,
    taia.__name__,
)

"""TAI64, TAI64N, TAI64NA implementations for Python.
"""
from __future__ import annotations

import binascii
import operator
import struct

try:
    from collections.abc import Buffer  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import Buffer

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
        self = object.__new__(cls)
        self._sec = int(sec)
        if not MIN <= self._sec <= MAX:
            raise ValueError('sec must be in 0..2**63-1', self._sec)
        return self

    @classmethod
    def from_hex(cls, s:str|Buffer) -> Self:
        buf = binascii.a2b_hex(s[0:cls._struct.size*2])
        return cls.unpack(buf)

    @classmethod
    def unpack(cls, buf:Buffer) -> Self:
        args = cls._struct.unpack(buf)
        return cls(*args)

    @property
    def sec(self) -> int:
        return self._sec

    def hex(self) -> str:
        return self.pack().hex()

    def pack(self) -> bytes:
        args = self._tuple()
        return self._struct.pack(*args)

    def _tuple(self) -> tuple[int]:
        return (self._sec,)

    def _compare(self, op, other) -> bool:
        if type(other) is type(self): return op(self._tuple(), other._tuple())
        return NotImplemented

    def __eq__(self, other): return self._compare(operator.eq, other)
    def __ge__(self, other): return self._compare(operator.ge, other)
    def __gt__(self, other): return self._compare(operator.gt, other)
    def __le__(self, other): return self._compare(operator.le, other)
    def __lt__(self, other): return self._compare(operator.lt, other)

    def __float__(self):
        return float(self.sec)

    def __hash__(self):
        return hash((self.__class__, *self._tuple()))

    def __repr__(self):
        cls = self.__class__
        args = ', '.join(f'{arg}' for arg in self._tuple())
        return f'{cls.__module__}.{cls.__name__}({args})'


class tain(tai):
    __slots__ = ('_nano')
    _struct = struct.Struct('>QL')
    _nano: int

    def __new__(cls, sec:int, nano:int):
        self = super().__new__(cls, sec)
        self._nano = int(nano)
        if not 0 <= self._nano <= 999_999_999:
            raise ValueError('nano must be in 0..999_999_999', self._nano)
        return self

    @classmethod
    def from_tai(cls, t:tai) -> Self:
        return cls(t.sec, 0)

    @property
    def nano(self) -> int:
        return self._nano

    def frac(self) -> float:
        return self.nano/1e9

    def _tuple(self) -> tuple[int, int]:  # type: ignore[override]
        return (self._sec, self._nano)

    def _compare(self, op, other) -> bool:
        typ = type(other)
        if typ is type(self): return op(self._tuple(), other._tuple())
        if typ is tai: return op(self._tuple(), (*other._tuple(), 0))
        return NotImplemented

    def __float__(self):
        return float(self.sec) + self.frac()


class taia(tain):
    __slots__ = ('_atto')
    _struct = struct.Struct('>QLL')
    _atto: int

    def __new__(cls, sec:int, nano:int, atto:int):
        self = super().__new__(cls, sec, nano)
        self._atto = int(atto)
        if not 0 <= self._atto <= 999_999_999:
            raise ValueError('atto must be in 0..999_999_999', self._atto)
        return self

    @classmethod
    def from_tai(cls, t:tai) -> Self:
        return cls(t.sec, 0, 0)

    @classmethod
    def from_tain(cls, t:tain) -> Self:
        return cls(t.sec, t.nano, 0)

    @property
    def atto(self) -> int:
        return self._atto

    def frac(self) -> float:
        return self.nano/1e9 + self.atto/1e18

    def _tuple(self) -> tuple[int, int, int]:  # type: ignore[override]
        return (self._sec, self._nano, self._atto)

    def _compare(self, op, other) -> bool:
        typ = type(other)
        if typ is type(self): return op(self._tuple(), other._tuple())
        if typ is tain: return op(self._tuple(), (*other._tuple(), 0))
        if typ is tai: return op(self._tuple(), (*other._tuple(), 0, 0))
        return NotImplemented


__all__ = (
    'EPOCH',
    'MIN',
    'MAX',
    'UNIX_EPOCH',
    tai.__name__,
    tain.__name__,
    taia.__name__,
)

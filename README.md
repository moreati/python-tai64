# Python TAI64

TAI64, TAI64N, TAI64NA implementations for Python.

International Atomic Time (TAI) is the basic standard for measuring time.
Universal Coordinated Time (UTC) is derived from TAI by adding or subtracting
leap seconds according to the measured rotation speed of the Earth.

TAI64 is a family of formats for TAI times, first implemented in libtai.
They have well known serialisations to bytes or hexadecimal.

| Format  | Bytes |         Resolution       |       Range       |
| ------- | ----: | -------------------------| ----------------- |
| TAI64   |     8 | 1 second                 | 292 billion years |
| TAI64N  |    12 | 1 nanosecond (10**-9 s)  | 292 billion years |
| TAI64NA |    16 | 1 attosecond (10**-18 s) | 292 billion years |

## Usage

```pycon
>>> import tai64
>>> tai64.tai(sec=tai64.EPOCH)  # TAI64 epoch is 1970-01-01 00:00:00 TAI
tai64.tai(4611686018427387904)
>>> tai64.tai(sec=tai64.UNIX_EPOCH)  # UNIX epoch is 10 seconds later
tai64.tai(4611686018427387914)
>>> t = tai64.tai.now()
>>> t
tai64.tai(4611686020113283116)
>>> t.pack()
b'@\x00\x00\x00d|\xb8,'
>>> t.hex()
'40000000647cb82c'
>>> t == tai64.tai.unpack(t.pack())
True
>>> t == tai64.tai.from_hex(t.hex())
True
>>> t2 = tai64.taina.now()
>>> t2
tai64.taina(4611686020113284055, 314132000, 0)
>>> t2.hex()
'40000000647cbbd712b9462000000000'
```

## TODO

- Implement TAI64 <-> UTC
- Unit tests
- PyPI package
- Docstrings
- License
- Decide: should `tai()` take raw unsigned int (current behaviour) or offset from epoch (`time.time()` behaviour)
- Decide `tai()` vs `tai64()`
- Decide `hash()` behaviour (should `hash(tain(i, 0)) == hash(tai(i)) == hash(i)`)
- Decide and implement exceptions hierarchy
- Decide and implement `str()` behaviour
- Decide and implement `format()` behaviour
- Decide `int()` behaviour of TAI64N and TAI64NA
- Decide `__floor__()` et al
- Decide arithmatic behaviour
- Investigate `CLOCK_TAI`

## Further Reading
- https://en.wikipedia.org/wiki/International_Atomic_Time
- https://cr.yp.to/proto/utctai.html
- https://cr.yp.to/libtai/tai64.html
- https://cr.yp.to/libtai.html

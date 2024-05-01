# Python TAI64

TAI64, TAI64N, TAI64NA implementations for Python.

[International Atomic Time (TAI)][TAI] is the basic standard for measuring time.
Universal Coordinated Time (UTC) is derived from TAI by adding or subtracting
leap seconds according to the measured rotation speed of the Earth.

[TAI64] is a family of formats for TAI times, first implemented in [libtai].
They have well known serialisations to bytes or hexadecimal.

| Format  | Bytes |         Resolution       |       Range       |
| ------- | ----: | -------------------------| ----------------- |
| TAI64   |     8 | 1 second                 | 292 billion years |
| TAI64N  |    12 | 1 nanosecond (10**-9 s)  | 292 billion years |
| TAI64NA |    16 | 1 attosecond (10**-18 s) | 292 billion years |

## Usage

The epoch for TAI64 is 1970-01-01 00:00:00 TAI, this is assigned the integer value 2**62.

```pycon
>>> import tai64
>>> tai64.tai(sec=tai64.EPOCH)
tai64.tai(4611686018427387904)
```

To deserialise a TAI64, TAI64N, or TAI64NA call the `from_hex()` or
`unpack()` class method.

```pycon
>>> tai64.tai.from_hex('400000001dc03c40')
tai64.tai(4611686018926525504)
>>> tai64.tai.unpack(b'@\x00\x00\x00\x1d\xc0<@')
tai64.tai(4611686018926525504)
```

To serialise call the `hex()` or `pack()` method

```pycon
>>> tai64.tai(4611686018926525504).hex()
'400000001dc03c40'
>>> tai64.tai(4611686018926525504).pack()
b'@\x00\x00\x00\x1d\xc0<@'
```

For nanosecond precision (9 decimal places) use `tai64.tain()`,
or for attosecond (18 decimal places) use `tai64.taia()`.

```pycon
>>> tai64.tain(4611686018926525504, nano=123).hex()
'400000001dc03c400000007b'
>>> tai64.taia(4611686018926525504, nano=1193046, atto=11259375).hex()
'400000001dc03c400012345600abcdef'
>>> tai64.taia.unpack(b'@\x00\x00\x00\x1d\xc0<@\x00\x124V\x00\xab\xcd\xef')
tai64.taia(4611686018926525504, 1193046, 11259375)
```

## TODO

- Implement TAI64 <-> UTC
- PyPI package
- Docstrings
- Decide: should `tai()` take raw unsigned int (current behaviour) or offset from epoch (`time.time()` behaviour)
- Decide and implement exceptions hierarchy
- Decide and implement `str()` behaviour
- Decide and implement `format()` behaviour
- Decide `int()` behaviour of TAI64N and TAI64NA
- Decide `__floor__()` et al
- Decide arithmatic behaviour
- Investigate `CLOCK_TAI`

## Other implementations

- [calends] for Go, C/C++, Dart, Javascript, WASM, and PHP
- [Go cactus/tai64]
- [Go paulhammond/tai64]
- [Javascript tai64]
- [libtai] original C implementation, by D. J. Bernstein.
- [Perl Time::TAI64]
- [Python tai64n]
- [Python taiconverter]
- [Rust tai64]

## Further Reading

- https://en.wikipedia.org/wiki/International_Atomic_Time
- https://cr.yp.to/proto/utctai.html
- https://cr.yp.to/libtai/tai64.html
- https://cr.yp.to/libtai.html

[TAI]: https://en.wikipedia.org/wiki/International_Atomic_Time
[TAI64]: https://cr.yp.to/libtai/tai64.html
[calends]: https://calends.readthedocs.io/en/latest/
[Go cactus/tai64]: https://github.com/cactus/tai64
[Go paulhammond/tai64]: https://github.com/paulhammond/tai64
[Javascript tai64]: https://www.npmjs.com/package/tai64
[libtai]: https://cr.yp.to/libtai.html
[Perl Time::TAI64]: https://metacpan.org/pod/Time::TAI64
[Python tai64n]: https://pypi.org/project/tai64n/
[Python taiconverter]: https://pypi.org/project/tai64converter/
[Rust tai64]: https://docs.rs/tai64/latest/tai64/

import hypothesis as hyp
import hypothesis.strategies as hst
import pytest

import tai64


INVALID_SEC_TYPES = [
    None,
    1.0,
    '1',
]


INVALID_SEC_VALS = [
    -1,
    2**63,
]


TAI64_LABELS_HEX = [
    ('3fffffffffffffff', 2**62 - 1,             '1969-12-31 23:59:59 TAI'),
    ('4000000000000000', 2**62,                 '1970-01-01 00:00:00 TAI'),
    ('400000002a2b2c2d', 4611686019134860333,   '1992-06-02 08:07:09 TAI'),
]


TAI64_LABELS = [
    (bytes.fromhex(buf), sec, isofmt)
    for buf, sec, isofmt in TAI64_LABELS_HEX
]


def test_constants():
    assert tai64.EPOCH == 0x4000000000000000
    assert tai64.MIN == 0
    assert tai64.MAX == 0x7fffffffffffffff
    assert type(tai64.EPOCH) is int
    assert type(tai64.MIN) is int
    assert type(tai64.MAX) is int


def test__all__():
    for s in tai64.__all__:
        assert s in dir(tai64)


def hst_secs(): return hst.integers(0, 2**63-1)
def hst_nanos(): return hst.integers(0, 999_999_999)
def hst_attos(): return hst.integers(0, 999_999_999)


class TestTai:
    def test_constructor(self):
        assert tai64.tai(0)
        assert tai64.tai(1234)
        assert tai64.tai(2**63-1)

    @pytest.mark.parametrize('sec', INVALID_SEC_TYPES)
    def test_constructor_invalid_type(self, sec):
        with pytest.raises(TypeError):
            tai64.tai(sec)

    @pytest.mark.parametrize('sec', INVALID_SEC_VALS)
    def test_constructor_invalid_val(self, sec):
        with pytest.raises(ValueError):
            tai64.tai(sec)

    @pytest.mark.parametrize(['buf', 'sec', 'isofmt'], TAI64_LABELS_HEX)
    def test_from_hex(self, buf, sec, isofmt):
        t = tai64.tai.from_hex(buf)
        assert t.sec == sec

    @pytest.mark.parametrize(['buf', 'sec', 'isofmt'], TAI64_LABELS)
    def test_unpack(self, buf, sec, isofmt):
        t = tai64.tai.unpack(buf)
        assert t.sec == sec

    def test_attributes(self):
        t = tai64.tai(1234)
        assert t.sec == 1234
        assert type(t.sec) is int
        assert t.size == 8
        assert type(t.size) is int

    @pytest.mark.parametrize(['buf', 'sec', 'isofmt'], TAI64_LABELS_HEX)
    def test_hex(self, buf, sec, isofmt):
        t = tai64.tai(sec)
        assert t.hex() == buf

    @pytest.mark.parametrize(['buf', 'sec', 'isofmt'], TAI64_LABELS)
    def test_pack(self, buf, sec, isofmt):
        t = tai64.tai(sec)
        assert t.pack() == buf
        assert t.size == len(buf)

    def test_replace(self):
        t = tai64.tai(1234)
        assert t.replace().sec == t.sec
        assert t.replace(2345).sec == 2345

    @hyp.given(hst_secs(), hst_secs())
    def test_cmp(self, sec1, sec2):
        assert (sec1 == sec2) == (tai64.tai(sec1) == tai64.tai(sec2))
        assert (sec1 != sec2) == (tai64.tai(sec1) != tai64.tai(sec2))
        assert (sec1 >= sec2) == (tai64.tai(sec1) >= tai64.tai(sec2))
        assert (sec1 >  sec2) == (tai64.tai(sec1) >  tai64.tai(sec2))
        assert (sec1 <= sec2) == (tai64.tai(sec1) <= tai64.tai(sec2))
        assert (sec1 <  sec2) == (tai64.tai(sec1) <  tai64.tai(sec2))

    def test_float(self):
        t = tai64.tai(1234)
        f = float(t)
        assert f == 1234
        assert type(f) is float

    def test_repr(self):
        t = tai64.tai(1234)
        assert repr(t) == 'tai64.tai(1234)'

    def test_str(self):
        assert str(tai64.tai(0)) == '0'
        assert str(tai64.tai(1)) == '1'
        assert str(tai64.tai(tai64.EPOCH)) == '4611686018427387904'
        assert str(tai64.tai.max) == '9223372036854775807'

    def test_constants(self):
        assert tai64.tai.epoch.sec == 0x4000000000000000
        assert tai64.tai.min.sec == 0
        assert tai64.tai.max.sec == 0x7fffffffffffffff


INVALID_NANO_TYPES = INVALID_SEC_TYPES
INVALID_NANO_VALS = [
    -1,
    1_000_000_000,
]

TAI64N_LABELS_HEX = [
    ('3fffffffffffffff00000000', 2**62 - 1,             0,          '1969-12-31 23:59:59.0 TAI'),
    ('40000000000000003b9ac9ff', 2**62,                 999999999,  '1970-01-01 00:00:00.999999999 TAI'),
    ('400000002a2b2c2d1dcd6500', 4611686019134860333,   500000000,  '1992-06-02 08:07:09.5 TAI'),
]


TAI64N_LABELS = [
    (bytes.fromhex(buf), sec, nano, isofmt)
    for buf, sec, nano, isofmt in TAI64N_LABELS_HEX
]


class TestTain:
    def test_constructor(self):
        assert tai64.tain(1234, 0)
        assert tai64.tain(1234, 2345)
        assert tai64.tain(1234, 999_999_999)

    @pytest.mark.parametrize('sec', INVALID_SEC_TYPES)
    def test_constructor_invalid_sec_type(self, sec):
        with pytest.raises(TypeError):
            tai64.tain(sec)

    @pytest.mark.parametrize('nano', INVALID_NANO_TYPES)
    def test_constructor_invalid_nano_type(self, nano):
        with pytest.raises(TypeError):
            tai64.tain(123, nano)

    @pytest.mark.parametrize('sec', INVALID_SEC_VALS)
    def test_constructor_invalid_sec_val(self, sec):
        with pytest.raises(ValueError):
            tai64.tain(sec, 0)

    @pytest.mark.parametrize('nano', INVALID_NANO_VALS)
    def test_constructor_invalid_nano_val(self, nano):
        with pytest.raises(ValueError):
            tai64.tain(123, nano)

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'isofmt'], TAI64N_LABELS_HEX)
    def test_from_hex(self, buf, sec, nano, isofmt):
        t = tai64.tain.from_hex(buf)
        assert t.sec == sec
        assert t.nano == nano

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'isofmt'], TAI64N_LABELS)
    def test_unpack(self, buf, sec, nano, isofmt):
        t = tai64.tain.unpack(buf)
        assert t.sec == sec
        assert t.nano == nano

    def test_attributes(self):
        t = tai64.tain(1234, 2345)
        assert t.sec == 1234
        assert t.nano == 2345
        assert type(t.sec) is int
        assert type(t.nano) is int
        assert t.size == 12
        assert type(t.size) is int

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'isofmt'], TAI64N_LABELS_HEX)
    def test_hex(self, buf, sec, nano, isofmt):
        t = tai64.tain(sec, nano)
        assert t.hex() == buf

    def test_frac(self):
        t = tai64.tain(1234, 2345)
        assert t.frac() == 0.000_002_345
        assert type(t.frac()) is float

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'isofmt'], TAI64N_LABELS)
    def test_pack(self, buf, sec, nano, isofmt):
        t = tai64.tain(sec, nano)
        assert t.pack() == buf
        assert t.size == len(buf)

    def test_replace(self):
        t = tai64.tain(1234, 2345)
        assert t.replace().sec == t.sec
        assert t.replace().nano == t.nano
        assert t.replace(sec=5678).sec == 5678
        assert t.replace(sec=5678).nano == t.nano
        assert t.replace(nano=6789).sec == t.sec
        assert t.replace(nano=6789).nano == 6789

    @hyp.given(hst_secs(), hst_nanos(), hst_secs(), hst_nanos())
    def test_cmp(self, sec1, nano1, sec2, nano2):
        tup1 = (sec1, nano1)
        tup2 = (sec2, nano2)
        tn1 = tai64.tain(sec1, nano1)
        tn2 = tai64.tain(sec2, nano2)
        assert (tup1 == tup2) == (tn1 == tn2)
        assert (tup1 != tup2) == (tn1 != tn2)
        assert (tup1 >= tup2) == (tn1 >= tn2)
        assert (tup1 >  tup2) == (tn1 >  tn2)
        assert (tup1 <= tup2) == (tn1 <= tn2)
        assert (tup1 <  tup2) == (tn1 <  tn2)

    @hyp.given(hst_secs(), hst_nanos())
    def test_cmp_tai(self, sec, nano):
        tup1 = (sec, nano)
        tup2 = (sec, 0)
        tn1 = tai64.tain(sec, nano)
        t2 = tai64.tai(sec)
        assert (tup1 == tup2) == (tn1 == t2)
        assert (tup1 != tup2) == (tn1 != t2)
        assert (tup1 >= tup2) == (tn1 >= t2)
        assert (tup1 >  tup2) == (tn1 >  t2)
        assert (tup1 <= tup2) == (tn1 <= t2)
        assert (tup1 <  tup2) == (tn1 <  t2)

    def test_float(self):
        t = tai64.tain(1234, 2345)
        f = float(t)
        assert f == 1234.000002345
        assert type(f) is float

    def test_repr(self):
        t = tai64.tain(1234, 2345)
        assert repr(t) == 'tai64.tain(1234, 2345)'

    def test_str(self):
        assert str(tai64.tain(0, 0)) == '0.0'
        assert str(tai64.tain(0, 1)) == '0.000000001'
        assert str(tai64.tain(1, 2)) == '1.000000002'
        assert str(tai64.tain(tai64.EPOCH, 123456789)) == '4611686018427387904.123456789'
        assert str(tai64.tain.max) == '9223372036854775807.999999999'

    def test_constants(self):
        assert tai64.tain.epoch.sec == 0x4000000000000000
        assert tai64.tain.epoch.nano == 0
        assert tai64.tain.min.sec == 0
        assert tai64.tain.min.nano == 0
        assert tai64.tain.max.sec == 0x7fffffffffffffff
        assert tai64.tain.max.nano == 999_999_999


INVALID_ATTO_TYPES = INVALID_SEC_TYPES
INVALID_ATTO_VALS = INVALID_NANO_VALS

TAI64NA_LABELS_HEX = [
    ('3fffffffffffffff0000000000000001',
     2**62 - 1,             0,          1,
     '1969-12-31 23:59:59.000000000000000001 TAI'),
    ('40000000000000003b9ac9ff1dcd6500',
     2**62,                 999999999,  500000000,
     '1970-01-01 00:00:00.9999999995 TAI'),
    ('400000002a2b2c2d1dcd65003b9ac9ff',
     4611686019134860333,   500000000,  999999999,
     '1992-06-02 08:07:09.500000000999999999 TAI'),
]


TAI64NA_LABELS = [
    (bytes.fromhex(buf), sec, nano, atto, isofmt)
    for buf, sec, nano, atto, isofmt in TAI64NA_LABELS_HEX
]

class TestTaia:
    def test_constructor(self):
        assert tai64.taia(1234, 0, 0)
        assert tai64.taia(1234, 2345, 3456)
        assert tai64.taia(1234, 999_999_999, 999_999_999)

    @pytest.mark.parametrize('sec', INVALID_SEC_TYPES)
    def test_constructor_invalid_sec_type(self, sec):
        with pytest.raises(TypeError):
            tai64.taia(sec, 0, 0)

    @pytest.mark.parametrize('nano', INVALID_NANO_TYPES)
    def test_constructor_invalid_nano_type(self, nano):
        with pytest.raises(TypeError):
            tai64.taia(123, nano, 0)

    @pytest.mark.parametrize('atto', INVALID_ATTO_TYPES)
    def test_constructor_invalid_atto_type(self, atto):
        with pytest.raises(TypeError):
            tai64.taia(123, 0, atto)

    @pytest.mark.parametrize('sec', INVALID_SEC_VALS)
    def test_constructor_invalid_sec_val(self, sec):
        with pytest.raises(ValueError):
            tai64.taia(sec, 0, 0)

    @pytest.mark.parametrize('nano', INVALID_NANO_VALS)
    def test_constructor_invalid_nano_val(self, nano):
        with pytest.raises(ValueError):
            tai64.taia(123, nano, 0)

    @pytest.mark.parametrize('atto', INVALID_ATTO_VALS)
    def test_constructor_invalid_atto_val(self, atto):
        with pytest.raises(ValueError):
            tai64.taia(123, 0, atto)

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'atto', 'isofmt'], TAI64NA_LABELS_HEX)
    def test_from_hex(self, buf, sec, nano, atto, isofmt):
        t = tai64.taia.from_hex(buf)
        assert t.sec == sec
        assert t.nano == nano
        assert t.atto == atto

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'atto', 'isofmt'], TAI64NA_LABELS)
    def test_unpack(self, buf, sec, nano, atto, isofmt):
        t = tai64.taia.unpack(buf)
        assert t.sec == sec
        assert t.nano == nano
        assert t.atto == atto

    def test_attributes(self):
        t = tai64.taia(1234, 2345, 3456)
        assert t.sec == 1234
        assert t.nano == 2345
        assert t.atto == 3456
        assert type(t.sec) is int
        assert type(t.nano) is int
        assert type(t.atto) is int
        assert t.size == 16
        assert type(t.size) is int

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'atto', 'isofmt'], TAI64NA_LABELS_HEX)
    def test_hex(self, buf, sec, nano, atto, isofmt):
        t = tai64.taia(sec, nano, atto)
        assert t.hex() == buf

    def test_frac(self):
        t = tai64.taia(1234, 2345, 3456)
        assert t.frac() == 0.000_002_345_000_003_456
        assert type(t.frac()) is float

    @pytest.mark.parametrize(['buf', 'sec', 'nano', 'atto', 'isofmt'], TAI64NA_LABELS)
    def test_pack(self, buf, sec, nano, atto, isofmt):
        t = tai64.taia(sec, nano, atto)
        assert t.pack() == buf
        assert t.size == len(buf)

    def test_replace(self):
        t = tai64.taia(1234, 2345, 3456)
        assert t.replace().sec == t.sec
        assert t.replace().nano == t.nano
        assert t.replace().atto == t.atto

        assert t.replace(sec=5678).sec == 5678
        assert t.replace(sec=5678).nano == t.nano
        assert t.replace(sec=5678).atto == t.atto

        assert t.replace(nano=6789).sec == t.sec
        assert t.replace(nano=6789).nano == 6789
        assert t.replace(nano=6789).atto == t.atto

        assert t.replace(atto=7890).sec == t.sec
        assert t.replace(atto=7890).nano == t.nano
        assert t.replace(atto=7890).atto == 7890


    @hyp.given(hst_secs(), hst_nanos(), hst_attos(),
               hst_secs(), hst_nanos(), hst_attos())
    def test_cmp(self, sec1, nano1, atto1, sec2, nano2, atto2):
        tup1 = (sec1, nano1, atto1)
        tup2 = (sec2, nano2, atto2)
        ta1 = tai64.taia(sec1, nano1, atto1)
        ta2 = tai64.taia(sec2, nano2, atto2)
        assert (tup1 == tup2) == (ta1 == ta2)
        assert (tup1 != tup2) == (ta1 != ta2)
        assert (tup1 >= tup2) == (ta1 >= ta2)
        assert (tup1 >  tup2) == (ta1 >  ta2)
        assert (tup1 <= tup2) == (ta1 <= ta2)
        assert (tup1 <  tup2) == (ta1 <  ta2)

    @hyp.given(hst_secs(), hst_nanos(), hst_attos())
    def test_cmp_tain(self, sec, nano, atto):
        tup1 = (sec, nano, atto)
        tup2 = (sec, nano, 0)
        ta1 = tai64.taia(sec, nano, atto)
        tn2 = tai64.tain(sec, nano)
        assert (tup1 == tup2) == (ta1 == tn2)
        assert (tup1 != tup2) == (ta1 != tn2)
        assert (tup1 >= tup2) == (ta1 >= tn2)
        assert (tup1 >  tup2) == (ta1 >  tn2)
        assert (tup1 <= tup2) == (ta1 <= tn2)
        assert (tup1 <  tup2) == (ta1 <  tn2)

    @hyp.given(hst_secs(), hst_nanos(), hst_attos())
    def test_cmp_tai(self, sec, nano, atto):
        tup1 = (sec, nano, atto)
        tup2 = (sec, 0, 0)
        ta1 = tai64.taia(sec, nano, atto)
        t2 = tai64.tai(sec)
        assert (tup1 == tup2) == (ta1 == t2)
        assert (tup1 != tup2) == (ta1 != t2)
        assert (tup1 >= tup2) == (ta1 >= t2)
        assert (tup1 >  tup2) == (ta1 >  t2)
        assert (tup1 <= tup2) == (ta1 <= t2)
        assert (tup1 <  tup2) == (ta1 <  t2)

    def test_float(self):
        t = tai64.taia(1234, 2345, 3456)
        f = float(t)
        assert f == 1234.000_002_345_000_000_000  # float() has to approximate
        assert type(f) is float

    def test_repr(self):
        t = tai64.taia(1234, 2345, 3456)
        assert repr(t) == 'tai64.taia(1234, 2345, 3456)'

    def test_str(self):
        assert str(tai64.taia(0, 0, 0)) == '0.0'
        assert str(tai64.taia(0, 0, 1)) == '0.000000000000000001'
        assert str(tai64.taia(0, 1, 2)) == '0.000000001000000002'
        assert str(tai64.taia(1, 2, 3)) == '1.000000002000000003'
        assert str(tai64.taia(tai64.EPOCH, 123456789, 987654321)) == '4611686018427387904.123456789987654321'
        assert str(tai64.taia.max) == '9223372036854775807.999999999999999999'


    def test_constants(self):
        assert tai64.taia.epoch.sec == 0x4000000000000000
        assert tai64.taia.epoch.nano == 0
        assert tai64.taia.epoch.atto == 0
        assert tai64.taia.min.sec == 0
        assert tai64.taia.min.nano == 0
        assert tai64.taia.min.atto == 0
        assert tai64.taia.max.sec == 0x7fffffffffffffff
        assert tai64.taia.max.nano == 999_999_999
        assert tai64.taia.max.atto == 999_999_999

######################################################################
#
# File: test/unit/test_base.py
#
# Copyright 2019 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

from contextlib import contextmanager
import re
import unittest
import voluptuous as vol


class TestBase(unittest.TestCase):
    @contextmanager
    def assertRaises(self, exc, msg=None):
        try:
            yield
        except exc as e:
            if msg is not None:
                if msg != str(e):
                    assert False, "expected message '%s', but got '%s'" % (msg, str(e))
        else:
            assert False, 'should have thrown %s' % (exc,)

    @contextmanager
    def assertRaisesRegexp(self, expected_exception, expected_regexp):
        try:
            yield
        except expected_exception as e:
            if not re.search(expected_regexp, str(e)):
                assert False, "expected message '%s', but got '%s'" % (expected_regexp, str(e))
        else:
            assert False, 'should have thrown %s' % (expected_exception,)


class Elo:
    @staticmethod
    def from_dict(dict):
        if dict is None:
            raise ValueError('nope')

        return 0


class Coerce(object):
    def __call__(self, v):
        if v is None:
            raise vol.Invalid('nope')
        return v

    def __repr__(self):
        return 'Coerce(%s, msg=%r)' % (self.type_name, self.msg)


class TestVol(TestBase):
    def test_vol(self):
        s = vol.Schema({
            'a': int,
            'b': vol.Coerce(float),
        })
        d = {'a': 7, 'b': '9.5'}

        self.assertEqual({'a': 7, 'b': 9.5}, s(d))

        s = vol.Schema(
            {
                'a': int,
                vol.Optional('b', default=None): vol.Any(vol.Coerce(float), None),
            }
        )

        self.assertEqual({'a': 7, 'b': 9.5}, s({'a': 7, 'b': 9.5}))
        self.assertEqual({'a': 7, 'b': 9.5}, s({'a': 7, 'b': '9.5'}))
        self.assertEqual({'a': 7, 'b': None}, s({'a': 7, 'b': None}))
        self.assertEqual({'a': 7, 'b': None}, s({'a': 7}))

        s = vol.Schema([{
            'a': int,
            vol.Optional('b', default=None): Coerce(),
        }])
        self.assertEqual(
            [{
                'a': 7,
                'b': 1
            }, {
                'a': 8,
                'b': 9
            }], s([{
                'a': 7,
                'b': 1
            }, {
                'a': 8,
                'b': 9
            }])
        )
        with self.assertRaises(vol.MultipleInvalid, "nope for dictionary value @ data[1]['b']"):
            s([{'a': 7, 'b': 1}, {'a': 8, 'b': None}])

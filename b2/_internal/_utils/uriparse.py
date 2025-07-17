######################################################################
#
# File: b2/_internal/_utils/uriparse.py
#
# Copyright 2025 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
import re

_CONTROL_CHARACTERS_AND_SPACE = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
_B2_URL_RE = re.compile(
    r"""
    (
        (?P<scheme>[a-z0-9]+)
        ://
    )?                       # the delimiter is optional if there is no scheme defined
    (?P<netloc>[-a-z0-9]*)   # scheme and
    (?P<path>\.{0,2}(/.*)?)            # everything else from the first / is part of the path
    """,
    re.VERBOSE | re.IGNORECASE,
)


class SplitB2Result:
    def __init__(self, scheme, netloc, path):
        self._parts = (scheme, netloc, path)

    def __iter__(self):
        return iter(self._parts)

    def __getitem__(self, key):
        return self._parts[key]

    def __len__(self):
        return len(self._parts)

    def replace(self, scheme=None, netloc=None, path=None):
        return SplitB2Result(
            scheme=self.scheme if scheme is None else scheme,
            netloc=self.netloc if netloc is None else netloc,
            path=self.path if path is None else path,
        )

    @property
    def scheme(self):
        return self._parts[0]

    @property
    def netloc(self):
        return self._parts[1]

    @property
    def path(self):
        return self._parts[2]

    def __repr__(self):
        return f'SplitB2Result(scheme={self.scheme!r}, netloc={self.netloc!r}, path={self.path!r})'


def b2_urlsplit(url: str) -> SplitB2Result:
    # clean the url
    url = url.lstrip(_CONTROL_CHARACTERS_AND_SPACE)
    for i in ['\n', '\r', '\t']:
        url.replace(i, '')

    match = _B2_URL_RE.fullmatch(url)
    if not match:
        raise ValueError(f'Invalid B2 URI: {url!r}')

    scheme = (match.group('scheme') or '').lower()
    netloc = match.group('netloc') or ''
    path = match.group('path') or ''

    return SplitB2Result(scheme, netloc, path)

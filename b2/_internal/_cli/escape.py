######################################################################
#
# File: b2/_internal/_cli/escape.py
#
# Copyright 2023 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

import re
import shlex

# skip newline, tab
UNPRINTABLE_PATTERN = re.compile(r'[\x00-\x08\x0e-\x1f\x7f-\x9f]')


def unprintable_to_hex(s):
    def hexify(match):
        return fr'\x{ord(match.group()):02x}'

    if s:
        return UNPRINTABLE_PATTERN.sub(hexify, s)
    return None


def escape_control_chars(s):
    if s:
        return shlex.quote(unprintable_to_hex(s))
    return None


def substitute_control_chars(s):
    match_result = UNPRINTABLE_PATTERN.match(s)
    s = UNPRINTABLE_PATTERN.sub('�', s)
    return (s, match_result is not None)

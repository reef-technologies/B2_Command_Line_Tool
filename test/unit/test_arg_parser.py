######################################################################
#
# File: test/unit/test_arg_parser.py
#
# Copyright 2020 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

import argparse
import io

from b2.arg_parser import ArgumentParser, parse_comma_separated_list, parse_millis_from_float_timestamp, parse_range
from b2.console_tool import B2, CreateKey

from .test_base import TestBase


class TestCustomArgTypes(TestBase):
    def test_parse_comma_separated_list(self):
        self.assertEqual([''], parse_comma_separated_list(''))
        self.assertEqual(['1', '2', '3'], parse_comma_separated_list('1,2,3'))

    def test_parse_millis_from_float_timestamp(self):
        self.assertEqual(1367900664000, parse_millis_from_float_timestamp('1367900664'))
        self.assertEqual(1367900664152, parse_millis_from_float_timestamp('1367900664.152'))
        with self.assertRaises(ValueError):
            parse_millis_from_float_timestamp('!$@$%@!@$')

    def test_parse_range(self):
        self.assertEqual((1, 2), parse_range('1,2'))
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_range('1')
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_range('1,2,3')
        with self.assertRaises(ValueError):
            parse_range('!@#,%^&')


class TestNonUTF8TerminalSupport(TestBase):
    def check_help_string(self, command_class):
        help_string = command_class.__doc__

        # Create a parser with a help message that is based on the command_class.__doc__ string
        parser = ArgumentParser(description=help_string)

        # Create a BytesIO instance to capture the output, simulating a non-UTF-8 terminal
        output = io.BytesIO()

        try:
            # Try to write the help message to the BytesIO instance as bytes
            output.write(parser.format_help().encode('ascii'))
            assert len(output.getvalue()) > 0, "No data written to the output"

        except UnicodeEncodeError as e:
            self.fail(f'Failed to encode help message for a non-UTF-8 terminal: {e}')

    def test_b2_help_in_non_utf8_terminal(self):
        self.check_help_string(B2)

    def test_create_key_help_in_non_utf8_terminal(self):
        self.check_help_string(CreateKey)

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
import sys

from b2.arg_parser import ArgumentParser, parse_comma_separated_list, parse_millis_from_float_timestamp, parse_range

from b2.console_tool import (
    AuthorizeAccount, 
    CancelAllUnfinishedLargeFiles, 
    CancelLargeFile, 
    ClearAccount, 
    CopyFileById, 
    CreateBucket, 
    DeleteBucket, 
    DeleteFileVersion, 
    DeleteKey, 
    DownloadFileById, 
    DownloadFileByName, 
    GetBucket, 
    GetDownloadAuth, 
    GetDownloadUrlWithAuth, 
    HideFile, 
    ListBuckets, 
    ListKeys, 
    ListParts, 
    ListUnfinishedLargeFiles, 
    Ls, 
    Rm, 
    MakeUrl, 
    Sync, 
    UpdateBucket, 
    UploadFile, 
    UpdateFileLegalHold, 
    UpdateFileRetention, 
    ReplicationSetup, 
    ReplicationDelete, 
    ReplicationPause, 
    ReplicationUnpause, 
    ReplicationStatus, 
    License, 
    InstallAutocomplete
)

from b2.console_tool import B2, CancelAllUnfinishedLargeFiles, CopyFileById, CreateKey, GetAccountInfo, UpdateFileRetention

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

    class ASCIIEncodedStream:
        def __init__(self, original_stream):
            self.original_stream = original_stream
            self.encoding = 'ascii'

        def write(self, data):
            if isinstance(data, str):
                data = data.encode(self.encoding, 'strict')
            self.original_stream.buffer.write(data)

        def flush(self):
            self.original_stream.flush()

    def check_help_string(self, command_class):
        help_string = command_class.__doc__
        command_name = command_class.__name__.lower()

        # Create a parser with a help message that is based on the command_class.__doc__ string
        parser = ArgumentParser(description=help_string)

        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = TestNonUTF8TerminalSupport.ASCIIEncodedStream(sys.stdout)
            sys.stderr = TestNonUTF8TerminalSupport.ASCIIEncodedStream(sys.stderr)

            parser.print_help()

        except UnicodeEncodeError as e:
            self.fail(f'Failed to encode help message for command "{command_name}" on a non-UTF-8 terminal: {e}')

        finally:
            # Restore original stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def test_authorize_account_help_in_non_utf8_terminal(self):
        self.check_help_string(AuthorizeAccount)

    def test_cancel_large_file_help_in_non_utf8_terminal(self):
        self.check_help_string(CancelLargeFile)

    def test_clear_account_help_in_non_utf8_terminal(self):
        self.check_help_string(ClearAccount)

    def test_copy_file_by_id_help_in_non_utf8_terminal(self):
        self.check_help_string(CopyFileById)

    def test_create_bucket_help_in_non_utf8_terminal(self):
        self.check_help_string(CreateBucket)

    def test_delete_bucket_help_in_non_utf8_terminal(self):
        self.check_help_string(DeleteBucket)

    def test_delete_file_version_help_in_non_utf8_terminal(self):
        self.check_help_string(DeleteFileVersion)

    def test_delete_key_help_in_non_utf8_terminal(self):
        self.check_help_string(DeleteKey)

    def test_download_file_by_id_help_in_non_utf8_terminal(self):
        self.check_help_string(DownloadFileById)

    def test_download_file_by_name_help_in_non_utf8_terminal(self):
        self.check_help_string(DownloadFileByName)

    def test_get_bucket_help_in_non_utf8_terminal(self):
        self.check_help_string(GetBucket)

    def test_get_download_auth_help_in_non_utf8_terminal(self):
        self.check_help_string(GetDownloadAuth)

    def test_get_download_url_with_auth_help_in_non_utf8_terminal(self):
        self.check_help_string(GetDownloadUrlWithAuth)

    def test_hide_file_help_in_non_utf8_terminal(self):
        self.check_help_string(HideFile)

    def test_list_buckets_help_in_non_utf8_terminal(self):
        self.check_help_string(ListBuckets)

    def test_list_keys_help_in_non_utf8_terminal(self):
        self.check_help_string(ListKeys)

    def test_list_parts_help_in_non_utf8_terminal(self):
        self.check_help_string(ListParts)

    def test_list_unfinished_large_files_help_in_non_utf8_terminal(self):
        self.check_help_string(ListUnfinishedLargeFiles)

    def test_ls_help_in_non_utf8_terminal(self):
        self.check_help_string(Ls)

    def test_rm_help_in_non_utf8_terminal(self):
        self.check_help_string(Rm)

    def test_make_url_help_in_non_utf8_terminal(self):
        self.check_help_string(MakeUrl)

    def test_sync_help_in_non_utf8_terminal(self):
        self.check_help_string(Sync)

    def test_update_bucket_help_in_non_utf8_terminal(self):
        self.check_help_string(UpdateBucket)

    def test_upload_file_help_in_non_utf8_terminal(self):
        self.check_help_string(UploadFile)

    def test_update_file_legal_hold_help_in_non_utf8_terminal(self):
        self.check_help_string(UpdateFileLegalHold)

    def test_update_file_retention_help_in_non_utf8_terminal(self):
        self.check_help_string(UpdateFileRetention)

    def test_replication_setup_help_in_non_utf8_terminal(self):
        self.check_help_string(ReplicationSetup)

    def test_replication_delete_help_in_non_utf8_terminal(self):
        self.check_help_string(ReplicationDelete)

    def test_replication_pause_help_in_non_utf8_terminal(self):
        self.check_help_string(ReplicationPause)

    def test_replication_unpause_help_in_non_utf8_terminal(self):
        self.check_help_string(ReplicationUnpause)

    def test_replication_status_help_in_non_utf8_terminal(self):
        self.check_help_string(ReplicationStatus)

    def test_license_help_in_non_utf8_terminal(self):
        self.check_help_string(License)

    def test_install_autocomplete_help_in_non_utf8_terminal(self):
        self.check_help_string(InstallAutocomplete)

    def test_cancel_all_unfinished_large_files_help_in_non_utf8_terminal(self):
        self.check_help_string(CancelAllUnfinishedLargeFiles)

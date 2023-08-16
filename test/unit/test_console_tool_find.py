######################################################################
#
# File: test/unit/test_console_tool_find.py
#
# Copyright 2023 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
import unittest.mock as mock
from typing import List, Optional

from b2sdk.v2 import (
    REALM_URLS,
    ProgressReport,
)
from b2sdk.v2.exception import Conflict  # Any error for testing fast-fail of the rm command.

from .test_console_tool import BaseConsoleToolTest


@mock.patch.dict(REALM_URLS, {'production': 'http://production.example.com'})
class TestFindConsoleTool(BaseConsoleToolTest):
    """
    These tests replace default progress reporter of Rm class
    to ensure that it reports everything as fast as possible.
    """

    class InstantReporter(ProgressReport):
        UPDATE_INTERVAL = 0.0

    def setUp(self):
        super().setUp()

        self._authorize_account()
        self._create_my_bucket()

        self.bucket = self.b2_api.get_bucket_by_name('my-bucket')
        self._upload_multiple_files(self.bucket)

    def test_findwildcard(self):
        self._run_command(
            ['find', '--recursive', '--withWildcard', '--noProgress', 'my-bucket', '**/*.csv'],
        )

        expected_stdout = '''
        a/test.tsv
        b/b2/test.tsv
        b/test.txt
        c/test.tsv
        '''
        self._run_command(['find', '--withWildcard', 'my-bucket', '**'], expected_stdout)

    def test_findversions(self):
        # Uploading content of the bucket again to create second version of each file.
        self._upload_multiple_files(self.bucket)

        self._run_command(
            ['find', '--versions', '--recursive', '--withWildcard', 'my-bucket', '**/*.csv'],
        )

        expected_stdout = '''
        a/test.tsv
        a/test.tsv
        b/b2/test.tsv
        b/b2/test.tsv
        b/test.txt
        b/test.txt
        c/test.tsv
        c/test.tsv
        '''
        self._run_command(
            ['find', '--withWildcard', '--versions', 'my-bucket', '**'], expected_stdout
        )

    def test_findno_recursive(self):
        self._run_command(['find', '--noProgress', 'my-bucket', 'b/'])

        expected_stdout = '''
        a/test.csv
        a/test.tsv
        c/test.csv
        c/test.tsv
        '''
        self._run_command(['find', '--withWildcard', 'my-bucket', '**'], expected_stdout)

    def test_finddry_run(self):
        expected_stdout = '''
        a/test.csv
        b/b/test.csv
        b/b1/test.csv
        c/test.csv
        '''
        self._run_command(
            ['find', '--recursive', '--withWildcard', '--dryRun', 'my-bucket', '**/*.csv'],
            expected_stdout,
        )

        expected_stdout = '''
        a/test.csv
        a/test.tsv
        b/b/test.csv
        b/b1/test.csv
        b/b2/test.tsv
        b/test.txt
        c/test.csv
        c/test.tsv
        '''
        self._run_command(['ls', '--withWildcard', 'my-bucket', '**'], expected_stdout)

    def test_findexact_filename(self):
        self._run_command(
            ['find', '--recursive', '--withWildcard', '--noProgress', 'my-bucket', 'b/b/test.csv'],
        )

        expected_stdout = '''
        a/test.csv
        a/test.tsv
        b/b1/test.csv
        b/b2/test.tsv
        b/test.txt
        c/test.csv
        c/test.tsv
        '''
        self._run_command(['ls', '--withWildcard', 'my-bucket', '**'], expected_stdout)

    def test_find_no_name_removes_everything(self):
        self._run_command(['find', '--recursive', '--noProgress', 'my-bucket'])
        self._run_command(['ls', 'my-bucket'], '')

    def test_find_queue_size_and_number_of_threads(self):
        self._run_command(
            ['find', '--recursive', '--threads', '2', '--queueSize', '4', 'my-bucket']
        )
        self._run_command(['ls', 'my-bucket'], '')

    def test_find_progress(self):
        expected_in_stdout = ' count: 4/4 '
        self._run_command(
            ['find', '--recursive', '--withWildcard', 'my-bucket', '**/*.csv'],
            expected_part_of_stdout=expected_in_stdout,
        )

        expected_stdout = '''
        a/test.tsv
        b/b2/test.tsv
        b/test.txt
        c/test.tsv
        '''
        self._run_command(['find', '--withWildcard', 'my-bucket', '**'], expected_stdout)

    def _run_problematic_removal(
        self,
        additional_parameters: Optional[List[str]] = None,
        expected_in_stdout: Optional[str] = None,
        unexpected_in_stdout: Optional[str] = None
    ):
        additional_parameters = additional_parameters or []

        original_delete_file_version = self.b2_api.raw_api.delete_file_version

        def mocked_delete_file_version(this, account_auth_token, file_id, file_name):
            if file_name == 'b/b1/test.csv':
                raise Conflict()
            return original_delete_file_version(this, account_auth_token, file_id, file_name)

        with mock.patch.object(
            self.b2_api.raw_api,
            'delete_file_version',
            side_effect=mocked_delete_file_version,
        ):
            self._run_command(
                [
                    'find',
                    '--delete',
                    '--recursive',
                    '--withWildcard',
                    '--threads',
                    '1',
                    '--queueSize',
                    '1',
                    *additional_parameters,
                    'my-bucket',
                    '**',
                ],
                expected_status=1,
                expected_part_of_stdout=expected_in_stdout,
                unexpected_part_of_stdout=unexpected_in_stdout,
            )

    def test_find_fail_fast(self):
        # Since we already have all the jobs submitted to another thread,
        # we can only rely on the log to tell when it stopped.
        expected_in_stdout = '''
        Deletion of file "b/b1/test.csv" (9996) failed: Conflict:
         count: 3/4'''
        unexpected_in_stdout = ' count: 5/5 '
        self._run_problematic_removal(['--failFast'], expected_in_stdout, unexpected_in_stdout)

    def test_find_skipping_over_errors(self):
        self._run_problematic_removal()

        expected_stdout = '''
        b/b1/test.csv
        '''
        self._run_command(['find', '--withWildcard', 'my-bucket'], expected_stdout)

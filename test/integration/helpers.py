######################################################################
#
# File: test/integration/helpers.py
#
# Copyright 2022 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
from __future__ import annotations

import dataclasses
import json
import logging
import os
import pathlib
import platform
import random
import re
import secrets
import shutil
import string
import subprocess
import sys
import threading
import time
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import sha256
from os import environ, linesep
from pathlib import Path
from tempfile import mkdtemp, mktemp
from typing import Any, Iterable, TypeVar

import tenacity
from b2sdk.v3 import (
    ALL_CAPABILITIES,
    BUCKET_NAME_CHARS_UNIQ,
    BUCKET_NAME_LENGTH_RANGE,
    NO_RETENTION_FILE_SETTING,
    B2Api,
    Bucket,
    EncryptionAlgorithm,
    EncryptionKey,
    EncryptionMode,
    EncryptionSetting,
    InMemoryAccountInfo,
    InMemoryCache,
    LegalHold,
    RetentionMode,
    fix_windows_path_limit,
)
from b2sdk.v3.exception import (
    BadRequest,
    BucketIdNotFound,
    FileNotPresent,
    TooManyRequests,
)

from b2._internal.console_tool import Command, current_time_millis

logger = logging.getLogger(__name__)

BUCKET_CLEANUP_PERIOD_MILLIS = timedelta(hours=3).total_seconds() * 1000
ONE_HOUR_MILLIS = 60 * 60 * 1000
ONE_DAY_MILLIS = ONE_HOUR_MILLIS * 24

BUCKET_NAME_LENGTH = BUCKET_NAME_LENGTH_RANGE[1]
BUCKET_CREATED_AT_MILLIS = 'created_at_millis'

NODE_DESCRIPTION = f'{platform.node()}: {platform.platform()} {platform.python_version()}'


def get_seed() -> str:
    """
    Get seed for random number generator.

    The `WORKFLOW_ID` variable has to be set in the CI to uniquely identify
    the current workflow (including the attempt)
    """
    seed = ''.join(
        (
            os.getenv('WORKFLOW_ID', secrets.token_hex(8)),
            NODE_DESCRIPTION,
            str(time.time_ns()),
            os.getenv('PYTEST_XDIST_WORKER', 'gw0'),
        )
    )
    return sha256(seed.encode()).hexdigest()[:16]


RNG_SEED = get_seed()
RNG = random.Random(RNG_SEED)
RNG_COUNTER = 0

if sys.version_info < (3, 9):
    RNG.randbytes = lambda n: RNG.getrandbits(n * 8).to_bytes(n, 'little')

SSE_NONE = EncryptionSetting(
    mode=EncryptionMode.NONE,
)
SSE_B2_AES = EncryptionSetting(
    mode=EncryptionMode.SSE_B2,
    algorithm=EncryptionAlgorithm.AES256,
)
_SSE_KEY = RNG.randbytes(32)
SSE_C_AES = EncryptionSetting(
    mode=EncryptionMode.SSE_C,
    algorithm=EncryptionAlgorithm.AES256,
    key=EncryptionKey(secret=_SSE_KEY, key_id='user-generated-key-id'),
)
SSE_C_AES_2 = EncryptionSetting(
    mode=EncryptionMode.SSE_C,
    algorithm=EncryptionAlgorithm.AES256,
    key=EncryptionKey(secret=_SSE_KEY, key_id='another-user-generated-key-id'),
)


def random_token(length: int, chars=string.ascii_letters) -> str:
    return ''.join(RNG.choice(chars) for _ in range(length))


def bucket_name_part(length: int) -> str:
    assert length >= 1
    global RNG_COUNTER
    RNG_COUNTER += 1
    name_part = random_token(length, BUCKET_NAME_CHARS_UNIQ)
    logger.info('RNG_SEED: %s', RNG_SEED)
    logger.info('RNG_COUNTER: %i, length: %i', RNG_COUNTER, length)
    logger.info('name_part: %s', name_part)
    logger.info('WORKFLOW_ID: %s', os.getenv('WORKFLOW_ID'))
    return name_part


T = TypeVar('T')


def wrap_iterables(generators: list[Iterable[T]]):
    for g in generators:
        yield from g


@dataclass
class Api:
    account_id: str
    application_key: str
    realm: str
    general_bucket_name_prefix: str
    this_run_bucket_name_prefix: str

    api: B2Api = None
    bucket_name_log: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        info = InMemoryAccountInfo()
        cache = InMemoryCache()
        self.api = B2Api(info, cache=cache)
        self.api.authorize_account(self.account_id, self.application_key, realm=self.realm)
        assert (
            BUCKET_NAME_LENGTH - len(self.this_run_bucket_name_prefix) > 5
        ), self.this_run_bucket_name_prefix

    def new_bucket_name(self) -> str:
        bucket_name = self.this_run_bucket_name_prefix + bucket_name_part(
            BUCKET_NAME_LENGTH - len(self.this_run_bucket_name_prefix)
        )
        self.bucket_name_log.append(bucket_name)
        return bucket_name

    def new_bucket_info(self) -> dict:
        return {
            BUCKET_CREATED_AT_MILLIS: str(current_time_millis()),
            'created_by': NODE_DESCRIPTION,
        }

    def create_bucket(self, bucket_type: str = 'allPublic', **kwargs) -> Bucket:
        bucket_name = self.new_bucket_name()
        return self.api.create_bucket(
            bucket_name,
            bucket_type=bucket_type,
            bucket_info=self.new_bucket_info(),
            **kwargs,
        )

    def _should_remove_bucket(self, bucket: Bucket) -> tuple[bool, str]:
        if bucket.name.startswith(self.this_run_bucket_name_prefix):
            return True, 'it is a bucket for this very run'
        if bucket.name.startswith(self.general_bucket_name_prefix):
            if BUCKET_CREATED_AT_MILLIS in bucket.bucket_info:
                delete_older_than = current_time_millis() - BUCKET_CLEANUP_PERIOD_MILLIS
                this_bucket_creation_time = int(bucket.bucket_info[BUCKET_CREATED_AT_MILLIS])
                if this_bucket_creation_time < delete_older_than:
                    return (
                        True,
                        f'this_bucket_creation_time={this_bucket_creation_time} < delete_older_than={delete_older_than}',
                    )
                return (
                    False,
                    f'this_bucket_creation_time={this_bucket_creation_time} >= delete_older_than={delete_older_than}',
                )
            else:
                return True, 'undefined ' + BUCKET_CREATED_AT_MILLIS
        return False, f'does not start with {self.general_bucket_name_prefix!r}'

    def clean_buckets(self, quick=False):
        # even with use_cache=True, if cache is empty API call will be made
        buckets = self.api.list_buckets(use_cache=quick)
        remaining_buckets = []
        for bucket in buckets:
            should_remove, why = self._should_remove_bucket(bucket)
            if not should_remove:
                print(f'Skipping bucket removal {bucket.name!r} because {why}')
                remaining_buckets.append(bucket)
                continue

            print('Trying to remove bucket:', bucket.name, 'because', why)
            try:
                self.clean_bucket(bucket)
            except BucketIdNotFound:
                print(f'It seems that bucket {bucket.name} has already been removed')
        print('Total bucket count after cleanup:', len(remaining_buckets))
        for bucket in remaining_buckets:
            print(bucket)

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(TooManyRequests),
        wait=tenacity.wait_exponential(),
        stop=tenacity.stop_after_attempt(8),
    )
    def clean_bucket(
        self,
        bucket_object: Bucket | str,
        only_files: bool = False,
        only_folders: list[str] | None = None,
        ignore_retentions: bool = False,
    ):
        """
        Clean contents of bucket, by default also deleting the bucket.

        Args:
            bucket (Bucket | str): Bucket object or name
            only_files (bool): If to only delete files and not the bucket
            only_folders (list[str] | None): If not None, filter to only files in given folders.
            ignore_retentions (bool): If deletion should happen regardless of files' retention mode.
        """
        bucket: Bucket
        if isinstance(bucket_object, str):
            bucket = self.api.get_bucket_by_name(bucket_object)
        else:
            bucket = bucket_object

        if not only_files:
            # try optimistic bucket removal first, since it is completely free (as opposed to `ls` call)
            try:
                return self.api.delete_bucket(bucket)
            except BucketIdNotFound:
                return  # bucket was already removed
            except BadRequest as exc:
                assert exc.code == 'cannot_delete_non_empty_bucket', exc.code

        files_leftover = False

        file_versions: Iterable[Any]
        if only_folders:
            file_versions = wrap_iterables(
                [
                    bucket.ls(
                        path=folder,
                        latest_only=False,
                        recursive=True,
                    )
                    for folder in only_folders
                ]
            )
        else:
            file_versions = bucket.ls(latest_only=False, recursive=True)

        for file_version_info, _ in file_versions:
            if file_version_info.file_retention and not ignore_retentions:
                if file_version_info.file_retention.mode == RetentionMode.GOVERNANCE:
                    print('Removing retention from file version:', file_version_info.id_)
                    self.api.update_file_retention(
                        file_version_info.id_,
                        file_version_info.file_name,
                        NO_RETENTION_FILE_SETTING,
                        True,
                    )
                elif file_version_info.file_retention.mode == RetentionMode.COMPLIANCE:
                    if file_version_info.file_retention.retain_until > current_time_millis():
                        print(
                            f'File version: {file_version_info.id_} cannot be removed due to compliance mode retention'
                        )
                        files_leftover = True
                        continue
                elif file_version_info.file_retention.mode == RetentionMode.NONE:
                    pass
                else:
                    raise ValueError(
                        f'Unknown retention mode: {file_version_info.file_retention.mode}'
                    )
            if file_version_info.legal_hold.is_on():
                print('Removing legal hold from file version:', file_version_info.id_)
                self.api.update_file_legal_hold(
                    file_version_info.id_, file_version_info.file_name, LegalHold.OFF
                )
            print('Removing file version:', file_version_info.id_)
            try:
                self.api.delete_file_version(file_version_info.id_, file_version_info.file_name)
            except FileNotPresent:
                print(
                    f'It seems that file version {file_version_info.id_} has already been removed'
                )

        if files_leftover:
            print('Unable to remove bucket because some retained files remain')
        elif not only_files:
            print('Removing bucket:', bucket.name)
            try:
                self.api.delete_bucket(bucket)
            except BucketIdNotFound:
                print(f'It seems that bucket {bucket.name} has already been removed')
        print()

    def count_and_print_buckets(self) -> int:
        buckets = self.api.list_buckets()
        count = len(buckets)
        print(f'Total bucket count at {datetime.now()}: {count}')
        for i, bucket in enumerate(buckets, start=1):
            print(f'- {i}\t{bucket.name} [{bucket.id_}]')
        return count


def print_text_indented(text):
    """
    Prints text that may include weird characters, indented four spaces.
    """
    for line in text.split(linesep):
        Command._print_helper(sys.stdout, sys.stdout.encoding, '   ', repr(line)[1:-1])


def print_output(status, stdout, stderr):
    print('  status:', status)
    if stdout != '':
        print('  stdout:')
        print_text_indented(stdout)
    if stderr != '':
        print('  stderr:')
        print_text_indented(stderr)
    print()


def serialize_enc_settings(value):
    if not isinstance(value, EncryptionSetting):
        raise TypeError
    return value.as_dict()


def print_json_indented(value):
    """
    Converts the value to JSON, then prints it.
    """
    print_text_indented(
        json.dumps(
            value, indent=4, sort_keys=True, ensure_ascii=True, default=serialize_enc_settings
        )
    )


def remove_warnings(text):
    return linesep.join(line for line in text.split(linesep) if 'DeprecationWarning' not in line)


class StringReader:
    def __init__(self):
        self.string = None

    def get_string(self):
        return self.string

    def read_from(self, f):
        try:
            self.string = f.read()
        except Exception as e:
            print(e)
            self.string = str(e)


def should_equal(expected, actual):
    print('  expected:')
    print_json_indented(expected)
    print('  actual:')
    print_json_indented(actual)
    assert expected == actual
    print()


class CommandLine:
    EXPECTED_STDERR_PATTERNS = [
        re.compile(r'^Using https?://[\w.]+$'),  # account auth
        re.compile(r'.*B/s]$', re.DOTALL),  # progress bar
        re.compile(r'^\r?$'),  # empty line
        re.compile(
            r'Encrypting file\(s\) with SSE-C without providing key id. '
            r'Set B2_DESTINATION_SSE_C_KEY_ID to allow key identification'
        ),
        re.compile(
            r'WARNING: Unable to print unicode.  Encoding for stdout is: ' r'\'[a-zA-Z0-9]+\''
        ),  # windows-bundle tests on CI use cp1252
        re.compile(r'Trying to print: .*'),
    ]

    def __init__(
        self,
        command,
        account_id,
        application_key,
        realm,
        bucket_name_prefix,
        env_file_cmd_placeholder,
        api_wrapper: Api,
        b2_uri_args,
    ):
        self.command = command
        self.account_id = account_id
        self.application_key = application_key
        self.realm = realm
        self.bucket_name_prefix = bucket_name_prefix
        self.env_file_cmd_placeholder = env_file_cmd_placeholder
        self.api_wrapper = api_wrapper
        self.b2_uri_args = b2_uri_args

    def generate_bucket_name(self):
        return self.api_wrapper.new_bucket_name()

    def get_bucket_info_args(self) -> tuple[str, str]:
        return '--bucket-info', json.dumps(self.api_wrapper.new_bucket_info(), ensure_ascii=True)

    def run_command(self, args, additional_env: dict | None = None):
        """
        Runs the command with the given arguments, returns a tuple in form of
        (succeeded, stdout)
        """
        status, stdout, stderr = self.execute(args, additional_env)
        return status == 0 and stderr == '', stdout

    def should_succeed(
        self,
        args: list[str] | None,
        expected_pattern: str | None = None,
        additional_env: dict | None = None,
        expected_stderr_pattern: str | re.Pattern = None,
    ) -> str:
        """
        Runs the command-line with the given arguments.  Raises an exception
        if there was an error; otherwise, returns the stdout of the command
        as string.
        """
        status, stdout, stderr = self.execute(args, additional_env)
        assert status == 0, f'FAILED with status {status}, stderr={stderr}'

        if expected_stderr_pattern:
            assert expected_stderr_pattern.search(
                stderr
            ), f'stderr did not match pattern="{expected_stderr_pattern}", stderr="{stderr}"'
        elif stderr != '':
            for line in (s.strip() for s in stderr.split(os.linesep)):
                assert any(
                    p.match(line) for p in self.EXPECTED_STDERR_PATTERNS
                ), f'Unexpected stderr line: {repr(line)}'

        if expected_pattern is not None:
            assert re.search(
                expected_pattern, stdout
            ), f'did not match pattern="{expected_pattern}", stdout="{stdout}"'

        return stdout.replace(os.linesep, '\n')

    @classmethod
    def prepare_env(self, additional_env: dict | None = None):
        environ['PYTHONIOENCODING'] = 'utf-8'
        env = environ.copy()
        env.update(additional_env or {})
        return env

    def parse_command(self, env):
        """
        Split `self.command` into a list of strings. If necessary, dump the env vars to a tmp file and substitute
        one the command's argument with that file's path.
        """
        command = self.command.split(' ')
        if self.env_file_cmd_placeholder:
            if any('\n' in var_value for var_value in env.values()):
                raise ValueError(
                    'Env vars containing new line characters will break env file format'
                )
            env_file_path = mktemp()
            pathlib.Path(env_file_path).write_text('\n'.join(f'{k}={v}' for k, v in env.items()))
            command = [
                (c if c != self.env_file_cmd_placeholder else env_file_path) for c in command
            ]
        return command

    def execute(
        self,
        args: list[str | Path | int] | None = None,
        additional_env: dict | None = None,
    ):
        """
        :param cmd: a command to run
        :param args: command's arguments
        :param additional_env: environment variables to pass to the command, overwriting parent process ones
        :return: (status, stdout, stderr)
        """
        # We'll run the b2 command-line by running the b2 module from
        # the current directory or provided as parameter
        env = self.prepare_env(additional_env)
        command = self.parse_command(env)

        args: list[str] = [str(arg) for arg in args] if args else []
        command.extend(args)

        print('Running:', ' '.join(command))

        stdout = StringReader()
        stderr = StringReader()

        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=platform.system() != 'Windows',
            env=env,
        )
        p.stdin.close()
        reader1 = threading.Thread(target=stdout.read_from, args=[p.stdout])
        reader1.start()
        reader2 = threading.Thread(target=stderr.read_from, args=[p.stderr])
        reader2.start()
        p.wait()
        reader1.join()
        reader2.join()

        stdout_decoded = remove_warnings(stdout.get_string().decode('utf-8', errors='replace'))
        stderr_decoded = remove_warnings(stderr.get_string().decode('utf-8', errors='replace'))

        print_output(p.returncode, stdout_decoded, stderr_decoded)
        return p.returncode, stdout_decoded, stderr_decoded

    def should_succeed_json(self, args, additional_env: dict | None = None, **kwargs):
        """
        Runs the command-line with the given arguments.  Raises an exception
        if there was an error; otherwise, treats the stdout as JSON and returns
        the data in it.
        """
        result = self.should_succeed(args, additional_env=additional_env, **kwargs)
        try:
            loaded_result = json.loads(result)
        except json.JSONDecodeError:
            raise ValueError(f'{result} is not a valid json')
        return loaded_result

    def should_fail(self, args, expected_pattern, additional_env: dict | None = None):
        """
        Runs the command-line with the given args, expecting the given pattern
        to appear in stderr.
        """
        status, stdout, stderr = self.execute(args, additional_env)
        assert status != 0, 'ERROR: should have failed'

        assert re.search(
            expected_pattern, stdout + stderr
        ), f'did not match pattern="{expected_pattern}", stdout="{stdout}", stderr="{stderr}"'

    def reauthorize(self, check_key_capabilities=False):
        """Clear and authorize again to the account."""
        self.should_succeed(['account', 'clear'])
        self.should_succeed(
            [
                'account',
                'authorize',
                '--environment',
                self.realm,
                self.account_id,
                self.application_key,
            ]
        )
        if check_key_capabilities:
            auth_dict = self.should_succeed_json(['account', 'get'])
            private_preview_caps = {
                'readBucketNotifications',
                'writeBucketNotifications',
            }
            missing_capabilities = (
                set(ALL_CAPABILITIES)
                - {'readBuckets', 'listAllBucketNames'}
                - private_preview_caps
                - set(auth_dict['allowed']['capabilities'])
            )
            assert not missing_capabilities, f'it appears that the raw_api integration test is being run with a non-full key. Missing capabilities: {missing_capabilities}'

    def list_file_versions(self, bucket_name, path=''):
        return self.should_succeed_json(
            ['ls', '--json', '--recursive', '--versions', *self.b2_uri_args(bucket_name, path)]
        )

    def cleanup_buckets(self, buckets: dict[str, dict | None]) -> None:
        for bucket_name, bucket_dict in buckets.items():
            self.cleanup_bucket(bucket_name, bucket_dict)

    def cleanup_bucket(self, bucket_name: str, bucket_dict: dict | None = None) -> None:
        """
        Cleanup bucket

        Since bucket was being handled by the tool, it is safe to assume it is cached in its cache and we don't
        need to call C class API list_buckets endpoint to get it.
        """
        if not bucket_dict:
            try:
                bucket_dict = self.should_succeed_json(['bucket', 'get', bucket_name])
            except (ValueError, AssertionError):  # bucket doesn't exist
                return

        bucket = self.api_wrapper.api.BUCKET_CLASS(
            api=self.api_wrapper.api,
            id_=bucket_dict['bucketId'],
            name=bucket_name,
        )
        self.api_wrapper.clean_bucket(bucket)


class TempDir:
    def __init__(self):
        warnings.warn(
            'TempDir is deprecated; use pytest tmp_path fixture instead',
            DeprecationWarning,
            stacklevel=2,
        )
        self.dirpath = None

    def __enter__(self):
        self.dirpath = mkdtemp()
        return Path(self.dirpath)

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(fix_windows_path_limit(self.dirpath))


def read_file(path: str | Path):
    with open(path, 'rb') as f:
        return f.read()


def write_file(path: str | Path, contents: bytes):
    with open(path, 'wb') as f:
        f.write(contents)


def file_mod_time_millis(path: str | Path) -> int:
    return int(os.path.getmtime(path) * 1000)


def set_file_mod_time_millis(path: str | Path, time):
    os.utime(path, (os.path.getatime(path), time / 1000))


def random_hex(length):
    return ''.join(RNG.choice('0123456789abcdef') for _ in range(length))

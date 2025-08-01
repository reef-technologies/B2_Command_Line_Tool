# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the 
upcoming release can be found in [changelog.d](changelog.d).

<!-- towncrier release notes start -->

## [4.4.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.4.1) - 2025-07-30


### Fixed

- Pin `docutils` version to avoid breaking the dependent `rst2ansi` library. ([#1101](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1101))


## [4.4.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.4.0) - 2025-07-30


### Changed

- Migrate to b2sdk.v3.
- Switched to cloud-based signing using DigiCert KeyLocker.

### Added

- Add multi-bucket keys support to the `key create` subcommand. ([#1083](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1083))
- Support multi-bucket keys in `key list` subcommand.

### Infrastructure

- Replace backoff with tenacity for handling retries in tests. ([#1088](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1088))
- Fix flaky integration test for multi-bucket key restrictions.
- Redesign console tools tests using b2sdk.v1 to use b2sdk.v3.
- Replace deprecated windows-2019 ci runner image with windows-2025.


## [4.3.3](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.3.3) - 2025-06-04


### Fixed

- Fix autocomplete install for `zsh`. ([#1086](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1086))

### Added

- Suggest running `b2 bucket list` on `NonExistentBucket` errors.


## [4.3.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.3.2) - 2025-04-24


### Fixed

- Bump `b2sdk` to `v2.8.1` to fix TimeoutError handling.

### Infrastructure

- Capture stdout in integration tests.
- Improve error messaging in autocomplete integration tests.
- Increase terminal size window in autocomplete integration tests.


## [4.3.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.3.1) - 2025-02-22


### Fixed

- Avoid failing on BrokenPipeError when running commands. ([#1071](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1071))
- Display error message when trying to use `--with-auth` param for `b2id://` urls in the `file url` command.

### Infrastructure

- Deleting used files by integration tests right away.


## [4.3.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.3.0) - 2025-01-07


### Fixed

- Fix shell autocompletion for Python >=3.12.8 and >=3.13.1.
- Update to b2sdk 2.7.0 to fix integration tests on Windows.

### Added

- Add `--exclude-if-uploaded-after` to `sync`.
- Add `-l` as an alias for `--long` argument.

### Infrastructure

- Fix event notification tests when introducing new keys in API outputs.
- Remove yapf in favor of ruff.
- Upgraded to pytest 8.
- Use SHA384 for Windows signing instead of expired SHA256withRSA.


## [4.2.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.2.0) - 2024-10-29


### Changed

- Remove Python 3.7 support in new releases.
  Under Python 3.7 `pip` will keep resolving the latest version of the package that supports active interpreter.
  This change comes at benefit of using newer versions of B2 CLI dependencies in `b2` standalone binary as well as in the official docker image.
  Python 3.8 is now the minimum supported version, [until it reaches EOL in October 2024](https://devguide.python.org/versions/).
  We encourage use of latest stable Python release.
  If Python interpreter upgrade from 3.7 is not an option, please use provided standalone binaries or official docker image.

### Fixed

- Update to b2sdk 2.5.1 to fix `b2 sync` stopping when encountering inaccessible directory. ([#1040](https://github.com/Backblaze/B2_Command_Line_Tool/issues/1040))
- Fix `b2 file hide b2://bucket/file` handling and test coverage.
- Fix `getdefaultlocale` deprecation warning on Python 3.11+.

### Added

- Add `b2 file server-side-copy b2id://XXX` (also accepts `b2://bucket/objectName` syntax).
  Add deprecation notice to `b2 file copy-by-id` - use `b2 file server-side-copy` instead in new scripts.
- Declare official support for Python 3.13 in `b2` CLI.
  Test `b2` CLI against Python 3.13 in CI.

### Infrastructure

- Integration tests now use reuse test buckets whenever possible to speed up test execution and prevent bucket limit exhaustion.


## [4.1.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.1.0) - 2024-07-31


### Fixed

- Update `b2sdk` to 2.5.0, to fix `TruncatedOutput` download errors when network is congested (e.g., due use of high downloader thread count). ([#554](https://github.com/Backblaze/B2_Command_Line_Tool/issues/554))

### Added

- Add `b2 file unhide` command.
- Support both new `b2_uri` and deprecated `bucket_name file_name` arguments in `b2 file hide`.


## [4.0.3](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.0.3) - 2024-06-19


### Fixed

- Fix `sync` reuploading files on re-run despite no changes in the source.
  Fixed by updating `b2sdk` to `2.4.1`.


## [4.0.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.0.2) - 2024-06-17


### Fixed

- Fix `--lifecycle-rule` validation on `python<3.10`.
- Update required `b2sdk` to `2.4.0` which includes following fixes:
  - Move scan filters before a read on filesystem access attempt.
  - Fix & improve Lifecycle Rule validation.
  - Don't retry on `NoPaymentHistory` exception.

### Doc

- Add `--lifecycle-rule` example to CLI `--help` and documentation. ([#432](https://github.com/Backblaze/B2_Command_Line_Tool/issues/432))


## [4.0.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.0.1) - 2024-05-15


### Fixed

- Fix `-` handling in file upload commands - even if file with `-` name exists, the stdin will be chosen over it.
  This change affects `b2v4` (which is also aliased as `b2`), but not `b2v3` to keep backwards compatibility.
- Fix `b2 ls b2://bucketName/fileName` and `b2 rm b2://bucketName/fileName` to respectively, list and remove file identified by supplied B2 URI.


## [4.0.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v4.0.0) - 2024-05-13


### Changed

- CLI `b2` executable now points to the latest stable ApiVer version, `b2v4`, previously it pointed to `b2v3`.
  These means following breaking changes:
  - `b2` will no longer persists credentials and other secrets on disk if credentials were passed through `B2_*` environment variables. To explicitly persist them and keep using local cache for better performance, user can simply call `b2 account account`
  - `b2 ls` and `b2 rm` no longer accept two positional arguments, instead accepting only `B2 URI` (e.g. `b2://bucketName/path`)
  - `-` is no longer supported as a valid filename, always being interpreted as standard input alias instead
- Changed `sync` command exit status code from 0 to 1 if any warnings or errors were encountered during the operation.

### Fixed

- Invalid unicode characters read from filesystem will no longer interrupt `b2 sync`

### Deprecated

- Deprecated `authorize-account`, `get-account-info` and `clear-account`, use `account {authorize|get|clear}` instead.
- Deprecated `delete-file-version`, use `rm` instead. Added `--bypass-governance` option to `rm`.
- Deprecated `file-info`, `get-url`, `cat`, `upload-file`, `download-file`, `copy-file-by-id`, `hide-file`, `update-file-legal-hold` and `update-file-retention`, use `file {info|url|cat|upload|download|copy-by-id|hide|update}` instead.
- Deprecated `get-download-url-with-auth`, use `file url` instead. Added `--with-auth` and `--duration` options to `file url`.
- Deprecated `list-buckets`, `get-bucket`, `create-bucket`, `update-bucket`, `delete-bucket`, `get-download-auth` and `notification-rules`, use `bucket {list|get|create|update|delete|get-download-auth|notification-rule}` instead.
- Deprecated `list-keys`, `create-key` and `delete-key`, use `key {list|create|delete}` instead.
- Deprecated `list-parts`, use `file large parts` instead.
  Deprecated `list-unfinished-large-files`, use `file large unfinished list` instead.
  Deprecated `cancel-large-file` amd `cancel-all-unfinished-large-files`, use `file large unfinished cancel` instead.
- Deprecated `replication-{setup|delete|pause|unpause|status}`, use `replication {setup|delete|pause|unpause|status}` instead.

### Added

- Add `account {authorize|get|clear}` commands.
- Add `bucket {list|get|create|update|delete|get-download-auth|notification-rule}` commands.
- Add `file large {parts|unfinished list|unfinished cancel}` commands.
- Add `file {info|url|cat|upload|download|copy-by-id|hide|update}` commands.
- Add `key {list|create|delete}` commands.
- Add `replication {setup|delete|pause|unpause|status}` commands.
- Allow `b2v3` to be run in official Docker image without the need to change entrypoint.

### Doc

- Automate nested subcommand documentation generation.
- Display short descriptions instead of arguments in subcommands help messages.
- Sort subcommands in `--help` alphabetically for better readability.


## [3.19.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.19.1) - 2024-04-23


### Fixed

- Fix `create-key --all-capabilities` error when using `b2sdk>=2.1`.


## [3.19.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.19.0) - 2024-04-15


### Added

- Add `notification-rules` commands for manipulating Bucket notification rules as part of Event Notifications feature Private Preview.
  See https://www.backblaze.com/blog/announcing-event-notifications/ for details.


## [3.18.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.18.0) - 2024-04-02


### Changed

- Change all `_b2v4 --camelCase` CLI flags to --kebab-case.
  Add deprecation warning for `b2v3 --camelCase` CLI flags.

### Fixed

- Don't persist credentials provided in the Environment variables in any command other than `authorize-account` when using `b2v4`.
- Fix `b2 --help` showing full binary path instead of just basename.

### Added

- Add autocomplete support for `zsh` and `fish` shells.
- Add support for calling `b2 ls` without arguments to list all buckets.

### Infrastructure

- Add dockerhub description deployment to CD workflow.
- Add support for pre-releases in CD.
- Fix missing command output when running `nox` under CI.
- Increase verbosity when running tests under CI.
- Update to [GitHub Actions using Node 20](https://github.blog/changelog/2023-09-22-github-actions-transitioning-from-node-16-to-node-20/).


## [3.17.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.17.0) - 2024-03-15


### Fixed

- Control character escaping is now enabled by default if running in a terminal for improved security.

### Added

- Added `--escape-control-characters` and `--no-escape-control-characters` flags,
  as well as `B2_ESCAPE_CONTROL_CHARACTERS` env var to explicitly enable or disable control character escaping.


## [3.16.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.16.1) - 2024-02-26


### Fixed

- Fix `--threads` option being silently ignored in upload commands.


## [3.16.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.16.0) - 2024-02-19


### Changed

- All internal Python modules were moved to the `b2._internal` package to further discourage users from importing them.
- Change `ls` and `rm` commands to use the `b2://` URI scheme in the pre-release `_b2v4` command.

### Fixed

- Fix `--minPartSize` not supporting values above 100MB.
- Fix a bug where `rm bucketName folderName` command without the `--recursive` flag would
  remove a first file from every subdirectory inside `folderName`.
- Fix handling of `?` and `#` in B2 URI.

### Added

- ApiVer introduced. `b2` executable points to the latest stable ApiVer version, while
  `b2v3` will always point to v3 ApiVer release of `b2` CLI.
- Add `--include` and `--exclude` filters to the `ls` and `rm` commands.
- Add support for deleting a single file by `b2id://` URI in the pre-release `_b2v4` command.
- Print account info if `b2 authorize-account` is successful using the same format as `b2 get-account-info`.
- Print output file path in `download-file` command.

### Infrastructure

- Fix CI failing on `mkdir` when testing docker image.
- Use pdm for building, testing and managing dependencies.
- Remove unnecessary files (continuous integration scripts, tests) from sdist tarball.


## [3.15.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.15.0) - 2023-12-07


### Changed

- Use Python 3.12 in the official `b2` Docker image.

### Fixed

- Loosen platformdirs dependency version specifier.

### Added

- Whenever target filename is a directory, file is downloaded into that directory.


## [3.14.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.14.0) - 2023-12-06


### Changed

- Update b2sdk to 1.28.0 (resolves [#958](https://github.com/Backblaze/B2_Command_Line_Tool/issues/958), [#934](https://github.com/Backblaze/B2_Command_Line_Tool/issues/934)).

### Fixed

- Don't print `Using https://REALM" in stderr unless explicitly set by user. ([#949](https://github.com/Backblaze/B2_Command_Line_Tool/issues/949))
- Added autocomplete suggestion caching to improve autocomplete performance.
- Do not include build cache in official `b2` docker image.
- Fix an error that caused multiprocessing semaphores to leak on OSX.

### Deprecated

- Deprecated `download-file-by-id` and `download-file-by-name`, use `download-file` instead.
  Deprecated `get-file-info`, use `file-info` instead.
  Deprecated `make-url` and `make-friendly-url`, use `get-url` instead.

### Added

- Add `--expires`, `--content-disposition`, `--content-encoding`, `--content-language` options to subcommands `upload-file`, `upload-unbound-stream`, `copy-file-by-id`.
- Add `download-file`, `file-info` and `get-url` commands using new B2 URI syntax allowing for referring to file-like objects by their bucket&name or ID.

### Doc

- Add `cat` command to documentation.
- Add additional linebreaks to ensure lists are properly rendered.

### Infrastructure

- Ensure CI checks Python package compatibility with latest setuptools. ([#952](https://github.com/Backblaze/B2_Command_Line_Tool/issues/952))
- Allow skipping changelog for PRs marked with `-changelog` label.
- Changelog entries are now validated as a part of CI pipeline.
- Disable dependabot requests for updates unrelated to security issues.
- Fix CI badge not showing correct status in README.
- Remove unused exception class and outdated todo.
- Skip draft step in releases - all successful releases are public.
- Update license text generation dependencies to prevent triggering security scan false-positives.
- Use cpython 3.12 (not 3.11) for integration tests with secrets.


## [3.13.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.13.1) - 2023-11-21


### Fixed

- Fix "pip install" by making pyproject.toml viable. ([#952](https://github.com/Backblaze/B2_Command_Line_Tool/issues/952))

### Doc

- Fix `docker run` example in README.md

### Infrastructure

- Towncrier changelog generation - to avoid conflicts when simultaneously working on PRs
- fix towncrier generated changelog to work with mindsers/changelog-reader-action


## [3.13.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.13.0) - 2023-11-16

### Added
- Add linux/arm64 platform support to the official Docker image
- Add `cat` command for downloading file contents directly to stdout
- Add `-r` as an alias for `--recursive` argument
- Add `-q` as an alias for `--quiet` argument

### Fixed
- Emit `Using https://api.backblazeb2.com` message to stderr instead of stdout, therefor prevent JSON output corruption

### Changed
- Stream `ls --json` JSON output instead of dumping it only after all objects have been fetched
- Alias `-` to stdout in `download-file-by-name` or `download-file-by-id` command

## [3.12.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.12.0) - 2023-10-28

### Added
- docker tests and pushing the official docker image on release

### Fixed
- `--quiet` now will implicitly set `--noProgress` option as well
- pypy integration tests

### Infrastructure
- Use stable Python 3.12 in CI
- Fix readthedocs build by updating to v2 configuration schema

## [3.11.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.11.0) - 2023-10-04

### Added
- Add `--quiet` option to all commands to suppress all messages printed to stdout & stderr

### Changed
- Improve `--quiet` and `--profile` options documentation mentions, while suppressing them in `--help` output

### Infrastructure
- Fix gathering licenses of typeshed libraries
- Fix spellcheck erroring out on LICENSE file

## [3.10.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.10.1) - 2023-09-27

### Fixed
- Fix lifecycle rules being cleared after using `update-bucket` command if not explicitly set again.
- Fix missing key ID for large file encrypted with SSE-C (fixed by `b2sdk` update)

### Infrastructure
- Fix bad version number generation in CD

## [3.10.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.10.0) - 2023-09-10

### Added
- Add ability to upload from an unbound source such as standard input or a named pipe
- --bypassGovernance option to delete_file_version
- Declare official support of Python 3.12
- Cache-Control option when uploading files
- Add `--lifecycleRule` to `create-bucket` and `update-bucket` and deprecate `--lifecycleRules` argument
- Add extra dependencies for better UX, installable with `pip install b2[full]`
- Add s3 endpoint to `get-account-info`

### Deprecated
- Deprecate support of `-` as a valid filename in `upload-file` command. In the future `-` will always be interpreted as standard input

### Changed
- Better help text for --corsRules
- if `--threads` is not explicitly set, number of threads is no longer guaranteed to be 10 

### Infrastructure
- Remove unsupported PyPy 3.7 from tests matrix and add PyPy 3.10 instead
- Autocomplete integration tests will now work properly even if tested package has not been installed
- Automatically set copyright date when generating the docs
- Increase timeout time in autocomplete tests to accommodate slower CI environments
- Update pyinstaller to fix Linux Bundle build
- Replace `pyflakes` with `ruff` for linting
- Make dependency version pinning less restrictive
- Fix tests by making mocks compatible with latest `b2sdk` version
- Fix readthedocs build

### Fixed
- Fast rm sometimes failing due to a rare race condition
- Fix UnicodeEncodeError in non-Unicode terminals by prioritizing stdout encoding
- When listing licenses in `license` command only show licenses of `b2` and its dependencies
- Fix license command failing on Windows when non-UTF8 encoding is the default

## [3.9.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.9.0) - 2023-04-28

### Added
- Support for custom file upload timestamp

### Infrastructure
- Limit GitHub CI workload by running most integration tests only against edge versions of supported Python versions
- Add a direct dependency from tqdm

## [3.8.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.8.0) - 2023-03-23

### Added
- Add `install-autocomplete` command for installing shell autocompletion (currently only `bash` is supported)

### Fixed
- Hitting the download endpoint twice in some cases

### Infrastructure
- GitHub CD builds and uploads an official B2 CLI image to docker hub
- Disable changelog verification for dependabot PRs

## [3.7.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.7.1) - 2023-02-08

### Fixed
- Remove unnecessary printing options from `rm`
- Clarify that `--recursive` is required when `--withWildcard` is used
- Adjust description of `rm`

### Infrastructure
- Remove macos stand-alone binary from CI/CD

## [3.7.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.7.0) - 2023-02-07

### Added
- Add `--incrementalMode` to `sync` and `upload-file`
- Add `license` command for printing licenses of b2 and libraries
- Add wildcard support for the `ls` command
- Add `rm` command

### Fixed
- Stop using b2sdk.v1 in arg_parser.py
- Fix issues when running commands on Python 3.11
- Fix tests after changes introduced in b2sdk 1.19.0
- `rm` can handle any number of files

### Infrastructure
- GitHub CI got checkout action updated to v3 and setup-python to v4
- Ensured that changelog validation only happens on pull requests
- GitHub CI uses GITHUB_OUTPUT instead of deprecated set-output
- Releases now feature digests of each file
- Change default Python version in CI/CD to 3.11
- Temporary marking all directories as `safe.directory` inside CI/CD when bundling

## [3.6.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.6.0) - 2022-09-20

### Added
- Add `replication-delete` command
- Add `replication-pause` command
- Add `replication-status` command
- Add `replication-unpause` command
- Add `--include-existing-files` to `replication-setup`
- Add `--max-streams` parameter to download commands
- Add `--fileLockEnabled` switch to `update-bucket` subcommand

### Fixed
- Fix `replication-setup` default priority setter

### Infrastructure
- Fix warnings in tests
- Fix `test_keys` unit test after changes in b2sdk
- Fix running tests on the CI with the latest SDK from the master branch

## [3.5.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.5.0) - 2022-07-27

As in 3.4.0, replication support may be unstable, however no backward-incompatible
changes are currently planned.
This version is pinned strictly to `b2-sdk-python==1.17.3` for the same reason.

### Added
- Add `--write-buffer-size` parameter
- Add `--skip-hash-verification` parameter

### Changed
- Minimum MacOS version from 10.15 to 11.0

### Infrastructure
- Try not to crash tests due to bucket name collision
- Fix replication integration tests
- Fix leaking buckets in integration tests
- Limit number of workers for integration tests to 1 for now
- Make integration tests remove buckets only based on name, not based on creation time
- Add dependabot configuration

## [3.4.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.4.0) - 2022-05-04

This release contains a preview of replication support. It allows for basic usage
of B2 replication feature (currently in closed beta). Until this notice is removed,
the interface of replication related functionality should be not considered as public
API (as defined by SemVer).
This version is pinned strictly to `b2-sdk-python==1.16.0` for the same reason.

### Added
- Add basic replication support to `create-bucket` and `update-bucket`
- Add more fields to `get-account-info` json
- Add `--replication` to `ls --long`
- Add `replication-setup` command
- Add "quick start guide" to documentation

### Changed
- Made `bucketType` positional argument to `update-bucket` optional
- Run unit tests on all CPUs

## [3.3.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.3.0) - 2022-04-20

### Added
- Add `--threads` parameter to `download-file-by-name` and `download-file-by-id`
- Add `--uploadThreads` and `--downloadThreads` parameters to `sync`
- Add `--profile` switch support
- Add `applicationKeyId` and `isMasterKey` to the output of `get-account-info`

### Changed
- Rename `--threads` parameter for `--sync` to `--syncThreads`

### Fixed
- Fix license header checker on Windows
- Fix `UnicodeEncodeError` after successful SSE-C download on a non-utf8 terminal (#786)

### Removed
- Remove official support for python 3.5
- Remove official support for python 3.6

## [3.2.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.2.1) - 2022-02-23

### Fixed
- Fix setting permissions for local sqlite database (thanks to Jan Schejbal for responsible disclosure!)

## [3.2.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.2.0) - 2021-12-23

### Added
- Add compatibility support for arrow >= 1.0.2 on newer Python versions while
  continuing to support Python 3.5

### Fixed
- Fallback to `ascii` decoder when printing help in case the locales are not properly set
- Apply the value of `--threads` parameter to `sync` downloader threads

## [3.1.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.1.0) - 2021-11-02

### Added
- Add `--allCapabilities` to `create-key`
- Add support for Python 3.10

### Fixed
- Fix testing bundle in CI for a new `staticx` version

## [3.0.3](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.0.3) - 2021-09-27

### Fixed
- Fix pypy selector in CI
- Fix for static linking of Linux binary (CD uses python container)

## [3.0.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.0.2) - 2021-09-17

### Added
- Sign Windows binary

### Changed
- Download instruction in README.md (wording suggested by https://github.com/philh7456)
- Make Linux binary statically linked

## [3.0.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.0.1) - 2021-08-09

### Fixed
- logs from all loggers (in dependencies too) brought back

## [3.0.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v3.0.0) - 2021-08-07

### Added
- Add possibility to change realm during integration tests
- Add possibility to install SDK from local folder instead of pypi when running tests
- Add full support of establishing file metadata when copying, with either source or target using SSE-C
- Add `--noInfo` option to `copy-file-by-id`
- Integration test for checking if `bad_bucket_id` error code is returned

### Fixed
- Fix integration tests on non-production environments
- Fix warnings thrown by integration tests
- delete-key unit test adjusted to a less mocked simulator
- Fix integration test cleanup
- Representing encryption-related metadata in buckets and file versions is now consistent

### Changed
- CLI now uses `b2sdk.v2`
- Downloading files prints file metadata as soon as the download commences (not when it finishes)
- New way of establishing location of the SQLite cache file, using `XDG_CONFIG_HOME` env var
- Downloaded file's metadata is complete and is displayed before the file is downloaded, a `Download finished` message
  is issued at the end
- `contentLength` changed to `size` where appropriate
- Log configuration: stack traces are not printed in case of errors by default, `--verbose` changes that
- Log configuration arguments behaviour altered: `--logConfig` is exclusive with `--verbose` and `--debugLogs`
- Log configuration arguments behaviour altered: `--verbose` and `--debugLogs` can be used at the same time
  (and they will both be taken into account)

### Removed
- Support of `--metadataDirective` argument in `copy-file-by-id` (the `metadataDirective` sent to B2 cloud is
  detected automatically)

## [2.5.1](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.5.1) - 2021-08-06

- `SRC_LAST_MODIFIED_MILLIS` import fix

## [2.5.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.5.0) - 2021-05-22

### Added
- Add integration test for sync within one bucket with different encryption
- Notarize OSX binary
- File lock arguments and new commands

### Fixed
- Fixed breaking integration test case
- Add zoneinfo to the Windows bundle
- Fixed unit tests failing on new attributes of FileVersionInfo
- Removing old buckets in integration tests
- Bucket name entropy in tests increased

## [2.4.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.4.0) - 2021-04-22

### Added
- Sign OSX binary
- Add support for SSE-C server-side encryption mode

### Fixed
- Exclude packages inside the test package when installing

## [2.3.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.3.0) - 2021-03-25

### Added
- Add support for SSE-B2 server-side encryption mode

### Fixed
- Pin `setuptools-scm<6.0` as `>=6.0` doesn't support Python 3.5
- Fix boot speed regression caused by the `rst2ansi` invocations

## [2.2.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.2.0) - 2021-03-15

### Added
- Option to automatically authorize account when running commands other than `authorize-account` via
  `B2_APPLICATION_KEY_ID` and `B2_APPLICATION_KEY` env vars

### Changed
- Improve setup and teardown for the integration tests
- Use `setuptools-scm` for versioning
- Improve CLI and RTD descriptions of the commands
- Add upper version limit for arrow dependency, because of a breaking change

### Fixed
- Fix for the Windows bundled version
- Fix docs autogen

## [2.1.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.1.0) - 2020-11-03

### Added
- Add support for Python 3.9
- Add a possibility to append a string to the User-Agent via `B2_USER_AGENT_APPEND` env

### Changed
- Update `b2 sync` usage text for bucket-to-bucket sync

### Removed
- Drop Python 2 support :tada: (for old systems you can now use the [binary distribution](https://www.backblaze.com/b2/docs/quick_command_line.html))
- Remove `--prefix` from `ls` (it didn't really work, use `folderName` argument)
- Clean up legacy code (`CliBucket`, etc.)

### Fixed
- Fix docs generation in CI
- Correct names of the arguments in `b2 create-key` usage text

## [2.0.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.0.2) - 2020-07-15

### Added
- Add `--environment` internal parameter for `authorize-account`

## [2.0.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v2.0.0) - 2020-06-25

### Added
- Add official support for python 3.8
- Add `make-friendly-url` command
- Add `--excludeIfModifiedAfter` parameter for `sync`
- Add `--json` parameter to `ls` and `list-buckets`
- Introduce bundled versions of B2 CLI for Linux, Mac OS and Windows

### Changed
- Switch to b2sdk api version v1: remove output of `delete-bucket`
- Use b2sdk >1.1.0: add large file server-side copy
- Switch option parser to argparse: readthedocs documentation is now generated automatically
- Normalize output indentation level to 4 spaces

### Removed
- Remove the ability to import b2sdk classes through b2cli (please use b2sdk directly)
- Remove official support for python 3.4
- Remove `list-file-names` command. Use `ls --recursive --json` instead
- Remove `list-file-versions` command. Use `ls --recursive --json --versions` instead

## [1.4.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.4.2) - 2019-10-03

### Added
- Add `prefix` parameter to `list-file-names` and `list-file-versions`
- Add support for (server-side) copy-file command

### Changed
- Make parameters of `list-file-names` and `list-file-versions` optional (use an empty string like this: `""`)
- (b2sdk) Fix sync when used with a key restricted to filename prefix
- When authorizing with application keys, optional application key ID and
  application key can be added using environment variables
  B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY respectively.

## [1.4.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.4.0) - 2019-04-25

### Added
- (b2sdk) Support for python 3.7

### Changed
- Renaming accountId for authentication to application key Id
    Note: this means account Id is still backwards compatible,
    only the terminology has changed.
- Most of the code moved to b2sdk [repository](https://github.com/Backblaze/b2-sdk-python) and [package](https://pypi.org/project/b2sdk/)
- (b2sdk) Fix transferer crashing on empty file download attempt
- (b2sdk) Enable retries of non-transfer operations
- (b2sdk) Enable continuation of download operations

### Deprecated
- Deprecation warning added for imports of sdk classes from cli package

## [1.3.8](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.3.8) - 2018-12-06

### Added
- New `--excludeAllSymlinks` option for `sync`.
- Faster downloading of large files using multiple threads and bigger buffers.

### Fixed
- Fixed doc for cancel-all-unfinished-large-files

## [1.3.6](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.3.6) - 2018-08-21

### Fixed
- Fix auto-reauthorize for application keys.
- Fix problem with bash auto-completion module.
- Fix (hopefully) markdown display in PyPI.

## [1.3.4](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.3.4) - 2018-08-10

### Fixed
- Better documentation for authorize-account command.
- Fix error reporting when using application keys
- Fix auth issues with bucket-restricted application keys.

## [1.3.2](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.3.2) - 2018-07-28

### Fixed
- Tests fixed for Python 3.7
- Add documentation about what capabilities are required for different commands.
- Better error messages for authorization problems with application keys.

## [1.3.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.3.0) - 2018-07-20

### Added
- Support for [application keys](https://www.backblaze.com/b2/docs/application_keys.html).
- Support for Python 3.6
- Drop support for Python 3.3 (`setuptools` no longer supports 3.3)

### Changed
- Faster and more complete integration tests

### Fixed
- Fix content type so markdown displays properly in PyPI
- The testing package is called `test`, not `tests`

## [1.2.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.2.0) - 2018-07-06

### Added
- New `--recursive` option for ls
- New `--showSize` option for get-bucket
- New `--excludeDirRegex` option for sync

### Fixed
- Include LICENSE file in the source tarball. Fixes #433
- Test suite now runs as root (fixes #427)
- Validate file names before trying to upload
- Fix scaling problems when syncing large numbers of files
- Prefix Windows paths during sync to handle long paths (fixes #265)
- Check if file to be synced is still accessible before syncing (fixes #397)

## [1.1.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.1.0) - 2017-11-30

### Added
- Add support for CORS rules in `create-bucket` and `update-bucket`.  `get-bucket` will display CORS rules.

### Fixed
- cleanup in integration tests works

## [1.0.0](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v1.0.0) - 2017-11-09

### Added
- Require `--allowEmptySource` to sync from empty directory, to help avoid accidental deletion of all files.

## [0.7.4](https://github.com/Backblaze/B2_Command_Line_Tool/releases/tag/v0.7.4) - 2017-11-09

### Added
- More efficient uploads by sending SHA1 checksum at the end.

### Fixed
- File modification times are set correctly when downloading.
- Fix an off-by-one issue when downloading a range of a file (affects library, but not CLI).
- Better handling of some errors from the B2 service.

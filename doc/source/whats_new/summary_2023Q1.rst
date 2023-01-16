.. footer::
    ###Page### / ###Total###

.. _2023q1_in_b2_cli:

################
2023Q1
################


.. _2023q1_ls_command:

************************
LS command with wildcard
************************

So far you've been able to list the content of the bucket limiting ourselves to certain directories. Now you can specify a bash-like pattern that the files will match.

Let's say that you have a bucket ``BUCKET`` that contains multiple ``.csv`` files among others. If you want to list all the ``.csv`` files, you can simply run the following:

.. code-block:: bash

    b2 ls --withWildcard --recursive BUCKET "*.csv"

.. todo: enter actual result of the command here.

Note that the ``"*.csv"`` is enclosed in quotes. This is to stop ``bash`` from expanding it. Also note that a single asterisk (``*``) matches everything, including directories.

The pattern below shows off most of the remaining capabilities:

.. code-block:: bash

    b2 ls --withWildcard --recursive BUCKET "dir_?/file_[!2].[tc]sv"

``?`` matches any single character, ``[!2]`` matches only entries that doesn't have ``2`` in the given place and ``[tc]`` matches everything that has either ``t`` or ``c`` in given position.


It's worth noting that whenever you want to use ``--withWildcard`` it requires ``--recursive`` as well.


.. _2023q1_rm_command:

**********
RM command
**********

Removing files from B2 just became a lot easier. Using the same engine that powers the ``ls`` command, you can now use the ``rm`` command.

.. code-block:: bash

    b2 rm --withWildcard --recursive BUCKET "temp_dir/*.csv"

.. todo: enter actual result of the command here.

will remove every single ``.csv`` file from the ``temp_dir`` directory.

To determine what files are to be removed, you have two options. First one is to use ``ls`` command, the second one is to use the ``--dryRun`` option to the ``rm`` command.

.. code-block:: bash

    b2 rm --withWildcard --recursive --dryRun BUCKET "production_dir/*.tsv"

.. todo: enter actual result of the command here.

Removal happens in parallel in multiple threads. You can specify the number of threads removing objects by providing the ``--threads NUM_THREADS`` option. Also, if you want to e.g. check whether you have the proper rights you can add the ``--failFast`` option to ensure that the command will stop after the first encountered issue. Otherwise it'll try to remove each and every file, hoping for the best.


.. _2023q1_incremental_upload:

*************************
Incremental upload / sync
*************************

Both ``upload-file`` and ``sync`` commands got a new option – ``--incremental``. This is perfect for files that are just appended, like logs. Whenever a file is uploaded with this option we first check whether the hash of the start of the local file matches the hash of the file that's already on B2. If it does, the command will make a copy of it and upload only the new part at the end of the file.

The question remains about large files – these don't have ``SHA1`` calculated by default. But whenever you upload a file with this new version of B2Cli, a file will have a new metadata called ``large_file_sha1`` – and the ``--incremental`` option will use it to compare files whenever applicable.


.. _2023q1_stdin_streaming:

********************
Streaming from STDIN
********************

``upload-file`` command now has the ability to accept a stream of bytes from standard input when the local file is specified as dash (``-``). Whatever you pipe into it will become the content of the file in B2. You can e.g. compress the content of the whole directory on the fly.

.. code-block:: bash

    tar -czf - large_directory | b2 upload-file BUCKET - large_directory.tar.gz

.. todo: enter actual result of the command here.


.. _2023q1_libcurl:

****************************
experimental libcurl support
****************************

So far, ``b2`` console tool has used ``urllib3`` for communication. With this new release you can also use ``libcurl`` as an alternative. One attractive option that ``libcurl`` provides over ``urllib3`` is full support for ``100-continue``.

If your system already has ``libcurl`` installed (e.g. on Ubuntu the package is ``libcurl4-openssl-dev``), the new ``b2`` will use it out of the box.

You can control it by providing ``--urllib`` and ``--libcurl`` options. Note that ``--urllib`` will always work while providing ``--libcurl`` on a system where ``libcurl`` is not available or misconfigured will result in an error.


.. _2023q1_dockerfile:

**********************
Official B2 Dockerfile
**********************

For those willing to use ``b2`` console tool without installing any ``Python`` or a standalone release, it's now possible using ``docker``.

.. code-block:: bash

    docker run --rm -it -v <absolute-local-path-to-account-info>:/b2 b2:latest authorize-account
    docker run --rm -v <absolute-local-path-to-account-info>:/b2 b2:latest create-bucket test-bucket allPrivate
    docker run --rm -v <absolute-local-path-to-account-info>:/b2 -v <absolute-local-path-to-data>:/data b2:latest upload-file test-bucket /data/local-file remote-file

As an alternative, one can use environmental variables for authorisation.

.. code-block:: bash

    B2_APPLICATION_KEY=<key> B2_APPLICATION_KEY_ID=<key-id> docker run --rm -e B2_APPLICATION_KEY -e B2_APPLICATION_KEY_ID b2:latest authorize-account
    B2_APPLICATION_KEY=<key> B2_APPLICATION_KEY_ID=<key-id> docker run --rm -e B2_APPLICATION_KEY -e B2_APPLICATION_KEY_ID b2:latest create-bucket test-bucket allPrivate
    B2_APPLICATION_KEY=<key> B2_APPLICATION_KEY_ID=<key-id> docker run --rm -e B2_APPLICATION_KEY -e B2_APPLICATION_KEY_ID -v <absolute-local-path-to-data>:/data b2:latest upload-file test-bucket /data/local-file remote-file

.. footer::
    ###Page### / ###Total###

.. _2022q3_in_b2_cli:

################
2022Q3
################


.. _2022q3_profiles:

*****************
Multiple profiles
*****************

One of the new features that ``B2 CLI`` offers now, is the ability to use multiple profiles. Each of them may lead to any key/account-id pair, including other accounts.

.. note::

    Environmental variables ``B2_APPLICATION_KEY_ID`` and ``B2_APPLICATION_KEY`` take precedence over profiles, so you might consider unsetting those before proceeding.

    .. code-block:: bash

        $ unset B2_APPLICATION_KEY_ID
        $ unset B2_APPLICATION_KEY

New profiles are created using ``authorize-account`` with the ``--profile`` option.

.. code-block:: bash

    $ b2 authorize-account --profile <profile-name>

With multiple profiles it's easier than ever to use different accounts, keys and regions.


.. _2022q3_replication:

***********
Replication
***********

Using replication, you can ask ``B2`` to copy everything from our source bucket to the destination bucket.

.. code-block:: bash

    $ b2 replication-setup <source-bucket-name> <destination-bucket-name>


Setup between different accounts can be accomplished by using the ``--destination-profile`` option.

.. code-block:: bash

    $ b2 replication-setup --destination-profile <profile-name> <source-bucket-name> <destination-bucket-name>


You can check the status of the replication via ``replication-status`` command:

.. code-block:: bash

    $ b2 replication-status <source-bucket-name>

Expected output looks like this:

.. code-block::

    Replication "<name of the replication rule>":
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    | source        | source   | source       | source     | source      | source   | destination   | metadata   | hash      |   count |
    | replication   | has      | encryption   | has        | has         | has      | replication   | differs    | differs   |         |
    | status        | hide     | mode         | large      | file        | legal    | status        |            |           |         |
    |               | marker   |              | metadata   | retention   | hold     |               |            |           |         |
    +===============+==========+==============+============+=============+==========+===============+============+===========+=========+
    | COMPLETED     | No       | NONE         | No         | No          | No       |               |            |           |      82 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    |               | Yes      | NONE         | No         | No          | No       |               |            |           |      30 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    | COMPLETED     | No       | SSE_B2       | No         | No          | No       |               |            |           |      10 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    |               | Yes      | NONE         | No         | No          | No       | REPLICA       | Yes        | Yes       |      16 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    | COMPLETED     | No       | NONE         | No         | No          | No       | REPLICA       | No         | No        |      38 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+
    | COMPLETED     | No       | SSE_B2       | No         | No          | No       | REPLICA       | No         | No        |      11 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+


You can see even more details if we use ``ls --long`` with a new ``--replication`` option.

.. code-block:: bash

    $ b2 ls --long --replication <source-bucket-name>
    <file-id>  upload  2022-12-20  08:32:00       2048  COMPLETED  data1.bin
    $ b2 ls --long --replication <destination-bucket-name>
    <file-id>  upload  2022-12-20  08:32:00       2048  REPLICA  data1.bin


We've only scratched the surface here. For full list of options (e.g. ability to replicate only files that have a common prefix) check:

.. code-block:: bash

    $ b2 replication-setup --help

Other commands connected to the replication include:

.. code-block:: bash

    $ b2 replication-delete --help
    $ b2 replication-pause --help
    $ b2 replication-unpause --help
    $ b2 replication-status --help


.. _2022q3_controlling_downloads_parallelization:

*************************************
Controlling downloads parallelization
*************************************

So far the ``--threads`` option was only available to ``sync`` and ``upload-file`` commands. This was expanded to both ``download-file-by-name`` and ``download-file-by-id`` to allow for better control over download performance.

Also, ``sync`` command now has better control over the threads, with addition of ``--syncThreads``, ``--downloadThreads`` and ``--uploadThreads``. While the last two are self-explanatory, ``--syncThreads`` defines a number of parallel threads that perform scanning and schedule actions. ``--threads`` can still be used, however it is incompatible with new options.


.. _2022q3_write_buffer_size:

******************************
``--write-buffer-size`` option
******************************

If you want to optimize download of a file or sync operation, you can now specify the size of the internal buffer from which the data is streamed to the disk. Default size of this buffer can be obtained by running:

.. code-block:: bash

    $ python -c "import io; print(io.DEFAULT_BUFFER_SIZE)"

However, specifying a larger value can lead to a better performance when downloading large files.

To use this new option, it's enough to add ``--write-buffer-size`` option with value in bytes, like this:

.. code-block:: bash

    $ b2 download-file-by-name --write-buffer-size $((20 * 1024 * 1024)) <bucket> <file-name> <file-target>

This will use 20 megabytes of buffer for writing, sacrificing some memory to reduce i/o.

.. note::

    Size of data each thread is trying to read from the B2 is also controlled by this value. It's not beneficial to set it to some artificially high value. Sadly, one, universal constant cannot be provided. "The best" value has to be found empirically for each setup of the network / drive bandwidth pair.


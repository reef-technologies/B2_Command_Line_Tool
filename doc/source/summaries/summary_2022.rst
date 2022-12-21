.. footer::
    ###Page### / ###Total###

.. _2022_in_b2_cli:

##############
2022 in B2 CLI
##############


.. _profiles:

*****************
Multiple profiles
*****************

One of the new features that ``B2 CLI`` offers now, is the ability to use multiple profiles. Each of them may lead to any key/account-id pair, including other accounts.

.. note::

    Environmental variables ``B2_APPLICATION_KEY_ID`` and ``B2_APPLICATION_KEY`` take precedence over profiles, so you might consider unsetting them before proceeding.

    .. code-block:: bash

        $ unset B2_APPLICATION_KEY_ID
        $ unset B2_APPLICATION_KEY

New profiles are created using ``authorize-account`` with the ``--profile`` option.

.. code-block:: bash

    $ b2 authorize-account --profile <profile-name>

With multiple profiles it's easier than ever to safely handle data and buckets. One could consider making a ``master`` profile, which uses the most powerful key, while having the default profile have read-only capabilities and additional profiles limited to particular buckets and/or particular capabilities.


.. _replication:

***********
Replication
***********

We can ask ``B2`` to copy everything from our source bucket to the destination bucket.

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
    | COMPLETED     | No       | NONE         | No         | No          | No       | REPLICA       | No         | No        |       1 |
    +---------------+----------+--------------+------------+-------------+----------+---------------+------------+-----------+---------+

We can see more details if we use ``ls --long`` with a new ``--replication`` option.

.. code-block:: bash

    $ b2 ls --long --replication <source-bucket-name>
    <file-id>  upload  2022-12-20  08:32:00       2048  COMPLETED  data1.bin
    $ b2 ls --long --replication <destination-bucket-name>
    <file-id>  upload  2022-12-20  08:32:00       2048  REPLICA  data1.bin


We've only scratched the surface here. For full list of options (e.g. ability to sync only files that have a common prefix) check:

.. code-block:: bash

    $ b2 replication-setup --help

Other commands connected to the replication include:

.. code-block:: bash

    $ b2 replication-delete --help
    $ b2 replication-pause --help
    $ b2 replication-unpause --help
    $ b2 replication-status --help


.. _controlling_downloads_parallelization:

*************************************
Controlling downloads parallelization
*************************************

So far the ``--threads`` option was only available to ``sync`` and ``upload-file`` commands. This was expanded to both ``download-file-by-name`` and ``download-file-by-id``. Users with capable networks can now download large files with multiple threads significantly speeding up the transfer.

Also, ``sync`` command now has better control over the threads, with addition of ``--syncThreads``, ``--downloadThreads`` and ``--uploadThreads``. While the last two are self-explanatory, ``--syncThreads`` defines a number of parallel threads that perform scanning and schedule actions. ``--threads`` can still be used, however it is incompatible with new options.


.. _write_buffer_size:

******************************
``--write-buffer-size`` option
******************************

If we want to optimize download of a file or sync operation, we can now specify the size of the internal buffer from which the data is streamed to the disk. Default size of this buffer can be obtained by running:

.. code-block:: bash

    $ python -c "import io; print(io.DEFAULT_BUFFER_SIZE)"

However, specifying a larger value can lead to a better performance. Especially if we're downloading large files.

To use this new option, it's enough to add ``--write-buffer-size`` option with value in bytes, like this:

.. code-block:: bash

    $ b2 download-file-by-name --write-buffer-size $((20 * 1024 * 1024)) <bucket> <file-name> <file-target>

This will provide you with 20 megabytes of buffer for writing.

.. note::

    Size of data each thread is trying to read from the B2 is also controlled by this value. It's not beneficial to set it to some artificially high value. Sadly, one, universal constant cannot be provided. "The best" value has to be found empirically for each setup of the network / drive bandwidth pair.


.. _cve_2022_23653_defeated:

***********************
CVE-2022-23653 defeated
***********************

While not a feature in itself, it's worth noting that there was vulnerability discovered in the CLI. This bug allowed, in certain cases, for a user of the same machine to get access to the application key and key id of another user. It was limited to the very first call to ``authorize-account``, so the impact was not large. Nevertheless it was taken seriously. From the version ``3.2.1`` not only this issue is resolved, but also workarounds and remediation were described.

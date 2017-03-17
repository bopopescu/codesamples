Hadoop-related options
======================

Since mrjob is geared toward Hadoop, there are a few Hadoop-specific options.
However, due to the difference between the different runners, the Hadoop
platform, and Elastic MapReduce, they are not all available for all runners.


Options specific to the local and inline runners
------------------------------------------------

.. mrjob-opt::
    :config: hadoop_version
    :switch: --hadoop-version
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    Set the version of Hadoop to simulate (this currently only matters for
    :mrjob-opt:`jobconf`).

    If you don't set this, the ``local`` and
    ``inline`` runners will run in a version-agnostic mode, where anytime
    the runner sets a simulated jobconf variable, it'll use *every* possible
    name for it (e.g. ``user.name`` *and* ``mapreduce.job.user.name``).


Options available to local, hadoop, and emr runners
---------------------------------------------------

These options are both used by Hadoop and simulated by the ``local``
and ``inline`` runners to some degree.

.. mrjob-opt::
    :config: jobconf
    :switch: --jobconf
    :type: :ref:`dict <data-type-plain-dict>`
    :set: all
    :default: ``{}``

    ``-jobconf`` args to pass to hadoop streaming. This should be a map from
    property name to value.  Equivalent to passing ``['-jobconf',
    'KEY1=VALUE1', '-jobconf', 'KEY2=VALUE2', ...]`` to
    :mrjob-opt:`hadoop_extra_args`.


Options available to hadoop and emr runners
-------------------------------------------

.. mrjob-opt::
    :config: hadoop_extra_args
    :switch: --hadoop-extra-arg
    :type: :ref:`string list <data-type-string-list>`
    :set: all
    :default: ``[]``

    Extra arguments to pass to hadoop streaming. This option is called
    **extra_args** when passed as a keyword argument to
    :py:class:`MRJobRunner`.

.. mrjob-opt::
    :config: hadoop_streaming_jar
    :switch: --hadoop-streaming-jar
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: (automatic)

    Path to a custom hadoop streaming jar.

    On EMR, this can be either a local path or a URI (``s3://...``). If you
    want to use a jar at a path on the master node, use
    :mrjob-opt:`hadoop_streaming_jar_on_emr`.

    On Hadoop, mrjob tries its best to find your hadoop streaming jar,
    searching these directories (recursively) for a ``.jar`` file with
    ``hadoop`` followed by ``streaming`` in its name:

    * :mrjob-opt:`hadoop_home` (the runner option)
    * ``$HADOOP_PREFIX``
    * ``$HADOOP_HOME``
    * ``$HADOOP_INSTALL``
    * ``$HADOOP_MAPRED_HOME``
    * the parent of the directory containing the Hadoop binary (see :mrjob-opt:`hadoop_bin`), unless it's one of ``/``, ``/usr`` or ``/usr/local``
    * ``$HADOOP_*_HOME`` (in alphabetical order by environment variable name)
    * ``/home/hadoop/contrib``
    * ``/usr/lib/hadoop-mapreduce``

    (The last two paths allow the Hadoop runner to work out-of-the box
    inside EMR.)

.. mrjob-opt::
    :config: label
    :switch: --label
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: script's module name, or ``no_script``

    Alternate label for the job

.. mrjob-opt::
    :config: owner
    :switch: --owner
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: :py:func:`getpass.getuser`, or ``no_user`` if that fails

    Who is running this job (if different from the current user)

.. mrjob-opt::
    :config: partitioner
    :switch: --partitioner
    :type: :ref:`string <data-type-string>`
    :set: no_mrjob_conf
    :default: ``None``

    Optional name of a Hadoop partitoner class, e.g.
    ``'org.apache.hadoop.mapred.lib.HashPartitioner'``. Hadoop Streaming will
    use this to determine how mapper output should be sorted and distributed
    to reducers. You can also set this option on your job class with the
    :py:attr:`~mrjob.job.MRJob.PARTITIONER` attribute or the
    :py:meth:`~mrjob.job.MRJob.partitioner` method.

.. mrjob-opt::
    :config: check_input_paths
    :switch: --check-input-paths, --no-check-input-paths
    :type: boolean
    :set: all
    :default: ``True``

    Option to skip the input path check. With ``--no-check-input-paths``,
    input paths to the runner will be passed straight through, without
    checking if they exist.

    .. versionadded:: 0.4.1

Options available to hadoop runner only
---------------------------------------

.. mrjob-opt::
    :config: hadoop_bin
    :switch: --hadoop-bin
    :type: :ref:`command <data-type-command>`
    :set: hadoop
    :default: (automatic)

    Name/path of your hadoop program (may include arguments).

    mrjob tries its best to find your hadoop binary, checking all of the
    following places for an executable file named ``hadoop``:

    * :mrjob-opt:`hadoop_home`/``bin``
    * ``$HADOOP_PREFIX/bin``
    * ``$HADOOP_HOME/bin``
    * ``$HADOOP_INSTALL/bin``
    * ``$HADOOP_INSTALL/hadoop/bin``
    * ``$PATH``
    * ``$HADOOP_*_HOME/bin`` (in alphabetical order by environment variable name)

    If all else fails, we just use ``hadoop`` and hope for the best.

.. mrjob-opt::
    :config: hadoop_home
    :switch: --hadoop-home
    :type: :ref:`path <data-type-path>`
    :set: hadoop
    :default: ``None``

    Hint about where to find the hadoop binary and streaming jar. Instead, just
    set :mrjob-opt:`hadoop_bin` and/or :mrjob-opt:`hadoop_streaming_jar` as
    needed.

    .. deprecated: 0.5.0

.. mrjob-opt::
    :config: hadoop_tmp_dir
    :switch: --hadoop-tmp-dir
    :type: :ref:`path <data-type-path>`
    :set: hadoop
    :default: :file:`tmp/mrjob`

    Scratch space on HDFS. This path does not need to be fully qualified with
    ``hdfs://`` URIs because it's understood that it has to be on HDFS.

    .. versionchanged:: 0.5.0

       This option used to be named ``hdfs_scratch_uri``.

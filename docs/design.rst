Design principles
-----------------

.. include:: /includes/all.rst

* Generic

  When you look around in the Internet, you find hundreds of public and/or
  school holiday APIs, libraries, websites providing HTML calenders, iCALs,
  PDFs. At least for Germany. This is an attempt to harvest holidays and
  convert them.

* Idempotent.

  The program can be run against it’s output and should not make any changes to
  it. This property is checked by integration testing.

* Caching

  Make the fewest requests to external resources possible and use extensive caching.
  The cache is provided as separate git repository (hc-tests-cache_)
  to also make use of the cache during CI testing which is done against a
  support matrix of Python versions and environments and therefore runs in
  parallel a number of times for each commit.

* Expendable

  Convert from anything to anything using a common internal data structure.

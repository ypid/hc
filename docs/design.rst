Design principles
-----------------

.. include:: /includes/all.rst

* Generic

  When you look around on the Internet, you find hundreds of public and/or
  school holiday APIs, libraries, websites providing HTML calenders, iCALs,
  PDFs, at least for Germany. Most of these have some artificial kind of limitation or restriction.
  This is an attempt to harvest holidays (which are generally not copyright
  protected), convert them and provide them without any limitations.

  The available tools where found useless for the use case of bundling holiday
  definitions for opening_hours.js_ which is why this tool has been written.

* Free Software

  All sources are provided under the `GNU Affero General Public License v3 (AGPL-3.0)`_.
  Resources such as holiday data is released under a `Creative Commons Zero v1.0 Universal`_.
  Enjoy.

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

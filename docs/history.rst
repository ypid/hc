History
-------

This tool was created because Germany as of 2017 seems to be unable/unwilling to provide school holidays or holidays in general in a machine readable format.
There are sites like http://www.schulferien.org/ which do a really good job in getting the data anyway through various sources and "providing them".
Back in 2013, everything was great and schulferien.org just provided all iCal files they had for the school holidays of the current year and the following years as far as they are defined by the German Kultusministerkonferenz. A Perl Script has been used to parse all the iCal files and convert them (ref: `convert_ical_to_json <https://gitlab.com/ypid/hc/blob/master/legacy/convert_ical_to_json>`_). Unfortunately, those days are over and after checking out all the available sources the least bad one was to go ahead and parse the HTML table of schulferien.org because the HTML version still provides all data. schulferien.org was contacted before to find a better solution but none has been found. One concern from schulferien.org are the use of (faulty) scripts which put load on their servers. It is therefore one key design goal of this tool to make the fewest requests to external resources possible and use extensive caching. This has been implemented see :ref:`Design principles`.

Refer to `this issue <https://github.com/opening-hours/opening_hours.js/issues/192>`_ for more details.

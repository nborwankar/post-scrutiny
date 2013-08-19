A repository for work on analyzing open source mailing lists.

Nothing much formalized, but here's what we've got:

### dumps/

This directory contains some mbox dumps from Mozilla mailing lists.

Mozilla has a lot of [Forums](http://www.mozilla.org/about/forums/).  Each is mirrored in Mailman, a Newsgroup, and a Google Groups.

The dumps in this directory were retrieved using the `nntp-pull` tool that's part of the `[sinntp](http://manpages.ubuntu.com/manpages/lucid/man1/sinntp.1.html)` package.

### scripts/

This directory has a couple basic scripts I've been playing with or trying ot port over.

 * `news-sources.perl` A script from Mozilla's Gervase Markham that gets the subscription information from the list.

 * `Threader.java` Jamie Zawinski's code for message threading, ported from C in 1997.  See his [description](http://www.jwz.org/doc/threading.html) of the algorithm.

 * `thread.py` An (incomplete!) port of the Threader algorithm to Python.

 * `timeseries.py` Plots a histogram of the timing of posts to an email message.

### charts/

Contains a couple saved visualizations outputed by analysis scripts. Currently, time series histograms of mailing lists.

### notebooks

Some attempts to use iPython notebooks for this wor.

### version-control

Some scripts, analysis, and charts from a related study using version control data.
pbswebmon.py
===

This is a fork of the [original pbswebmon](http://pbswebmon.sf.net).  The original version required [pbs\_python](https://subtrac.sara.nl/oss/pbs_python) version 3.X.

Depends on pbs_python version 4.1+

Should be able to run either on the PBS head node, or a 
separate machine authorised as a client of the head node. 
(To configure the server address, edit the configuration
file /etc/pbswebmon.conf)

Manual installation
---
Put cgi-bin/pbswebmon.py into your CGI directory.

Put the js and css files in a directory called pbswebmon under your web root.

(The RPM install will put the files in these locations.)

RPM
---
Run `make rpm` to build an installable RPM file.

PBS note
---

Note: Make sure that your PBS server is setup to allow querying of other people's jobs. Otherwise, you'd only see the jobs for the user your webserver runs under.

`qmgr -c "set server query_other_jobs = True"`
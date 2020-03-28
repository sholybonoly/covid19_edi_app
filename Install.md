# Installation #

This python script can be installed on any suitable host with internet access in order to read mailbox and to forward onto specific email addresses

For Edinburgh Coronavirus volunter groups this has been setup on google cloud host.

### Installation Steps ###

* Pull the latest source from this repo onto the new host

  <code>
    git clone https://github.com/sholybonoly/covid19_edi_app.git /opt/app
  </code>

* Install python
   * This script requires python 3 or above to run
* Install python packages required
   * See /opt/app/requirements.txt for packages required
   * Install these pip (NB: For correct python installation)

* Update /opt/app/config.ini with mailbox details and password and teams.csv for forwarding on emails

* Add mail gun API key based on mail gun account (required to send emails)

* Set a log file output where you have permissions to write to


    <code>
        >crontab -e

    \* * * * * cd /opt/app && /usr/bin/python3 /opt/app/process.py
    </code>

* You can then tail log

    <code>
        tail -f /opt/app/relay.log
    </code>
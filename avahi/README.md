Avahi Configuration File
========================

copy `temppi.service` to `/etc/avahi/services/` and restart Avahi: `sudo systemctl restart avahi-daemon`. Afterwards, check the status by typing `sudo systemctl status avahi-daemon`.

You can now find the web service using for example avahi-discover.

Fork of rotating-free-proxies_, which automatically fetches rotating proxies from free-proxy-list.net_ when using Scrapy.

.. _free-proxy-list.net: https://free-proxy-list.net/
.. _rotating-free-proxies: https://pypi.org/project/rotating-free-proxies/

Notable changes
============================

Choose what types of proxies will be fetched (settings.py)
----------------------------------------------------------
::

    ANONYMITY_TYPES = {"TRANSPARENT","ANONYMOUS","ELITE"}

Set how recently proxy must have been checked (settings.py)
-----------------------------------------------------------
::

    MAX_PROXY_AGE = 7200

Ports <1000 are now also valid.

NUMBER_OF_PROXIES_TO_FETCH now has a default value (318).
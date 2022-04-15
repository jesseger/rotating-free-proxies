from __future__ import absolute_import

import logging

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy

from dateutil import parser


logger = logging.getLogger(__name__)


def extract_proxy_hostport(proxy):
    """
    Return the hostport component from a given proxy:

    >>> extract_proxy_hostport('example.com')
    'example.com'
    >>> extract_proxy_hostport('http://www.example.com')
    'www.example.com'
    >>> extract_proxy_hostport('127.0.0.1:8000')
    '127.0.0.1:8000'
    >>> extract_proxy_hostport('127.0.0.1')
    '127.0.0.1'
    >>> extract_proxy_hostport('localhost')
    'localhost'
    >>> extract_proxy_hostport('zot:4321')
    'zot:4321'
    >>> extract_proxy_hostport('http://foo:bar@baz:1234')
    'baz:1234'
    """
    return _parse_proxy(proxy)[3]


def fetch_new_proxies(proxy_path, max_number_of_proxies, max_proxy_age, anonymity_types):
    logger.warning(f"Fetching new proxies; dumping location = {proxy_path}")
    import requests
    from bs4 import BeautifulSoup
    import socket

    def get_soup(url):
        return BeautifulSoup(requests.get(url).text)

    soup = get_soup("https://free-proxy-list.net/")
    trs = soup.find_all("tr")

    def validate_ip(addr):
        try:
            socket.inet_aton(addr)
            return True
        except socket.error:
            return False

    def validate_port(port):
        return str(port).isdigit() and 0 < int(port) < 99999

    def validate_age(age_string, max_age):
        clean_age_string = age_string.replace(" ago","").replace("min","minute").replace("sec","second")
        age = parser.parse(clean_age_string).second + parser.parse(clean_age_string).minute*60 + parser.parse(clean_age_string).hour*3600      
        return age <= max_age

    proxies = list()

    logger.warning(f"Total proxies listed in source webpage={len(trs)}")
    for tr in trs:
        tds = tr.find_all("td")
        if tds:
            ip = tds[0].text
            if not validate_ip(ip):
                continue
            port = tds[1].text
            if not validate_port(port):
                continue
            if tds[4].text.replace("proxy","").strip().upper() not in anonymity_types: #"elite" not in tds[4].text and "anonymous" not in tds[4].text:
                continue
            age_text = tds[-1].text
            if not validate_age(age_text, max_proxy_age):
                continue
            protocol = "https" if "yes" in tds[6].text.strip() else "http"
            proxy = f"{protocol}://{ip}:{port}"
            proxies.append(proxy)
            if len(proxies) > max_number_of_proxies:
                break

    with open(proxy_path, "w") as f:
        logger.warning(
            f"updating list of proxies ({len(proxies)}) to location {proxy_path}"
        )
        f.write("\n".join(proxies) + "\n")
    return proxies

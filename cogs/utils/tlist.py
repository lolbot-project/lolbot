"""
TLD List defined things.
"""
import urllib.parse

api = 'https://tld-list.com/xaja/dac'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
    ' like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 '
    'Safari/537.36',
    'Origin': 'https://tld-list.com',
    'Referer': 'https://tld-list.com/',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


# I swear this isn't sexual
def construct(sub, dom):
    """
    Makes a form data for processing
    by our lord and savior tld list.
    Requires arguments: subdomain, tld
    """
    csrf = '42f662721815dbcb75ffc4481330c401cb9754c23c7d1f5d9a'
    csrf += '156b8007eb7d9068c1ffba80ccea2e7b1b922545117bad'
    return {
        'csrf': csrf,
        'subdomain': urllib.parse.quote_plus(sub),
        'suffix[]': urllib.parse.quote_plus(dom),
        'c': 0
    }

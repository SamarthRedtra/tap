__version__ = "0.0.1"
api_key = 'sk_test_mtqi2RGWJ8cFjCzYuH3hkBNo'
client_id = None
api_base = 'https://api.tap.company'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
app_info = None
max_network_retries = 0
merchant_id = None
live_mode = 0
post_base_url = ""
# Set to either 'debug' or 'info', controls console logging
log = None


from tap.api_resources.customer import Customer
from tap.api_resources.token import Token
from tap.api_resources.charge import Charge
from tap.api_resources.card import Card
from tap.api_resources.refund import Refund


from tap.api_resources import *  # noqa

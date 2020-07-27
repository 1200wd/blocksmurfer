# -*- coding: utf-8 -*-
#
#    Blocksmurfer Crypto block explorer based on Bitcoinlib
#    © 2020 January - 1200 Web Development <http://1200wd.com/>
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from flask import abort, current_app, session
from bitcoinlib.encoding import *
from bitcoinlib.keys import Address
from bitcoinlib.services.services import Service, ServiceError


network_code_translation = {
    'btc': 'bitcoin',
    'ltc': 'litecoin',
    'xlt': 'litecoin_testnet',
    'tbtc': 'testnet',
}


class SmurferService(Service):

    def __init__(self, network_code='btc', timeout=5, *args, **kwargs):
        nw_enabled = network_code_translation.keys() if not current_app else current_app.config['NETWORKS_ENABLED']
        # TODO: Enable other networks
        # if not network_code and current_app:
        #     network_code = session.get('network_code', current_app.config['NETWORK_DEFAULT'])
        #     session['network_code'] = network_code
        if network_code in network_code_translation and network_code in nw_enabled:
            network = network_code_translation[network_code]
            Service.__init__(self, network=network, timeout=timeout, *args, **kwargs)
        else:
            abort(422, "Error opening network with specified code")


def check_txid(txid=None, error_on_empty=False):
    if not txid:
        if error_on_empty:
            return False
        return True
    try:
        assert (len(txid) == 64)
        assert (to_hexstring(txid) == txid)
    except (AssertionError, EncodingError):
        return False
    return True


def check_address(address=None, error_on_empty=False):
    if not address:
        if error_on_empty:
            return False
        return True
    try:
        assert (Address.import_address(address).address == address)
    except (AssertionError, EncodingError):
        return False
    return True

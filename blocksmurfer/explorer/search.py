from bitcoinlib.keys import Address, get_key_format
from blocksmurfer.explorer.service import check_txid, network_code_translation
from flask import redirect, url_for, flash
from flask_babel import _


def search_query(s):
    if check_txid(s):
        return redirect(url_for('main.transaction', network='btc', txid=s))
    try:
        key_dict = get_key_format(s)
        if not key_dict or 'networks' not in key_dict or 'format' not in key_dict or not key_dict['networks']:
            flash(_('Invalid search query, not a valid address or key'), category='error')
            return redirect(url_for('main.index'))
        network_name = key_dict['networks'] if not isinstance(key_dict['networks'], list) else key_dict['networks'][0]
        network = [x for x, y in network_code_translation.items() if y == network_name][0]
        if key_dict['format'] == 'address':
            if Address.import_address(s):
                return redirect(url_for('main.address', address=s, network=network))
        elif key_dict['format']:
            return redirect(url_for('main.key', key=s, network=network))
        flash(_('No address, key or transaction found.'), category='error')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(_('Not a valid address, key or transaction ID. Response: %s' % e), category='error')
        return redirect(url_for('main.index'))

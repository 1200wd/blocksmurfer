# -*- coding: utf-8 -*-
#
#    Blocksmurfer - Blockchain Explorer
#
#    © 2020-2021 March - 1200 Web Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#

from flask import jsonify, abort
from flask_restful import marshal, request
from flask_babel import _
from bitcoinlib.transactions import Transaction
from blocksmurfer.api import bp
from blocksmurfer.api.structures import transaction_fields
from blocksmurfer.explorer.service import *
# import logging


# _logger = logging.getLogger(__name__)


@bp.route('/<string:network>/transaction/<string:txid>')
def transaction(network, txid):
    srv = SmurferService(network)
    raw = request.args.get('raw', '', type=bool)
    if not check_txid(txid):
        abort(422, "Invalid txid provided")
    t = srv.gettransaction(txid)
    if not t:
        abort(404, "Could not find transaction")
    # Try to fetch address from previous transaction
    for i in t.inputs:
        if not i.address:
            try:
                ti = srv.gettransaction(i.prev_txid.hex())
                i.address = ti.outputs[i.output_n_int].address
            except:
                pass
    if raw:
        tx_dict = {'raw_hex': t.raw_hex()}
    else:
        tx_dict = marshal(t, transaction_fields)
    return jsonify(tx_dict)


@bp.route('/<string:network>/isspent/<string:txid>/<int:output_n>')
def isspent(network, txid, output_n):
    if not check_txid(txid):
        abort(422, "Invalid txid provided")
    srv = SmurferService(network)
    data = {
        'spent': srv.isspent(txid, output_n)
    }
    return jsonify(data)


@bp.route('/<string:network>/fees/<int:blocks>')
@bp.route('/<string:network>/fees')
def fees(network, blocks=3):
    srv = SmurferService(network)
    data = {
        'network': network,
        'blocks': blocks,
        'estimated_fee_sat_kb': srv.estimatefee(blocks)
    }
    return jsonify(data)


@bp.route('/<string:network>/transaction_broadcast', methods=['POST'])
def transaction_broadcast(network):
    rawtx = request.data.decode()
    srv = SmurferService(network)
    errors = []
    txid = ''
    res = {}
    try:
        t = Transaction.parse_hex(rawtx)
    except Exception as e:
        errors.append(_('Invalid raw transaction hex, could not parse: %s' % e))
    else:
        known_tx = srv.gettransaction(t.txid)
        if known_tx:
            errors.append(_('This transaction %s is already included in the blockchain' % t.txid))
        else:
            res = srv.sendrawtransaction(rawtx)
            if not res or 'txid' not in res:
                # TODO: Get decent error message, without private details
                errors.append(_('Could not send raw transaction. %s' % srv.errors.get('bcoin', '')))
    data = {
        'success': True if txid else False,
        'txid': txid,
        'errors': ','.join(errors),
        'raw_response': res
    }
    return jsonify(data), 200 if txid else 400

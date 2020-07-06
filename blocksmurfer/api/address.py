from flask import jsonify
from flask_restful import marshal, request
from blocksmurfer.api import bp
from blocksmurfer.main import MAX_TRANSACTIONS_REQUESTS
from blocksmurfer.api.structures import transaction_fields, utxo_fields
from blocksmurfer.explorer.service import *
# import logging


# _logger = logging.getLogger(__name__)

@bp.route('/<string:network>/transactions/<string:address>')
def transactions(network, address):
    after_txid = request.args.get('after_txid', '', type=str)
    if after_txid and not check_txid(after_txid):
        abort(422, "Invalid after_txid provided")
    limit = request.args.get('limit', 10, type=int)
    limit = MAX_TRANSACTIONS_REQUESTS if limit > MAX_TRANSACTIONS_REQUESTS else limit

    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")
    txs = srv.gettransactions(address, after_txid=after_txid, limit=limit)
    # _logger.debug("Got transactions from provider: %s" % srv.results.items())
    txs_dict = marshal(txs, transaction_fields)
    return jsonify(txs_dict)


@bp.route('/<string:network>/utxos/<string:address>')
def utxos(network, address):
    after_txid = request.args.get('after_txid', '', type=str)
    if after_txid and not check_txid(after_txid):
        abort(422, "Invalid after_txid provided")
    limit = request.args.get('limit', 10, type=int)
    limit = MAX_TRANSACTIONS_REQUESTS if limit > MAX_TRANSACTIONS_REQUESTS else limit

    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")

    txs = srv.getutxos(address, after_txid=after_txid, limit=limit)
    # _logger.debug("Got UTXOS from provider: %s" % srv.results.items())
    txs_dict = marshal(txs, utxo_fields)
    return jsonify(txs_dict)


@bp.route('/<string:network>/address_balance/<string:address>')
def address_balance(network, address):
    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")
    balance = srv.getbalance(address)
    data = {
        'address': address,
        'balance': balance
    }
    return jsonify(data)

from flask import jsonify
from flask_restful import marshal, request
from blocksmurfer.api import bp
from blocksmurfer.api.errors import resp_error
from blocksmurfer.api.structures import transaction_fields
from blocksmurfer.explorer.service import *


@bp.route('/<string:network>/transaction/<string:txid>')
def transaction(network, txid):
    srv = SmurferService(network)
    raw = request.args.get('raw', '', type=bool)
    if not check_txid(txid):
        return resp_error(501, message="Invalid txid provided")
    t = srv.gettransaction(txid)
    if not t:
        return resp_error(404, message="Could not find transaction")
    if raw:
        tx_dict = {'raw_hex': t.raw_hex()}
    else:
        tx_dict = marshal(t, transaction_fields)
    return jsonify(tx_dict)


@bp.route('/<string:network>/fees/<int:blocks>')
def fees(network, blocks=3):
    srv = SmurferService(network)
    data = {
        'network': network,
        'blocks': blocks,
        'fees': srv.estimatefee(blocks)
    }
    return jsonify(data)
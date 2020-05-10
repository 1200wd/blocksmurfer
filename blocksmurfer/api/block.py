from flask import jsonify
from flask_restful import marshal, request
from blocksmurfer.api import bp
from blocksmurfer.api.errors import resp_error
from blocksmurfer.api.structures import transaction_fields
from blocksmurfer.explorer.service import *


@bp.route('/<string:network>/block/<blockid>')
def block(network, blockid):
    srv = SmurferService(network)
    if blockid == 'last':
        blockid = srv.blockcount()
    bk = srv.getblock(blockid, limit=5)
    # bk = srv.getblock(blockid, parse_transactions=True, limit=5)
    if not bk:
        return resp_error(404, message="Block not found")
    # bk['txs'] = marshal(bk['txs'], transaction_fields)
    return bk


@bp.route('/<string:network>/blockcount')
def blockcount(network):
    srv = SmurferService(network)
    blockcount = srv.blockcount()
    if not blockcount:
        return resp_error(404, message="Could not determine blockcount for this network")
    data = {
        'network': network,
        'blockcount': blockcount
    }
    return jsonify(data)

from flask import jsonify, current_app
from flask_restful import marshal, request
from blocksmurfer.api import bp
from blocksmurfer.api.structures import transaction_fields_block, block_fields
from blocksmurfer.explorer.service import *


@bp.route('/<string:network>/block/<blockid>')
def block(network, blockid):
    parse_transactions = request.args.get('parse_transactions') in ['1', 'true', 'True']
    limit = request.args.get('limit', current_app.config['REQUEST_LIMIT_DEFAULT'], type=int)
    limit = current_app.config['REQUEST_LIMIT_MAX'] if limit > current_app.config['REQUEST_LIMIT_MAX'] else limit
    page = request.args.get('page', 1, type=int)

    if blockid != 'last' and not blockid.isdigit() and not (isinstance(blockid, str) and len(blockid) == 64):
        abort(422, "Invalid Block ID provided")
    srv = SmurferService(network)
    if blockid == 'last':
        blockid = srv.blockcount()
    if parse_transactions:
        bk = srv.getblock(blockid, parse_transactions=True, limit=limit, page=page)
    else:
        bk = srv.getblock(blockid, parse_transactions=False)
    if not bk:
        abort(422, "Block with this ID not found on the network")
    bdict = marshal(bk.as_dict(), block_fields)
    if parse_transactions:
        bdict['transactions'] = marshal(bk.transactions, transaction_fields_block)
    else:
        bdict['transactions'] = bk.transactions
    return jsonify(bdict)


@bp.route('/<string:network>/blockcount')
def blockcount(network):
    srv = SmurferService(network)
    blockcount = srv.blockcount()
    if not blockcount:
        abort(500, "Could not determine blockcount for this network")
    data = {
        'network': network,
        'blockcount': blockcount
    }
    return jsonify(data)

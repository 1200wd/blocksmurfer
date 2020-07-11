from flask import jsonify
from flask_restful import marshal
from blocksmurfer.api import bp
from blocksmurfer.api.structures import network_field
from blocksmurfer.explorer.service import *


@bp.route('/<string:network>/')
def network(network):
    srv = SmurferService(network)
    info = srv.getinfo()
    network = srv.network.__dict__
    network_dict = marshal(network, network_field)
    info.update(network_dict)
    prefixes_wif = []
    for pw in network['prefixes_wif']:
        prefixes_wif.append({
            'hex': pw[0],
            'prefix': pw[1],
            'public': pw[2],
            'multisig': pw[3],
            'witnesse': pw[4],
            'script': pw[5]
        })
    info['prefixes_wif'] = prefixes_wif

    return jsonify(info)



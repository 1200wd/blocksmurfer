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



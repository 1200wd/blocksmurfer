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

from flask_restful import fields
from flask_restful.fields import MarshallingException


class Hexstring(fields.String):

    def format(self, value):
        try:
            return value.hex()
        except ValueError as ve:
            raise MarshallingException(ve)


class HexstringKey(fields.String):

    def format(self, key):
        try:
            return key.public_hex
        except ValueError as ve:
            raise MarshallingException(ve)


transaction_input_fields = {
    'prev_txid': fields.String(attribute=lambda obj: obj.prev_txid.hex()),
    'output_n': fields.Integer(attribute='output_n_int'),
    'address': fields.String,
    'compressed': fields.Boolean,
    'double_spend': fields.Boolean,
    'encoding': fields.String,
    'index_n': fields.Integer,
    'locktime_cltv': fields.Integer,
    'locktime_csv': fields.Integer,
    'public_hash': fields.String(attribute=lambda obj: obj.public_hash.hex()),
    'redeemscript': fields.String(attribute=lambda obj: obj.redeemscript.hex()),
    'script': fields.String(attribute=lambda obj: obj.unlocking_script.hex()),
    'locking_script': fields.String(attribute=lambda obj: obj.locking_script.hex()),
    'script_type': fields.String,
    'sequence': fields.Integer,
    'signatures': fields.List(Hexstring),
    'sigs_required': fields.Integer,
    'valid': fields.Boolean,
    'value': fields.Integer,
    'witnesses': fields.List(Hexstring),
    'witness_type': fields.String,
    'keys': fields.List(Hexstring),
}

transaction_output_fields = {
    'address': fields.String,
    'output_n': fields.Integer(attribute='output_n_int'),
    'public_hash': fields.String(attribute=lambda obj: obj.public_hash.hex()),
    'script': fields.String(attribute=lambda obj: obj.lock_script.hex()),
    'script_type': fields.String,
    'spent': fields.Boolean,
    'value': fields.Integer,
}

transaction_fields = {
    'txid': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
    'block_hash': fields.String,
    'block_height': fields.Integer,
    'coinbase': fields.Boolean,
    'confirmations': fields.Integer,
    'fee': fields.Integer,
    'inputs': fields.List(fields.Nested(transaction_input_fields)),
    'input_total': fields.Integer,
    'outputs': fields.List(fields.Nested(transaction_output_fields)),
    'output_total': fields.Integer,
    'locktime': fields.Integer,
    'network': fields.String(attribute='network.name'),
    'raw_hex': fields.String(attribute=lambda obj: obj.raw_hex()),
    'size': fields.Integer,
    'status': fields.String,
    'verified': fields.Boolean,
    'version': fields.Integer(attribute='version_int'),
    'vsize': fields.Integer,
    'witness_type': fields.String,
}

transaction_fields_block = {
    'txid': fields.String,
    'coinbase': fields.Boolean,
    'fee': fields.Integer,
    'inputs': fields.List(fields.Nested(transaction_input_fields)),
    'input_total': fields.Integer,
    'outputs': fields.List(fields.Nested(transaction_output_fields)),
    'output_total': fields.Integer,
    'locktime': fields.Integer,
    'raw_hex': fields.String(attribute=lambda obj: obj.raw_hex()),
    'size': fields.Integer,
    'status': fields.String,
    'verified': fields.Boolean,
    'version': fields.Integer(attribute='version_int'),
    'vsize': fields.Integer,
    'witness_type': fields.String,
}

utxo_fields = {
    'address': fields.String,
    'txid': fields.String,
    'confirmations': fields.Integer,
    'output_n': fields.Integer,
    'input_n': fields.Integer,
    'block_height': fields.Integer,
    'fee': fields.Integer,
    'size': fields.Integer,
    'value': fields.Integer,
    'script': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
}

block_fields = {
    'bits': fields.Integer,
    'depth': fields.Integer(attribute='confirmations'),
    'block_hash': fields.String,
    'height': fields.Integer,
    'merkle_root': fields.String,
    'nonce': fields.Integer,
    'prev_block': fields.String,
    'time': fields.Integer(attribute='timestamp'),
    'tx_count': fields.Integer,
    'version': fields.Integer,
}

# network_prefix_field = fields.List({'a': fields.String, 'b': fields.String, 'c': fields.String, 'd': fields.String, 'e': fields.String, 'f': fields.String})

network_field = {
    'bip44_cointype': fields.Integer,
    'currency_code': fields.String,
    'currency_name': fields.String,
    'currency_name_plural': fields.String,
    'currency_symbol': fields.String,
    'denominator': fields.Float,
    'description': fields.String,
    'dust_amount': fields.Integer,
    'fee_default': fields.Integer,
    'fee_max': fields.Integer,
    'fee_min': fields.Integer,
    'name': fields.String,
    'prefix_address':  fields.String(attribute=lambda obj: obj['prefix_address'].hex()),
    'prefix_address_p2sh': fields.String(attribute=lambda obj: obj['prefix_address_p2sh'].hex()),
    'prefix_bech32': fields.String,
    'prefix_wif': fields.String(attribute=lambda obj: obj['prefix_wif'].hex()),
}
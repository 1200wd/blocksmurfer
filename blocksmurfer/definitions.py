SIGHASH_FLAGS = {
    0x01: ('ALL', 'Signature applies to all inputs and outputs'),
    0x02: ('NONE', 'Signature applies to all inputs, none of the outputs'),
    0x03: ('SINGLE', 'Signature applies to all inputs but only the one output with the same index number as the signed input'),
    0x81: ('ALL|ANYONECANPAY', 'Signature applies to one input and all outputs'),
    0x82: ('NONE|ANYONECANPAY', 'Signature applies to one input, none of the outputs'),
    0x83: ('SINGLE|ANYONECANPAY', 'Signature applies to one input and the output with the same index number')
}


BLOCKSMURFER_EXAMPLES = {
    'address_transactions': {
        'btc': 'bc1qxfrgfhs49d7dtcfzlhp7f7cwsp8zpp60hywp0f',
        'tbtc': 'tb1qzf2wpucjq6hc5qam2aw7rd5ujfq3emjdn73jm2',
        'ltc': 'LLxi9Bnc3UGVA2peZ4p2n8oNuSMvtMyJ25',
    },
    'address_transactions_after_txid': {
        'btc': '333d66019c73c9ca015cb25d81f95ff26d320432c23b94edccb90a7b08c84063',
        'tbtc': '308858b179a28f2db429e2f6df334b016203ab6b2788a8d15c856396ecbd797d',
        'ltc': 'ff01bd36e9f68e83e212b34a025ab6c47e347041b93b39c5858aedf6b0d90abd',
    },
    'address_utxos': {
        'btc': '1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1',
        'tbtc': 'n3GNqMveyvaPvUbH469vDRadqpJMPc84JA',
        'ltc': 'LLxi9Bnc3UGVA2peZ4p2n8oNuSMvtMyJ25',
    },
    'address_utxos_after_txid': {
        'btc': '1ed74cf9ec10bb9eb881dfcbc97318baadff371e25f227587b8d87466f260cad',
        'tbtc': '164f86f0226afdda9d431e58e94b48ac4bd382b7c72b8814d6eb502678e32268',
        'ltc': 'ff01bd36e9f68e83e212b34a025ab6c47e347041b93b39c5858aedf6b0d90abd',
    },
    'transaction': {
        'btc': '5fd3d8275afb5b5cc202ae8480daefa4fe16d0cf480ce78545d6dc06c6fb101a',
        'tbtc': '005f9f4258f03d3393477edb2cfece51666015b19be30737e719deaee41bea0f',
        'ltc': 'f17dd941a48860d00f930b7c0d67df3cb41d05dffd77932c4d5985529ae5af0c',
    },
}

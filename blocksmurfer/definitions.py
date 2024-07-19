SIGHASH_FLAGS = {
    0x01: ('ALL', 'Signature applies to all inputs and outputs'),
    0x02: ('NONE', 'Signature applies to all inputs, none of the outputs'),
    0x03: ('SINGLE', 'Signature applies to all inputs but only the one output with the same index number as the signed input'),
    0x81: ('ALL|ANYONECANPAY', 'Signature applies to one input and all outputs'),
    0x82: ('NONE|ANYONECANPAY', 'Signature applies to one input, none of the outputs'),
    0x83: ('SINGLE|ANYONECANPAY', 'Signature applies to one input and the output with the same index number')
}
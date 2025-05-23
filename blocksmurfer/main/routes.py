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

from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_babel import _
from datetime import timezone, datetime
import time
import inspect
import re
import difflib
from config import Config
from blocksmurfer import definitions
from blocksmurfer.main import bp
from blocksmurfer.main.forms import *
from blocksmurfer.explorer.search import search_query
from blocksmurfer.explorer.service import *
from bitcoinlib.keys import HDKey, Signature
from bitcoinlib.transactions import Transaction, Output, TransactionError
from bitcoinlib.scripts import Script, ScriptError, Stack
from bitcoinlib.encoding import Quantity
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.config.opcodes import opcodeints, opcodenames


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/<network>/index', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/<network>/index', methods=['GET', 'POST'])
def index(network='btc'):
    form = SearchForm()
    if form.validate_on_submit():
        return search_query(form.search.data, network=network)
    srv = SmurferService(network)
    blockcount = srv.blockcount()
    return render_template('index.html', title=_('Explorer'), subtitle=_('Smurfing the blockchain since 2020'),
                           form=form, blockcount=blockcount, network=network, network_name=srv.network.name)


@bp.route('/search/<search_string>')
@bp.route('/<network>/search/<search_string>')
def search(search_string, network='btc'):
    return search_query(search_string, network)


@bp.route('/api')
@bp.route('/<network>/api')
def api(network='btc'):
    if not Config.ENABLE_API:
        flash(_('API not available'), category='error')
        return redirect(url_for('main.index'))
    api_url = request.host_url + 'api/v1/'
    if Config.API_BASE_URL:
        api_url = Config.API_BASE_URL
    return render_template('api.html', title=_('API'), subtitle=_('Bitcoin blockchain API'),
                           network=network, api_url=api_url, examples=definitions.BLOCKSMURFER_EXAMPLES)


@bp.route('/about')
@bp.route('/<network>/about')
def about(network='btc'):
    srv = SmurferService(network)
    providers = sorted(srv.providers.items(), key=lambda x: x[1]['priority'], reverse=True)
    for provider in providers:
        if '@' in provider[1]['url']:
            provider[1]['url'] = ''
    return render_template('about.html', title=_('About'), subtitle=_('Keep on smurfing!'), providers=providers,
                           network_name=srv.network.name, network=network, bitcoinlib_version=BITCOINLIB_VERSION)


@bp.route('/providers')
@bp.route('/<network>/providers')
def providers(network='btc'):
    srv = SmurferService(network)
    providers = sorted(srv.providers.items(), key=lambda x: x[1]['priority'], reverse=True)
    for provider in providers:
        if '@' in provider[1]['url']:
            provider[1]['url'] = ''
    return render_template('providers.html', title=_('Providers'), subtitle=_('Service providers overview'),
                           providers=providers, network_name=srv.network.name, network=network)

@bp.route('/<network>/providers/status')
def providers_status(network='btc'):
    provider_stats = {}

    for provider in SmurferService(network).providers:
        start_time = datetime.now()
        try:
            srv = SmurferService(network, provider_name=provider, cache_uri='')
            blockcount = srv.blockcount()
            provider_stats.update({provider: (blockcount, srv.execution_time or 0, '')})
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            provider_stats.update({provider: (0, execution_time, str(e))})

    return render_template('providers_status.html', title=_('Providers Status'),
                           subtitle=_('Service providers current status'),
                           provider_stats=provider_stats, network=network)

@bp.route('/<network>/transactions', methods=['GET', 'POST'])
def transactions(network='btc'):
    page = request.args.get('page', 1, type=int)
    blockid = request.args.get('blockid', type=str)
    show_mempool = request.args.get('show_mempool', type=bool, default=False)
    block = None
    limit = 10
    mempool = []
    # show_mempool = True
    transactions = []

    # if blockid:
    #     show_mempool = False

    form = SearchForm()
    form.search.render_kw = {'placeholder': 'enter transaction id'}
    if form.validate_on_submit():
        return search_query(form.search.data, network)

    srv = SmurferService(network)
    if show_mempool:
        mempool = srv.mempool() or []
        if page < 1:
            page = 1
        if page > len(mempool) / limit:
            page = (len(mempool) // limit) + 1
        for txid in mempool[(page-1)*limit:page*limit]:
            transactions.append(srv.gettransaction(txid))
        total_txs = len(mempool)
    if not transactions:
        if not blockid or blockid == 'last':
            blockid = srv.blockcount()
        block = srv.getblock(blockid, parse_transactions=True, limit=10, page=page)
        if not block:
            flash(_("Block not found"), category='error')
            return redirect(url_for('main.index'))
        total_txs = block.tx_count
        transactions = block.transactions

    prev_url = None
    next_url = None
    if (mempool and len(mempool) > limit) or \
            (block and not mempool and not srv.complete and block.transactions and block.tx_count >= limit):
        next_url = url_for('main.transactions', network=network, blockid=blockid, page=page+1)
    if page > 1:
        prev_url = url_for('main.transactions', network=network, blockid=blockid, page=page-1)

    subtitle = _('Latest unconfirmed transactions')
    if blockid:
        subtitle = _('Block %s transactions' % blockid)

    tzutc = timezone.utc
    return render_template('explorer/transactions.html', title=_('Transactions'), total_txs=total_txs,
                           subtitle=subtitle, block=block, network=network,
                           form=form, transactions=transactions, page=page, limit=limit,
                           prev_url=prev_url, next_url=next_url, tzutc=tzutc)


@bp.route('/<network>/transaction/<txid>')
def transaction(network, txid):
    srv = SmurferService(network)
    if not check_txid(txid):
        flash(_('Invalid transaction ID'), category='error')
        return redirect(url_for('main.index'))
    t = srv.gettransaction(txid)
    if not t:
        flash(_('Transaction %s not found' % txid), category='error')
        return redirect(url_for('main.index'))
    # Try to fetch address from previous transaction
    for i in t.inputs:
        if not i.address:
            try:
                ti = srv.gettransaction(i.prev_txid.hex())
                i.address = ti.outputs[i.output_n_int].address
            except:
                pass
    tzutc = timezone.utc
    return render_template('explorer/transaction.html', title=_('Transaction'),
                           subtitle=txid, transaction=t, network=network, tzutc=tzutc)


@bp.route('/<network>/transaction_broadcast', methods=['GET', 'POST'])
def transaction_broadcast(network):
    rawtx = request.args.get('rawtx', type=str)
    form = TransactionSendForm()
    if form.validate_on_submit():
        srv = SmurferService(network)
        try:
            t = Transaction.parse(form.rawtx.data, network=srv.network)
        except Exception as e:
            flash(_('Invalid raw transaction hex, could not parse: %s' % e), category='error')
        else:
            # Retrieve prev_tx input values
            try:
                t = srv.getinputvalues(t)
                t.verify()
            except Exception as e:
                flash(_('Could not verify transaction: %s' % e), category='warning')

            known_tx = srv.gettransaction(t.txid)
            if known_tx:
                flash(_('This transaction %s is already included in the blockchain' % t.txid), category='error')
            elif not t.verified:
                flash(_('Invalid transaction, could not verify transaction %s' % t.txid), category='error')
            else:
                res = srv.sendrawtransaction(form.rawtx.data)
                if not res or 'txid' not in res:
                    # TODO: Get decent error message, without private details
                    flash(_('Could not send raw transaction. %s' % srv.errors.get('bcoin', '')), category='error')
                return render_template('explorer/transaction_send.html', title=_('Transaction Send'),
                                       subtitle=_('Your Transaction was broadcasted successfully!'),
                                       txid=res['txid'], network=network)
    form.rawtx.data = rawtx
    return render_template('explorer/transaction_broadcast.html', title=_('Send Transaction'), rawtx=rawtx,
                           subtitle=_('Broadcast your transaction on the network'), form=form, network=network)


@bp.route('/<network>/transaction_decompose', methods=['GET', 'POST'])
def transaction_decompose(network):
    rawtx = request.args.get('rawtx', type=str)
    form = TransactionDecomposeForm()
    srv = SmurferService(network)
    if form.validate_on_submit():
        try:
            t = Transaction.parse_hex(form.rawtx.data, network=srv.network)
        except Exception as e:
            flash(_('Invalid raw transaction hex, could not parse: %s' % e), category='error')
        else:
            # TODO: Retrieving prev_tx input values should be included in bitcoinlib
            try:
                for n, i in enumerate(t.inputs):
                    if i.prev_txid != b'\0' * 32:
                        ti = srv.gettransaction(i.prev_txid.hex())
                        if not ti:
                            flash(_('Could not verify transaction: previous transaction not found'), category='warning')
                            break
                        t.inputs[n].value = ti.outputs[i.output_n_int].value
                t.verify()
            except TransactionError as e:
                flash(_('Could not verify transaction: %s' % e), category='warning')
            t_json = t.as_json()
            return render_template('explorer/transaction_elements.html', title=_('Decomposed Transaction'),
                                   subtitle=_('Transaction elements as dictionary'),
                                   transaction_dict=t_json, rawtx=form.rawtx.data, network=network)
    form.rawtx.data = rawtx
    return render_template('explorer/transaction_decompose.html', title=_('Decompose Transaction'),
                           subtitle=_('Decompose your raw transaction hex'), form=form, network=network)


@bp.route('/<network>/transaction/<txid>/input/<index_n>')
def transaction_input(network, txid, index_n):
    if not check_txid(txid) or not index_n.isdigit():
        flash(_('Invalid transaction ID or input number'), category='error')
        return redirect(url_for('main.index'))
    srv = SmurferService(network)
    t = srv.gettransaction(txid)
    if not t:
        flash(_('Transaction %s not found' % txid), category='error')
        return redirect(url_for('main.index'))
    if int(index_n) > len(t.inputs):
        flash(_('Transaction input with index number %s not found' % index_n), category='error')
        return redirect(url_for('main.transaction', network=network, txid=txid))
    input = t.inputs[int(index_n)]
    if not t.coinbase:
        ti = srv.gettransaction(input.prev_txid.hex())
        if not ti:
            flash(_('Could not verify transaction: previous transaction not found'), category='error')
        input.value = ti.outputs[input.output_n_int].value
        input.address = ti.outputs[input.output_n_int].address

    return render_template('explorer/transaction_input.html', title=_('Transaction Input %s' % index_n), subtitle=txid,
                           transaction=t, network=network, input=input, index_n=index_n)


@bp.route('/<network>/transaction/<txid>/output/<output_n>')
def transaction_output(network, txid, output_n):
    if not check_txid(txid) or not output_n.isdigit():
        flash(_('Invalid transaction ID or output number'), category='error')
        return redirect(url_for('main.index'))
    srv = SmurferService(network)
    t = srv.gettransaction(txid)
    if not t:
        flash(_('Transaction %s not found' % txid), category='error')
        return redirect(url_for('main.index'))
    for n, o in enumerate(t.outputs[:5]):
        if o.spent is None:
            o.spent = srv.isspent(t.txid, n)
    if int(output_n) > len(t.outputs):
        flash(_('Transaction output with index number %s not found' % output_n), category='error')
        return redirect(url_for('main.transaction', network=network, txid=txid))
    output = t.outputs[int(output_n)]
    return render_template('explorer/transaction_output.html', title=_('Transaction Output %s' % output_n),
                           subtitle=txid, transaction=t, network=network, output=output, output_n=output_n)


@bp.route('/<network>/address/<address>')
def address(network, address):
    srv = SmurferService(network)
    after_txid = request.args.get('after_txid', '', type=str)
    limit = request.args.get('limit', current_app.config['REQUEST_LIMIT_DEFAULT'], type=int)
    limit = current_app.config['REQUEST_LIMIT_MAX'] if limit > current_app.config['REQUEST_LIMIT_MAX'] else limit

    try:
        address_obj = Address.parse(address)
    except:
        flash(_('Invalid address'), category='error')
        return redirect(url_for('main.index'))
    else:
        script = Script(public_hash=address_obj.hash_bytes, script_types=[address_obj.script_type])

    txs = srv.gettransactions(address, after_txid=after_txid, limit=limit)
    address_info = srv.getcacheaddressinfo(address)
    # FIXME: Bitcoinlib gives wrong balance if txs list is incomplete
    # balance_tot = address_info['balance']
    # if not balance_tot:
    balance_tot = srv.getbalance(address)

    prev_url = None
    next_url = None
    if not srv.complete and txs and len(txs) >= limit:
        next_url = url_for('main.address', network=network, address=address, after_txid=txs[-1:][0].txid)
    if after_txid:
        prev_url = url_for('main.address', network=network, address=address)

    inputs = []
    for t in txs:
        t.balance_change = sum([o.value for o in t.outputs if o.address == address]) - \
                           sum([i.value for i in t.inputs if i.address == address])
        inputs += [i for i in t.inputs if i.address == address]
    input = None if not inputs else inputs[0]

    tzutc = timezone.utc
    return render_template('explorer/address.html', title=_('Address'), subtitle=address,
                           transactions=txs, address=address_obj, balance=balance_tot, network=network,
                           next_url=next_url, prev_url=prev_url, address_info=address_info, after_txid=after_txid,
                           limit=limit, script=script, input=input, tzutc=tzutc)


@bp.route('/<network>/key/<key>')
def key(network, key):
    network_name = Config.NETWORKS_ENABLED[network]
    witness_type = request.args.get('witness_type', DEFAULT_WITNESS_TYPE, type=str)
    try:
        k = HDKey(key, network=network_name, witness_type=witness_type)
    except Exception as e:
        flash(_('Invalid key: %s' % e), category='error')
        return redirect(url_for('main.index'))

    if k.is_private:
        flash(_('Never post your private key online. Only use this for test keys or in an offline environment!'),
              category='error')
    return render_template('explorer/key.html', title=_('Key'), subtitle=k.wif(), key=k, network=network)


@bp.route('/<network>/signature/<signature>')
def signature(network, signature):
    try:
        sig = Signature.parse(signature)
        subtitle = sig.hex()[:12] + "..." + sig.hex()[-12:]
    except Exception as e:
        flash(_('Invalid signature: %s' % e), category='error')
        return redirect(url_for('main.index'))

    return render_template('explorer/signature.html', title=_('Signature'), subtitle=subtitle,
                           sig=sig, network=network, definitions=definitions)


@bp.route('/<network>/blocks', methods=['GET', 'POST'])
def blocks(network):
    srv = SmurferService(network)
    blockcount = srv.blockcount()
    from_block = request.args.get('from_block', blockcount, type=int)

    form = SearchForm()
    form.search.render_kw = {'placeholder': 'enter block hash or block height'}
    if form.validate_on_submit():
        return search_query(form.search.data, network=network)

    blocks = []
    for blockid in range(from_block, from_block-10, -1):
        blocks.append(srv.getblock(blockid, parse_transactions=False, limit=0))

    prev_url = None
    if blockcount > from_block:
        prev_block = from_block + 10
        if prev_block > blockcount:
            prev_block = blockcount
        prev_url = url_for('main.blocks', network=network, from_block=prev_block)
    next_url = url_for('main.blocks', network=network, from_block=from_block-10)

    return render_template('explorer/blocks.html', title=_('Blocks'),
                           subtitle=_('Latest blocks in the %s blockchain' % srv.network.name.capitalize()),
                           next_url=next_url, prev_url=prev_url,
                           blockcount=blockcount, blocks=blocks, network=network, form=form)


@bp.route('/<network>/block/<blockid>')
def block(network, blockid):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config['REQUEST_LIMIT_DEFAULT'], type=int)
    limit = current_app.config['REQUEST_LIMIT_MAX'] if limit > current_app.config['REQUEST_LIMIT_MAX'] else limit

    srv = SmurferService(network)
    if blockid == 'last':
        blockid = srv.blockcount()
    if not blockid.isdigit() and not (isinstance(blockid, str) and len(blockid) == 64):
        flash(_("Invalid Block id"), category='error')
        return redirect(url_for('main.index'))
    block = srv.getblock(blockid, parse_transactions=True, limit=limit, page=page)
    if not block:
        flash(_("Block not found"), category='error')
        return redirect(url_for('main.index'))

    prev_url = None
    next_url = None
    txs = block.transactions

    coinbase_data = ''
    if txs and len(txs) and txs[0].coinbase:
        coinbase_data = txs[0].inputs[0].unlocking_script

    if not srv.complete and txs and len(txs) >= limit:
        next_url = url_for('main.block', network=network, blockid=blockid, limit=limit, page=page+1)
    if page > 1:
        prev_url = url_for('main.block', network=network, blockid=blockid, limit=limit, page=page-1)

    tzutc = timezone.utc
    return render_template('explorer/block.html', title=_('Block'), subtitle=blockid, block=block, network=network,
                           coinbase_data=coinbase_data, prev_url=prev_url, next_url=next_url, tzutc=tzutc)


@bp.route('/<network>/script', methods=['GET', 'POST'])
@bp.route('/<network>/script/<script_hex>', methods=['GET', 'POST'])
def script(network, script_hex=""):
    form = ScriptForm()
    if form.validate_on_submit() or script_hex:
        try:
            script_hex = script_hex or form.script_hex.data
            if not form.script_hex.data:
                form.script_hex.data = script_hex
            script = Script.parse_hex(script_hex)
        except (ScriptError, ValueError) as e:
            flash(_('Could not parse script. Error: %s' % e), category='error')
            return redirect(url_for('main.script', network=network))
        return render_template('explorer/script_decomposed.html', title=_('Decomposed Script'),
                               subtitle=_('Parse script and extract type, data and opcodes'), form=form,
                               script=script, network=network, definitions=definitions)

    return render_template('explorer/script.html', title=_('Script'), subtitle=_('Decompose Scripts'),
                           form=form, network=network)

@bp.route('/<network>/sighash_flag/<flag>', methods=['GET'])
def sighash_flag(network, flag):
    try:
        flag_int = int(flag)
        flag_name = definitions.SIGHASH_FLAGS[flag_int][0]
        flag_desc = definitions.SIGHASH_FLAGS[flag_int][1]
    except Exception as e:
        flash(_("SIGHASH flag not recognised"), category='error')
        return redirect(url_for('main.index'))
    return render_template('explorer/sighash_flag.html', title=_('SIGHASH Flag'), network=network,
                           flag=flag, flag_name=flag_name, flag_desc=flag_desc)


@bp.route('/<network>/network')
def network(network):
    srv = SmurferService(network)
    network_details = srv.network
    network_info = srv.getinfo()
    if not network_info:
        flash(_('Could not connect to %s network' % network_details.name), category='error')
        return redirect(url_for('main.index', network=network))
    hashrate = Quantity(network_info['hashrate'], 'H/s')

    return render_template('explorer/network.html', title=_('Network'),
                           network=network, network_info=network_info, network_details=network_details,
                           hashrate=hashrate,
                           subtitle='Nerdy details about the %s network' % network_details.name)


@bp.route('/<network>/store_data', methods=['GET', 'POST'])
def store_data(network):  # pragma: no cover
    srv = SmurferService(network)
    form = StoreDataForm()
    tx_fee = srv.estimatefee(10) // 10
    if form.validate_on_submit():
        w = wallet_create_or_open('BS_embed_data_wallet', witness_type='p2sh-segwit', network=srv.network.name)
        w.scan(scan_gap_limit=1)
        if w.balance():
            lock_script = b'\x6a' + varstr(form.data.data)
            t = w.send([Output(0, lock_script=lock_script)], fee=form.transaction_fee.data, broadcast=True)
            tzutc = timezone.utc
            return render_template('explorer/store_data_send.html', title=_('Push Transaction'),
                                   subtitle=_('Embed the data on the %s network' % srv.network.name),
                                   transaction=t, t=t, tzutc=tzutc, network=network)
        else:
            k = w.get_key()
            message = "Store%20Data%20-%20Blocksmurfer"
            paymentlink = '%s:%s?amount=%.8f&message=%s' % \
                          (srv.network.name, k.address, form.transaction_fee.data * srv.network.denominator, message)
            return render_template('explorer/store_data_fund.html', title=_('Fund Transaction'),
                                   subtitle=_('Fund the %s transaction and store data on the blockchain' %
                                              srv.network.name),
                                   address=k.address, tx_fee=form.transaction_fee.data, data=form.data.data,
                                   paymentlink=paymentlink, network=network)

    return render_template('explorer/store_data.html', title=_('Store Data'),
                           subtitle=_('Embed data on the %s blockchain' % srv.network.name), form=form,
                           tx_fee=tx_fee, network=network)

@bp.route('/<network>/op_code/<op_code>', methods=['GET'])
def op_code(network, op_code):
    opcodenames_lower = [x[3:].lower() for x in opcodenames.values()]
    if op_code.startswith('op_'):
        method_str = op_code.split('_', 1)[1]
        if method_str.isnumeric() and int(method_str) >= 0 and int(method_str) <= 16:
            method_code = ("# Representation of Bitcoin script number. Value between 0 and 16\n"
                           "# Numeric value %s\n"
                           "Stack.op_%s"
                           % (method_str, method_str))
        else:
            try:
                method_code = inspect.getsource(getattr(Stack, op_code))
            except Exception as e:
                flash(_('Source code for op_code not found: %s') % e, category='error')
                opcodeint = opcodeints[op_code.upper()]
                all_methods = ['op_' + i for i in difflib.get_close_matches(op_code[3:], opcodenames_lower, cutoff=0)]
                all_methods += ['op_verify', 'op_add', 'op_if']
                all_methods = list(set(all_methods))
                method_code = ''
                return render_template('explorer/op_code.html', title=_('%s opcode' % op_code[3:].upper()),
                                       subtitle=_('%s bitcoin script command' % op_code), network=network,
                                       op_code=op_code,
                                       method_code=method_code, opcodeint=opcodeint, all_methods=all_methods)
    else:
        flash(_('Unknown op_code'), category='error')
        return redirect(url_for('main.index', network=network))

    opcodeint = opcodeints[op_code.upper()]
    all_methods = re.findall(r'op_\w+', method_code)
    all_methods += ['op_' + i for i in difflib.get_close_matches(op_code[3:], opcodenames_lower, cutoff=0)]
    all_methods =\
        list(set([m.lower() for m in all_methods if m != 'op_as_number']))
    return render_template('explorer/op_code.html', title=_('%s opcode' % op_code[3:].upper()),
                           subtitle=_('%s bitcoin script command' % op_code), network=network, op_code=op_code,
                           method_code=method_code, opcodeint=opcodeint, all_methods=all_methods)

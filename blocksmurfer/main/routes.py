from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from blocksmurfer.main import bp
from blocksmurfer.main.forms import SearchForm
from blocksmurfer.explorer.search import search_query
from blocksmurfer.explorer.service import *
from bitcoinlib.keys import HDKey
from bitcoinlib.transactions import script_to_string, script_deserialize


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return search_query(form.search.data)
    return render_template('index.html', title=_('Explorer'), subtitle=_('Smurfing the blockchain since 2020'),
                           form=form)


@bp.route('/search/<search_string>')
def search(search_string):
    return search_query(search_string)


@bp.route('/bitcoinlib')
def bitcoinlib():
    return render_template('bitcoinlib.html', title=_('Bitcoinlib'), subtitle=_('Python bitcoin library'))


@bp.route('/api')
def api():
    return render_template('api.html', title=_('API'), subtitle=_('Bitcoin blockchain API'))


@bp.route('/about')
def about():
    return render_template('about.html', title=_('About'), subtitle=_('Keep on smurfing!'))


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
    return render_template('explorer/transaction.html', title=_('Transaction'), subtitle=txid, transaction=t,
                           network=network)


@bp.route('/<network>/transaction/<txid>/input/<index_n>')
def transaction_input(network, txid, index_n):
    srv = SmurferService(network)
    t = srv.gettransaction(txid)
    if not t:
        flash(_('Transaction %s not found' % txid), category='error')
        return redirect(url_for('main.index'))
    if int(index_n) > len(t.inputs):
        flash(_('Transaction input with index number %s not found' % index_n), category='error')
        return redirect(url_for('main.transaction', network=network, txid=txid))
    input = t.inputs[int(index_n)]
    locking_script_op = ''
    locking_script_dict = ''
    unlocking_script_op = ''
    unlocking_script_dict = ''
    try:
        locking_script_op = script_to_string(input.unlocking_script_unsigned, name_data=True)
    except:
        pass
    try:
        locking_script_dict = script_deserialize(input.unlocking_script_unsigned)
    except:
        pass
    try:
        unlocking_script_op = script_to_string(input.unlocking_script, name_data=True)
    except:
        pass
    try:
        unlocking_script_dict = script_deserialize(input.unlocking_script)
    except:
        pass

    return render_template('explorer/transaction_input.html', title=_('Transaction Input %s' % index_n), subtitle=txid,
                           transaction=t, network=network, input=input, index_n=index_n,
                           locking_script_op=locking_script_op, locking_script_dict=locking_script_dict,
                           unlocking_script_op=unlocking_script_op, unlocking_script_dict=unlocking_script_dict)


@bp.route('/<network>/transaction/<txid>/output/<output_n>')
def transaction_output(network, txid, output_n):
    srv = SmurferService(network)
    t = srv.gettransaction(txid)
    if not t:
        flash(_('Transaction %s not found' % txid), category='error')
        return redirect(url_for('main.index'))
    if int(output_n) > len(t.outputs):
        flash(_('Transaction output with index number %s not found' % output_n), category='error')
        return redirect(url_for('main.transaction', network=network, txid=txid))
    output = t.outputs[int(output_n)]
    locking_script_op = ''
    locking_script_dict = ''
    try:
        locking_script_op = script_to_string(output.lock_script, name_data=True)
    except:
        pass
    try:
        locking_script_dict = script_deserialize(output.lock_script)
    except:
        pass
    return render_template('explorer/transaction_output.html', title=_('Transaction Output %s' % output_n),
                           subtitle=txid, transaction=t, network=network, output=output, output_n=output_n,
                           locking_script_dict=locking_script_dict, locking_script_op=locking_script_op)


@bp.route('/<network>/address/<address>')
def address(network, address):
    srv = SmurferService(network)
    after_txid = request.args.get('after_txid', '', type=str)

    address_obj = Address.import_address(address)

    txs = srv.gettransactions(address, after_txid=after_txid, max_txs=5)
    address_info = srv.getcacheaddressinfo(address)
    # FIXME: Bitcoinlib gives wrong balance if txs list is incomplete
    # balance_tot = address_info['balance']
    # if not balance_tot:
    balance_tot = srv.getbalance(address)

    prev_url = None
    next_url = None
    if not srv.complete and txs and len(txs) >= 5:
        next_url = url_for('main.address', network=network, address=address, after_txid=txs[-1:][0].hash)
    if after_txid:
        prev_url = url_for('main.address', network=network, address=address)

    for t in txs:
        t.balance_change = sum([o.value for o in t.outputs if o.address == address]) - \
                           sum([i.value for i in t.inputs if i.address == address])
                           
    return render_template('explorer/address.html', title=_('Address'), subtitle=address, transactions=txs,
                           address=address_obj, balance=balance_tot, network=network, next_url=next_url,
                           prev_url=prev_url, address_info=address_info)


@bp.route('/<network>/key/<key>')
def key(network, key):
    network_name = network_code_translation[network]
    try:
        k = HDKey(key, network=network_name)
    except Exception as e:
        flash(_('Invalid key: %s' % e), category='error')
        return redirect(url_for('main.index'))

    if k.is_private:
        flash(_('Never post your private key online. Only use this for test keys or in an offline environment!'),
              category='error')
    return render_template('explorer/key.html', title=_('Key'), subtitle=k.wif(), key=k, network=network)


@bp.route('/<network>/block/<blockid>')
def block(network, blockid):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    srv = SmurferService(network)
    if blockid == 'last':
        blockid = srv.blockcount()
    block = srv.getblock(blockid, parse_transactions=True, limit=limit)
    if not block:
        flash(_("Block not found"), category='error')
        return redirect(url_for('main.index'))

    prev_url = None
    next_url = None
    txs = block['txs']
    if not srv.complete and txs and len(txs) >= limit:
        next_url = url_for('main.block', network=network, blockid=blockid, limit=limit, page=page+1)
    if page > 1:
        prev_url = url_for('main.block', network=network, blockid=blockid, limit=limit, page=page-1)

    return render_template('explorer/block.html', title=_('Block'), block=block, network=network, prev_url=prev_url,
                           next_url=next_url)

import unittest
from blocksmurfer import current_app
from tests.test_custom import CustomAssertions
from blocksmurfer.explorer.service import SmurferService


class TestSite(unittest.TestCase):

    def setUp(self):
        self.app = current_app().test_client()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        expected_str = b'Smurfing'
        self.assertIn(expected_str, response.data)
        self.assertEqual(response.status_code, 200)

    def test_api_page(self):
        response = self.app.get('/api', follow_redirects=True)
        expected_str = b'Blocksmurfer API documentation'
        self.assertIn(expected_str, response.data)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        expected_str = b'Coineva'
        self.assertIn(expected_str, response.data)
        self.assertEqual(response.status_code, 200)

    def test_search_address(self):
        response = self.app.get('/search/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1')
        self.assertIn(b'Redirecting...', response.data)
        self.assertIn(b'/btc/address/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1', response.data)
        self.assertEqual(response.status_code, 302)

    def test_search_transaction(self):
        response = self.app.get('/search/258478e8b7a3b78301661e78b4f93a792af878b545442498065ab272eaacf035')
        self.assertIn(b'Redirecting...', response.data)
        self.assertIn(b'/btc/transaction/258478e8b7a3b78301661e78b4f93a792af878b545442498065ab272eaacf035',
                      response.data)
        self.assertEqual(response.status_code, 302)

    def test_search_block(self):
        response = self.app.get('/search/123456')
        self.assertIn(b'Redirecting...', response.data)
        self.assertIn(b'/btc/block/123456', response.data)
        self.assertEqual(response.status_code, 302)

    def test_search_key(self):
        response = self.app.get('/search/xpub661MyMwAqRbcGpWkuXwKRMAnJUnwBBSFo3KpormL4ti5m5i7q8D7Rih8fvCAHWXhCA'
                                '3aF3KvGWw4PZtqc9ymsSrkCLbC9Xgeqao6t5eWbrD')
        self.assertIn(b'Redirecting...', response.data)
        self.assertIn(b'/btc/key/xpub661MyMwAqRbcGpWkuXwKRMAnJUnwBBSFo', response.data)
        self.assertEqual(response.status_code, 302)

    def test_explorer_address(self):
        response = self.app.get('/btc/address/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1')
        self.assertIn(b'b3407d4b4d1fca87fb930abe3fa6c2baed6e6fd8', response.data)
        self.assertIn(b'2013-09-11 22:05:17', response.data)
        self.assertIn(b'/btc/transaction/5fd3d8275afb5b5cc202ae8480daefa4fe16d0cf480ce78545d6dc06c6fb101a',
                      response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_address_p2sh(self):
        response = self.app.get('/btc/address/3Guw4MDSyLJCiP5yWBAVVapvHMS7KsXAFP')
        self.assertIn(b'a6fb3b9982aa381c426a8f28af4652c814bc98ad', response.data)
        self.assertIn(b'd09def635126ba8971908024102d21bb88ff09e74dfcda65acd29b7fe1e467ab', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_address_bech32(self):
        response = self.app.get('/btc/address/bc1qhxzdefx7d4gw473d47xtj6frnglqnx5yfdn7q6')
        self.assertIn(b'f14980037c5fc011f231847bba308ff0e3435976e1766e53c7bfafc3065ef41b', response.data)
        self.assertIn(b'b984dca4de6d50eafa2daf8cb969239a3e099a84', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_address_paging(self):
        response = self.app.get('/btc/address/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1?after_txid=d658ab87cc053b8dbcfd4a'
                                'a2717fd23cc3edfe90ec75351fadd6a0f7993b461d')
        self.assertIn(b'4be9e8f3a35a7c597ae9641b2767242aca0d0abe20bf419b9168ea373b88fe48', response.data)
        self.assertIn(b'1ed74cf9ec10bb9eb881dfcbc97318baadff371e25f227587b8d87466f260cad', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction(self):
        response = self.app.get('/btc/transaction/258478e8b7a3b78301661e78b4f93a792af878b545442498065ab272eaacf035')
        self.assertIn(b'1LtjWsKsrr2RweDLAmv75oGL7tjVF4wx7W', response.data)
        self.assertIn(b'8098000000', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_segwit(self):
        response = self.app.get('/btc/transaction/466490c0401d4d7ea781ca1a4ef22ac889c3404385c95c18edd1447c3a500d45')
        self.assertIn(b'2020-01-08 03:52:41', response.data)
        self.assertIn(b'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej', response.data)
        self.assertIn(b'0.15175083', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_coinbase(self):
        response = self.app.get('/btc/transaction/ce242be116c5caf016185f4f4e75628843ecb18faeb2935c9a9c848464f693a4')
        self.assertIn(b'2020-01-08', response.data)
        self.assertIn(b'611838', response.data)
        self.assertIn(b'3QLeXx1J9Tp3TBnQyHrhVxne9KqkAS9JSR', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_unconfirmed(self):
        srv = SmurferService()
        mempool = srv.mempool()
        if not isinstance(mempool, list) or not mempool:
            pass
        else:
            response = self.app.get('/btc/transaction/%s' % mempool[0])
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'unconfirmed', response.data)

    def test_explorer_transaction_input(self):
        response = self.app.get('btc/transaction/f59f7d4f1a0df81ad48e2dc4dd6320b15744ed38e16ab9a7f16507eca0c6a6de/'
                                'input/6')
        self.assertIn(b'02ea08ccfdda6183c3e7d57c813567299efd0f0b233a3a32267ba9c2af3080aa1b', response.data)
        self.assertIn(b'86e49fa2a32c1f8e9828512a97ea87fbd1ef1e4af701', response.data)
        self.assertIn(b'signature-1 SIGHASH_ALL public_key', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_input_coinbase(self):
        response = self.app.get('btc/transaction/a2fcf9af82c1ced2c2ab14fe07dcf9c725473cc6ac35865d65a1adc3b767eb96/'
                                'input/0')
        self.assertIn(b'a2fcf9af82c1ced2c2ab14fe07dcf9c725473cc6ac35865d65a1adc3b767eb96', response.data)
        self.assertIn(b'coinbase', response.data)
        self.assertIn(b'0.00000000', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_output(self):
        response = self.app.get('btc/transaction/ffccb3c55dccc6d1596008f66c894ef94820a6667833b35c7d5180d603d77c09/'
                                'output/0')
        self.assertIn(b'001497cfc76442fe717f2a3f0cc9c175f7561b661997', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction_output_nulldata(self):
        response = self.app.get('btc/transaction/7af7bea324b9cf4d6692d7b63518c076c55616c7943310dec9c23b2435ca4609/'
                                'output/0')
        self.assertIn(b'1 wallet_create_or_open\nfrom bitcoinlib.encoding import varstr\n\nwallet = wa', response.data)
        self.assertIn(b'Nulldata', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_block(self):
        response = self.app.get('/btc/block/123456')
        self.assertIn(b'0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca', response.data)
        self.assertIn(b'60925f1948b71f429d514ead7ae7391e0edf965bf5a60331398dae24c6964774', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_block_paging(self):
        response = self.app.get('/btc/block/630000?limit=3&page=2')
        self.assertIn(b'40352adf6fba255e083c60a21f9f85774ce7c97017f542bf22c63be2ef9f366b', response.data)
        self.assertIn(b'3ea1a64c550ff91c6faba076aa776faa60aa524b48a54801d458d1c927333c8f', response.data)

    def test_explorer_key(self):
        response = self.app.get('/btc/key/0253d6e3713c055cb564e95e74e1f22481c5b20e469392bd99f4959f1edc5b5bd1')
        self.assertIn(b'a5dab81699794b605f62373f786fdbe611511ed1', response.data)
        self.assertIn(b'1G7xWXE9C8sFxoPjTaskMawTjd73Xi3Hdt', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_key_uncompressed(self):
        response = self.app.get('/btc/key/049c75653ef36730eeab77cf9b7b5f16a47aa559f1f180537c060601a58201ab66633cb1b'
                                'fbfdab45dcbd9954d59937e5edb85b4e9a6395cb61f46fd50bd62a59e')
        self.assertIn(b'1HuDmRYnLGcwKaxBpU8Pf8VoP64yqbd5uj', response.data)
        self.assertIn(b'44886209612287888408981908687942174778875113046523022127243311468090985981342', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_key_private(self):
        response = self.app.get('/btc/key/L3Y9yh4Y51MdAaFRwGxWr1YfH4yzQMHBhYRJGjFR21HJtZX31L32')
        self.assertIn(b'1G7xWXE9C8sFxoPjTaskMawTjd73Xi3Hdt', response.data)
        self.assertIn(b'bc8356addcde4cb937fea0e70e3895236ac55cc9dd2fa14254c1443faf14fd59', response.data)
        self.assertIn(b'Never post your private key online', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_key_private_wif(self):
        response = self.app.get('/btc/key/xprv9s21ZrQH143K3r8xRLrpQ9z7P5NUcxmmWZ12GPMQJfsSpVn56Yo9CFymaKdDePM1WbmqPc'
                                'TNQnkzZz2LjfmWNH8ap22PRWYHq7R3qDY7ehg')
        self.assertIn(b'1BBVxhsVgGg6WZJaXF6k3g3XEydUQheXbB', response.data)
        self.assertIn(b'L4Lq174mgGYDpyQjJsmYniv9PkeDQ4CasgqSrppQGfmukh2xiUDe', response.data)
        self.assertIn(b'Never post your private key online', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_key_xpub(self):
        response = self.app.get('/btc/key/xpub661MyMwAqRbcGpWkuXwKRMAnJUnwBBSFo3KpormL4ti5m5i7q8D7Rih8fvCAHWXhCA'
                                '3aF3KvGWw4PZtqc9ymsSrkCLbC9Xgeqao6t5eWbrD')
        self.assertIn(b'02e454cea7d62cef1e959f20aa5bfe7c852a15341de1899892ab37372f01c5ec63', response.data)
        self.assertIn(b'103277170915039968320476074728082180282525753362284913527381919915150173138019', response.data)
        self.assertEqual(response.status_code, 200)


class TestAPI(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.app = current_app().test_client()

    def test_api_block(self):
        response = self.app.get('/api/v1/btc/block/120000')
        self.assertEqual(response.status_code, 200)
        expected = {"hash": "0000000000000e07595fca57b37fea8522e95e0f6891779cfd34d7e537524471", "height": 120000,
                    "limit": 99999, "merkle_root": "6dbba50b72ad0569c2449090a371516e3865840e905483cac0f54d96944eee28",
                    "page": 1, "pages": 1,
                    "time": 1303687201, "total_txs": 56,
                    "txs": ["1829755bdbe84f5a1ca579c1ed2f78a051a817b66ed4dfff35704cd6d4d644f9",
                            "db6d13b57fb0daef6ebb8af735a4b2776f11143e760d0c90e4251613bb00e43b",
                            "1824bac57c0ba9565e867a4915906a9c78c83ba3f668d0164bb0c4c9acb34fac",
                            "a7ee0da5061982cb9c2bb95da715a90c3f8a717fa6d2f74a9934825017acaea6",
                            "79b8ea58d3a3d18b583ac7b8fed5b7b06706a5198d4ffc38095d9fc55dc62030",
                            "ba716aaf87bc2030bdc1a3ee7deadf34d36e8fa02cb848e73eabedd3e6a7d74b",
                            "dedabaa2b1e6e5fff513bf0a2aeebccf2b650617ff540e4baa27ff3588692acc",
                            "6182f42ea89a59df3a417f958e1c9bb3f0ea8ee7193cda760b477c4ce09c357c",
                            "8469c30ba524b81509db66d1729bb2ee470329de6f3174f11ea7b86a4158b5d6",
                            "1ecc492e27064d4d6ddf428376135f3fabdc1d8816e1b1655d28d82fe9e3c13d",
                            "5bb631bfd9a819e9d4ee6188c624dd3d975970fb4d1ffdeb62dd39b92dd526a6",
                            "875b82878572987f448f122bbe1f2235afa7eeab128619321221e703d99e4368",
                            "ca744b08ea45c22d2951c25c48298b751c7caf6eea2c799054d484606d7a7f13",
                            "c0cbad983ca538c242134c086b652f4ca068a89294dd68aab9c1d9de72e58653",
                            "d81a57980bfcec9989e34f85d4c1e8905b940ea0d13949242a2de720d0b5b592",
                            "3acd6221d34327217c06162cdf9ee133b47e7efe92e7b55361c96904faee0c6c",
                            "0132cff762fbeb15d7d1421264c412401adda2a53a8fe173321aacdb37e5b7b0",
                            "356e6a86dd145d2feb54cdef948de9ae23092469d5e9632abff6f81ad22c02e0",
                            "cb7b6ef9ed762549cfcebf17076a22a726683ebbcf37e5a3fb678b45dc3b51db",
                            "453369ba6418d0dfe687abec6f47e60244b4b76dacb844e53051c5944195227b",
                            "77a0b8913236a39bc5f5e585efa893cd39e426ec1e766121becccecc4f49af39",
                            "80808e54b8fd5391c88b5e5db8167516555a993bb4a7ddbe868e1854db9b4b02",
                            "162cb86244da265330a264341ece720edc425eafe90efbc18258c4f1764b7076",
                            "8f29c46680afd7d6e55fa46e3b1fcf00605c2640ff1e1cec7ba5441191054c36",
                            "409be0865675eb7c3078401c994ea6a4c6c138b4e87ed53c73e9d0e71dee4598",
                            "3420b2c059781f5ee772836b5207860ccf5f958a2c045161270f11eaf004c335",
                            "5fb7b81731b7a0cfbe30f17b0a8c4844f6c48ce80a10d86e7110b0d820470e07",
                            "09d79e6249a7233621a4f0889fe72898d730456ebae7854658faeb16d596fef2",
                            "31f429a9b22ab93ab4548ab3b9b245f1e9e09407d66cb397244e07fa337264e7",
                            "43d2584065ccb69a0b8b6f1f41544d07dea07411ba1fd25b456d49ce687bbacb",
                            "3bad7fd1ca33664a96ed20c308683d82e6dfb8b12be3be5f6f61f438b6ce912b",
                            "d619da0cd8aa21e1b33a7bcaf1e5ede1906308992ae5ffb41a02d16953b7ca2c",
                            "c8c2bd8367dce6305d974c59741f8383833c1908cf27e18b614bd2b2e2517a8b",
                            "ab1584e050d81da5565e93f40e6c5058079da429522471179e4de0fa5cf9611c",
                            "fe8b4de4caca2fb8910194a34d0b6b8d3a08e518febe276f2a1646c6985828a8",
                            "259d1dd303f1bcc8c40128596073cdcf243fb7af2d62ad36525dc49d5f913008",
                            "6e78164bdb78b66616b70ba38e0916422f34c6316ade1ed39d795f04840bbdab",
                            "c2d3aca99b1ca6c50494b8f90632a14c0c4ed9138f0c1fd7bf5084368eb86ced",
                            "5c463283e2deeb1eccdf143d970c40dd117bfd85ad3f2e38ea3fdbca8e3198c3",
                            "be26ca600b2566d20ccf59b3808ce283619902268407e5599802b5d4d8f52f0f",
                            "6997dfd7f7f288a1ba7989b13a225f575316bbe9beb2dab91ce52a63324c6154",
                            "57a14b64ea112d3cfc86395a19aff5267a1686d70c3726170b50ad218c7bfb0c",
                            "5df91dea542064a69b1495e1899f84255dcbd50394a3b10602b70b1a27ef8a35",
                            "76582f0ca5f93e2051a25a509d06155ebc7f46b87bfbe5b77db649cb02cc968e",
                            "8d60c324946d620a794e89438c703c927af7da1184d0767709fc52846399d14c",
                            "2e7a15f604e78871c621d737c3e9655363424ce9e85579b97eb420009a58d4f0",
                            "854e1717d5d5f063367aee1345da0a4824d34c1c4456106c4dddd1c0265bf95a",
                            "d2cedcae4b336b9daf5ffd050ad3895eaeb3a90f6fc87130eab7b583ad3c2bdd",
                            "1adce1ebeb39c6f9a3b2c8ac5189f161d987217720c44ed81b10c3f1471e7438",
                            "2e1aaa51b0433b83c65e7269b830675ad6a59f795ceb1b5ecbbd80af15c8b557",
                            "fdfcbed87364ac3ffda6ff5eced6f2e39cb4d3d3dee42f18056b06bfac0c0cc9",
                            "840ae018fd594b5e5927451c98d73d033651303ad00c4ef8f8546f9a33ab7415",
                            "64ed1e2b01458624e74225e18deba497f4a122334ae03a77b980c98ca794aa8a",
                            "42aed02a99f2dfa3cb32d64933bc569c127f352f29bd26a06e292dbeabd74119",
                            "d7c9fa4b801a3a4ef78613f4c00707fbb5fea339a7a650bdcfdc11c749e8773e",
                            "6a9fa4566fd2454f73daf71005c9f2ddb75e1c0ced2bcab89472583d60d92a4b"]}
        self.assertDictEqualExt(expected, response.json)

    def test_api_block_paging(self):
        response = self.app.get('/api/v1/btc/block/120000?limit=1&page=4&parse_transactions=True')
        self.assertEqual(response.status_code, 200)
        expected = {
            "hash": "0000000000000e07595fca57b37fea8522e95e0f6891779cfd34d7e537524471", "height": 120000,
            "limit": 1, "merkle_root": "6dbba50b72ad0569c2449090a371516e3865840e905483cac0f54d96944eee28",
            "page": 4, "pages": 56,
            "time": 1303687201, "total_txs": 56, "txs": [
                {"block_hash": "0000000000000e07595fca57b37fea8522e95e0f6891779cfd34d7e537524471",
                 "block_height": 120000, "coinbase": False, "date": "2011-04-24T23:20:01",
                 "fee": 0, "input_total": 2732000000, "inputs": [
                    {"address": "1HCfKLEKipVE9tzuPoYPftQgqXE7acDwKL", "compressed": False, "double_spend": False,
                     "encoding": "base58", "index_n": 0, "locktime_cltv": 0, "locktime_csv": 0, "output_n": 0,
                     "prev_hash": "87975e0549826e2c59fec247c3d52fe2ab4772d6c8c12b89283c62f08bb6361f",
                     "public_hash": "b1b692a037daee7b56a9cd653d61af351b55fce2", "redeemscript": "",
                     "script": "483045022100a832a2f88ff96ad797bc288b1b02158228cc7f6bd605603561b7ae95a62a823202206c376813efc39342d34c353ac8d0a08d3f6c6d9f24e3423fb94d721daa4580ff014104aa10d74f4f377f49fe2961909ae4135b214ee2f1e2e4e497d1e2003532e9ba831e0f42e43f2cb5f2d147be7976586a9606153c2fb067c618a6ef0749693710aa",
                     "script_code": "76a914b1b692a037daee7b56a9cd653d61af351b55fce288ac", "script_type": "sig_pubkey",
                     "sequence": 4294967295,
                     "signatures": "a832a2f88ff96ad797bc288b1b02158228cc7f6bd605603561b7ae95a62a82326c376813efc39342d34c353ac8d0a08d3f6c6d9f24e3423fb94d721daa4580ff",
                     "sigs_required": 1, "valid": None, "value": 2732000000,
                     "witness": "3045022100a832a2f88ff96ad797bc288b1b02158228cc7f6bd605603561b7ae95a62a823202206c376813efc39342d34c353ac8d0a08d3f6c6d9f24e3423fb94d721daa4580ff0104aa10d74f4f377f49fe2961909ae4135b214ee2f1e2e4e497d1e2003532e9ba831e0f42e43f2cb5f2d147be7976586a9606153c2fb067c618a6ef0749693710aa",
                     "witness_type": "legacy"}], "locktime": 0, "network": "bitcoin", "output_total": 2732000000,
                 "outputs": [{"address": "1Yapu4N4f64xkrJVQsLLuWwezL4mXZdGp", "output_n": 0,
                              "public_hash": "05f9219587d9af618b3d051be9595fa1e09b021d",
                              "script": "76a91405f9219587d9af618b3d051be9595fa1e09b021d88ac", "script_type": "p2pkh",
                              "spent": None, "value": 2533000000},
                             {"address": "1LFSZag1HnRKJngVqUJpY2jZjtyMze7GRN", "output_n": 0,
                              "public_hash": "d3258d1c9949d78a6fb29e4b48e47dfaa18dec65",
                              "script": "76a914d3258d1c9949d78a6fb29e4b48e47dfaa18dec6588ac", "script_type": "p2pkh",
                              "spent": None, "value": 199000000}],
                 "raw_hex": "01000000011f36b68bf0623c28892bc1c8d67247abe22fd5c347c2fe592c6e8249055e9787000000008b483045022100a832a2f88ff96ad797bc288b1b02158228cc7f6bd605603561b7ae95a62a823202206c376813efc39342d34c353ac8d0a08d3f6c6d9f24e3423fb94d721daa4580ff014104aa10d74f4f377f49fe2961909ae4135b214ee2f1e2e4e497d1e2003532e9ba831e0f42e43f2cb5f2d147be7976586a9606153c2fb067c618a6ef0749693710aaffffffff024083fa96000000001976a91405f9219587d9af618b3d051be9595fa1e09b021d88acc07fdc0b000000001976a914d3258d1c9949d78a6fb29e4b48e47dfaa18dec6588ac00000000",
                 "size": 258, "status": "confirmed",
                 "txid": "a7ee0da5061982cb9c2bb95da715a90c3f8a717fa6d2f74a9934825017acaea6", "verified": False,
                 "version": 1, "vsize": 258, "witness_type": "legacy"}]}
        self.assertDictEqualExt(expected, response.json)

    def test_api_block_last_and_blockcount(self):
        response = self.app.get('/api/v1/btc/block/last')
        response2 = self.app.get('/api/v1/btc/blockcount')
        self.assertEqual(response.json['height'], response2.json['blockcount'])

    def test_api_transactions(self):
        response = self.app.get('/api/v1/btc/transactions/1KoAvaL3wfpcNvGCQYkqFJG9Ccqm52sZHa?limit=1')
        expected = {
            "height": 246976,
            "coinbase": True, "fee": 0,
            "inputs": [   # FIXME: Add "input_total": 0,
                {"address": "", "encoding": "base58", "index_n": 0, "script_type": "coinbase",
                 "value": 0, "witness_type": "legacy"}],
            "locktime": 0, "network": "bitcoin", "output_total": 2509821000,
            "outputs": [{"address": "1KoAvaL3wfpcNvGCQYkqFJG9Ccqm52sZHa", "output_n": 0, "script_type": "p2pkh",
                         "value": 2509821000}],  # FIXME: Check for spent=True
            "size": 104, "status": "confirmed",
            "txid": "fc27565334c7faa7ceeb457dfb5c8ba459e42c1cd8551a99af41f336fc4fd64d", "witness_type": "legacy"}
        self.assertDictEqualExt(expected, response.json[0])

    def test_api_transactions_after_txid(self):
        response = self.app.get('/api/v1/btc/transactions/1KoAvaL3wfpcNvGCQYkqFJG9Ccqm52sZHa?limit=1&'
                                'after_txid=e10e6acd0465db47a8308befbe53cc267e3d2c078691e9776bd4dd6e6c8ba14b')
        expected = {"coinbase": True, "date": "2013-08-01T12:03:45",
                    "fee": 0, "input_total": 0,
                    "inputs": [
                        {"address": "", "compressed": True, "encoding": "base58", "index_n": 0,
                         "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
                         "script_type": "coinbase", "value": 0, "witness_type": "legacy"}],
                    "output_total": 2514554728,
                    "outputs": [
                        {"address": "1KoAvaL3wfpcNvGCQYkqFJG9Ccqm52sZHa", "output_n": 0,
                         "public_hash": "ce2daea72b5b48fc85d9bba2263225cbe98985e0",
                         "script": "76a914ce2daea72b5b48fc85d9bba2263225cbe98985e088ac", "script_type": "p2pkh",
                         "value": 2514554728}],  # FIXME: Check for spent=True
                    "size": 104, "status": "confirmed",
                    "txid": "060e777d543f905f732b13cc37efc621c47793ba699e4559bd4c2ee83d94a73d",
                    "witness_type": "legacy"}
        self.assertDictEqualExt(expected, response.json[0])

    def test_api_utxos(self):
        response = self.app.get('/api/v1/btc/utxos/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1')
        self.assertEqual(response.status_code, 200)
        expected = [
                    # Blockstream missing first few blocks
                    # {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1", "block_height": 2,
                    #  "date": "2009-01-09T02:55:44", "input_n": 0, "output_n": 0,
                    #  "tx_hash": "9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5",
                    #  "value": 5000000000},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "5fd3d8275afb5b5cc202ae8480daefa4fe16d0cf480ce78545d6dc06c6fb101a", "value": 1},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "b9a84cffd3766bb642a697065b477eed032e36c377db80faac79b18e61b43b0d", "value": 1},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "0986d70aaa03213135998cf1a9b8a33012c033c6607584e84b8ae33d49fadce3", "value": 1},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "d658ab87cc053b8dbcfd4aa2717fd23cc3edfe90ec75351fadd6a0f7993b461d", "value": 911},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "4be9e8f3a35a7c597ae9641b2767242aca0d0abe20bf419b9168ea373b88fe48", "value": 1},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "8f5351233a89bdce6dcf73fbfe295204f8ea67775be0ecd294d30e9932667f76", "value": 10000},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "201d27f660a82b7bee7f00e93dfb7b8cb722ac4ce6e22af502f6047fc7da0a32", "value": 10000},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "7cd30ddf7ec214c80b6accc22f33ddafd42d04d5f583f4d5d0a35c29f8f296d9", "value": 5757},
                    {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                     "tx_hash": "1ed74cf9ec10bb9eb881dfcbc97318baadff371e25f227587b8d87466f260cad", "value": 5757}]
        n = 0
        results = sorted(response.json, key=lambda x: x['block_height'])
        if results[0]["block_height"] == 2:
            results = results[1:]
        for u in results[:len(expected)]:
            self.assertDictEqualExt(expected[n], u)
            n += 1

    def test_api_utxos_after_txid(self):
        response = self.app.get('/api/v1/btc/utxos/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1?'
                                'after_txid=d658ab87cc053b8dbcfd4aa2717fd23cc3edfe90ec75351fadd6a0f7993b461d')
        self.assertEqual(response.status_code, 200)
        expected = {"address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1", "output_n": 0,
                    "tx_hash": "4be9e8f3a35a7c597ae9641b2767242aca0d0abe20bf419b9168ea373b88fe48", "value": 1}
        self.assertDictEqualExt(expected, response.json[0])

    def test_api_address_balance(self):
        response = self.app.get('/api/v1/btc/address_balance/1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json['balance'], 0.01477486)

    def test_api_transaction(self):
        response = self.app.get('/api/v1/btc/transaction/6ab6432a6b7b04ecc335c6e8adccc45c25f46e33752478f0bcacaf3f1'
                                'b61ad92')
        expected = {
            "height": 630000, "coinbase": False, "date": "2020-05-11T19:23:43",
            "fee": 35109, "input_total": 2170991196, "inputs": [
                {"address": "3KPUySzYeEpUyTg4JHBHV4nNPkELzprRnP",
                 "encoding": "base58", "index_n": 0, "output_n": 8,
                 "sigs_required": 1, "valid": None, "value": 2170991196,
                 "witness_type": "p2sh-segwit"}], "network": "bitcoin", "output_total": 2170956087,
            "outputs": [{"address": "12nDYwnGiNhitbVcWC5mVtbMJNCwQfkJZQ", "output_n": 0, "value": 1863367},
                        {"address": "33WXa8ymotqgjQpnimpGkYEyacus77hejz", "output_n": 0, "value": 2169092720}],
            "size": 249, "status": "confirmed",
            "txid": "6ab6432a6b7b04ecc335c6e8adccc45c25f46e33752478f0bcacaf3f1b61ad92", "witness_type": "segwit"}
        self.assertDictEqualExt(expected, response.json)

    def test_api_transaction_raw(self):
        response = self.app.get('/api/v1/btc/transaction/bbf7f927234fc718b153e180b43892528437f135c471ba11ebd33390f2'
                                'cb0dd7?raw=True')
        expected = "02000000012ef46e7e5d1a2e3360e4cf6fe44e1ed3216ec62efbf8b81fcd4468ed99ea2da1000000006a47304402205" \
                   "d7846bc12a851092a0f7c16c30d06ec50b3239f556ef6eb552d31d5a9fd3be202201d74b12d19631848f6f645e7b368" \
                   "ce7565cf720076f51e5366248e77ddfeefe0012102efebe277d93372905c05a2995e24f8b0611c887bdb3b65d549b19" \
                   "c7dbd15ae13ffffffff01385c2a000000000017a91495a8bfd89066c378d747b1ace39e6e1ccd85b3b58700000000"
        self.assertEqual(expected, response.json['raw_hex'])

    def test_api_transaction_fee(self):
        response = self.app.get('/api/v1/btc/fees/5')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['estimated_fee_sat_kb'])

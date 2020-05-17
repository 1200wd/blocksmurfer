import unittest
from blocksmurfer import create_app


class TestSite(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

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
        self.assertIn(b'50.01477486', response.data)
        self.assertIn(b'2009-01-09 02:55:44', response.data)
        self.assertIn(b'btc/transaction/9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5',
                      response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_address2(self):
        response = self.app.get('/btc/address/bc1qjl8uwezzlech723lpnyuza0h2cdkvxvh54v3dn')
        self.assertIn(b'ffccb3c55dccc6d1596008f66c894ef94820a6667833b35c7d5180d603d77c09', response.data)
        self.assertIn(b'97cfc76442fe717f2a3f0cc9c175f7561b661997', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_transaction(self):
        response = self.app.get('/btc/transaction/258478e8b7a3b78301661e78b4f93a792af878b545442498065ab272eaacf035')
        self.assertIn(b'1LtjWsKsrr2RweDLAmv75oGL7tjVF4wx7W', response.data)
        self.assertIn(b'8098000000', response.data)
        self.assertEqual(response.status_code, 200)

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
        self.assertIn(b'4294967295', response.data)
        self.assertIn(b'coinbase', response.data)
        self.assertIn(b'03639f0904992cc05e535a30322f4254432e434f4d2ffabe6d6ddcb3921d5735819ea6fe8ad', response.data)
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

    def test_explorer_key(self):
        # http://localhost:5000/btc/transaction/07d0f317b516e9510a93817c67aba001a8d759e7e5a293d874a240669f2dddb7/input/0
        response = self.app.get('/btc/key/029c75653ef36730eeab77cf9b7b5f16a47aa559f1f180537c060601a58201ab66')
        self.assertIn(b'1HuDmRYnLGcwKaxBpU8Pf8VoP64yqbd5uj', response.data)
        self.assertIn(b'12TcUST6vj3FEJdQwb98AipVfGJEEbfnsD', response.data)
        self.assertIn(b'44886209612287888408981908687942174778875113046523022127243311468090985981342', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_key_xpub(self):
        response = self.app.get('/btc/key/xpub661MyMwAqRbcGpWkuXwKRMAnJUnwBBSFo3KpormL4ti5m5i7q8D7Rih8fvCAHWXhCA'
                                '3aF3KvGWw4PZtqc9ymsSrkCLbC9Xgeqao6t5eWbrD')
        self.assertIn(b'02e454cea7d62cef1e959f20aa5bfe7c852a15341de1899892ab37372f01c5ec63', response.data)
        self.assertIn(b'103277170915039968320476074728082180282525753362284913527381919915150173138019', response.data)
        self.assertEqual(response.status_code, 200)
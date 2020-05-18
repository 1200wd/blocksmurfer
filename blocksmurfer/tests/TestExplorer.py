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

    def test_explorer_address_p2sh(self):
        response = self.app.get('/btc/address/3DPNFXGoe8QGiEXEApQ3QtHb8wM15VCQU3')
        self.assertIn(b'804afd8b3479267b0cd0bb2fa2e217096005fb8d', response.data)
        self.assertIn(b'41d590e937135232a9ff88fd199629e83c349d6f4c0a3f15da88fceaa399abb8', response.data)
        self.assertEqual(response.status_code, 200)

    def test_explorer_address_bech32(self):
        response = self.app.get('/btc/address/bc1qjl8uwezzlech723lpnyuza0h2cdkvxvh54v3dn')
        self.assertIn(b'ffccb3c55dccc6d1596008f66c894ef94820a6667833b35c7d5180d603d77c09', response.data)
        self.assertIn(b'97cfc76442fe717f2a3f0cc9c175f7561b661997', response.data)
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
        self.assertIn(b'2020-01-08 03:52:41', response.data)
        self.assertIn(b'020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff4e03'
                      b'fe5509040a52155e434e2f54545454545433333333fabe6d6deaccb8c04410ac109e44b1df7f8ff22cb137b78c'
                      b'8a1876bf4b12326f2a3b0ff6020000004204cb9a84039e40a770b35d60ad2300ffffffff03b862244b00000000'
                      b'17a914f870b7fbb0ce391d9ddc16ad98479d8cbbbd5c41870000000000000000266a24aa21a9ed6d23356a7beb'
                      b'b4c789e1ec07185a369d4a40fd71fd9116761fcac31fecadd0010000000000000000266a24b9e11b6dfae908d0'
                      b'8429e68cf06c601a329a3bfae282bcb4fd0379759738971ea341b1050000000000', response.data)
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



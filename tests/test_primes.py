import unittest
from functionality import primes


class MyTestCase(unittest.TestCase):
    def test_ipow(self):
        list = primes.ipow(10, 2, 3)
        for i in list:
            self.assertEqual(i, 1)
    def test_rabinmillerwitness(self):
        result = primes.rabin_miller_witness(10,3)
        result2 = primes.rabin_miller_witness(1,1)
        self.assertEqual(result, False)
        self.assertEqual(result2, True)
    def test_defaultk(self):
        self.assertEqual(primes.default_k(24), 48)
        self.assertEqual(primes.default_k(2), 40)
        self.assertEqual(primes.default_k(20), 40)
        self.assertEqual(primes.default_k(0), 40)
    def test_probably_prime(self):
        self.assertEqual(primes.is_probably_prime(1), True)
        self.assertEqual(primes.is_probably_prime(7), True)
        self.assertEqual(primes.is_probably_prime(4), False)
    def test_generateprime(self):
        test1 = primes.generate_prime(8)
        test2 = primes.generate_prime(128)
        self.assertEqual(primes.is_probably_prime(test1), True)
        self.assertEqual(primes.is_probably_prime(test2), True)
        self.assertRaises(AssertionError, lambda: primes.generate_prime(4))
    def test_invmod(self):
        self.assertRaises(ValueError, lambda: primes.invmod(0,2))
        self.assertEqual(primes.invmod(2,9), 5)
    def test_puk(self):
        obj = primes.PublicKey(2)
        self.assertEqual(obj.n, 2)
        self.assertEqual(obj.n_sq, 4)
        self.assertEqual(obj.g, 3)
        self.assertEqual(obj.__repr__(), "<PublicKey: 2>")
    def test_pk(self):
        obj = primes.PrivateKey(4, 3, 5)
        self.assertEqual(obj.l, 6)
        self.assertEqual(obj.m, 1)
        self.assertEqual(obj.__repr__(), "<PrivateKey: 6 1>")
    def test_genkeypair(self):
        obj = primes.generate_keypair(16)
        for idx, i in enumerate(obj):
            if idx == 0:
                self.assertIsInstance(i, primes.PrivateKey)
            if idx == 1:
                self.assertIsInstance(i, primes.PublicKey)
            assert idx < 2
    def test_decrypt(self):
        obj = primes.PrivateKey(4, 3, 5)
        obj2 = primes.PublicKey(2)
        self.assertEqual(primes.decrypt_int(obj, 10, 4), 9)
        self.assertEqual(primes.decrypt(obj, obj2, 4), 1)

if __name__ == '__main__':
    unittest.main()

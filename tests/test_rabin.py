import unittest

import rabincryptosystem as rabin


# Fixed primes congruent to 3 (mod 4). Their product is an 8-byte modulus,
# so a message longer than the modulus is split into 3-byte chunks.
P = 4000000007
Q = 3999999979
N = P * Q


class EncryptRejectsTests(unittest.TestCase):
    def test_rejects_a_message_that_is_not_smaller_than_the_modulus(self):
        with self.assertRaises(ValueError):
            rabin.encrypt(N, N)

    def test_rejects_a_message_whose_square_is_not_larger_than_the_modulus(self):
        with self.assertRaises(ValueError):
            rabin.encrypt(77, 2)

    def test_rejects_padding_when_the_message_does_not_fit(self):
        with self.assertRaises(ValueError):
            rabin.add_padding(77, 10)


class RoundTripTests(unittest.TestCase):
    def test_single_block_matches_the_pinned_ciphertext(self):
        ciphertext = rabin.extended_encrypt(N, b"hi")

        self.assertEqual(ciphertext, 0x6ED58848036F9E70)
        self.assertEqual(rabin.extended_decrypt(ciphertext, P, Q), b"hi")

    def test_split_message_matches_the_pinned_blocks_and_decrypts(self):
        ciphertext = rabin.extended_encrypt(N, b"abcdefghi")

        self.assertEqual(
            ciphertext,
            [
                0xFB4464D022B3A0C,
                0x5AE2CF48C92EE721,
                0x745ED385265E902C,
            ],
        )
        self.assertEqual(rabin.extended_decrypt(ciphertext, P, Q), b"abcdefghi")

    def test_hello_round_trips(self):
        ciphertext = rabin.extended_encrypt(N, b"hello")

        self.assertIsInstance(ciphertext, int)
        self.assertEqual(rabin.extended_decrypt(ciphertext, P, Q), b"hello")


if __name__ == "__main__":
    unittest.main()

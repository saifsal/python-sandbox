# Misc. helper functions

def size_int(arg: int) -> int:
    return len(int_to_bytes(arg))


def int_to_bytes(i: int, *, signed: bool = False) -> bytes:
    length = ((i + ((i * signed) < 0)).bit_length() + 7 + signed) // 8
    return i.to_bytes(length, byteorder='big', signed=signed)


def bytes_to_int(b: bytes, *, signed: bool = False) -> int:
    return int.from_bytes(b, byteorder='big', signed=signed)

# Core functionality


def generate_keys(bits: int) -> tuple:

    def make_prime(mod: int, rem: int) -> int:
        import Crypto.Util.number
        import os
        while True:
            prime = Crypto.Util.number.getPrime(bits, os.urandom)
            if prime % mod == rem:
                return prime

    # create two prime numbers, p and q, congruent with 3 when moded by 4
    p = make_prime(4, 3)
    q = make_prime(4, 3)
    # compute public key n
    n = p * q
    # return public key followed by the two private integers
    return n, p, q


def encrypt(n: int, m: int) -> int:
    # the encryption is only well-defined for m less than n
    if m < n and pow(m, 2) > n:
        return pow(m, 2, n)
    else:
        raise ValueError(
            "m must be less than n and m^2 must be greater than n")


def decrypt(c: int, p: int, q: int) -> list:

    def sqrt_mod(arg: int, mod: int) -> int:
        return pow(arg, (mod + 1)//4, mod)

    def inv_mod(arg: int, mod: int) -> int:
        res = pow(arg, -1, mod)
        if (arg < mod):
            res -= mod
        return res

    def solve_radicals(y_p: int, y_q: int, p: int, q: int) -> list:
        n = p*q
        r1 = (y_p * p * m_q + y_q * q * m_p) % n
        r2 = n - r1
        r3 = (y_p * p * m_q - y_q * q * m_p) % n
        r4 = n - r3
        return [r1, r2, r3, r4]

    # compute square root of c mod p and q
    m_p = sqrt_mod(c, p)
    m_q = sqrt_mod(c, q)

    # use extended Euclidean algorithm to find yp and yq
    # such that yp * p + yq * q = gcd(p,q)
    y_p = inv_mod(p, q)
    y_q = inv_mod(q, p)

    # compute the four plaintext candidates
    r = solve_radicals(y_p, y_q, p, q)

    return r


def find_solution(r: list) -> bytes:
    for a in r:
        a = int_to_bytes(a)
        pad = a[-1]
        if a.endswith(bytes([pad] * pad)):
            return a[:-pad]

# Useful wrapper functions


def split_m_too_big(n: int, m: int) -> list:
    m_bytes = int_to_bytes(m)
    step = size_int(n) - 5
    return [bytes_to_int(m_bytes[i:i + step]) for i in range(0, len(m_bytes), step)]


def add_padding(n: int, m: int) -> int:
    m_bytes = int_to_bytes(m)
    pad = min(size_int(n) - size_int(m) - 1, 255)
    if pad <= 0:
        raise ValueError("m must be less than n")

    m_bytes += bytes([pad] * pad)
    return bytes_to_int(m_bytes)

# Complete functionality


def extended_encrypt(n: int, m: bytes):
    m = bytes_to_int(m)
    if m > n:
        ms = split_m_too_big(n, m)
        return [encrypt(n, add_padding(n, i)) for i in ms]
    else:
        return encrypt(n, add_padding(n, m))


def extended_decrypt(c, p: int, q: int):
    if type(c) == list:
        return b''.join([find_solution(decrypt(chunk, p, q)) for chunk in c])
    else:
        return find_solution(decrypt(c, p, q))


if __name__ == "__main__":
    n, p, q = generate_keys(1536)

    m = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

    print('\nYour plaintext is:')
    print(f'\t``{m.decode()}\'\'')

    c = extended_encrypt(n, m)
    print('\nYour ciphertext is:')
    for a in c:
        print(f'\n{hex(a)}\n')

    r = extended_decrypt(c, p, q)
    print('\nYour decryption result is:')
    print(f'\t``{r.decode()}\'\'')

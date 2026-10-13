# python-sandbox

A sandbox of small Python scripts that do not share a library or an application. The repository description is "Collection of Python scripts". Clone it and run the file you want.

| Script | What you get |
| --- | --- |
| [`rabincryptosystem.py`](rabincryptosystem.py) | A Rabin public-key demo: square a message modulo `n`, then recover it from the four square roots. |
| [`shortestpath.py`](shortestpath.py) | Shortest land-border routes between countries in [`countries.json`](countries.json). |
| [`bowling.py`](bowling.py) | One random ten-pin game and a score. |
| [`neighborcountries.js`](neighborcountries.js) | A browser snippet that reads a Wikipedia borders table. |

## Features

### Rabin cryptosystem

`generate_keys` draws two primes that are 3 modulo 4 and returns the public modulus `n` together with the private factors `p` and `q`. `encrypt` computes `m² mod n`. `decrypt` recovers the four square roots, and `find_solution` keeps the candidate whose trailing bytes are a repeated pad.

`extended_encrypt` and `extended_decrypt` accept a byte string, pad it, and split it into chunks when it is larger than `n`. Running the file encrypts a fixed lorem-ipsum paragraph under a fresh 1536-bit key and prints the decrypted text, which matches the plaintext.

### Land-border paths

`countries.json` maps 159 countries to their land neighbours (323 undirected borders). `shortest_path` is breadth-first search. `validate_graph` checks that names are strings, that every neighbour exists, that borders are not duplicated or self-referential, and that every border has its reverse.

The graph has two components. Haiti and the Dominican Republic connect only to each other. The other 157 countries form the rest of the graph. Pairs with no land route are omitted.

The program prints the path with the most countries in between, then the top 100 such pairs. "Intermediate" means `len(path) - 2`.

### Bowling

`play_game` rolls ten frames. Each of the first two balls is a random integer, and the two balls sum to at most 10 (`MAX`). A tenth frame classified as a strike or a spare gets a third ball. `count_points` walks the frames using the `Bonus` markers (`NO`, `STRIKE`, `SPARE`) and returns the total. Running the file prints the frames and that total.

### Wikipedia neighbour table

`neighborcountries.js` is an immediately invoked function for the browser console. It looks for `table.wikitable`, reads the country name from the first cell's wiki link, and reads neighbour names from the wiki links in the last cell. It returns a plain object. It does not write `countries.json`.

## Example output

From the repository root, `python3 shortestpath.py` starts with:

```
Graph is consistent.
East Timor -> Indonesia -> Malaysia -> Thailand -> Laos -> China -> Afghanistan -> Iran -> Iraq -> Jordan -> Palestine -> Egypt -> Sudan -> Central African Republic -> Democratic Republic of the Congo -> Angola -> Namibia -> South Africa -> Lesotho
17 | East Timor -> Lesotho
```

The path has 17 intermediate countries. El Salvador–Lesotho and Lesotho–Papua New Guinea are tied with it. The script then prints the rest of the top 100 pairs.

`python3 bowling.py` prints the frames and the score. One run looked like this; the next run deals a new game:

```
[(3, 5), (8, 1), (7, 0), (2, 5), (9, 1), (2, 0), (3, 3), (2, 0), (3, 4), (3, 5)]
68
```

`python3 rabincryptosystem.py` prints three labelled sections: the lorem-ipsum plaintext, one `0x…` ciphertext block per chunk, and the decryption result. The decrypted text is the same paragraph. The hex blocks change whenever the key changes.

## Prerequisites

- Python 3.8 or newer. The Rabin modular inverse uses `pow(base, -1, modulus)`.
- [`pycryptodome`](https://www.pycryptodome.org/) for `rabincryptosystem.py` (`import Crypto.Util.number`).
- A browser, for `neighborcountries.js` only.

`bowling.py` and `shortestpath.py` use the standard library. These commands were run with CPython 3.12.3 and `pycryptodome` 3.24.1.

## Install

```bash
git clone https://github.com/saifsal/python-sandbox.git
cd python-sandbox
python3 -m pip install pycryptodome
```

Nothing is published to PyPI, and there is no `requirements.txt`. `mise.toml` records `python = "latest"` for people who use [mise](https://mise.jdx.dev/).

## Usage

Run the scripts from the repository root so `shortestpath.py` can open `countries.json`:

```bash
python3 bowling.py
python3 shortestpath.py
python3 rabincryptosystem.py
```

`rabincryptosystem.py` guards its demo with `if __name__ == "__main__"`, so this works from the repository root:

```python
from rabincryptosystem import generate_keys, extended_encrypt, extended_decrypt

n, p, q = generate_keys(1536)
ciphertext = extended_encrypt(n, b"hello")
print(extended_decrypt(ciphertext, p, q))
```

Importing `bowling` or `shortestpath` runs them immediately. Call their functions only if that side effect is acceptable, or run the files as scripts.

Paste `neighborcountries.js` into the developer console on a page that contains `table.wikitable`. The snippet's return value is the country map.

## Configuration

There is no config file.

| Location | Value | Effect |
| --- | --- | --- |
| `bowling.py` | `MAX = 10`, `ROUNDS = 10` | Pins per frame and frames per game. |
| `rabincryptosystem.py` `__main__` | `generate_keys(1536)` | Modulus size for the demo. |
| `shortestpath.py` | `"countries.json"` | Graph path, relative to the current directory. |
| `mise.toml` | `python = "latest"` | Python version for mise. |

## Development and testing

The repository has no test suite, linter, formatter, or type checker. After a change, compile the Python files and run the script you edited:

```bash
python3 -m py_compile bowling.py shortestpath.py rabincryptosystem.py
python3 bowling.py
python3 shortestpath.py
python3 rabincryptosystem.py
```

`shortestpath.py` must be started from the repository root. The Rabin demo needs PyCryptodome.

Agent instructions live in [`AGENTS.md`](AGENTS.md).

## Project status

This is a sandbox. The initial commit is the licence. `bowling.py` and `mise.toml` came next, then `rabincryptosystem.py`, then `shortestpath.py` with `countries.json` and `neighborcountries.js`. There is no roadmap, release, or issue template in the repository.

## Licence

GNU General Public License v3.0. The full text is in [`LICENSE`](LICENSE).

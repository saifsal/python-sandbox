# python-sandbox

## Overview

`python-sandbox` is a collection of small, independent Python scripts. That is the GitHub repository description, and the tree matches it: the files do not form a shared library, application, or service. Each script is a self-contained experiment you run on its own.

The scripts are:

- `rabincryptosystem.py` implements the Rabin public-key cryptosystem. Key generation builds a modulus from two primes that are congruent to 3 modulo 4. Encryption is modular squaring. Decryption recovers four square roots and uses a repeated-byte pad to choose one. The module can be imported. Running it as a program generates a 1536-bit key, encrypts a fixed lorem-ipsum plaintext, and prints the ciphertext and the decrypted text.
- `shortestpath.py` finds breadth-first shortest paths over land borders in `countries.json`. Running it checks that the graph is consistent, prints one path with the most intermediate countries, then prints the 100 pairs with the most intermediate countries.
- `bowling.py` plays one random ten-pin game (10 frames; the two balls in a frame sum to at most 10) and prints the frames and a score from `count_points`.
- `neighborcountries.js` is a browser-console snippet. On a page with `table.wikitable`, it returns an object mapping each country name to neighbouring names. It leaves the page and `countries.json` unchanged.

Current status: the Python scripts run as standalone programs. The repository has no installable package, test suite, continuous integration, or roadmap. The licence is the GNU General Public License v3.0 (`LICENSE`).

## Repository layout

```
python-sandbox/
├── AGENTS.md                          # Canonical agent instructions
├── README.md                          # Human-facing documentation
├── LICENSE                            # GNU GPL v3.0
├── mise.toml                          # Declares Python for mise
├── bowling.py                         # Random bowling game and scorer
├── rabincryptosystem.py               # Rabin cryptosystem
├── shortestpath.py                    # Border-graph shortest paths
├── countries.json                     # Country to list of land neighbours
└── neighborcountries.js               # Browser snippet for a Wikipedia table
```

`countries.json` is a JSON object of 159 country names. Each value is a list of bordering countries. The file contains 323 undirected borders and two connected components: Haiti with the Dominican Republic, and the other 157 countries. Every country in the file has at least one neighbour. `shortestpath.py` reports the graph as consistent (`validate_graph` returns no errors).

## Setup

Commands below were run with CPython 3.12.3 and `pycryptodome` 3.24.1.

`rabincryptosystem.py` uses the three-argument form of `pow` for modular inverses, which requires Python 3.8 or newer. `bowling.py` and `shortestpath.py` use only the standard library. `rabincryptosystem.py` imports `Crypto.Util.number` from PyCryptodome when `generate_keys` runs.

`mise.toml` sets `python = "latest"` for [mise](https://mise.jdx.dev/). The verified setup uses `python3` directly.

From the repository root:

```bash
python3 -m pip install pycryptodome
```

## Build, run and test

Build: Not applicable. There is no compile step, lockfile, or package build.

Run each program from the repository root:

```bash
python3 bowling.py
python3 shortestpath.py
python3 rabincryptosystem.py
```

`bowling.py` prints a list of ten frames and then an integer score. Frames are random, so the score changes between runs. A frame is a pair of rolls. The tenth frame is a triple when that frame is classified as a strike or a spare.

`shortestpath.py` prints `Graph is consistent.`, then one border path, then 100 lines of `intermediate | country_a -> country_b`. On the current `countries.json` the first path is:

```
East Timor -> Indonesia -> Malaysia -> Thailand -> Laos -> China -> Afghanistan -> Iran -> Iraq -> Jordan -> Palestine -> Egypt -> Sudan -> Central African Republic -> Democratic Republic of the Congo -> Angola -> Namibia -> South Africa -> Lesotho
```

That path has 17 intermediate countries. Two other pairs also have 17: El Salvador–Lesotho and Lesotho–Papua New Guinea.

`rabincryptosystem.py` prints the fixed plaintext, one hexadecimal ciphertext block per chunk, and the decrypted plaintext, which matches the original. With PyCryptodome 3.24.1, generating the 1536-bit key and finishing the round trip took a few seconds.

There is no test suite and no test runner. This syntax check completed successfully:

```bash
python3 -m py_compile bowling.py shortestpath.py rabincryptosystem.py
```

Before committing, run `py_compile` and the script you changed. Run `python3 shortestpath.py` from the repository root. Run `python3 rabincryptosystem.py` when PyCryptodome is installed.

`neighborcountries.js` is for a browser console on a page that contains `table.wikitable`. `node neighborcountries.js` fails with `ReferenceError: document is not defined`.

## Code style and conventions

- Scripts live at the repository root. There is no `src` layout, package name, or shared module.
- Python indentation is four spaces. `countries.json` is indented with four spaces.
- Match the file you are editing. `bowling.py` and `rabincryptosystem.py` annotate functions. `shortestpath.py` does not.
- `rabincryptosystem.py` separates helpers, core operations, wrappers, and the command-line demo with comment banners. The demo is under `if __name__ == "__main__"`.
- `bowling.py` and `shortestpath.py` run their main logic at import time.
- Names in Python are `snake_case`. Module-level constants in `bowling.py` are `MAX` and `ROUNDS`. The `Bonus` class holds `NO`, `STRIKE`, and `SPARE`.
- No formatter, linter, or type checker is configured. Leave that alone unless the change is specifically about tooling.
- `neighborcountries.js` is one immediately invoked function expression. It is not an npm package.

## CI and tooling

Not applicable for CI. The repository has no `.github/workflows` pipeline, pre-commit hooks, Makefile, or task runner.

Tooling that is present:

- `mise.toml` declares `python = "latest"`.
- PyCryptodome is a runtime dependency of `generate_keys` only. It is not listed in a requirements file.
- GitHub reports the licence as GNU General Public License v3.0, matching `LICENSE`.

## Working rules for agents

- Keep changes small and focused.
- Run the tests before committing. There is no automated suite; run `python3 -m py_compile` on the Python files you touch, and run the affected script from the repository root.
- Never commit secrets.
- Update the docs when behaviour changes. That includes this file, `README.md`, and the command output quoted above when `countries.json` or a script's printed results change.
- Use conventional commit messages (`docs:`, `fix:`, `feat:`, and so on).

## Gotchas

- `bowling.py` and `shortestpath.py` have no `__main__` guard. Importing either module executes it. `shortestpath.py` opens `countries.json` in the current working directory, so the import fails from another directory.
- `bonus` in `bowling.py` is annotated as returning `int` and returns a pair `(bonus_code, carry)`. A frame is treated as a strike when `max(f) == 10`, so `(0, 10)` is scored as a strike.
- `encrypt` raises `ValueError` unless `m < n` and `m * m > n`. `extended_encrypt` pads the message and, when the plaintext integer is larger than `n`, splits it into chunks of `size_int(n) - 5` bytes before padding. The return value is one `int`, or a `list` of ints when the message was split. `extended_decrypt` special-cases `list` and otherwise treats the argument as a single ciphertext integer.
- Decryption returns four roots. `find_solution` keeps the candidate whose trailing bytes are a repeated pad length. Ambiguous padding can select the wrong root.
- PyCryptodome is imported inside `generate_keys`. Importing `rabincryptosystem` does not load it. `generate_keys` raises `ModuleNotFoundError` when the package is absent.
- The Rabin script is a teaching implementation: the pad is a repeated byte, and the ciphertext carries no authentication tag. The demo keeps `p` and `q` in local variables and does not print them.
- `make_graph_consistent` is defined and unused by the script's main flow. That flow calls `validate_graph` and leaves the loaded graph unchanged.
- Pairs in different connected components have no path. Haiti and the Dominican Republic are one component, so they never appear on a path with the other 157 countries. `find_all_country_pairs` skips pairs whose search returns `None`.
- `neighborcountries.js` stores a country only when the last table cell yields at least one neighbour link, and it skips a link whose label equals the country name. The return value stays in the console.

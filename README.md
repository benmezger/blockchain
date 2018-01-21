# Blockchain

Ths is a simple blockchain implementation using Python.

## How does a block looks like

A block contains an `index`, a Unix `timestamp`, a `list of transactions`, a
`proof` and the `hash` of a previous block. See [this](./misc/block.json) as an
example.

1. Each block contains the hash of the previous block.

## Proof of work

The proof of work algorithm is used to create of mine blocks on the blockchain.

### The goal of PoW

1. Discover a number which solves a problem.
2. The number *must* be difficult to find, but easy to verify.


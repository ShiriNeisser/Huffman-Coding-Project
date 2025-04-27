# Huffman-Coding-Project
This Huffman coding project compresses and decompresses text by analyzing character frequency to assign shorter binary codes to more frequent characters, reducing file size effectively. The repository includes modules for both compression and decompression, supporting efficient data encoding and recovery.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Code Structure](#code-structure)
  - [Compression Details](#compression-details)
  - [Decompression Details](#decompression-details)

## Introduction

Huffman Coding is a widely used algorithm for lossless data compression. This project implements the algorithm to compress text files into a more compact binary format and decompress them back to their original form.

## Features

- **Efficient Compression**: Converts text files into a compact binary format.
- **Reliable Decompression**: Restores the original text file from the compressed format.
- **Structured Code**: Clear separation of concerns with dedicated classes for each functionality.


## Code Structure

### Compression Details

- **`UniqueValue` Class**: Manages unique identifiers for each node in the Huffman tree, ensuring each node can be traced and debugged effectively.
- **`HT_Node` Class**: Represents nodes within the Huffman tree, including their frequency and character data. Internal nodes are created by combining smaller nodes.
- **`HuffmanTree` Class**: Responsible for building the Huffman tree from a given text file, generating a character frequency histogram, and encoding the text using the tree structure.
- **`HuffmanEncoder` Class**: Handles the conversion of the original text into the compressed binary format using the Huffman tree.

### Decompression Details

- **`Order` Class**: Parses the in-order and pre-order traversal strings used to reconstruct the Huffman tree during decompression.
- **`TreeNode` Class**: Represents nodes in the reconstructed Huffman tree, facilitating the decoding process.
- **`HuffmanDecoder` Class**: Reconstructs the Huffman tree from the encoded data and decodes the compressed file back into the original text format.











import heapq
from collections import Counter
from colorama import Fore, Style, init
import time
import sys

init(autoreset=True)


class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

        print(
            Fore.YELLOW + "Merging nodes:",
            f"{left.char} ({left.freq})",
            "and",
            f"{right.char} ({right.freq})"
        )
        time.sleep(0.5)

    return heap[0]


def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
            print(Fore.GREEN + f"Assigning code to character {node.char}: {prefix}")
            time.sleep(0.3)

        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encoding(data):
    if not data:
        return "", {}

    frequencies = Counter(data)
    print(Fore.CYAN + "Character Frequencies: ", dict(frequencies))

    root = build_huffman_tree(frequencies)
    codebook = generate_codes(root, prefix="", codebook={})
    encoded_data = ''.join(codebook[char] for char in data)

    print(Fore.CYAN + "Encoded Data: ", encoded_data)
    return encoded_data, codebook


def huffman_decoding(encoded_data, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_data = ""
    current_code = ""

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_data += reverse_codebook[current_code]
            print(
                Fore.MAGENTA
                + f"Decoding: {current_code} -> {reverse_codebook[current_code]}"
            )
            current_code = ""
            time.sleep(0.2)

    return decoded_data


def animate_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()


if __name__ == "__main__":
    animate_text(Fore.BLUE + "Welcome to Huffman Coding CLI Application!")
    data = input(Fore.YELLOW + "Enter the text to encode: ")

    animate_text(Fore.GREEN + "Starting Huffman Encoding...")
    encoded_data, codebook = huffman_encoding(data)
    animate_text(Fore.GREEN + "Encoding completed!")

    print(Fore.CYAN + "Codebook: ", codebook)

    animate_text(Fore.RED + "Starting Huffman Decoding...")
    decoded_data = huffman_decoding(encoded_data, codebook)
    animate_text(Fore.RED + "Decoding completed!")

    print(Fore.BLUE + "Original data:", Fore.WHITE + data)
    print(Fore.BLUE + "Decoded data:", Fore.WHITE + decoded_data)

    if data == decoded_data:
        print(Fore.GREEN + "Success: The original and decoded data match!")
    else:
        print(Fore.RED + "Error: The original and decoded data do not match!")

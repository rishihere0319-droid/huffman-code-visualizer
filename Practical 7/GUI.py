import heapq
import time
import tkinter as tk
from collections import Counter
from tkinter import ttk, messagebox


class Node:

    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding Visualizer")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e1e2e")

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="Huffman Coding CLI & GUI Application",
            font=("Consolas", 18, "bold"),
            fg="#cba6f7",
            bg="#1e1e2e",
        )
        title_label.pack(pady=10)

        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            input_frame,
            text="Enter text to encode:",
            font=("Consolas", 11),
            fg="#cdd6f4",
            bg="#1e1e2e",
        ).pack(side="left", padx=5)

        self.input_entry = tk.Entry(
            input_frame,
            font=("Consolas", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            width=40,
        )
        self.input_entry.insert(0, "RISHI")
        self.input_entry.pack(side="left", padx=5)

        self.run_btn = tk.Button(
            input_frame,
            text="Start Encoding",
            font=("Consolas", 10, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            command=self.process_huffman,
        )
        self.run_btn.pack(side="left", padx=10)

        middle_frame = tk.Frame(self.root, bg="#1e1e2e")
        middle_frame.pack(fill="both", expand=True, padx=20, pady=10)

        log_frame = tk.Frame(middle_frame, bg="#1e1e2e")
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            log_frame,
            text="Process Animation Log",
            font=("Consolas", 11, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(anchor="w")

        self.log_text = tk.Text(
            log_frame,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#cdd6f4",
            wrap="word",
            height=15,
            width=45,
        )
        self.log_text.pack(fill="both", expand=True, pady=5)

        self.log_text.tag_config("blue", foreground="#89b4fa")
        self.log_text.tag_config("green", foreground="#a6e3a1")
        self.log_text.tag_config("yellow", foreground="#f9e2af")
        self.log_text.tag_config("cyan", foreground="#89dceb")
        self.log_text.tag_config("magenta", foreground="#f5c2e7")
        self.log_text.tag_config("red", foreground="#f38ba8")
        self.log_text.tag_config("white", foreground="#ffffff")

        table_frame = tk.Frame(middle_frame, bg="#1e1e2e")
        table_frame.pack(side="right", fill="both", expand=False)

        tk.Label(
            table_frame,
            text="Generated Codebook",
            font=("Consolas", 11, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(anchor="w")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#313244",
            foreground="#cdd6f4",
            fieldbackground="#313244",
            rowheight=25,
            font=("Consolas", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#45475a",
            foreground="#cdd6f4",
            font=("Consolas", 10, "bold"),
        )

        self.table = ttk.Treeview(
            table_frame, columns=("Char", "Code"), show="headings"
        )
        self.table.heading("Char", text="Char")
        self.table.heading("Code", text="Binary Code")
        self.table.column("Char", width=80, anchor="center")
        self.table.column("Code", width=120, anchor="center")
        self.table.pack(fill="both", expand=True, pady=5)

        res_frame = tk.Frame(self.root, bg="#181825", bd=1, relief="solid")
        res_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_encoded = tk.Label(
            res_frame,
            text="Encoded Bitstream: -",
            font=("Consolas", 10, "bold"),
            fg="#89dceb",
            bg="#181825",
            anchor="w",
        )
        self.lbl_encoded.pack(fill="x", padx=10, pady=2)

        self.lbl_decoded = tk.Label(
            res_frame,
            text="Decoded String: -",
            font=("Consolas", 10, "bold"),
            fg="#a6e3a1",
            bg="#181825",
            anchor="w",
        )
        self.lbl_decoded.pack(fill="x", padx=10, pady=2)

        self.lbl_status = tk.Label(
            res_frame,
            text="Status: Ready",
            font=("Consolas", 10, "bold"),
            fg="#cdd6f4",
            bg="#181825",
            anchor="w",
        )
        self.lbl_status.pack(fill="x", padx=10, pady=2)

    def append_log(self, text, color_tag="white", delay=0.01):
        for char in text:
            self.log_text.insert(tk.END, char, color_tag)
            self.log_text.see(tk.END)
            self.root.update()
            time.sleep(delay)
        self.log_text.insert(tk.END, "\n")

    def build_huffman_tree(self, frequencies):
        heap = [Node(char, freq) for char, freq in frequencies.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

            log_msg = f"Merging nodes: '{left.char}' ({left.freq}) and '{right.char}' ({right.freq})"
            self.append_log(log_msg, "yellow", delay=0.01)
            time.sleep(0.15)

        return heap[0]

    def generate_codes(self, node, prefix="", codebook=None):
        if codebook is None:
            codebook = {}

        if node:
            if node.char is not None:
                codebook[node.char] = prefix
                log_msg = f"Assigning code to '{node.char}': {prefix}"
                self.append_log(log_msg, "green", delay=0.01)
                time.sleep(0.1)

            self.generate_codes(node.left, prefix + "0", codebook)
            self.generate_codes(node.right, prefix + "1", codebook)

        return codebook

    def huffman_decoding(self, encoded_data, codebook):
        reverse_codebook = {v: k for k, v in codebook.items()}
        decoded_data = ""
        current_code = ""

        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_codebook:
                char = reverse_codebook[current_code]
                decoded_data += char
                self.append_log(
                    f"Decoding bit sequence: {current_code} -> '{char}'",
                    "magenta",
                    delay=0.005,
                )
                current_code = ""
                time.sleep(0.08)

        return decoded_data

    def process_huffman(self):
        data = self.input_entry.get()
        if not data:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return

        self.run_btn.config(state="disabled")
        self.log_text.delete("1.0", tk.END)
        for row in self.table.get_children():
            self.table.delete(row)

        self.lbl_encoded.config(text="Encoded Bitstream: Running...")
        self.lbl_decoded.config(text="Decoded String: Running...")
        self.lbl_status.config(text="Status: Processing...", fg="#f9e2af")

        self.append_log("Starting Huffman Encoding...", "blue")
        frequencies = Counter(data)
        self.append_log(f"Frequencies: {dict(frequencies)}", "cyan")

        root = self.build_huffman_tree(frequencies)
        codebook = self.generate_codes(root)

        for char, code in codebook.items():
            display_char = f"Space (' ')" if char == " " else char
            self.table.insert("", "end", values=(display_char, code))

        encoded_data = "".join(codebook[char] for char in data)
        self.append_log(f"Encoded Bitstream: {encoded_data}", "cyan")
        self.lbl_encoded.config(text=f"Encoded Bitstream: {encoded_data}")

        self.append_log("Starting Huffman Decoding...", "red")
        decoded_data = self.huffman_decoding(encoded_data, codebook)
        self.lbl_decoded.config(text=f"Decoded String: {decoded_data}")

        if data == decoded_data:
            self.lbl_status.config(
                text="Status: SUCCESS - Decoded data matches original input!",
                fg="#a6e3a1",
            )
            self.append_log(
                "SUCCESS: Original data and Decoded data match!", "green"
            )
        else:
            self.lbl_status.config(
                text="Status: ERROR - Decoded data does not match!",
                fg="#f38ba8",
            )
            self.append_log(
                "ERROR: Original data and Decoded data do not match!", "red"
            )

        self.run_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

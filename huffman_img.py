from PIL import Image
import os
import json
import pickle
import io

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.root = None
        self.codes = {}
        self.reverse_mapping = {}
        self.width, self.height = Image.open(self.path).size

    class TreeNode:
        def __init__(self, value, freq):
            self.value = value
            self.freq = freq
            self.left = None
            self.right = None
            self.binary = ''

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if not isinstance(other, HuffmanCoding.TreeNode):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, pixels):
        frequency = {}
        for pixel in pixels:
            pixelTemp = pixel[0]
            if pixelTemp not in frequency:
                frequency[pixelTemp] = 0
            frequency[pixelTemp] += 1
            
        # Sorting kamus berdasarkan nilai frekuensi dari terbesar ke terkecil
        # sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1]))
        return frequency

    def make_bt(self, frequency):
        nodes = [self.TreeNode(key, frequency[key]) for key in frequency]

        firstIter = True
        nodes = sorted(nodes, key=lambda x: x.freq)
        # for node in nodes:
        #     print(node.value, node.freq)
        while len(nodes) > 1:
        
            if firstIter:
                right = nodes.pop(0)
                left = nodes.pop(0)
                merged = self.TreeNode(None, left.freq + right.freq)
                merged.left = left
                merged.right = right
                left.binary = "0"
                right.binary = "1"
                firstIter = False
            else:
                left = nodes.pop(0)
                mergedTemp = merged
                merged = self.TreeNode(None, left.freq + merged.freq)
                merged.left = left
                merged.right = mergedTemp
                # Atur representasi biner pada simpul-simpul yang baru dibuat
                left.binary = "0"
                mergedTemp.binary = "1"

        left = nodes.pop(0)
        mergedTemp = merged
        merged = self.TreeNode(None, left.freq + merged.freq)
        merged.left = left
        merged.right = mergedTemp
        left.binary = "0"
        mergedTemp.binary = "1"
        self.root = merged
        self.root.binary = "0"

    def make_codes_helper(self, root, current):
        if root is None:
            return
        if root.value is not None:
            self.codes[root.value] = current
            self.reverse_mapping[current] = root.value
            return

        self.make_codes_helper(root.left, current + root.left.binary)
        self.make_codes_helper(root.right, current + root.right.binary)

    def make_codes(self):
        self.make_codes_helper(self.root, "")
        self.reverse_mapping["height"] = self.height
        self.reverse_mapping["width"] = self.width

    def get_encoded_text(self, pixels):
        encoded_text = ""
        for pixel in pixels:
            pixelTemp = pixel[0]
            if pixelTemp in self.codes:
                encoded_text += self.codes[pixelTemp]
            else:
                # Handle case when pixel value is not in codes_dict
                print(f"Warning: Pixel value {pixelTemp} not found in codes_dict.")
                return
        return encoded_text
    
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text
    
    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        byte_list = []
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            byte_list.append(int(byte, 2))
            
        b = bytes(byte_list)
        return b


    def compress(self):
        image = Image.open(self.path)
        pixels = list(image.getdata())

        frequency = self.make_frequency_dict(pixels)
        # print (frequency, type(frequency))
        self.make_bt(frequency)
        self.make_codes()
        
        key_code1 = b'\xEE\xFF\x00'
        key_code2 = b'\xAA\xBB\xCC'
        key_code3 = b'\xDD\xEE\xFF'
        key_code4 = b'\xBB\xCC\xDD'
        

        encoded_text = self.get_encoded_text(pixels)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        
        bytes_io = io.BytesIO()
        pickle.dump(self.reverse_mapping, bytes_io)
        reverse_mapping_json = bytes_io.getvalue()
        reverse_mapping_bytes = bytes(reverse_mapping_json)
        
        b = self.get_byte_array(padded_encoded_text)
        
        with open("decompress_huffman_img.py", 'rb') as file:
            # Baca konten file sebagai byte
            python_file_bytes = file.read()
        
        # Save compressed file
        bin_output_path = os.path.splitext(self.path)[0] + "_compressed.bin"
        with open(bin_output_path, 'wb') as output:
            pickle.dump(key_code1, output)
            pickle.dump(b, output)
            pickle.dump(key_code2, output)
            pickle.dump(reverse_mapping_bytes, output)
            pickle.dump(key_code3, output)
            pickle.dump(python_file_bytes, output)
            pickle.dump(key_code4, output)
        
        print("Compression successful.")
        print("Compressed file path: " + bin_output_path)
        return bin_output_path
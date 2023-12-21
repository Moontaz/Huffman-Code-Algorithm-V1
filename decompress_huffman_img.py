from PIL import Image
import os
import json

class HuffmanCoding:
    def __init__(self, bin_path, json_path):
        self.bin_path = bin_path
        self.json_path = json_path
        self.key_code = {}

    class TreeNode:
        def __init__(self, value, freq):
            self.value = value
            self.freq = freq
            self.left = None
            self.right = None
            self.binary = ""

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if not isinstance(other, HuffmanCoding.TreeNode):
                return False
            return self.freq == other.freq

    def decode_text(self, encoded_text):
       current_code = ""
       decoded_text = []

       for bit in encoded_text:
        current_code += bit
        if current_code in self.key_code:
            character = self.key_code[current_code]
            decoded_text.append(character)
            current_code = ""

       return decoded_text
   
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text
    
    def decompress(self, bin_path, json_path):
       # Read compressed file
        with open(bin_path, 'rb') as file:
            bit_string =""
            
            byte = file.read(1)
            while(len(byte) > 0):
                byte = int.from_bytes(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            
            encoded_text = self.remove_padding(bit_string)
            
        with open(json_path, 'r') as json_file:
            # Load the JSON data
            self.key_code = json.load(json_file)
        
        height = self.key_code["height"]
        width = self.key_code["width"]
        decoded_pixels = self.decode_text(encoded_text)

        # Save decompressed file
        output_path = os.path.splitext(self.bin_path[: -len("_compressed")])[0] + "_decompressed.jpg"
       
        image = Image.new("L", (width, height))
        image.putdata(decoded_pixels)
        image.save(output_path)

        print("Decompression successful.")
        return output_path

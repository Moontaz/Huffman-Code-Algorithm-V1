import sys
import json
import pickle

primary_bin_path = "dataset_image1_compressed.bin"
key_code1 = b'\xEE\xFF\x00'
key_code2 = b'\xAA\xBB\xCC'
key_code3 = b'\xDD\xEE\xFF'
key_code4 = b'\xBB\xCC\xDD'

# Read compressed file
with open(primary_bin_path, 'rb') as file:
         bin_bytes = b''
         json_bytes = b''
         python_bytes = b''
         try:
            while True:
               code = pickle.load(file)
               if code == key_code1:
                  data = pickle.load(file)
                  bin_bytes += data
               elif code == key_code2:
                  data = pickle.load(file)
                  json_bytes += data
               elif code == key_code3:
                  data = pickle.load(file)
                  python_bytes += data
               elif code == key_code4:
                  break 
         except EOFError:
            pass  
             
         with open("dataset_image1_image.bin", 'wb') as output:
            # output.write(bytes(byte_array))
            output.write(bytes(bin_bytes))
            
         json_dict = pickle.loads(json_bytes)
         with open("dataset_image1_key_code.json", 'w') as json_output:
            json.dump(json_dict, json_output)
            
                
         with open("decompress_huffman_img_executor.py", 'wb') as output_file:
             output_file.write(python_bytes)

from decompress_huffman_img_executor import HuffmanCoding as HI

bin_path = "dataset_image1_image.bin"
json_path = "dataset_image1_key_code.json"
hi = HI(bin_path, json_path)

decom_path = hi.decompress(bin_path, json_path)
print("Decompressed file path: " + decom_path)

from huffman_img import HuffmanCoding as HI
import sys

path_img = "dataset_image1.jpg"
hi = HI(path_img)

output_path = hi.compress()

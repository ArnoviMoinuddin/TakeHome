from PIL import Image
import hashlib
import numpy as np
import os
import re


class ImageGenerator:
    def __init__(self, input_string, size=256):
        self.input_string = input_string
        self.size = size

    def get_hash(self, string):
       
        if len(string) == 0:
            string = "blank"
            self.input_string = string
        else:
            pattern = r'[^a-zA-Z0-9\s]'
            string = re.sub(pattern, '', string) 
            self.input_string = string
        hash_bytes = hashlib.sha256(self.input_string.upper().encode('utf-8')).digest()
        return hash_bytes

    def get_color(self, hash_byte):
        color1 = (hash_byte[0], hash_byte[1], hash_byte[2])
        color2 = (hash_byte[3], hash_byte[4], hash_byte[5])
        color3 = (hash_byte[6], hash_byte[7], hash_byte[8])
        return (color1, color2, color3)

    def get_color_array(self, hash, colors):
        hash_list = list(hash)
        color_list = []
        for x in hash_list:
            if x % 17 == 0:
                color = colors[0]
            elif x % 2 == 0:
                color = colors[1]
            elif x % 2 == 1:
                color = colors[2]
            color_list.append(color)

        color_array = np.array(color_list, dtype=np.uint8).reshape((8, 4, 3))
        color_flipped = np.fliplr(color_array)
        color_comb = np.hstack((color_array, color_flipped))

        while True: 
            try: 
                scale = int(self.size / 8)
                kron_array = np.ones((scale, scale, 1), dtype=np.uint8)
                kron_comb = np.kron(color_comb, kron_array)
                color_comb_resized = kron_comb.reshape(self.size, self.size, 3)
                break 
            except ValueError:
                self.size = 256
                print('Not a valid multiple of 8 -- setting size to 256 x 256')

        return color_comb_resized

    def get_image(self):
        hash = self.get_hash(self.input_string)
        colors = self.get_color(hash)
        final_colors = self.get_color_array(hash, colors)
        final_image = Image.fromarray(final_colors)

        

        return final_image

def main():
    
    input_string = input("Enter string for identicon: ")
    while True:
        try:
            size = int(input("Enter identicon size (default 256 x 256, must be multiple of 8 -- hit ENTER to skip):  ") or 256)
            break
        except ValueError:
            print('Please enter a valid multiple of 8')

    final_image = ImageGenerator(input_string, size).get_image()
    
    output_path = input_string + ".png"
    final_image.save(output_path)
    print(f"Image saved as {output_path}")
    os.system(f'open {output_path}') 
    

if __name__ == "__main__":
    main()
